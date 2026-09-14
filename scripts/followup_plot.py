"""Export the measured development curve and individual fresh-state outcomes."""
import argparse
import json
from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--fresh',type=Path,required=True)
    p.add_argument('--primary-step',default='256')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    dev={}
    for name in ['followup-development-v1-audit','followup-development-v2-audit']:
        d=json.loads(Path('evidence',name,'metrics.json').read_text())
        for step,values in d['totals'].items():
            if int(step) in dev: assert dev[int(step)]==values
            dev[int(step)]=values
    f=json.loads(a.fresh.read_text())
    colors={'mixture':'#186f65','selected':'#c16b2e','none':'#6b7280'}
    fig,(left,right)=plt.subplots(1,2,figsize=(12,4.6),gridspec_kw={'width_ratios':[1,1.65]})
    xs=sorted(dev)
    for key,label in [('mixture','Fixed balanced mixture'),('selected','Current-error gap policy')]:
        left.plot(xs,[100*dev[x][key]/32 for x in xs],marker='o',label=label,color=colors[key],lw=2)
    left.axhline(50,color=colors['none'],ls='--',label='No update')
    left.set_xscale('log',base=2);left.set_xticks(xs,labels=xs)
    left.set(xlabel='Subsequent optimizer updates',ylabel='Later accuracy (%)',ylim=(0,105),title='Development: duration matters')
    left.legend(fontsize=8,loc='lower right')
    rows=[(r['config']['seed'],name,state) for r in f['runs'] for name,state in r['states'].items()]
    indices=np.arange(len(rows));width=.24
    for offset,key,label in [(-1,'none','No update'),(0,'selected','Gap policy'),(1,'mixture','Fixed mixture')]:
        ys=[]
        for _,_,state in rows:
            checkpoint=state['checkpoints'][a.primary_step]
            score=(state['no_update'] if key=='none' else checkpoint['selected']['scores'] if key=='selected'
                   else checkpoint['sources']['mixture']['scores'])
            ys.append(sum(score.values()))
        bars=right.bar(indices+offset*width,ys,width,color=colors[key],label=label)
        right.bar_label(bars,padding=2,fontsize=7)
    right.set_xticks(indices,labels=[f'{seed}\n{name}' for seed,name,_ in rows],fontsize=8)
    right.set(ylabel='Correct later queries (of 16)',ylim=(0,18),xlabel='Fresh seed and starting state',
              title=f'Fresh evaluation: fixed {a.primary_step}-update budget')
    right.legend(fontsize=8,loc='lower right')
    for ax in [left,right]:
        ax.spines[['top','right']].set_visible(False)
        ax.set_axisbelow(True);ax.grid(axis='y',alpha=.18)
    fig.suptitle('Correcting current errors can lose an already learned rule',fontsize=13)
    fig.tight_layout(rect=(0,.07,1,.95))
    fig.text(.5,.02,'Synthetic routing: four shared rule cells. Fresh tickets and initializations; no independent-task error bars.',
             ha='center',fontsize=8,color='#4b5563')
    a.output.mkdir(parents=True,exist_ok=False)
    for ext in ['svg','png']:fig.savefig(a.output/f'source-comparison.{ext}',dpi=180)
    (a.output/'provenance.json').write_text(json.dumps(dict(matplotlib=matplotlib.__version__,numpy=np.__version__,
          fresh=str(a.fresh),primary_step=a.primary_step),indent=2)+'\n')
    (a.output/'followup_plot.py').write_bytes(Path(__file__).read_bytes())


if __name__=='__main__':main()
