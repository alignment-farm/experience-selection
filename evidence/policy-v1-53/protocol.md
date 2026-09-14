# Fresh evaluation of a checked-agreement abstention rule

2026-09-14. Fixed after development established base acquisition at128 and zero
incremental benefit from checked updates at the acquired state. The remaining
opposite/self acquired development branches do not determine this rule. This
protocol must be committed before any fresh evaluation generation.

## Rule and strongest fixed comparator

Use the same 16 available checked training observations as probes. Generate the
starting learner's greedy answers without teaching context. If all16 agree with
the checked answers, abstain; otherwise perform128 checked-label CE updates.
No confidence threshold, held-out utility lookup, or state name enters the rule.
Decision is saved before candidate training and before candidate evaluation.
Checked labels are privileged task supervision, supplied to both the rule and
always-checked reference; the gate additionally pays for16 probe generations and
16 exact-match verifications per state. This is a supervised gate, not a detector
of source reliability from unlabelled experience. Acquisition training is extra.

Checked is the strongest fixed development source at128 steps (base16/16 and
acquired16/16). No online choice among multiple beneficial sources is claimed.
The gate can match this accuracy while skipping redundant updates, but cannot
exceed a ceiling. This experiment tests when abstention helps and whether its
placement matters beyond the number of skipped updates.

## Fresh material, frozen runs

Three independent LoRA initialization/order seeds:47,53,59. Training ticket seeds:
20260914101,20260914201,20260914301, respectively; evaluation seed is training seed+1.
Each split contains four random tickets × two channels × two priorities (16).
All differ from development and from each other. Same channel mapping and prompt
family: this is narrow within-template generalization, not new-rule transfer.
Runner calls the evaluation split `development` for compatibility; for these three
runs ONLY it is the prospectively reserved evaluation split. No settings or rule
are changed based on these outputs. Report every seed, including failed acquisition.

Each seed constructs base and locally acquired starting states. All source arms
and no-update/context references repeat development-v1 controls.128 is the fixed
primary endpoint;32 is a prespecified diagnostic checkpoint, never selection data.
For each state record gate decision before training. Reuse counterfactual outcomes
of independently reset candidates to calculate gate outcome; do not misdescribe
this replay as a live multi-episode deployment. No-update observations are exact
same-state outcomes. The repeated initial base evaluation is a reproducibility
check and excluded from denominators.

Compare gate to always checked, always self, always opposite, never update, and
same checked examples in context. For a matched-count reference, enumerate uniformly
all placements of the gate's number of128-step checked update blocks over the two
states. This is an exact expectation over two possible placements if one update
block is used, not extra neural observations. Both skip and update outcomes are
measured. Report per-seed counts and totals; cases crossed on tickets are dependent,
so do not treat96 decisions as96 independent task draws.

## Costs and limitations

Separate the128-step construction of each acquired state from subsequent updates.
Charge gate probe prompt/completion tokens and wall time,32 total verifications per
seed, plus retained updates. Report fixed-source and context inference costs and
all experimental computation separately. No energy, hardware price, or investigator
labor measurement. Context is deliberately allowed the same16 checked examples on
every query. No claim of compute repayment over an unmeasured long horizon.

Single model, synthetic known labels, two deliberately separated learner states,
one mapping, small templated splits. Opposite labels are a controlled stressor;
0%-reliable data are not representative of real noisy observation streams. A gate
advantage over matched random placement is not an advantage over the best fixed
source in accuracy and does not establish open-ended source selection.
