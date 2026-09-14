"""New routing-only workload. Identifiers and priority are nuisance fields."""
import random,string
SCHEMA='Return only the destination name: heron or otter. Apply the established channel routing protocol. Priority and ticket identify the request.'
CHANNELS=['amber','teal']
def cases(seed,n):
 rng=random.Random(seed)
 words=[''.join(rng.choice(string.ascii_lowercase) for _ in range(8)) for _ in range(n)]
 assert len(set(words))==n
 return [dict(channel=c,priority=p,ticket=w) for w in words for c in CHANNELS for p in ['slow','fast']]
def answer(c):return {'amber':'otter','teal':'heron'}[c['channel']]
def wrong(c):return {'amber':'heron','teal':'otter'}[c['channel']]
def query(c):return f'channel={c["channel"]}; priority={c["priority"]}; ticket={c["ticket"]}'
def prompt(c,examples=()):
 extra=('\nChecked examples (the same channel rule applies to every ticket and priority):\n'+'\n'.join(query(x)+' -> '+answer(x) for x in examples)) if examples else ''
 return SCHEMA+extra+'\n'+query(c)
