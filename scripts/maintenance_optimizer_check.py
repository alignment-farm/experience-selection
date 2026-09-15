"""Exercise virtual AdamW state isolation on CPU before recurrent model work."""
import json
from pathlib import Path
import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
from mlx.utils import tree_map, tree_flatten, tree_unflatten
mx.set_default_device(mx.cpu)
def arrays(tree):return [(k,mx.array(v)) for k,v in tree_flatten(tree)]
def equal(a,b):return all(k==j and bool(mx.all(x==y)) for (k,x),(j,y) in zip(a,b)) and len(a)==len(b)
m=nn.Linear(2,2);o=optim.AdamW(learning_rate=.0005,weight_decay=0.)
x=mx.array([[1.,2.]]);y=mx.array([[.2,.3]])
def step(opt):
    loss,g=nn.value_and_grad(m,lambda model:mx.mean((model(x)-y)**2))(m)
    opt.update(m,g);mx.eval(m.parameters(),opt.state);return loss.item()
for _ in range(3):step(o)
state=arrays(m.parameters());os=arrays(o.state)
v=optim.AdamW(learning_rate=.0005,weight_decay=0.);v.state=tree_map(lambda x:mx.array(x),o.state)
step(v);future=arrays(m.parameters());assert equal(os,arrays(o.state))
m.update(tree_unflatten(state));mx.eval(m.parameters());assert equal(state,arrays(m.parameters()))
step(o);assert equal(future,arrays(m.parameters()))
r=dict(device='cpu',priming_updates=3,virtual_optimizer_isolated=True,weights_restored=True,virtual_matches_actual=True)
Path('evidence/maintenance-optimizer-check.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
