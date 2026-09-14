"""Execute the prespecified fresh cohort sequentially; never overwrite evidence."""
import subprocess
import sys
from pathlib import Path


def main():
    runs=[(73,20260914601),(79,20260914701),(83,20260914801)]
    paths=[Path(f'evidence/followup-fresh-v1-{seed}') for seed,_ in runs]
    assert all(not p.exists() for p in paths), 'Fresh cohort already exists; reproduce manually under new names.'
    for (seed,data_seed),path in zip(runs,paths):
        with path.with_suffix('.log').open('x') as log:
            subprocess.run([sys.executable,'scripts/followup_experiment.py','--output',str(path),
                '--seed',str(seed),'--data-seed',str(data_seed),'--state-steps','64',
                '--checkpoints','128','256','--protocol','protocol/followup-fresh-v1.md'],
                stdout=log,stderr=subprocess.STDOUT,check=True)
        print('Finished',path,flush=True)
    subprocess.run([sys.executable,'scripts/followup_audit.py',*[str(p) for p in paths],
                    '--output','evidence/followup-fresh-v1-audit'],check=True)


if __name__=='__main__':main()
