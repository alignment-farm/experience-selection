"""Recompute follow-up scores, chronology and costs from preserved raw evidence."""
import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path

from followup_task import REGIONS, answer, prompt


def readlines(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def audit(path, tokenizer):
    for line in (path/'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ',1)
        assert hashlib.sha256((path/name).read_bytes()).hexdigest() == expected, name
    events = readlines(path/'events.jsonl')
    responses = readlines(path/'responses.jsonl')
    config = json.loads((path/'config.json').read_text())
    cases = json.loads((path/'cases.json').read_text())
    assert events[-1]['kind'] == 'complete' and events[-1]['status'] == 'complete'
    ticketsets = [{c['ticket'] for c in cs} for cs in cases.values()]
    assert all(not x&y for i,x in enumerate(ticketsets) for y in ticketsets[i+1:])
    grouped = defaultdict(list)
    for r in responses:
        assert r['case'] == cases[r['suite']][r['index']]
        assert r['expected'] == answer(r['case'])
        assert r['correct'] == (r['action'] == r['expected'])
        raw = tokenizer.decode(r['ids'][:-1] if r['ended'] else r['ids'])
        assert raw == r['raw'] and raw.strip() == r['action']
        examples = cases['train']+cases['probes'] if r['arm'].endswith('-context') else ()
        prefix = tokenizer.apply_chat_template([dict(role='user', content=prompt(r['case'],examples))],
                    tokenize=True, add_generation_prompt=True, enable_thinking=False, return_dict=False)
        assert prefix == r['prefix']
        assert r['prompt_tokens'] == len(prefix) and r['completion_tokens'] == len(r['ids'])
        grouped[(r['arm'],r['step'],r['suite'])].append(r)
    for e in events:
        if e['kind'] == 'evaluation':
            for suite,score in e['scores'].items():
                rows = grouped[(e['arm'],e['step'],suite)]
                assert len(rows) == len(cases[suite]) == score['total']
                assert sorted(r['index'] for r in rows) == list(range(len(rows)))
                counts = {region:sum(r['correct'] for r in rows if r['case']['region']==region) for region in REGIONS}
                assert counts == score['by_region'] and sum(counts.values()) == score['correct']
    orders = json.loads((path/'orders.json').read_text())
    tokens = json.loads((path/'training-tokens.json').read_text())
    assert len(tokens) == len(cases['train'])
    for t,c in zip(tokens,cases['train']):
        assert t['case'] == c
        assert t['target'] == tokenizer.encode(answer(c), add_special_tokens=False) + [tokenizer.eos_token_id]
    updates = defaultdict(list)
    starts = {}
    decisions = {}
    for position,e in enumerate(events):
        if e['kind'] == 'update':
            assert all(math.isfinite(e[k]) for k in ['loss','gradient_norm','seconds'])
            assert e['gradient_norm'] >= 0
            updates[e['arm']].append(e)
        elif e['kind'] == 'arm_start':
            assert e['optimizer_reset']
            starts[e['arm']] = e
        elif e['kind'] == 'decision':
            rows = grouped[(e['state']+'-probe',0,'probes')]
            errors = {region:sum(not r['correct'] for r in rows if r['case']['region']==region) for region in REGIONS}
            source = ('none' if not sum(errors.values()) else 'mixture' if errors['coast']==errors['inland'] else max(errors,key=errors.get))
            assert e['source'] == source and e['errors'] == errors
            assert not any(x['kind']=='arm_start' and x['arm'].startswith(e['state']+'-') for x in events[:position])
            decisions[e['state']] = e
    for arm,rows in updates.items():
        assert any(r['gradient_norm'] > 0 for r in rows)
        source = starts[arm]['source']
        assert [r['step'] for r in rows] == list(range(1,len(rows)+1))
        assert [r['index'] for r in rows] == orders[source][:len(rows)]
        for r in rows:
            t=tokens[r['index']]
            assert r['input_tokens'] == len(t['prefix'])+len(t['target'])-1
            assert r['loss_tokens'] == len(t['target'])
            assert source=='mixture' or r['region']==source
    for region,d in decisions.items():
        assert all(starts[region+'-'+s]['initial_hash']==d['state_hash'] for s in [*REGIONS,'mixture'])
    assert starts['state-coast']['initial_hash'] == starts['state-inland']['initial_hash']
    invariants = [e for e in events if e['kind']=='invariants']
    assert len(invariants)==2 and all(e['base_unchanged'] and e['reset_max_logit_delta']==0 for e in invariants)
    reloads = [e for e in events if e['kind']=='reload']
    assert {e['file'] for e in reloads} == {p.name for p in path.glob('*.safetensors') if p.name!='base.safetensors'}
    assert all(e['exact_tokens'] for e in reloads)
    def score(arm,step):
        rows = grouped[(arm,step,'later')]
        assert len(rows)==16
        return {region:sum(r['correct'] for r in rows if r['case']['region']==region) for region in REGIONS}
    def cost(arm,step):
        rows=updates.get(arm,[])[:step]
        return dict(updates=len(rows), **{k:sum(r[k] for r in rows) for k in ['input_tokens','loss_tokens','seconds']})
    def use_cost(arm,step,suite='later'):
        rows=grouped[(arm,step,suite)]
        return dict(calls=len(rows),**{k:sum(r[k] for r in rows) for k in ['prompt_tokens','completion_tokens','seconds']})
    states = {}
    for region in REGIONS:
        d=decisions[region]
        state=dict(no_update=score(region+'-none',0), context=score(region+'-context',0),
                   construction=cost('state-'+region,config['state_steps']), decision=d,
                   verification=use_cost(region+'-probe',0,'probes'), checkpoints={})
        for step in config['checkpoints']:
            outcomes = {s:dict(scores=score(region+'-'+s,step),training=cost(region+'-'+s,step),
                               use=use_cost(region+'-'+s,step)) for s in [*REGIONS,'mixture']}
            selected = outcomes.get(d['source'], dict(scores=state['no_update'], training=cost('',0),
                                                     use=use_cost(region+'-none',0)))
            state['checkpoints'][str(step)] = dict(sources=outcomes, selected=selected,
                oracle_correct=max(sum(v['scores'].values()) for v in outcomes.values()))
        state['context_use']=use_cost(region+'-context',0)
        state['no_update_use']=use_cost(region+'-none',0)
        states[region]=state
    base_mixture = {str(step): dict(scores=score('base-mixture',step), training=cost('base-mixture',step))
                    for step in config['checkpoints']} if config.get('include_base_mixture') else {}
    return dict(path=str(path),config=config,states=states,base=score('base-none',0),base_mixture=base_mixture,
                base_context=score('base-context',0),base_context_use=use_cost('base-context',0),
                actual_experiment_updates=sum(len(v) for v in updates.values()),
                actual_experiment_generation_calls=len(responses),run=events[-1],
                audit=dict(hashes=True,raw_decoding=True,prompts=True,scoring=True,matched_starts=True,
                           decision_before_candidates=True,reloads=len(reloads),invariants=True))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('runs',type=Path,nargs='+')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    # Only load tokenizer: audit is CPU-only and does not instantiate a learner.
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained('models/qwen3-4b-instruct')
    runs=[audit(path,tokenizer) for path in a.runs]
    totals={}
    for step in runs[0]['config']['checkpoints']:
        totals[str(step)]={s:sum(sum(state['checkpoints'][str(step)]['sources'][s]['scores'].values())
                     for run in runs for state in run['states'].values()) for s in [*REGIONS,'mixture']}
        totals[str(step)]['selected']=sum(sum(state['checkpoints'][str(step)]['selected']['scores'].values())
                     for run in runs for state in run['states'].values())
    result=dict(runs=runs,totals=totals,denominator=len(runs)*32,
                no_update=sum(sum(s['no_update'].values()) for run in runs for s in run['states'].values()),
                context=sum(sum(s['context'].values()) for run in runs for s in run['states'].values()))
    a.output.mkdir(parents=True,exist_ok=False)
    (a.output/'metrics.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2))


if __name__=='__main__': main()
