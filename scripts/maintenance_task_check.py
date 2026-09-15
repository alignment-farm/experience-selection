"""Exhaustive bounded trace checker: completion requires the unique valid path."""
import itertools
from maintenance_task import cases, answer, execute, explicit
for c in cases(11):
    for n in range(5):
        for xs in itertools.product(['heron','otter','scan','seal','ship','bad'],repeat=n):
            text=' '.join(xs)
            assert execute(c,text)['success']==(text==answer(c)),(c,text)
archive=[dict(c,actions=answer(c)) for c in cases(12)]
for c in cases(13):assert execute(c,explicit(c,archive))['success']
print('Checked all traces of length 0–4 across 8 rules and disjoint-ticket retrieval.')
