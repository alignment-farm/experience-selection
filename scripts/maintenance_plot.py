"""Standalone publication chart from audited complete-state outcomes."""
import argparse,hashlib,importlib.metadata,json
from pathlib import Path
import matplotlib.pyplot as plt
p=argparse.ArgumentParser();p.add_argument('metrics',type=Path,nargs='+');p.add_argument('--output',type=Path,required=True);p.add_argument('--title',required=True);p.add_argument('--with-costs',action='store_true');a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=False)
runs=[r for f in a.metrics for r in json.loads(f.read_text())['runs']]
arms=list(dict.fromkeys(arm for r in runs for arm in r['costs']))
fig,axs=plt.subplots(1,2 if a.with_costs else 1,figsize=(12 if a.with_costs else 8,4.3),layout='constrained',squeeze=False)
ax=axs[0,0]
for arm in arms:
 points=[]
 for ep in sorted({s['episode'] for r in runs for s in r['scores'] if s['arm']==arm and s['suite']=='later'}):
  ss=[s for r in runs for s in r['scores'] if s['arm']==arm and s['suite']=='later' and s['episode']==ep]
  points.append((ep,100*sum(s['success'] for s in ss)/sum(s['total'] for s in ss)))
 if points:ax.plot(*zip(*points),marker={'fixed75':'s','mir75':'o','stop75':'x'}.get(arm,'o'),linestyle={'mir75':'--','stop75':':'}.get(arm,'-'),label=arm)
max_ep=max(len(r['config']['sequence']) for r in runs)
ax.axhline(100,color='black',linestyle=':',label='explicit lookup')
if max_ep>3:ax.axvspan(3.5,max_ep+.2,color='gray',alpha=.12,label='recurring arrivals')
ax.set(xlabel='Arrival',ylabel='Complete workflows (%)',ylim=(-3,105),xticks=range(1,max_ep+1),title=a.title)
ax.grid(axis='y',alpha=.2);ax.legend(ncol=2,fontsize=8,loc='lower right')
if a.with_costs:
 cost=axs[0,1];train=[sum(r['costs'][arm]['update']['seconds'] for r in runs if arm in r['costs']) for arm in arms];select=[sum(r['costs'][arm]['selection_total_seconds'] for r in runs if arm in r['costs']) for arm in arms]
 cost.bar(arms,train,label='Maintenance training');cost.bar(arms,select,bottom=train,label='Replay selection')
 cost.set(ylabel='Observed seconds (all plotted runs)',title='Maintenance work; construction and use excluded')
 cost.tick_params(axis='x',rotation=20);cost.legend(fontsize=8);cost.grid(axis='y',alpha=.2)
fig.savefig(a.output/'complete-workflows.svg');fig.savefig(a.output/'complete-workflows.png',dpi=160);plt.close(fig)
(a.output/'provenance.json').write_text(json.dumps(dict(title=a.title,with_costs=a.with_costs,inputs={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in a.metrics},packages={n:importlib.metadata.version(n) for n in ['matplotlib','numpy']}),indent=2)+'\n')
