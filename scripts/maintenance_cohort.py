"""Aggregate the prospectively fixed fresh cohort, preserving seed and phase detail."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('metrics',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
runs=json.loads(a.metrics.read_text())['runs'];assert len(runs)==2
assert {(r['config']['seed'],r['config']['data_seed']) for r in runs}=={(103,2026091511),(107,2026091521)}
archive=set();fresh=set();cases_by_run=[]
for path in Path('evidence').glob('maintenance-development-v[1-4]/cases.json'):
 cs=json.loads(path.read_text());archive.update(c['ticket'] for rows in cs.values() for c in rows)
for r in runs:
 for name in ['maintenance_experiment.py','maintenance_task.py','runtime.py']:
  frozen=subprocess.check_output(['git','show',f'ba91a06:scripts/{name}'])
  assert (Path(r['path'])/name).read_bytes()==frozen
 assert (Path(r['path'])/'protocol.md').read_bytes()==subprocess.check_output(['git','show','ba91a06:protocol/maintenance-fresh-v1.md'])
 assert (Path(r['path'])/'uv.lock').read_bytes()==subprocess.check_output(['git','show','ba91a06:uv.lock'])
 c=r['config'];assert c['steps']==256 and c['state_steps']==128 and c['replicas']==16 and c['later_replicas']==2
 assert c['arms']==['none','fixed75','mir75','stop75'] and c['sequence']==['birch','cedar','dune']*2
 cs=json.loads((Path(r['path'])/'cases.json').read_text());tickets=[c['ticket'] for rows in cs.values() for c in rows]
 assert len(tickets)==len(set(tickets)) and not fresh.intersection(tickets) and not archive.intersection(tickets)
 fresh.update(tickets);cases_by_run.append(cs)
result=dict(input_sha256=hashlib.sha256(a.metrics.read_bytes()).hexdigest(),fresh_unique_later_tickets=sum(len(c['later']) for c in cases_by_run),fresh_disjoint_from_development=True,frozen_policy_commit='ba91a06',policy_snapshots_match_frozen_commit=True,arms={},seeds=[],actual_execution={})
for arm in ['none','fixed75','mir75','stop75']:
 scores=[s for r in runs for s in r['scores'] if s['arm']==arm and s['suite']=='later']
 pairs=[p for r in runs for p in r['pairs'] if p['arm']==arm]
 d={}
 for phase,lo,hi in [('all',1,6),('acquisition',1,3),('recurrence',4,6),('final',6,6)]:
  ss=[s for s in scores if lo<=s['episode']<=hi]
  d[phase]=dict(complete=sum(s['success'] for s in ss),total=sum(s['total'] for s in ss),resource=sum(s['resource'] for s in ss),preparation=sum(s['preparation'] for s in ss))
 d['pairs']={k:sum(p[k] for p in pairs) for k in ['retained','gained','lost','failed_both']}
 d['costs']={}
 for kind in ['update','virtual_update','selection_loss']:
  d['costs'][kind]={k:sum(r['costs'][arm][kind][k] for r in runs) for k in ['count','input_tokens','target_tokens','seconds']}
 for kind in ['use_generation','verification_generation']:
  d['costs'][kind]={k:sum(r['costs'][arm][kind][k] for r in runs) for k in ['count','prompt_tokens','completion_tokens','seconds']}
 d['costs']['selection_total_seconds']=sum(r['costs'][arm]['selection_total_seconds'] for r in runs)
 d['costs']['construction']={k:sum(r['acquisition'][k] for r in runs) for k in ['updates','input_tokens','target_tokens','seconds']}
 d['costs']['adapter_bytes_per_run']=[r['adapter_bytes'] for r in runs]
 assert d['all']['total']==168 and d['acquisition']['total']==72 and d['recurrence']['total']==96 and d['final']['total']==32
 result['arms'][arm]=d
result['explicit']={k:sum(r['explicit'][k] for r in runs) for k in ['success','total','retrieval_comparisons','action_tokens','archive_build_seconds','unique_archive_rows','seconds']}
assert result['explicit']['success']==result['explicit']['total']==168
result['explicit']['serialized_archive_bytes_per_run']=[r['explicit']['peak_archive_bytes'] for r in runs]
for r in runs:
 rows=[s for s in r['scores'] if s['suite']=='later' and s['arm'] in r['config']['arms']]
 result['seeds'].append(dict(seed=r['config']['seed'],path=r['path'],scores=rows,initial_acquisition=[s for s in r['scores'] if s['arm']=='state' and s['episode']==128]))
result['actual_execution']=dict(seconds=sum(r['execution']['seconds'] for r in runs),peak_mlx_bytes=max(r['execution']['peak_mlx_bytes'] for r in runs),optimizer_updates=sum(r['acquisition']['updates']+sum(c['update']['count']+c['virtual_update']['count'] for c in r['costs'].values()) for r in runs))
a.output.mkdir(parents=True,exist_ok=False);(a.output/'metrics.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({a:{k:v for k,v in d.items() if k!='costs'} for a,d in result['arms'].items()},indent=2))
