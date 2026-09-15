# Frozen fresh maintenance evaluation v1

15 September2026. Commit this protocol, final policy implementation and batch
runner before generating or evaluating any fresh cases. No primary choice is
changed in response to fresh scores. Development V4 audit: fixed75=18/18,
MIR50=17/18, MIR75=18/18 at256 updates/arrival. Fixed75 and MIR75 both end8/8;
MIR75 is the strongest tested selector by the predeclared complete-use criterion.
At128 updates, fixed75=16/18, so256 is the developed primary duration.

## Frozen design

- Initial LoRA/data seed pairs: (103,2026091511), (107,2026091521).
- Training:16 independently generated ticket replicas for each of8 rule cells.
  Later queries:2 replicas/cell from data seed+1. No prior development tickets
  are intentionally reused; audit all cross-run ticket intersections.
- Construct alder using128 steps, same model/runtime/CE and shuffled order.
  Record training and later acquisition; include both seeds even if acquisition
  fails. Do not filter seeds, replace failures or select a fresh checkpoint.
- Incoming sequence: birch,cedar,dune,birch,cedar,dune. All rules remain valid.
  Every arrival includes only the observed sites' archive. All policies have
  equivalent evidence access. Primary outcomes are complete sandbox execution
  on all seen sites after each arrival; pair with before-update outcomes.
- Policies: none, fixed75, mir75, stop75. All start at identical constructed
  weights. Fixed75 and MIR75 receive256 actual updates each arrival. MIR75 uses
  the unchanged16-step block, at-most16-candidate/top-half, cloned-current-AdamW
  loss-increase mechanism. No fresh policy tuning or threshold is allowed.
- Stop75 follows exactly fixed75 for the first3 arrivals and then unconditionally
  performs zero updates. It is a fixed schedule, not an acquisition-dependent
  gate. Count its failures if the prefix is incomplete. Verify byte-identical
  prefix checkpoints and unchanged weights after arrival3.
- None performs no maintenance updates. The competent explicit archive lookup
  uses exactly the same successful training records available at that arrival
  and executes the same action language and complete-state checker.
- Greedy generation, cap16 tokens; same prompts, objective, optimizer and frozen
  base as development. Every target has5 tokens including EOS. Optimizers reset
  per arrival for all updating policies. Record exact input-token differences.

## Primary reporting and costs

Report every seed, all6 arrivals and the full post-arrival complete-use aggregate:
84 outcomes/seed,168 total/policy. Separately show the acquisition prefix
(36/seed) and recurring suffix (48/seed), final completion (16/seed), and paired
retained/gained/lost/failed-both. These are repeated uses of32 distinct later-ticket
requests over8 rule cells and2 initializations, not168 independent task draws.
The rules and action grammar are unchanged; fresh testing concerns new tickets
and initializations in this bounded workload, not new workflow semantics.

Charge128 construction steps per deployed learned policy/seed. Fixed75 and MIR75
have1536 maintenance steps/seed, stop75 has768 and none0. MIR75 adds96 virtual
steps and3072 labeled loss-scoring forwards/seed. Keep units separate. Report
whole-selection wall time including its components without double counting;
archive construction/access, serialized bytes, adapter bytes, action tokens,
subsequent generation and complete behavior. Before-update generations and
checkpoint replay are paired research diagnostics, not hidden deployment calls.
Report actual counterfactual execution separately from one deployed policy.
No real human verification-cost or exclusive-hardware latency claim is allowed.

A selector advantage requires comparable complete behavior and a useful cost
advantage over the strongest developed fixed comparator. A stop75 saving is
attributed to its smaller update count and fixed stopping schedule, not damage
prediction. An informative null or local limitation is an acceptable result.

## Execution and audit

Recheck shared-device availability, then run one visible sequential two-seed
batch with scripts/run_maintenance_fresh.py --mir-arm mir75. Use the fresh-v1
output names; existing outputs must fail. Each child retains its3600s active-run
and40GB peak-MLX limits. Preserve any execution failure and stop the cohort rather
than silently replacing a run. Do not tune to fresh outcomes after a failure.
The CPU audit checks hashes, token decoding/prompts, exact evaluation membership,
source orders/quotas, historical-only candidate access, matched starts, native
virtual/reset invariants, frozen-prefix hashes, complete-state scores and costs.
Publish a separate MAINTENANCE_FINDINGS.md with links to raw evidence and methods.
