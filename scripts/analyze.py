"""Independent saved-record audit and paired utility/cost summary."""
import argparse,hashlib,json,collections
from pathlib import Path
from task import answer,wrong,prompt,cases
from transformers import AutoTokenizer
tokenizer=AutoTokenizer.from_pretrained("models/qwen3-4b-instruct")
def encode(s):return tokenizer.apply_chat_template([dict(role="user",content=s)],tokenize=True,add_generation_prompt=True,enable_thinking=False)
p=argparse.ArgumentParser();p.add_argument('run',type=Path);a=p.parse_args();root=a.run
for line in (root/'SHA256SUMS').read_text().splitlines():
 expected,name=line.split('  ',1);assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,name
rows=[json.loads(x) for x in (root/'responses.jsonl').read_text().splitlines()]
events=[json.loads(x) for x in (root/'events.jsonl').read_text().splitlines()]
assert events[-1]['kind']=='complete' and events[-1]['status']=='complete'
config=json.loads((root/'config.json').read_text());data=json.loads((root/'cases.json').read_text());order=json.loads((root/'order.json').read_text())
assert data==dict(train=cases(config['data_seed'],4),development=cases(config['data_seed']+1,4))
assert set(c['ticket'] for c in data['train']).isdisjoint(c['ticket'] for c in data['development'])
groups=collections.defaultdict(list)
for r in rows:
 assert r['expected']==answer(r['case'])
 assert r['correct']==(r['action']==r['expected'])
 assert r['case']==data[r['suite']][r['index']]
 assert r['prefix']==encode(prompt(r['case'],data['train'] if r['arm'].endswith('-context') else ()))
 assert tokenizer.decode(r['ids'][:-1] if r['ended'] else r['ids'])==r['raw']
 assert r['action']==r['raw'].strip()
 assert len(r['prefix'])==r['prompt_tokens'] and len(r['ids'])==r['completion_tokens']
 groups[(r['arm'],r['step'],r['suite'])].append(r)
summary=[]
repeated_baseline_records=0
for key,rs in groups.items():
 if key[0]=='base-none' and len(rs)==32:
  for left,right in zip(rs[:16],rs[16:]):
   assert all(left[k]==right[k] for k in ['index','case','prefix','ids','action','correct'])
  repeated_baseline_records+=16;rs=rs[:16]
 assert sorted(r['index'] for r in rs)==list(range(16))
 arm,step,suite=key;score=sum(r['correct'] for r in rs)
 matches=[e for e in events if e['kind']=='evaluation' and (e['arm'],e['step'])==(arm,step)]
 assert all(e[suite]==score for e in matches)
 summary.append(dict(arm=arm,step=step,suite=suite,correct=score,n=16,prompt_tokens=sum(r['prompt_tokens'] for r in rs),completion_tokens=sum(r['completion_tokens'] for r in rs),seconds=sum(r['seconds'] for r in rs)))
updates=collections.defaultdict(list);initials={}
for e in events:
 if e['kind']=='update':updates[e['arm']].append(e)
 if e['kind']=='arm_start':initials[e['arm']]=e['initial_hash'];assert e['optimizer_reset']
 if e['kind']=='invariants':assert e['base_unchanged'] and e['reset_max_logit_delta']==0
for state in ['base','acquired']:
 assert len({initials[state+'-'+s] for s in ['checked','self','opposite']})==1
 for source in ['checked','self','opposite']:
  arm=state+'-'+source;us=updates[arm]
  assert [u['index'] for u in us]==order[:config['steps']]
  assert [u['step'] for u in us]==list(range(1,config['steps']+1))
  assert all(u['gradient_norm']>=0 for u in us)
  tokens=json.loads((root/(arm+'-tokens.json')).read_text())
  self_rows=json.loads((root/(state+'-self.json')).read_text())
  for i,(c,t) in enumerate(zip(data['train'],tokens)):
   label=answer(c) if source=='checked' else wrong(c) if source=='opposite' else self_rows[i]['action']
   assert t['prefix']==encode(prompt(c))
   assert t['target']==tokenizer.encode(label,add_special_tokens=False)+[tokenizer.eos_token_id]
  for u in us:
   t=tokens[u['index']];assert u['input_tokens']==len(t['prefix'])+len(t['target'])-1 and u['loss_tokens']==len(t['target'])
 assert any(u['gradient_norm']>0 for u in updates[state+'-checked'])
assert initials['acquisition']==initials['base-checked']
cost={arm:dict(updates=len(us),seconds=sum(u['seconds'] for u in us),input_tokens=sum(u['input_tokens'] for u in us),loss_tokens=sum(u['loss_tokens'] for u in us),first_loss=us[0]['loss'],last_loss=us[-1]['loss']) for arm,us in updates.items()}
report=dict(run=str(root),verified_manifest=True,responses=len(rows),repeated_baseline_records=repeated_baseline_records,summary=summary,cost=cost,reloads=sum(e['kind']=='reload' for e in events),complete=events[-1])
output=root.parent/(root.name+'-analysis');output.mkdir(exist_ok=False)
(output/'analysis.json').write_text(json.dumps(report,indent=2)+'\n');(output/'analyze.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(report,indent=2))
