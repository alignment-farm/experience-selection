"""Sequential execution of protocol/policy-v1.md; one GPU job at a time."""
import json,subprocess,sys
from pathlib import Path
from task import cases
runs=[(47,20260914101),(53,20260914201),(59,20260914301)]
used={c['ticket'] for seed in [20260914031,20260914032] for c in cases(seed,4)}
fresh=[]
for seed,data_seed in runs:
 for split,s in [('train',data_seed),('evaluation',data_seed+1)]:
  tickets=sorted({c['ticket'] for c in cases(s,4)})
  assert not (used&set(tickets));used.update(tickets)
  fresh.append(dict(seed=seed,split=split,tickets=tickets))
with Path('evidence/confirmatory-freshness.json').open('x') as f:json.dump(fresh,f,indent=2)
paths=[]
for seed,data_seed in runs:
 path=f'evidence/policy-v1-{seed}';paths.append(path)
 with Path(path+'.log').open('x') as log:
  subprocess.run([sys.executable,'scripts/experiment.py','--output',path,'--seed',str(seed),'--data-seed',str(data_seed),'--protocol','protocol/policy-v1.md','--policy'],stdout=log,stderr=subprocess.STDOUT,check=True)
 with Path(path+'-audit.log').open('x') as log:
  subprocess.run([sys.executable,'scripts/analyze.py',path],stdout=log,stderr=subprocess.STDOUT,check=True)
 print('completed and audited',path,flush=True)
subprocess.run([sys.executable,'scripts/policy_report.py',*paths,'--output','evidence/policy-v1-analysis'],check=True)
