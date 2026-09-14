"""Evaluate a frozen gate by replaying complete, independently reset candidate arms.
This script must be used only under the prospective policy protocol.
"""
import argparse,json,itertools
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('runs',type=Path,nargs='+');p.add_argument('--output',type=Path,required=True);a=p.parse_args()
a.output.mkdir(exist_ok=False,parents=True)
all_rows=[]
for root in a.runs:
 report=json.loads((root.parent/(root.name+'-analysis')/'analysis.json').read_text())
 config=json.loads((root/'config.json').read_text());assert config['steps']==128
 lookup={(r['arm'],r['step'],r['suite']):r for r in report['summary']}
 states=[]
 for state in ['base','acquired']:
  probes=json.loads((root/(state+'-self.json')).read_text())
  decisions=json.loads((root/'decisions.json').read_text())
  correct=sum(r['correct'] for r in probes);choice='none' if correct==16 else 'checked'
  assert decisions[state]['source']==choice and decisions[state]['probe_correct']==correct
  outcomes={s:lookup[(state+'-'+s,0 if s in ['none','context'] else 128,'development')]['correct'] for s in ['none','context','checked','self','opposite']}
  costs={s:(report['cost'][state+'-'+s]['seconds'] if s not in ['none','context'] else 0) for s in outcomes}
  states.append(dict(state=state,probe_correct=correct,choice=choice,outcomes=outcomes,training_seconds=costs,probe_seconds=sum(r['seconds'] for r in probes),probe_prompt_tokens=sum(r['prompt_tokens'] for r in probes),probe_completion_tokens=sum(r['completion_tokens'] for r in probes)))
 count=sum(s['choice']=='checked' for s in states)
 gate=sum(s['outcomes'][s['choice']] for s in states)
 # Enumerate uniformly random placements with exactly the same update count.
 random_placements=[sum(s['outcomes']['checked' if i in subset else 'none'] for i,s in enumerate(states)) for subset in itertools.combinations(range(2),count)]
 all_rows.append(dict(run=str(root),seed=config['seed'],states=states,gate_correct=gate,n=32,gate_updates=128*count,fixed_checked_updates=256,fixed_checked_correct=sum(s['outcomes']['checked'] for s in states),no_update_correct=sum(s['outcomes']['none'] for s in states),context_correct=sum(s['outcomes']['context'] for s in states),matched_random_placements=random_placements,matched_random_expected_correct=sum(random_placements)/len(random_placements),gate_training_seconds=sum(s['training_seconds'][s['choice']] for s in states),gate_probe_seconds=sum(s['probe_seconds'] for s in states),gate_checked_verifications=32,fixed_checked_training_seconds=sum(s['training_seconds']['checked'] for s in states),acquisition_updates=report['cost']['acquisition']['updates']))
(a.output/'policy.json').write_text(json.dumps(all_rows,indent=2)+'\n');(a.output/'policy_report.py').write_bytes(Path(__file__).read_bytes())
print(json.dumps(all_rows,indent=2))
