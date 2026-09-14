"""Render findings from verified numeric publication tables."""
import json,argparse
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--metrics',type=Path,default=Path('evidence/publication-metrics/metrics.json'));parser.add_argument('--output',type=Path,default=Path('FINDINGS.md'));args=parser.parse_args()
m=json.loads(args.metrics.read_text());t=m['totals'];st=m['states'];p=m['seeds']
rows='\n'.join(f"| {label} | {st['base'][key]['correct']}/48 | {st['acquired'][key]['correct']}/48 |" for key,label in [('none','No update'),('checked','Checked labels, 128 updates'),('self','Self answers, 128 updates'),('opposite','Opposite labels, 128 updates'),('context','Same checked examples in context, no update')])
seed_rows='\n'.join(f"| {x['seed']} | {x['states'][0]['probe_correct']}/16 | {x['states'][0]['outcomes']['none']}/16 | {x['gate_correct']}/32 | {x['fixed_checked_correct']}/32 | {x['matched_random_expected_correct']:g}/32 |" for x in p)
basegain=st['base']['checked']['correct']-st['base']['none']['correct']
text=f'''# Experience selection: source utility depends on learner state

14 September 2026. Bounded study complete on functioning acquisition, measured
source contrasts, and a fresh evaluation of supervised abstention.

**The same perfectly checked source is useful before acquisition and redundant
after it.** Across three fresh seeds, 128 checked-label updates improve base routing
by {basegain}/48 requests, while adding no correct requests to an acquired learner
already at 48/48. A fixed checked-agreement gate matches always-checked training at
{t['gate_correct']}/96 while using {t['gate_updates']} subsequent optimizer updates instead of
{t['fixed_checked_updates']}. This is a placement and abstention result at a fixed 128-update budget in a small
supervised workload. It establishes neither a source selector that beats the best
fixed source in accuracy nor a neural advantage over accessible evidence: the
frozen base with the same checked examples in context scores 48/48. A shorter fixed
32-step schedule also reaches full accuracy on the fresh cases with fewer updates
than the gate, limiting the cost claim to the frozen 128-step comparison.

**What was measured.** A new synthetic ticket-routing rule maps amber to otter and
teal to heron. Priority and random eight-letter ticket identifiers are nuisance
fields. The generated answer must be exactly the destination name. This isolates
routing from the identifier-copying failures in the prior procedure-transfer study;
it does not measure complete tool-call production or an interactive agent task.
Each seed has four training tickets crossed with two channels and two priorities
(16 requests), plus four disjoint evaluation tickets with the same crossing.
Seeds 47, 53, 59 vary LoRA initialization and training order as well as ticket sets.
All splits are disjoint from development and one another; the rule and prompt
family stay fixed. These are 12 evaluation tickets, not 96 independent task draws.

The model is Qwen3-4B-Instruct-2507 bf16 at
`cdbee75f17c01a7cc42f958dc650907174af0554`, using native MLX 0.32.2 and MLX-LM
`86b48c461feebf87c58788655b7e57b5574b9e6d`. Rank 8 q/v LoRA in the final eight
blocks, scale 2, no dropout; answer-only cross-entropy including EOS; AdamW at
0.0005 with zero weight decay, batch one. Each source receives the same 128-example
order and starts with identical adapter weights and a fresh optimizer. Source
labels also have matched token counts in these runs. The acquired state is built
locally with 128 checked updates, charged separately; no sibling checkpoint is
loaded. Teaching examples are absent from all evidence-free evaluations.

**Development and freezing.** Development seed 43 initially scored 10/16 held-out
requests; 32 checked updates scored 8/16, but 128 reached 16/16 on both acquisition
and development. All failed early checkpoints remain saved. Checked, self and
opposite labels then yielded 16, 8, 0 correct development requests from base and
16, 16, 0 from acquired weights. The [development record](notes/development-results.md)
and [raw run](evidence/development-v1/) preserve this exploration. The gate protocol
was committed at `89f6bd2` after checked 128 reached ceiling in both states and before
fresh generation. Its remaining development branches did not determine the rule.
The [fixed protocol](protocol/policy-v1.md) reserves new seeds and tickets; 128 is
the endpoint, with 32 retained only as a diagnostic. All three fresh acquisition
runs reach 16/16 training and 16/16 evaluation. No checkpoint or policy was changed
based on these fresh results. The runner retains the split name `development` in
JSON; for these three runs only, that split is the reserved evaluation material.

**Source utilities, separated by starting state.** Each entry aggregates 48 fresh
routing requests. Source reliability is measured against the synthetic task oracle:
checked 100%, opposite 0%, and base self answers {sum(m['source_reliability']['base'])}/48.
Acquired self answers are 48/48 correct. The opposite source is a deliberately wrong
stress test, not a claim about naturally occurring noise.

| Treatment | Base state | Acquired state |
|---|---:|---:|
{rows}

The checked source's reliability does not change across states, but its incremental
utility does. Self-training is weaker than checked training from base. After
acquisition its labels equal checked labels; the supplemental audit verifies
byte-identical checked/self checkpoints at 32 and 128 in every fresh run. Thus these
are distinct named sources but identical training information in that state.
Opposite-label updates fit their own targets while destroying useful routing,
including from successfully acquired weights. Low training loss is therefore
insufficient evidence of useful learning. These contrasts hold loss, initialization
and order fixed within each state; across-state comparisons include the preceding
acquisition intervention and do not isolate every possible learner-state feature.

**A supervised abstention rule.** Generate the starting learner's answers to all 16
available checked training requests. Abstain if every answer agrees with its checked
label; otherwise train on checked labels for 128 updates. This rule uses checked
agreement, not the state name, future query answers, or candidate evaluation scores.
Decisions are saved before candidate training. It chooses checked updates for all
three base states and abstains for all three acquired states. Outcomes are calculated
from the independently reset candidate branches, a counterfactual replay rather
than a live deployment. Checked supervision is supplied to both this rule and the
always-checked reference; the gate additionally pays for its probe generations and
verifications. It does not infer source reliability without labels.

| Seed | Base checked-probe agreement | Base no update | Gate | Always checked | Matched-count random placement, expectation |
|---|---:|---:|---:|---:|---:|
{seed_rows}

The gate and strongest fixed source both score {t['gate_correct']}/96. Never updating
scores {t['no_update_correct']}/96. Randomly assigning the same one 128-update block
to one of the two starting states gives an exact expected score of
{t['matched_random_expected_correct']:g}/96, using measured outcomes for both possible
placements per seed. This is an expectation over assignments, not another set of
neural observations. It separates useful placement from merely doing fewer updates.
The gate cannot improve on always-checked accuracy here; the supported advantage
is avoiding redundant training under accessible checked supervision.

**Accessible evidence remains competitive.** The frozen base, shown the same 16
checked examples on each query, scores 48/48. This is a complete alternative for
this workload without any acquisition or update. Supplying those examples to
already acquired weights scores {st['acquired']['context']['correct']}/48 instead,
so the same-state context comparison totals {t['context_correct']}/96. Extra context
has a checkpoint-dependent effect here. That does not establish a general context
limitation; the successful frozen-base reference rules out a neural superiority
claim. No evidence is silently withheld from that reference.

**Costs.** Across the three two-state comparisons, the gate uses 384 subsequent
updates, against 768 for always checked. Including the 384 updates used to construct
the acquired states, those totals become 768 and 1152: one-third fewer total updates,
not one-half. The gate makes 96 probe generations and 96 checked-label comparisons.
Its measured gradient-step time sums to {t['gate_training_seconds']:.2f} seconds and
probe generation to {t['gate_probe_seconds']:.2f} seconds; always-checked gradient
steps sum to {t['fixed_checked_training_seconds']:.2f} seconds. These are sums of
measured components, not end-to-end deployment timings: model loading, resets,
audits, verifier time, label provision, hardware, energy and investigator work
are not priced. All neural training uses cached local weights, with no paid model
calls or new weight downloads. A brief resource overlap at the start of seed 47 is
[disclosed](notes/resource-use.md); timing is not an exclusive-machine benchmark.
The full fresh experiment costs {t['experimental_updates']} optimizer updates and
{t['experimental_seconds']:.1f} seconds of recorded run time, including all candidate
branches and checks. Peak recorded MLX allocation is {t['peak_mlx_bytes']/1e9:.3f} GB.
Development adds 896 updates and 301.2 seconds. No long-horizon repayment claim follows.

**A shorter fixed schedule limits the cost claim.** All fresh checked 32 diagnostic
checkpoints also score {t['checked_32_correct']}/96, using only
{t['checked_32_updates']} subsequent updates across the six states, fewer than the
gate's 384. That schedule failed on development (8/16) and was not chosen for the
prospective 128-step comparison. Its fresh success nevertheless rules out describing
the gate as cheaper than every fixed schedule or as compute-optimal. The supported
savings comparison holds update duration fixed; duration calibration is another
important decision. No settings were retuned or new test material consumed after
noticing this result.

**Verification and provenance.** The saved-record audits validate manifests, decoded
tokens, constructed prompts and targets, exact case separation, update order,
starting-state hashes and counts. The fresh runs preserve {t['raw_response_records']}
response records, of which {t['duplicate_baseline_records']} repeat the initial base
check and are excluded from accuracy denominators. Another 96 source generations
supply self labels and gate probes. All {t['checkpoint_replays']} saved fresh adapters
reproduce the first training request's exact tokens on reload; these repetitions
are verification only. Every source branch passes unchanged-base and exact reset-logit
checks with finite gradients. Native gradients and mutable adapter state are tested;
no soft-target teacher is used. All three runs' task, runner, runtime and protocol
snapshots have matching hashes. The initial independent audit's tokenizer return-type
failure and its fix are [preserved](notes/development.md); no experimental output
was rewritten. The [source record](sources/README.md) pins reused code and paper
versions; runtime reuse is from procedure-transfer at `dcdc0d6`, with diagnosis
read at `c183674`. No source-study files were modified.

The closest methods read were [aTTT 2607.03441v1](https://arxiv.org/html/2607.03441v1),
[Self-Guided TTT 2607.09415v1](https://arxiv.org/html/2607.09415v1),
[VANE 2608.09448v2](https://arxiv.org/html/2608.09448v2), and
[SEAL 2506.10943v2](https://arxiv.org/html/2506.10943v2). Their reading scopes and
cached hashes are recorded locally. This study adopts existing principles of
measuring post-update utility and controlling evidence access and update count;
it does not reproduce those methods or claim a new selection algorithm.

**Scope of closure.** The investigation now distinguishes useful, redundant and
harmful updates in a functioning acquisition regime and shows that an observable,
supervised agreement rule can place a reduced update budget usefully on fresh
cases. It closes this bounded phase on that explanatory progress. One model,
one arbitrary binary rule, two deliberately separated learner states, templated
inputs, strong checked labels and a small seed count limit the result. It does
not establish a dynamic choice between multiple useful sources, open-world source
reliability estimation, long-term retention, or real-agent task improvement.

Reproduce with [these instructions](notes/reproduction.md). Inspect
[aggregate metrics](evidence/publication-metrics/metrics.json),
[policy outcomes and component costs](evidence/policy-v1-analysis/policy.json),
[supplemental audit](evidence/policy-v1-supplemental/audit.json), and individual
[47](evidence/policy-v1-47/), [53](evidence/policy-v1-53/),
[59](evidence/policy-v1-59/) evidence directories.
'''
args.output.write_text(text)
