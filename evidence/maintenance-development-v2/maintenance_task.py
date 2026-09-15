"""Owned compatible dispatch workflow; no cases from earlier studies."""
import random
SITES = ['alder', 'birch', 'cedar', 'dune']
KINDS = ['copper', 'violet']
# Each pair specifies eligible resource and mandatory preparation.
RULES = {
    'alder': [('heron','scan'), ('otter','seal')],
    'birch': [('otter','scan'), ('heron','seal')],
    'cedar': [('heron','seal'), ('otter','scan')],
    'dune': [('otter','seal'), ('heron','scan')],
}
def cases(seed, replicas=1):
    rng=random.Random(seed)
    return [dict(site=s,kind=k,ticket=f'{rng.getrandbits(40):010x}')
            for _ in range(replicas) for s in SITES for k in KINDS]
def answer(c):
    return ' '.join((*RULES[c['site']][KINDS.index(c['kind'])], 'ship'))
def prompt(c):
    return ('Dispatch sandbox. Return three space-separated actions only. '
            'heron/otter reserves one unit of that resource; scan/seal prepares the reserved parcel; '
            'ship consumes the reservation and dispatches it. Use the site and kind rules learned from examples. '
            'Initially both resources have stock 1, no reservation, no preparation, not shipped. '
            f"Site {c['site']}; kind {c['kind']}; ticket {c['ticket']}. Actions:")
def execute(c, output):
    resource,prep=RULES[c['site']][KINDS.index(c['kind'])]
    state=dict(heron=1,otter=1,reserved=None,prepared=None,shipped=False)
    errors=[]
    for token in output.strip().split():
        if token in ('heron','otter') and state['reserved'] is None and not state['shipped'] and state[token]>0:
            state[token]-=1;state['reserved']=token
        elif token in ('scan','seal') and state['reserved'] is not None and state['prepared'] is None:
            state['prepared']=token
        elif token=='ship' and state['reserved']==resource and state['prepared']==prep and not state['shipped']:
            state['reserved']=None;state['shipped']=True
        else: errors.append(token)
    expected=dict(heron=1-int(resource=='heron'),otter=1-int(resource=='otter'),reserved=None,prepared=prep,shipped=True)
    tokens=output.strip().split()
    return dict(success=not errors and state==expected, state=state, errors=errors,
                resource_correct=bool(tokens) and tokens[0]==resource,
                preparation_correct=len(tokens)>1 and tokens[1]==prep)
def explicit(c, archive):
    # Exact-key retrieval of a checked successful trace; ticket is intentionally irrelevant.
    for row in archive:
        if (row['site'],row['kind'])==(c['site'],c['kind']): return row['actions']
    return ''
