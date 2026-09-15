"""One visible sequential cohort; run only after checking shared-device availability."""
import argparse,hashlib,json,subprocess,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--mir-arm',required=True,choices=['mir50','mir75']);p.add_argument('--protocol',required=True);p.add_argument('--prefix',default='maintenance-fresh-v1');a=p.parse_args()
seeds=[(103,2026091511),(107,2026091521)]
paths=[Path('evidence')/f'{a.prefix}-{s}' for s,_ in seeds]
assert all(not p.exists() for p in paths)
batch=Path('evidence')/(a.prefix+'-batch');batch.mkdir(exist_ok=False)
(batch/'run_maintenance_fresh.py').write_bytes(Path(__file__).read_bytes());(batch/'protocol.md').write_bytes(Path(a.protocol).read_bytes())
start=time.monotonic();records=[]
for (seed,data_seed),out in zip(seeds,paths):
 cmd=[sys.executable,'scripts/maintenance_experiment.py','--output',str(out),'--mode','recur','--seed',str(seed),'--data-seed',str(data_seed),'--replicas','16','--later-replicas','2','--state-steps','128','--candidate-count','16','--sequence','birch','cedar','dune','birch','cedar','dune','--steps','256','--arms','none','fixed75',a.mir_arm,'stop75','--protocol',a.protocol]
 tick=time.monotonic();result=subprocess.run(cmd)
 records.append(dict(command=cmd,returncode=result.returncode,seconds=time.monotonic()-tick))
 (batch/'runs.json').write_text(json.dumps(dict(runs=records,elapsed=time.monotonic()-start),indent=2)+'\n')
 if result.returncode:raise SystemExit(result.returncode)
(batch/'SHA256SUMS').write_text('\n'.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name for f in sorted(batch.iterdir()) if f.is_file() and f.name!='SHA256SUMS')+'\n')
