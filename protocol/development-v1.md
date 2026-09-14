# Development comparison v1 — 2026-09-14

Committed before execution. This is workload calibration, not a confirmatory test.
Task: amber→otter, teal→heron; priority and random ticket are nuisance variables.
This new two-way routing task removes identifier production from the prior task.
No prior study's examples or adapters are loaded. Reuse only runtime and frozen base.

Train: four tickets, seed 20260914031, crossed with both channels and priorities
(16 cases). Development: four new tickets, seed 20260914032 (16 cases).
Initialize LoRA with seed 43, acquire by 128 CE updates on checked labels, evaluating
at 32 and 128. Acquisition requires at least 15/16 train AND development.
If it fails, preserve results and diagnose before interpreting source utility.

From identical base and acquired snapshots, reset AdamW for each source:
checked canonical labels; fixed pre-update greedy self answers; deliberately
opposite labels (a diagnostic 0%-reliable source, not a natural corruption claim).
All use answer-only CE including EOS, LR .0005, batch one, same shuffled order,
rank8 q/v adapters in final eight layers, scale2, no dropout. Evaluate 32 and128
updates on recall and development, with teaching text absent. Save checkpoints,
raw token records, source correctness, step loss/gradient and token/time costs.
No-update and same-16-checked-examples-in-context evaluated at each starting state.
Self outputs may differ in length: objective and update count matched, tokens charged.
Compare all source utilities within starting state. Across-state differences include
128 acquisition updates and must not be called source effects.

Bound: 896 optimizer steps (128 acquisition + 2×3×128); 40 GB MLX allocation and
30 minutes per run. Probe resets and frozen base; verify final checkpoints reload.
No full-vocabulary teacher used or required for this hard-label study.
A policy is developed only after utility contrasts are measured. Fresh tickets and
a fixed rule are required for any subsequent evaluation of that policy. No claim
of real-agent success, long-term retention, or cost repayment follows this task.
