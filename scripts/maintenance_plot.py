"""Standalone publication chart from audited complete-state outcomes."""
import argparse,hashlib,importlib.metadata,json
from pathlib import Path
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('metrics',type=Path,nargs='+');p.add_argument('--output',type=Path,required=True);p.add_argument('--title',required=True);a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=False)
runs=[r for f in a.metrics for r in json.loads(f.read_text())['runs']]
arms=list(dict.fromkeys(arm for r in runs for arm in r['costs']))
fig,ax=plt.subplots(figsize=(8,4.3),layout='constrained')
for arm in arms:
 points=[]
 for ep in sorted({s['episode'] for r in runs for s in r['scores'] if s['arm']==arm and s['suite']=='later'}):
  ss=[s for r in runs for s in r['scores'] if s['arm']==arm and s['suite']=='later' and s['episode']==ep]
  points.append((ep,100*sum(s['success'] for s in ss)/sum(s['total'] for s in ss)))
 if points:ax.plot(*zip(*points),marker='o',label=arm)
max_ep=max(len(r['config']['sequence']) for r in runs)
ax.axhline(100,color='black',linestyle=':',label='explicit lookup')
if max_ep>3:ax.axvspan(3.5,max_ep+.2,color='gray',alpha=.12,label='recurring arrivals')
ax.set(xlabel='Arrival',ylabel='Complete workflows (%)',ylim=(-3,105),xticks=range(1,max_ep+1),title=a.title)
ax.grid(axis='y',alpha=.2);ax.legend(ncol=2,fontsize=8,loc='lower right')
fig.savefig(a.output/'complete-workflows.svg');plt.close(fig)
(a.output/'provenance.json').write_text(json.dumps(dict(title=a.title,inputs={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in a.metrics},packages={n:importlib.metadata.version(n) for n in ['matplotlib','numpy']}),indent=2)+'\n')
