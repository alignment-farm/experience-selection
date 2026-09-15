# Fresh partial-state source comparison v1

Fixed before fresh generation, training or evaluation. Development seed 71 and
all its tickets remain exploratory. This is a local reproducibility comparison,
not an independent sample of new rule systems or a general selector benchmark.

## Development basis and primary comparison

The same two-region task and unchanged learner/runtime are retained. Development
v1 found gap-only training learned the missing region while losing the previously
learned region. V2 extended the identical update trajectories: mixture128 reached
10/16 from coast-state and16/16 from inland-state; mixture256 repaired coast-state
16/16. Joint base-mixture256 reached16/16, establishing representability. The
complete v2 audit is required before launching this protocol.

**Primary:** fixed 50:50 mixture versus the pre-update gap policy, at256 subsequent
updates per state. Pure coast and pure inland sources, no update, and all-evidence
context remain comparisons. Mixture is the strongest fixed source composition
chosen on development. **Secondary diagnostic:** all three sources and gap policy
at128 updates; do not promote this checkpoint after seeing fresh results.
Keep state construction at64 updates on its source. No fresh tuning of duration,
loss, mixture ratio, prompts, policy thresholds, case counts or seeds.

This policy is an explicit test of choosing a pool by current errors, not a claim
that it is the best adaptive method. A possible useful null is that balanced
training suffices and current-error targeting destroys as much behavior as it
repairs. Neither a neural advantage nor an adaptive-selection advantage is required.

## Cohort and decisions

Three LoRA/order seeds and corresponding independent case-generation seeds:

| Initialization/order seed | Training data seed | Probe seed | Later seed |
|---:|---:|---:|---:|
| 73 | 20260914601 | 20260914602 | 20260914603 |
| 79 | 20260914701 | 20260914702 | 20260914703 |
| 83 | 20260914801 | 20260914802 | 20260914803 |

Each run has8 training cases,4 probes and16 later cases. Check ticket disjointness
within and across runs, and against both development attempts. All rules are the
same, and only tickets/initialization/order are fresh. Each later ticket crosses
all four region/channel cells. Report per-run and per-region raw counts; do not
treat96 correlated query outcomes as96 independent task draws or compute an
unjustified binomial significance claim.

Each run constructs coast and inland states independently from its exact base
initialization. Evaluate construction at8,16,32,64. The acquisition criterion is
8/8 later answers for the exposed region at64; partiality requires an error on the
other region. Include all states even if a criterion fails. Any later acquisition
diagnosis is separately exploratory and cannot replace this cohort silently.

At the final state, four greedy labeled probes determine the gap policy: none if
all agree; the region with more errors otherwise; mixture on a nonzero tie. Log
the decision before training any candidate. Final policy performance is read from
the exact selected candidate branch, with no best-outcome selection. There is no
online reselection during training and no candidate-outcome access for the policy.

## Information and cost controls

All controls can access the same two pools, synthetic checked labels and labeled
probe feedback. Training uses the original8 cases, not hidden extra probe labels.
Both source pools are100% correct by construction. The fixed mixture includes
both equally; each pure source trains on its four observations. Within-region
orders are matched and the mixture alternates coast then inland. All sources
use answer-only CE, same optimizer/settings and exact reset hash per state.

No update and the twelve checked examples in context are evaluated at both states;
also evaluate base with and without context. No base-mixture training is needed
in this cohort because the joint-acquisition question was diagnosed in development.
Do not claim a placement or amortized compute advantage from this untuned context
reference. A fixed source can omit policy checks at deployment; disclose that
advantage, alongside equal-access experimental accounting.

Charge state construction, four verification generations, update input/target
tokens and counts, and later generation tokens/time. Label acquisition is synthetic
oracle information, not a measured human or external verifier cost. Separate actual
counterfactual experiment expense from the cost of executing one chosen branch.
Keep per-component accuracy separate from training loss and overall success.

## Execution and evidence

Use scripts/run_followup_fresh.py after checking shared-resource availability.
Runs execute sequentially;1664 optimizer updates per run (128 state construction
+6×256 source updates),4992 for the cohort. Active limit30 minutes per run and
40GB MLX memory. Do not interfere with another study's active learner. Preserve
raw outputs and interrupted attempts; no silent run replacement or seed dropping.

Audit all file hashes, scoring/decoding/prompt reconstruction, matched states,
decision chronology, finite gradients, frozen base and exact reload generations.
Publish the follow-up separately from the accepted first-phase FINDINGS.md.
