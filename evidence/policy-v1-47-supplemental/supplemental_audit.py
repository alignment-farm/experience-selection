"""Audit equal-label equivalence, decision chronology, and source fit from saved data."""
import argparse,hashlib,json,collections
from pathlib import Path
from task import answer,prompt
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained("models/qwen3-4b-instruct")
p=argparse.ArgumentParser();p.add_argument('runs',type=Path,nargs='+');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
reports=[]
for root in a.runs:
 events=[json.loads(x) for x in (root/'events.jsonl').read_text().splitlines()]
 rows=[json.loads(x) for x in (root/'responses.jsonl').read_text().splitlines()]
 cfg=json.loads((root/'config.json').read_text());report=dict(run=str(root),source_fit={},equivalent_checkpoints=[])
 for state in ['base','acquired']:
  self_rows=json.loads((root/(state+'-self.json')).read_text())
  labels=[r['action'] for r in self_rows]
  for r in self_rows:
   assert r['correct']==(r['action']==answer(r['case']))
   assert tok.decode(r['ids'][:-1] if r['ended'] else r['ids'])==r['raw']
   assert r['action']==r['raw'].strip()
   assert r['prefix']==tok.apply_chat_template([dict(role='user',content=prompt(r['case']))],tokenize=True,add_generation_prompt=True,enable_thinking=False,return_dict=False)
  checked=json.loads((root/(state+'-checked-tokens.json')).read_text())
  own=json.loads((root/(state+'-self-tokens.json')).read_text())
  if checked==own:
   for step in [32,128]:
    left=root/f'{state}-checked-{step}.safetensors';right=root/f'{state}-self-{step}.safetensors'
    assert hashlib.sha256(left.read_bytes()).digest()==hashlib.sha256(right.read_bytes()).digest()
    report['equivalent_checkpoints'].append([left.name,right.name])
  targets={i:r['action'] for i,r in enumerate(self_rows)}
  for source in ['checked','self','opposite']:
   rs=[r for r in rows if r['arm']==state+'-'+source and r['step']==128 and r['suite']=='train'];assert len(rs)==16
   source_targets=targets if source=='self' else {i:('heron' if c['case']['channel']=='amber' else 'otter') if source=='opposite' else ('otter' if c['case']['channel']=='amber' else 'heron') for i,c in enumerate(self_rows)}
   us=[e for e in events if e['kind']=='update' and e['arm']==state+'-'+source]
   report['source_fit'][state+'-'+source]=dict(own_label_correct=sum(r['action']==source_targets[r['index']] for r in rs),task_correct=sum(r['correct'] for r in rs),last_epoch_mean_loss=sum(e['loss'] for e in us[-16:])/16)
  if cfg.get('policy'):
   idx=next(i for i,e in enumerate(events) if e['kind']=='decision' and e['state']==state)
   assert all(i>idx for i,e in enumerate(events) if e.get('arm','').startswith(state+'-') and e['kind']=='arm_start')
   decision=events[idx];assert decision['source']==('none' if all(r['correct'] for r in self_rows) else 'checked')
   report[state+'_decision_precedes_candidates']=True
 reports.append(report)
a.output.mkdir(exist_ok=False,parents=True)
(a.output/'audit.json').write_text(json.dumps(reports,indent=2)+'\n');(a.output/'supplemental_audit.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(reports,indent=2))
