"""CPU-only independent reconstruction of workflow outcomes and policy costs."""
import argparse, collections, hashlib, itertools, json, random
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def main():
    p=argparse.ArgumentParser();p.add_argument('runs',type=Path,nargs='+');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    all_runs=[]
    for run in a.runs:
        for line in (run/'SHA256SUMS').read_text().splitlines():
            h,n=line.split('  ',1);assert sha(run/n)==h,(run,n)
        config=json.loads((run/'config.json').read_text());cs=json.loads((run/'cases.json').read_text());events=lines(run/'events.jsonl');responses=lines(run/'responses.jsonl')
        assert events[-1]['status']=='complete'
        assert {c['ticket'] for c in cs['train']}.isdisjoint(c['ticket'] for c in cs['later'])
        # Separately specified table; valid complete output is the unique three-action path.
        paths={'alder':{'copper':'heron scan ship','violet':'otter seal ship'},'birch':{'copper':'otter scan ship','violet':'heron seal ship'},'cedar':{'copper':'heron seal ship','violet':'otter scan ship'},'dune':{'copper':'otter seal ship','violet':'heron scan ship'}}
        from transformers import AutoTokenizer
        tok=AutoTokenizer.from_pretrained('models/qwen3-4b-instruct')
        grouped=collections.defaultdict(list)
        for r in responses:
            raw=tok.decode(r['ids'][:-1] if r['ended'] else r['ids']);assert raw==r['raw'] and raw.strip()==r['action']
            c=r['case'];expected=paths[c['site']][c['kind']]
            correct=r['action'].split()==expected.split();assert correct==r['success']
            if correct:
                resource,prep,_=expected.split();assert r['state']==dict(heron=1-(resource=='heron'),otter=1-(resource=='otter'),reserved=None,prepared=prep,shipped=True)
            parts=r['action'].split();expected_parts=expected.split()
            assert r['resource_correct']==(bool(parts) and parts[0]==expected_parts[0])
            assert r['preparation_correct']==(len(parts)>1 and parts[1]==expected_parts[1])
            expected_prompt=('Dispatch sandbox. Return three space-separated actions only. '
                'heron/otter reserves one unit of that resource; scan/seal prepares the reserved parcel; '
                'ship consumes the reservation and dispatches it. Use the site and kind rules learned from examples. '
                'Initially both resources have stock 1, no reservation, no preparation, not shipped. '
                f"Site {c['site']}; kind {c['kind']}; ticket {c['ticket']}. Actions:")
            encoded=tok.apply_chat_template([dict(role='user',content=expected_prompt)],tokenize=True,add_generation_prompt=True,enable_thinking=False,return_dict=False)
            assert encoded==r['prefix']
            grouped[(r['arm'],r['episode'],r['suite'])].append(r)
        scores=[]
        for (arm,ep,suite),rs in grouped.items():
            scores.append(dict(arm=arm,episode=ep,suite=suite,success=sum(r['success'] for r in rs),total=len(rs),resource=sum(r['resource_correct'] for r in rs),preparation=sum(r['preparation_correct'] for r in rs),by_site={s:sum(r['success'] for r in rs if r['case']['site']==s) for s in sorted({r['case']['site'] for r in rs})}))
        costs={};pairs=[]
        for arm in config['arms'] if config['mode']=='recur' else ['state','joint']:
            costs[arm]={'selection_total_seconds':sum(e['seconds'] for e in events if e['kind']=='selection' and e['arm']==arm)}
            for kind in ['update','virtual_update','selection_loss']:
                rows=[e for e in events if e['kind']==kind and e['arm']==arm]
                costs[arm][kind]=dict(count=len(rows),input_tokens=sum(r['input_tokens'] for r in rows),target_tokens=sum(r['loss_tokens'] for r in rows),seconds=sum(r['seconds'] for r in rows))
                if kind.endswith('update'):assert all(r['gradient_norm']>0 and r['loss']>=0 for r in rows)
            rs=[r for r in responses if r['arm']==arm and r['suite']=='later']
            before_rows=[r for r in responses if r['arm']==arm+'-before' and r['suite']=='later']
            costs[arm]['verification_generation']=dict(count=len(before_rows),prompt_tokens=sum(r['prompt_tokens'] for r in before_rows),completion_tokens=sum(r['completion_tokens'] for r in before_rows),seconds=sum(r['seconds'] for r in before_rows))
            costs[arm]['use_generation']=dict(count=len(rs),prompt_tokens=sum(r['prompt_tokens'] for r in rs),completion_tokens=sum(r['completion_tokens'] for r in rs),seconds=sum(r['seconds'] for r in rs))
            if config['mode']=='recur':
                updates=[e for e in events if e['kind']=='update' and e['arm']==arm]
                assert len(updates)==(0 if arm=='none' else config['steps']*(min(3,len(config['sequence'])) if arm.startswith('stop') else len(config['sequence'])))
                for ep,site in enumerate(config['sequence'],1):
                    before=grouped[(arm+'-before',ep,'later')];after=grouped[(arm,ep,'later')]
                    b={r['index']:r for r in before};assert set(b)=={r['index'] for r in after}
                    pairs.append(dict(arm=arm,episode=ep,site=site,total=len(after),retained=sum(r['success'] and b[r['index']]['success'] for r in after),gained=sum(r['success'] and not b[r['index']]['success'] for r in after),lost=sum(not r['success'] and b[r['index']]['success'] for r in after),failed_both=sum(not r['success'] and not b[r['index']]['success'] for r in after)))
                    us=[e for e in updates if e['episode']==ep]
                    ratio=int(arm[-2:])/100 if arm.startswith(('fixed','mir','stop')) else 0
                    assert sum(cs['train'][u['index']]['site']!=site for u in us)==int((0 if arm.startswith('stop') and ep>3 else config['steps'])*ratio)
                    def order(pool,n,seed):
                        rng=random.Random(seed);result=[]
                        while len(result)<n:
                            batch=pool.copy();rng.shuffle(batch);result.extend(batch)
                        return result[:n]
                    pool=[i for i,c in enumerate(cs['train']) if c['site']==site]
                    incoming=[u['index'] for u in us if cs['train'][u['index']]['site']==site]
                    assert incoming==order(pool,config['steps'],config['seed']+ep)[:len(incoming)]
                    if arm.startswith(('fixed','stop')):
                        seen=['alder']+list(dict.fromkeys(config['sequence'][:ep]));seen=list(dict.fromkeys(seen))
                        old=[s for s in seen if s!=site]
                        pool=[i for s in old for i,c in enumerate(cs['train']) if c['site']==s]
                        replay=[u['index'] for u in us if cs['train'][u['index']]['site']!=site]
                        assert replay==order(pool,config['steps'],config['seed']+100+ep)[:len(replay)]
        selections=[e for e in events if e['kind']=='selection']
        for s in selections:
            assert s['reset_exact'] and s['optimizer_unchanged']
            ranked=sorted(s['ranked'],key=lambda v:(-(v[2]-v[1]),v[0]));assert ranked==s['ranked']
            assert s['chosen']==[v[0] for v in ranked[:max(1,len(ranked)//2)]]
            site=config['sequence'][s['episode']-1]
            assert all(cs['train'][i]['site']!=site for i in s['chosen'])
            selected_updates=[e for e in events if e['kind']=='update' and e['arm']==s['arm'] and e['episode']==s['episode'] and s['step']<=e['step']<s['step']+16 and cs['train'][e['index']]['site']!=site]
            assert all(e['index'] in s['chosen'] for e in selected_updates)
        assert len([e for e in events if e['kind']=='virtual_matches_actual' and e['exact']])==len(selections)
        starts=[e['initial_hash'] for e in events if e['kind']=='arm_start'];assert len(set(starts))<=1
        assert any(e['kind']=='invariants' and e['base_unchanged'] and e['reset_max_logit_delta']==0 for e in events)
        assert all(e['exact_tokens'] for e in events if e['kind']=='reload')
        ex=[e for e in events if e['kind']=='explicit']
        assert all(e['success'] and e['actions']==paths[e['case']['site']][e['case']['kind']] for e in ex)
        # Explicit rows were evaluated once per counterfactual arm: deploy just one copy.
        ex=[e for e in ex if e['arm']==config['arms'][0]]
        builds=[e for e in events if e['kind']=='archive_build' and e['arm']==config['arms'][0]]
        acquisition=[e for e in events if e['kind']=='update' and e['arm']=='state']
        all_runs.append(dict(path=str(run),manifest_sha256=sha(run/'SHA256SUMS'),config=config,scores=scores,pairs=pairs,costs=costs,acquisition=dict(updates=len(acquisition),input_tokens=sum(e['input_tokens'] for e in acquisition),target_tokens=sum(e['loss_tokens'] for e in acquisition),seconds=sum(e['seconds'] for e in acquisition)),selection_decisions=len(selections),explicit=dict(success=sum(e['success'] for e in ex),total=len(ex),retrieval_comparisons=sum(e['retrieval_comparisons'] for e in ex),action_tokens=sum(e.get('action_tokens',0) for e in ex),archive_build_seconds=sum(e['seconds'] for e in builds),unique_archive_rows=max([e['rows'] for e in builds],default=0),seconds=sum(e['seconds'] for e in ex),peak_archive_bytes=max([e['archive_bytes'] for e in ex],default=0)),adapter_bytes=max((f.stat().st_size for f in run.glob('*.safetensors')),default=0),execution=events[-1]))
    (a.output/'metrics.json').write_text(json.dumps(dict(runs=all_runs),indent=2)+'\n')
    print(json.dumps([dict(path=r['path'],scores=r['scores'],pairs=r['pairs']) for r in all_runs],indent=2))
if __name__=='__main__':main()
