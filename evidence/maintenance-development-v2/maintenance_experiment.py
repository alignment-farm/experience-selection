"""Calibration and recurrent maintenance with a virtual-damage replay policy."""
import argparse, json, random, subprocess, time
from pathlib import Path
import mlx.core as mx
import mlx.nn as nn
from mlx.utils import tree_map, tree_flatten
from runtime import Runtime, resource, digest, sha
from maintenance_task import SITES, cases, answer, prompt, execute, explicit

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--seed',type=int,default=101)
    p.add_argument('--data-seed',type=int,default=2026091501)
    p.add_argument('--protocol',default='protocol/maintenance-development-v1.md')
    p.add_argument('--mode',choices=['calibrate','recur'],default='calibrate')
    p.add_argument('--candidate-count',type=int,default=16)
    p.add_argument('--replicas',type=int,default=2)
    p.add_argument('--state-steps',type=int,default=128)
    p.add_argument('--steps',type=int,default=128)
    p.add_argument('--arms',nargs='+',default=['none','incoming','fixed25','fixed50','fixed75','mir50'])
    p.add_argument('--sequence',nargs='+',default=['birch','cedar','dune','birch','cedar','dune'])
    p.add_argument('--joint-checkpoints',nargs='+',type=int,default=[128,256,512])
    a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    def save(n,v): (out/n).write_text(json.dumps(v,indent=2)+'\n')
    for n in ['maintenance_experiment.py','maintenance_task.py','runtime.py']:(out/n).write_bytes(Path('scripts',n).read_bytes())
    (out/'protocol.md').write_bytes(Path(a.protocol).read_bytes());(out/'uv.lock').write_bytes(Path('uv.lock').read_bytes())
    ev=(out/'events.jsonl').open('x');responses=(out/'responses.jsonl').open('x')
    def event(kind,**kw):
        ev.write(json.dumps(dict(kind=kind,elapsed=time.monotonic()-start,**kw))+'\n');ev.flush()
    def check():
        assert time.monotonic()-start<3600 and mx.get_peak_memory()<40e9
    status='failed'
    try:
        save('config.json',{k:str(v) if isinstance(v,Path) else v for k,v in vars(a).items()})
        save('resource.json',resource());event('revision',git=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
        train,later=cases(a.data_seed,a.replicas),cases(a.data_seed+1,1)
        assert not {c['ticket'] for c in train}&{c['ticket'] for c in later}
        save('cases.json',dict(train=train,later=later))
        rt=Runtime();rt.reinitialize(a.seed);base=rt.snapshot();reloads=[]
        data=[(rt.encode(prompt(c)),answer(c)) for c in train]
        data=[(x,rt.target(x,y)) for x,y in data]
        save('training-tokens.json',[dict(case=c,prefix=x,target=y) for c,(x,y) in zip(train,data)])
        pools={s:[i for i,c in enumerate(train) if c['site']==s] for s in SITES}
        def evaluate(arm,episode,sites=SITES,suites=('later',),checkpoint=True):
            counts={};first=None
            for suite in suites:
                rows=[]
                for i,c in enumerate(train if suite=='train' else later):
                    if c['site'] not in sites:continue
                    check();x=rt.encode(prompt(c));r=rt.generate(x,limit=16);score=execute(c,r['action'])
                    row=dict(arm=arm,episode=episode,suite=suite,index=i,case=c,prefix=x,**r,**score)
                    responses.write(json.dumps(row)+'\n');responses.flush();rows.append(row)
                    if first is None:first=(x,r['ids'])
                counts[suite]={s:sum(r['success'] for r in rows if r['case']['site']==s) for s in sites}
            if checkpoint:
                file=f'{arm}-{episode}.safetensors';mx.save_safetensors(str(out/file),dict(rt.snapshot()));reloads.append((file,*first))
            event('evaluation',arm=arm,episode=episode,counts=counts)
            print(arm,episode,counts,flush=True)
        def update(arm,episode,step,index,opt,kind='update'):
            check();event(kind,arm=arm,episode=episode,step=step,index=index,**rt.step(*data[index],opt))
        def order(pool,n,seed):
            rng=random.Random(seed);result=[]
            while len(result)<n:
                batch=pool.copy();rng.shuffle(batch);result+=batch
            return result[:n]
        evaluate('base',0,suites=('train','later'))
        opt=rt.optimizer()
        for step,i in enumerate(order(pools['alder'],a.state_steps,a.seed),1):
            update('state',0,step,i,opt)
            if step in sorted(set([min(64,a.state_steps),a.state_steps])):evaluate('state',step,suites=('train','later'))
        initial=rt.snapshot();initial_hash=digest(initial)
        if a.mode=='calibrate':
            rt.restore(base);opt=rt.optimizer()
            for step,i in enumerate(order(list(range(len(train))),max(a.joint_checkpoints),a.seed),1):
                update('joint',0,step,i,opt)
                if step in a.joint_checkpoints:evaluate('joint',step,suites=('train','later'))
        else:
            def loss(index):
                tick=time.monotonic();x,y=data[index];ids=mx.array(x+y)[None,:]
                rt.model.eval();z=rt.model(ids[:,:-1])[:,len(x)-1:,:]
                v=nn.losses.cross_entropy(z.astype(mx.float32),ids[:,len(x):],reduction='mean');mx.eval(v)
                event('selection_loss',arm=arm,episode=episode,index=index,seconds=time.monotonic()-tick,input_tokens=len(x)+len(y)-1,loss_tokens=len(y))
                return v.item()
            for arm in a.arms:
                rt.restore(initial);assert digest(rt.snapshot())==initial_hash
                event('arm_start',arm=arm,initial_hash=initial_hash)
                seen=['alder'];archive=[]
                for episode,site in enumerate(a.sequence,1):
                    old=[s for s in seen if s!=site]
                    if site not in seen:seen.append(site)
                    archive_tick=time.monotonic()
                    archive=[dict(c,actions=answer(c)) for c in train if c['site'] in seen]
                    event('archive_build',arm=arm,episode=episode,rows=len(archive),new_rows=sum(c['site']==site for c in train) if site not in a.sequence[:episode-1] else 0,bytes=len(json.dumps(archive).encode()),seconds=time.monotonic()-archive_tick)
                    save(f'archive-{episode}.json',archive)
                    for c in later:
                        if c['site'] in seen:
                            tick=time.monotonic();actions=explicit(c,archive);score=execute(c,actions)
                            event('explicit',arm=arm,episode=episode,case=c,actions=actions,**score,seconds=time.monotonic()-tick,action_tokens=len(rt.tokenizer.encode(actions,add_special_tokens=False)),archive_rows=len(archive),archive_bytes=len(json.dumps(archive).encode()),retrieval_comparisons=next(i+1 for i,r in enumerate(archive) if (r['site'],r['kind'])==(c['site'],c['kind'])))
                    evaluate(arm+'-before',episode,seen,checkpoint=False)
                    opt=rt.optimizer();new_order=order(pools[site],a.steps,a.seed+episode)
                    replay_pool=[i for s in old for i in pools[s]]
                    fixed_order=order(replay_pool,a.steps,a.seed+100+episode)
                    ratio=int(arm[-2:])/100 if arm.startswith(('fixed','mir')) else 0
                    chosen=[];newpos=oldpos=0
                    for step in range(1,1 if arm=='none' else a.steps+1):
                        if arm.startswith('mir') and (step-1)%16==0:
                            before=rt.snapshot();h=digest(before)
                            candidate=random.Random(a.seed+10000*episode+step).sample(replay_pool,min(a.candidate_count,len(replay_pool)))
                            scores0=[loss(i) for i in candidate]
                            opt_hash=digest(tree_flatten(opt.state))
                            virtual=rt.optimizer();virtual.state=tree_map(lambda x:mx.array(x),opt.state)
                            update(arm,episode,step,new_order[newpos],virtual,kind='virtual_update')
                            future_hash=digest(rt.snapshot())
                            scores1=[loss(i) for i in candidate]
                            ranked=sorted(zip(candidate,scores0,scores1),key=lambda v:(-(v[2]-v[1]),v[0]))
                            chosen=[v[0] for v in ranked[:max(1,len(ranked)//2)]]
                            rt.restore(before);assert digest(rt.snapshot())==h
                            assert digest(tree_flatten(opt.state))==opt_hash
                            event('selection',arm=arm,episode=episode,step=step,ranked=ranked,chosen=chosen,reset_exact=True,optimizer_unchanged=True)
                        replay=int(step*ratio)>int((step-1)*ratio)
                        if replay:
                            i=chosen[oldpos%len(chosen)] if arm.startswith('mir') else fixed_order[oldpos]
                            oldpos+=1
                        else:i=new_order[newpos];newpos+=1
                        update(arm,episode,step,i,opt)
                        if arm.startswith('mir') and (step-1)%16==0:
                            assert digest(rt.snapshot())==future_hash
                            event('virtual_matches_actual',arm=arm,episode=episode,step=step,exact=True)
                    evaluate(arm,episode,seen)
        event('invariants',**rt.invariants())
        for file,x,y in reloads:
            rt.restore(list(mx.load(str(out/file)).items()));assert rt.generate(x,limit=16)['ids']==y
            event('reload',file=file,exact_tokens=True)
        status='complete'
    except BaseException as e:
        event('failure',error=repr(e));raise
    finally:
        event('complete',status=status,seconds=time.monotonic()-start,peak_mlx_bytes=mx.get_peak_memory());ev.close();responses.close()
        (out/'SHA256SUMS').write_text('\n'.join(sha(f)+'  '+f.name for f in sorted(out.iterdir()) if f.is_file() and f.name!='SHA256SUMS')+'\n')
if __name__=='__main__':main()
