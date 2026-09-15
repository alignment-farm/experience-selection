"""Render the follow-up publication from audited development and fresh evidence."""
import argparse
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--development-one',type=Path,default=Path('evidence/followup-development-v1-audit/metrics.json'))
    p.add_argument('--development-two',type=Path,default=Path('evidence/followup-development-v2-audit/metrics.json'))
    p.add_argument('--fresh',type=Path,required=True)
    p.add_argument('--primary-step',type=int,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    d1,d2,f=[json.loads(path.read_text()) for path in [a.development_one,a.development_two,a.fresh]]
    step=str(a.primary_step); n=f['denominator']; totals=f['totals'][step]
    states=[(r,s,v) for r in f['runs'] for s,v in r['states'].items()]
    def total_cost(key):
        return sum(v['checkpoints'][step][key]['training']['updates'] for _,_,v in states)
    selected_updates=total_cost('selected')
    mixture_updates=sum(v['checkpoints'][step]['sources']['mixture']['training']['updates'] for _,_,v in states)
    construction=sum(v['construction']['updates'] for _,_,v in states)
    probes=sum(v['verification']['calls'] for _,_,v in states)
    verification_tokens=sum(v['verification']['prompt_tokens']+v['verification']['completion_tokens'] for _,_,v in states)
    base_context=sum(sum(r['base_context'].values()) for r in f['runs'])
    no_update=f['no_update']; mixture=totals['mixture']; selected=totals['selected']
    abstentions=sum(v['decision']['source']=='none' for _,_,v in states)
    acquired=sum(v['no_update'][state]==8 for _,state,v in states)
    strict_mixture_wins=sum(sum(v['checkpoints'][step]['sources']['mixture']['scores'].values())>
                           sum(v['checkpoints'][step]['selected']['scores'].values()) for _,_,v in states)
    def fraction(v): return f'{v}/{n}'
    md=[f'''# Selecting correct experience under partial acquisition

Follow-up to the accepted [first-phase findings](FINDINGS.md).
The first-phase publication, protocols and evidence remain preserved.

## Result

At the prospectively fixed **{a.primary_step}-update budget**, a fixed balanced
mixture scored **{fraction(mixture)}** on fresh later queries. Selecting only the
region with more current errors scored **{fraction(selected)}**; no update scored
**{fraction(no_update)}**. Both source pools contain correct observations. This
comparison concerns choosing experience by present errors, not estimating source
truthfulness or implementing a general adaptive selector.

The useful distinction is between learning a missing rule and improving behavior
across both rules. Component outcomes below measure what new training repairs and
what it loses. The mixture spends half its updates on each region; every pure
source spends the entire matched budget on one region. Thus source composition
can be assessed separately from the number of updates and from abstention.

## Workload and information access

Two regions, coast and inland, have opposite correct mappings from copper/violet
channels to heron/otter destinations. A random ticket is irrelevant. The request
names its region; evaluation asks for only the destination. These are four rule
cells in a synthetic routing component, not four independent real-world tasks.

For each run, eight checked training observations cover two tickets and all four
cells. Four additional labeled probes use one disjoint ticket. Sixteen later
queries use four further disjoint tickets. Both controls and selector can access
the same eight training labels, four verification labels, and pre-update probe
answers. Probe tickets are used only for checking, never secretly added to an
update. The context reference receives all twelve labeled observations in every
prompt. Obtaining labels is privileged synthetic supervision; real verification
costs were not measured.

The same sixteen later queries are used across both starting states within each
run, giving {len(f['runs'])*16} distinct later requests and {n} state/query outcomes
for each source policy in the fresh cohort.

Two states are constructed independently from the same base initialization using
64 updates on one region. Each source branch starts from the exact same saved
partial-state weights, with a fresh optimizer. The sources are coast, inland,
and a fixed 50:50 mixture. Mixture updates alternate coast then inland, using the
same shuffled within-region orders as the pure sources. All targets are correct.
The same answer-only cross entropy including EOS is used throughout.

The diagnostic gap policy uses four labeled probes: abstain if none is wrong,
choose the region with more errors otherwise, and choose the mixture on a tie.
This rule is fixed before candidate training. It is not claimed to be the best
possible adaptive policy. Outcomes for the chosen branch are read from the paired
candidate experiment; deploying the policy requires only its chosen branch, not
all the counterfactual training used to measure source utility.

## Development and bounded diagnosis

Exploratory seed 71 first tested 8, 16, 32 and 64 updates. Both exposed regions
were acquired 8/8 at state construction. Gap-only updates eventually learned the
other region 8/8 while reducing the previously learned region to 0/8. The mixture
had not acquired both rules at 64 steps. We extended the identical trajectories
to 128 and 256, and added mixture training from base to test joint learnability.
No development failures or intermediate checkpoints were removed.

| Development | Updates per branch | Fixed coast | Fixed inland | Fixed mixture | Gap policy |
|---|---:|---:|---:|---:|---:|''']
    for label,d in [('v1',d1),('v2',d2)]:
        for s,t in d['totals'].items():
            md.append(f"| {label} | {s} | {t['coast']}/32 | {t['inland']}/32 | {t['mixture']}/32 | {t['selected']}/32 |")
    bm=d2['runs'][0]['base_mixture']
    md.append('\nJoint mixture acquisition from base: '+', '.join(f"{s} updates → {sum(v['scores'].values())}/16" for s,v in bm.items())+'.')
    md.append(f'''
The fixed source, primary duration and shorter diagnostic checkpoints were chosen
on development and committed in [the fresh protocol](protocol/followup-fresh-v1.md)
before generating or evaluating fresh cases. V2 and v1 share exact checkpoint
files and update prefixes, checked by [the repeat audit](evidence/followup-repeat-audit/audit.json).

## Fresh comparison

All {len(f['runs'])} prespecified initialization/data seeds are included. No fresh
checkpoint is promoted after seeing its score. Each row below is a complete
balanced evaluation across the two states and all fresh runs.

| Updates per branch | Fixed coast | Fixed inland | Fixed mixture | Gap policy |
|---:|---:|---:|---:|---:|''')
    for s,t in f['totals'].items():
        md.append(f"| {s}{' (primary)' if s==step else ' (diagnostic)'} | {fraction(t['coast'])} | {fraction(t['inland'])} | {fraction(t['mixture'])} | {fraction(t['selected'])} |")
    md.append(f'''
No update: {fraction(no_update)}. All-evidence context at partial states:
{fraction(f['context'])}. Base with all evidence: {base_context}/{len(f['runs'])*16}.
The context reference is one fixed prompt, not an optimized retrieval system;
these results do not establish a general advantage of storing knowledge in weights.

### Component outcomes at the primary duration

Each entry is **coast correct / inland correct**, out of 8 per region. The state
name indicates which source constructed it, not an assumption about acquisition.

| Seed | State | No update | Coast source | Inland source | Mixture | Policy choice |
|---:|---|---|---|---|---|---|''')
    def pair(x):return f"{x['coast']} / {x['inland']}"
    for r,s,v in states:
        sources=v['checkpoints'][step]['sources']
        md.append(f"| {r['config']['seed']} | {s} | {pair(v['no_update'])} | {pair(sources['coast']['scores'])} | {pair(sources['inland']['scores'])} | {pair(sources['mixture']['scores'])} | {v['decision']['source']} |")
    md.append(f'\n{acquired}/{len(states)} constructed states meet the exposed-region acquisition criterion. '
              f'The mixture strictly exceeds the gap policy in {strict_mixture_wins}/{len(states)} states. '
              f'The policy abstains in {abstentions}/{len(states)} states; its update totals below make any savings explicit.')
    shorter=[(s,t) for s,t in f['totals'].items() if int(s)<a.primary_step]
    if shorter:
        md.append('\nThe shorter fixed-mixture comparator scores '+', '.join(f"{fraction(t['mixture'])} at {s} updates" for s,t in shorter)
                  +'. These outcomes are reported without changing the primary checkpoint. The selected primary duration is not claimed to be globally minimal.')
    md.append(f'''
## Costs and audit

The {len(states)} partial-state constructions cost **{construction} updates**.
Subsequent fixed-mixture training costs **{mixture_updates} updates**, versus
**{selected_updates}** for the gap policy. Totals including construction are
**{construction+mixture_updates}** and **{construction+selected_updates}** respectively.
No-update and context arms cost no subsequent updates. State construction is a
workload intervention and is charged explicitly; it is not free pretraining.

The policy makes **{probes} verification generations**, totaling
**{verification_tokens} prompt plus completion tokens**. Controls have equal
access to those results in the paired experiment. A fixed policy could omit the
verification calls when deployed; no verification saving is credited to selection.
The source pools have equal numbers of observations and the output targets have
the same objective; update counts are matched, while exact token costs are reported
below. Token counts are not FLOPs.

| Primary arm | Subsequent training input tokens | Target tokens | Later prompt tokens | Later completion tokens |
|---|---:|---:|---:|---:|''')
    for source in ['coast','inland','mixture','selected']:
        vals=[v['checkpoints'][step]['selected'] if source=='selected' else v['checkpoints'][step]['sources'][source] for _,_,v in states]
        md.append(f"| {source} | {sum(x['training']['input_tokens'] for x in vals)} | {sum(x['training']['loss_tokens'] for x in vals)} | {sum(x['use']['prompt_tokens'] for x in vals)} | {sum(x['use']['completion_tokens'] for x in vals)} |")
    mix_tokens=sum(v['checkpoints'][step]['sources']['mixture']['training']['input_tokens'] for _,_,v in states)
    gap_tokens=sum(v['checkpoints'][step]['selected']['training']['input_tokens'] for _,_,v in states)
    if mix_tokens==gap_tokens and mixture_updates==selected_updates:
        md.append('\nThe mixture and gap policy also match in aggregate training input tokens; the composition contrast is not explained by more gradient updates or more total input tokens.')
    actual=sum(r['actual_experiment_updates'] for r in f['runs'])
    calls=sum(r['actual_experiment_generation_calls'] for r in f['runs'])
    sec=sum(r['run']['seconds'] for r in f['runs'])
    md.append(f'''
Actually running every fresh counterfactual and diagnostic cost {actual} optimizer
updates and {calls} recorded scoring generations, plus
{sum(r['audit']['reloads'] for r in f['runs'])} exact-token reload generations.
Fresh run timers sum to {sec:.2f} seconds; timings describe observed execution,
not isolated-hardware latency. [Resource notes](notes/resource-use.md) record
shared-device coordination. The local host is a 64 GiB M1 Ultra.

The [audited metrics]({a.fresh.as_posix()}) link all raw runs. The audit checks file
hashes, prompt/token decoding, independent score reconstruction, disjoint tickets,
source orders, matched starting hashes, finite gradients with nonzero updates,
decisions before candidate training, frozen-base invariants and exact token replay
after checkpoint reload (one saved generation per evaluated checkpoint). All
evaluated adapters, script snapshots and raw records
are preserved. See [reproduction](notes/followup-reproduction.md).

## Interpretation and limits

Present prediction errors measure a remaining gap, but do not measure the total
utility of training only on that gap. An already-correct experience can still
matter when another update would disrupt its behavior. Per-region scores and the
joint-mixture acquisition control distinguish this from failure to learn the
new component or impossibility of representing both rules. Training loss alone
does not identify balanced downstream utility.

This study tests a single source decision followed by a fixed update schedule,
not repeated online reselection, learned mixture ratios, or prediction of update
damage. There are only two correct pools, four rule cells, one model/objective,
and a balanced query distribution. Fresh tickets and initializations test local
reproducibility; the {n} query outcomes are not {n} independent task draws. No
general statistical or real-agent performance claim follows from these counts.

Rehearsal and interference-aware selection are established methods. [CLEAR](sources/followup-rehearsal/README.md)
mixes new and replayed experience with RL-specific objectives; [MIR](sources/followup-rehearsal/README.md)
selects replay by predicted loss increases after a virtual update. Neither method
is implemented here. The finding concerns the sufficiency of a simple fixed
mixture and the limitation of current-error targeting on this workload, not the
novelty of rehearsal or a universal failure of selection.

## Provenance

Runtime reused unchanged from this study's accepted publication
`dca27dd46b634616e8895e0a137f23225c5dc7cc`. Qwen/Qwen3-4B-Instruct-2507 revision
`cdbee75f17c01a7cc42f958dc650907174af0554`; MLX-LM revision
`86b48c461feebf87c58788655b7e57b5574b9e6d`, MLX 0.32.2, exact environment in
`uv.lock` and each run's resource.json. Native LoRA rank 8, scale 2, q/v projections
in the final eight layers, no dropout; AdamW learning rate .0005, no weight decay,
batch one. No teacher-distribution access is used or claimed.

Original primary methods and transitive code provenance are in
[sources/README.md](sources/README.md); additional proceedings versions and hashes
are in [rehearsal sources](sources/followup-rehearsal/README.md).
The [development log](notes/followup-development.md) preserves changes and diagnosis.
''')
    a.output.write_text('\n'.join(md)+'\n')


if __name__=='__main__':main()
