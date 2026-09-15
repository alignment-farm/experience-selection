"""Describe semantic replay coverage from saved selections; no causal attribution."""
import argparse,collections,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('run',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
cs=json.loads((a.run/'cases.json').read_text())['train'];ev=[json.loads(l) for l in (a.run/'events.jsonl').read_text().splitlines()]
key=lambda i:cs[i]['site']+'/'+cs[i]['kind']
blocks=[]
for e in ev:
 if e['kind']=='selection':
  blocks.append(dict(arm=e['arm'],episode=e['episode'],step=e['step'],candidate_cells=len({key(v[0]) for v in e['ranked']}),chosen_cells=len({key(i) for i in e['chosen']}),chosen_counts=dict(collections.Counter(key(i) for i in e['chosen'])),largest_delta=max(v[2]-v[1] for v in e['ranked']),smallest_selected_delta=min(v[2]-v[1] for v in e['ranked'] if v[0] in e['chosen'])))
counts=collections.defaultdict(collections.Counter)
for e in ev:
 if e['kind']=='update':counts[e['arm']+'/'+str(e['episode'])][key(e['index'])]+=1
out=dict(run=str(a.run),blocks=blocks,updates={k:dict(v) for k,v in counts.items()},note='Coverage is descriptive; selection changes the subsequent outcome, so these are not unbiased tests of damage prediction.')
a.output.write_text(json.dumps(out,indent=2)+'\n')
for ep in sorted({b['episode'] for b in blocks}):
 bs=[b for b in blocks if b['episode']==ep]
 print(ep,'mean candidate cells',sum(b['candidate_cells'] for b in bs)/len(bs),'mean chosen cells',sum(b['chosen_cells'] for b in bs)/len(bs))
