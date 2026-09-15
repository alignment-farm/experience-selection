"""CPU-only independent reconstruction of workflow outcomes and policy costs."""
import argparse, collections, hashlib, itertools, json
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
            costs[arm]={}
            for kind in ['update','virtual_update','selection_loss']:
                rows=[e for e in events if e['kind']==kind and e['arm']==arm]
                costs[arm][kind]=dict(count=len(rows),input_tokens=sum(r['input_tokens'] for r in rows),target_tokens=sum(r['loss_tokens'] for r in rows),seconds=sum(r['seconds'] for r in rows))
                if kind.endswith('update'):assert all(r['gradient_norm']>0 and r['loss']>=0 for r in rows)
            rs=[r for r in responses if r['arm']==arm and r['suite']=='later']
            costs[arm]['use_generation']=dict(count=len(rs),prompt_tokens=sum(r['prompt_tokens'] for r in rs),completion_tokens=sum(r['completion_tokens'] for r in rs),seconds=sum(r['seconds'] for r in rs))
            if config['mode']=='recur':
                updates=[e for e in events if e['kind']=='update' and e['arm']==arm]
                assert len(updates)==(0 if arm=='none' else config['steps']*len(config['sequence']))
                for ep,site in enumerate(config['sequence'],1):
                    before=grouped[(arm+'-before',ep,'later')];after=grouped[(arm,ep,'later')]
                    b={r['index']:r for r in before};assert set(b)=={r['index'] for r in after}
                    pairs.append(dict(arm=arm,episode=ep,site=site,total=len(after),retained=sum(r['success'] and b[r['index']]['success'] for r in after),gained=sum(r['success'] and not b[r['index']]['success'] for r in after),lost=sum(not r['success'] and b[r['index']]['success'] for r in after),failed_both=sum(not r['success'] and not b[r['index']]['success'] for r in after)))
                    us=[e for e in updates if e['episode']==ep]
                    ratio=int(arm[-2:])/100 if arm.startswith(('fixed','mir')) else 0
                    assert sum(cs['train'][u['index']]['site']!=site for u in us)==int(config['steps']*ratio)
        selections=[e for e in events if e['kind']=='selection']
        for s in selections:
            assert s['reset_exact'] and s['optimizer_unchanged']
            ranked=sorted(s['ranked'],key=lambda v:(-(v[2]-v[1]),v[0]));assert ranked==s['ranked']
            assert s['chosen']==[v[0] for v in ranked[:max(1,len(ranked)//2)]]
        assert len([e for e in events if e['kind']=='virtual_matches_actual' and e['exact']])==len(selections)
        starts=[e['initial_hash'] for e in events if e['kind']=='arm_start'];assert len(set(starts))<=1
        assert any(e['kind']=='invariants' and e['base_unchanged'] and e['reset_max_logit_delta']==0 for e in events)
        assert all(e['exact_tokens'] for e in events if e['kind']=='reload')
        ex=[e for e in events if e['kind']=='explicit']
        assert all(e['success'] and e['actions']==paths[e['case']['site']][e['case']['kind']] for e in ex)
        # Explicit rows were evaluated once per counterfactual arm: deploy just one copy.
        ex=[e for e in ex if e['arm']==config['arms'][0]]
        all_runs.append(dict(path=str(run),manifest_sha256=sha(run/'SHA256SUMS'),config=config,scores=scores,pairs=pairs,costs=costs,selection_decisions=len(selections),explicit=dict(success=sum(e['success'] for e in ex),total=len(ex),retrieval_comparisons=sum(e['retrieval_comparisons'] for e in ex),seconds=sum(e['seconds'] for e in ex),peak_archive_bytes=max([e['archive_bytes'] for e in ex],default=0)),execution=events[-1]))
    (a.output/'metrics.json').write_text(json.dumps(dict(runs=all_runs),indent=2)+'\n')
    print(json.dumps([dict(path=r['path'],scores=r['scores'],pairs=r['pairs']) for r in all_runs],indent=2))
if __name__=='__main__':main()
