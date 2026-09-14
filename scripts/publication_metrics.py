"""Reproducible numeric tables for the local publication, from audited records."""
import json,hashlib
from pathlib import Path
runs=[Path(f'evidence/policy-v1-{s}') for s in [47,53,59]]
policy=json.loads(Path('evidence/policy-v1-analysis/policy.json').read_text())
reports=[json.loads((r.parent/(r.name+'-analysis')/'analysis.json').read_text()) for r in runs]
metrics={'states':{},'seeds':policy,'totals':{},'timing_qualification':'Descriptive sums; initial seed47 had brief shared-resource overlap. Not dedicated end-to-end latency.'}
for state in ['base','acquired']:
 metrics['states'][state]={}
 for source in ['none','context','checked','self','opposite']:
  rows=[x for r in reports for x in r['summary'] if x['arm']==state+'-'+source and x['step']==(0 if source in ['none','context'] else 128) and x['suite']=='development']
  assert len(rows)==3
  metrics['states'][state][source]={k:sum(x[k] for x in rows) for k in ['correct','n','prompt_tokens','completion_tokens','seconds']}
for k in ['gate_correct','n','gate_updates','fixed_checked_updates','fixed_checked_correct','no_update_correct','context_correct','matched_random_expected_correct','gate_training_seconds','gate_probe_seconds','gate_checked_verifications','fixed_checked_training_seconds','acquisition_updates']:
 metrics['totals'][k]=sum(x[k] for x in policy)
metrics['totals']['experimental_updates']=sum(c['updates'] for r in reports for c in r['cost'].values())
metrics['totals']['experimental_seconds']=sum(r['complete']['seconds'] for r in reports)
metrics['totals']['peak_mlx_bytes']=max(r['complete']['peak_mlx_bytes'] for r in reports)
metrics['totals']['raw_response_records']=sum(r['responses'] for r in reports)
metrics['totals']['duplicate_baseline_records']=sum(r['repeated_baseline_records'] for r in reports)
metrics['totals']['checkpoint_replays']=sum(r['reloads'] for r in reports)
metrics['totals']['source_generations']=96
metrics['source_reliability']={state:[sum(x['correct'] for x in json.loads((r/(state+'-self.json')).read_text())) for r in runs] for state in ['base','acquired']}
metrics['acquisition']=[json.loads((r/'acquisition.json').read_text()) for r in runs]
metrics['source_snapshots']={name:[hashlib.sha256((r/name).read_bytes()).hexdigest() for r in runs] for name in ['experiment.py','task.py','runtime.py','protocol.md']}
assert all(len(set(h))==1 for h in metrics['source_snapshots'].values())
out=Path('evidence/publication-metrics');out.mkdir(exist_ok=False)
(out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');(out/'publication_metrics.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(metrics['totals'],indent=2))
