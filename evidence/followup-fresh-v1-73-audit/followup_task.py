"""Two correct experience pools with region-specific routing rules."""
import random
import string

REGIONS = ('coast', 'inland')
CHANNELS = ('copper', 'violet')
SCHEMA = ('Return only the destination name: heron or otter. Apply the established '
          'region-specific channel routing protocol. The ticket identifies the request.')


def cases(seed, n):
    rng = random.Random(seed)
    tickets = [''.join(rng.choice(string.ascii_lowercase) for _ in range(10)) for _ in range(n)]
    assert len(set(tickets)) == n
    return [dict(region=r, channel=c, ticket=t) for t in tickets for r in REGIONS for c in CHANNELS]


def answer(c):
    return 'heron' if (c['region'] == 'coast') == (c['channel'] == 'copper') else 'otter'


def query(c):
    return f"region={c['region']}; channel={c['channel']}; ticket={c['ticket']}"


def prompt(c, examples=()):
    evidence = ('\nChecked examples (each region has its own channel rule, independent of ticket):\n'
                + '\n'.join(query(x) + ' -> ' + answer(x) for x in examples)) if examples else ''
    return SCHEMA + evidence + '\n' + query(c)
