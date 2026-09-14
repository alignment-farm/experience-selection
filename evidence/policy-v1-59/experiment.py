"""Matched source comparison; all candidates are reset from identical state."""
import argparse,json,random,subprocess,time
from pathlib import Path
import mlx.core as mx
from runtime import Runtime,resource,digest,sha
from task import cases,answer,wrong,prompt
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--seed',type=int,default=43);p.add_argument('--data-seed',type=int,default=20260914031);p.add_argument('--steps',type=int,default=128);p.add_argument('--policy',action='store_true');p.add_argument('--protocol',default='protocol/development-v1.md');a=p.parse_args()
out=a.output;out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
def save(n,v):(out/n).write_text(json.dumps(v,indent=2)+'\n')
for f in ['experiment.py','runtime.py','task.py']:(out/f).write_bytes(Path('scripts',f).read_bytes())
(out/'protocol.md').write_bytes(Path(a.protocol).read_bytes());(out/'uv.lock').write_bytes(Path('uv.lock').read_bytes())
ev=(out/'events.jsonl').open('x');res=(out/'responses.jsonl').open('x')
def event(kind,**kw):ev.write(json.dumps(dict(kind=kind,elapsed=time.monotonic()-start,**kw))+'\n');ev.flush()
def check():
 assert time.monotonic()-start<1800
 assert mx.get_peak_memory()<40e9
status='failed'
try:
 save('config.json',dict(seed=a.seed,data_seed=a.data_seed,steps=a.steps,protocol=a.protocol,policy=a.policy))
 save('resource.json',resource());event('revision',git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
 train=cases(a.data_seed,4);dev=cases(a.data_seed+1,4)
 assert not ({c['ticket'] for c in train}&{c['ticket'] for c in dev})
 save('cases.json',dict(train=train,development=dev))
 rt=Runtime();rt.reinitialize(a.seed);base=rt.snapshot();replays=[]
 rng=random.Random(a.seed);order=[]
 for _ in range(8):
  row=list(range(16));rng.shuffle(row);order+=row
 save('order.json',order)
 def evaluate(arm,step,examples=()):
  scores={}
  for suite,cs in [('train',train),('development',dev)]:
   total=0
   for i,c in enumerate(cs):
    check();prefix=rt.encode(prompt(c,examples));r=rt.generate(prefix,limit=16);ok=r['action']==answer(c);total+=ok
    res.write(json.dumps(dict(arm=arm,step=step,suite=suite,index=i,case=c,prefix=prefix,expected=answer(c),correct=ok,**r))+'\n');res.flush()
    if suite=='train' and i==0 and not examples:first=(prefix,r['ids'])
   scores[suite]=total
  event('evaluation',arm=arm,step=step,**scores);print(arm,step,scores,flush=True)
  return scores,first if not examples else None
 def updates(arm,labels,n,checkpoints):
  opt=rt.optimizer();event('arm_start',arm=arm,initial_hash=digest(rt.snapshot()),optimizer_reset=True)
  data=[(rt.encode(prompt(c)),labels[i]) for i,c in enumerate(train)]
  data=[(x,rt.target(x,y)) for x,y in data];save(arm+'-tokens.json',[dict(prefix=x,target=y) for x,y in data])
  for j,index in enumerate(order[:n],1):
   check();x,y=data[index];r=rt.step(x,y,opt);event('update',arm=arm,step=j,index=index,**r)
   if j in checkpoints:
    filename=f'{arm}-{j}.safetensors';mx.save_safetensors(str(out/filename),dict(rt.snapshot()));scores,replay=evaluate(arm,j);replays.append((filename,*replay))
  return scores
 evaluate('base-none',0)
 acquired_scores=updates('acquisition',[answer(c) for c in train],128,[32,128]);acquired=rt.snapshot()
 save('acquisition.json',dict(scores=acquired_scores,criterion_met=min(acquired_scores.values())>=15))
 decisions={}
 for state,snapshot in [('base',base),('acquired',acquired)]:
  rt.restore(snapshot);evaluate(state+'-none',0);evaluate(state+'-context',0,train)
  self_records=[]
  for c in train:
   prefix=rt.encode(prompt(c));r=rt.generate(prefix,limit=16);self_records.append(dict(case=c,correct=r['action']==answer(c),prefix=prefix,**r))
  save(state+'-self.json',self_records)
  if a.policy:
   correct=sum(r['correct'] for r in self_records)
   decisions[state]=dict(source='none' if correct==16 else 'checked',probe_correct=correct,rule='abstain iff all 16 checked probes agree')
   save('decisions.json',decisions);event('decision',state=state,**decisions[state])
  for source,labels in [('checked',[answer(c) for c in train]),('self',[r['action'] for r in self_records]),('opposite',[wrong(c) for c in train])]:
   rt.restore(snapshot);event('source',state=state,source=source,correct=sum(y==answer(c) for y,c in zip(labels,train)),count=16)
   updates(state+'-'+source,labels,a.steps,sorted(set([min(32,a.steps),a.steps])))
   event('invariants',arm=state+'-'+source,**rt.invariants())
 for file,prefix,ids in replays:
  rt.restore(list(mx.load(str(out/file)).items()));r=rt.generate(prefix,limit=16);assert ids==r['ids'];event('reload',file=file,exact_tokens=True)
 status='complete'
except BaseException as e:event('failure',error=repr(e));raise
finally:
 event('complete',status=status,seconds=time.monotonic()-start,peak_mlx_bytes=mx.get_peak_memory());ev.close();res.close()
 (out/'SHA256SUMS').write_text('\n'.join(sha(f)+'  '+f.name for f in sorted(out.iterdir()) if f.is_file() and f.name!='SHA256SUMS')+'\n')
