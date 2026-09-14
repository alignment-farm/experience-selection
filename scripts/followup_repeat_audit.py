"""Check that duration diagnosis reproduces every shared prefix and checkpoint."""
import argparse
import hashlib
import json
from pathlib import Path


def lines(path):
    return [json.loads(x) for x in path.read_text().splitlines()]


def main():
    p=argparse.ArgumentParser()
    p.add_argument('earlier',type=Path)
    p.add_argument('extended',type=Path)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    assert (a.earlier/'cases.json').read_bytes()==(a.extended/'cases.json').read_bytes()
    def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
    shared=[]
    for old in a.earlier.glob('*.safetensors'):
        new=a.extended/old.name
        if new.exists():
            assert sha(old)==sha(new),old.name
            shared.append(old.name)
    assert len(shared)>=15
    old_events=lines(a.earlier/'events.jsonl')
    new_events=lines(a.extended/'events.jsonl')
    new_updates={(e['arm'],e['step']):e for e in new_events if e['kind']=='update'}
    count=0
    for e in old_events:
        if e['kind']=='update':
            n=new_updates[(e['arm'],e['step'])]
            for k in ['index','region','loss','gradient_norm','input_tokens','loss_tokens']:
                assert e[k]==n[k],(e['arm'],e['step'],k)
            count+=1
    keys=['arm','step','suite','index']
    newer={tuple(r[k] for k in keys):r for r in lines(a.extended/'responses.jsonl')}
    responses=0
    for r in lines(a.earlier/'responses.jsonl'):
        key=tuple(r[k] for k in keys)
        if key in newer:
            assert r['prefix']==newer[key]['prefix'] and r['ids']==newer[key]['ids'],key
            responses+=1
    result=dict(earlier=str(a.earlier),extended=str(a.extended),exact_checkpoint_files=sorted(shared),
                exact_update_records=count,exact_shared_responses=responses)
    a.output.mkdir(parents=True,exist_ok=False)
    (a.output/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.output/'followup_repeat_audit.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
