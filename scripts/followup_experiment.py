"""Owned follow-up: paired source branches and prospective gap decisions."""
import argparse
import json
import random
import subprocess
import time
from pathlib import Path

import mlx.core as mx
from runtime import Runtime, resource, digest, sha
from followup_task import REGIONS, cases, answer, prompt


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--seed', type=int, default=71)
    p.add_argument('--data-seed', type=int, default=20260914501)
    p.add_argument('--state-steps', type=int, default=64)
    p.add_argument('--checkpoints', type=int, nargs='+', default=[8, 16, 32, 64])
    p.add_argument('--protocol', default='protocol/followup-development-v1.md')
    a = p.parse_args()
    out = a.output
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    def save(name, value):
        (out / name).write_text(json.dumps(value, indent=2) + '\n')
    for name in ['followup_experiment.py', 'followup_task.py', 'runtime.py']:
        (out / name).write_bytes(Path('scripts', name).read_bytes())
    for src, dest in [(a.protocol, 'protocol.md'), ('uv.lock', 'uv.lock')]:
        (out / dest).write_bytes(Path(src).read_bytes())
    ev = (out / 'events.jsonl').open('x')
    res = (out / 'responses.jsonl').open('x')
    def event(kind, **kw):
        ev.write(json.dumps(dict(kind=kind, elapsed=time.monotonic()-start, **kw)) + '\n')
        ev.flush()
    def check():
        assert time.monotonic() - start < 1800
        assert mx.get_peak_memory() < 40e9
    status = 'failed'
    try:
        save('config.json', {k: str(v) if isinstance(v, Path) else v for k,v in vars(a).items()})
        save('resource.json', resource())
        event('revision', git=subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip())
        train, probes, later = cases(a.data_seed, 2), cases(a.data_seed+1, 1), cases(a.data_seed+2, 4)
        sets = [{c['ticket'] for c in cs} for cs in [train, probes, later]]
        assert all(not (x & y) for i,x in enumerate(sets) for y in sets[i+1:])
        save('cases.json', dict(train=train, probes=probes, later=later))
        rt = Runtime()
        rt.reinitialize(a.seed)
        base = rt.snapshot()
        mx.save_safetensors(str(out / 'base.safetensors'), dict(base))
        replays = []
        orders = {}
        length = max(a.state_steps, max(a.checkpoints))
        for r in REGIONS:
            rng = random.Random(a.seed)  # matched within-region channel/ticket orders
            pool = [i for i,c in enumerate(train) if c['region'] == r]
            order = []
            while len(order) < length:
                row = pool.copy(); rng.shuffle(row); order.extend(row)
            orders[r] = order[:length]
        orders['mixture'] = [i for pair in zip(orders['coast'], orders['inland']) for i in pair][:length]
        save('orders.json', orders)
        data = [(rt.encode(prompt(c)), answer(c)) for c in train]
        data = [(x, rt.target(x,y)) for x,y in data]
        save('training-tokens.json', [dict(case=c,prefix=x,target=y) for c,(x,y) in zip(train,data)])

        def evaluate(arm, step, examples=(), suites=None):
            scores = {}
            first = None
            for suite, cs in (suites or [('train',train), ('later',later)]):
                counts = {r: 0 for r in REGIONS}
                for index,c in enumerate(cs):
                    check()
                    prefix = rt.encode(prompt(c,examples))
                    result = rt.generate(prefix, limit=16)
                    correct = result['action'] == answer(c)
                    counts[c['region']] += correct
                    res.write(json.dumps(dict(arm=arm, step=step, suite=suite, index=index,
                                              case=c, prefix=prefix, expected=answer(c),
                                              correct=correct, **result)) + '\n'); res.flush()
                    if first is None: first = (prefix, result['ids'])
                scores[suite] = dict(correct=sum(counts.values()), total=len(cs), by_region=counts)
            event('evaluation', arm=arm, step=step, scores=scores)
            print(arm, step, scores, flush=True)
            return scores, first

        def updates(arm, source, steps, checkpoints):
            optimizer = rt.optimizer()
            event('arm_start', arm=arm, source=source, initial_hash=digest(rt.snapshot()), optimizer_reset=True)
            for step,index in enumerate(orders[source][:steps],1):
                check()
                x,y = data[index]
                event('update', arm=arm, step=step, index=index, region=train[index]['region'],
                      **rt.step(x,y,optimizer))
                if step in checkpoints:
                    filename = f'{arm}-{step}.safetensors'
                    mx.save_safetensors(str(out/filename),dict(rt.snapshot()))
                    scores, replay = evaluate(arm,step)
                    replays.append((filename,*replay))
            return scores

        evaluate('base-none',0)
        evaluate('base-context',0,train+probes)
        for region in REGIONS:
            rt.restore(base)
            state_arm = 'state-' + region
            scores = updates(state_arm, region, a.state_steps,
                             sorted(set([x for x in [8,16,32,64] if x <= a.state_steps] + [a.state_steps])))
            state = rt.snapshot()
            state_hash = digest(state)
            event('state', state=region, hash=state_hash, acquisition=scores['later']['by_region'][region] == 8,
                  partial=scores['later']['correct'] < 16)
            probe_scores,_ = evaluate(region+'-probe',0,suites=[('probes',probes)])
            errors = {r:2-probe_scores['probes']['by_region'][r] for r in REGIONS}
            source = ('none' if sum(errors.values()) == 0 else
                      'mixture' if errors['coast'] == errors['inland'] else max(errors,key=errors.get))
            event('decision', state=region, source=source, errors=errors, state_hash=state_hash,
                  rule='none if zero errors; maximum-error region; mixture on nonzero tie')
            evaluate(region+'-none',0)
            evaluate(region+'-context',0,train+probes)
            for source in [*REGIONS,'mixture']:
                rt.restore(state)
                assert digest(rt.snapshot()) == state_hash
                updates(region+'-'+source, source, max(a.checkpoints), a.checkpoints)
            event('invariants', state=region, **rt.invariants())
        for filename,prefix,ids in replays:
            rt.restore(list(mx.load(str(out/filename)).items()))
            assert rt.generate(prefix,limit=16)['ids'] == ids
            event('reload', file=filename, exact_tokens=True)
        status = 'complete'
    except BaseException as e:
        event('failure', error=repr(e))
        raise
    finally:
        event('complete', status=status, seconds=time.monotonic()-start, peak_mlx_bytes=mx.get_peak_memory())
        ev.close(); res.close()
        (out/'SHA256SUMS').write_text('\n'.join(sha(f)+'  '+f.name for f in sorted(out.iterdir())
                                              if f.is_file() and f.name != 'SHA256SUMS')+'\n')


if __name__ == '__main__':
    main()
