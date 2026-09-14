# Follow-up development log

## 2026-09-14: resumption

Read README.md, AGENTS.md, FOLLOWUP.md, first-phase methods/reproduction/resource
notes, root source guidance and source provenance. The root assessment linked in
FOLLOWUP.md (`../../construct-2/studies/2026-09-14-concurrent-findings.md`) is absent
in this checkout. The local handoff supplies sufficient authority and direction;
no source-study files were changed.

Re-read cached exact-version primary methods: SEAL 2506.10943v2 Algorithm 1 and
state-dependent reward discussion; aTTT 2607.03441v1 §4.5 matched-count/context
controls and §5 source-selection limitation; Self-Guided TTT 2607.09415v1 Algorithm
1 and its full-context final evaluation; VANE 2608.09448v2 validation/atomic state
deployment and measured task interference. Cached retrieval.json hashes and the
existing sources/README.md apply. No new arXiv request or paper code reuse.

Reuse this study's runtime.py unchanged from accepted publication
dca27dd46b634616e8895e0a137f23225c5dc7cc, with the model, MLX-LM revision and package
lock documented in sources/README.md. New workload and adapter initialization;
no first-phase or sibling adapters reused. Native CE gradients are the mechanism,
so chat or teacher-distribution access is unnecessary.

Development v1 commits the complementary-region workload, two partial-state
constructions, single-region sources, balanced mixture, and four update durations.
The observations are all correct. This tests selection among experience pools,
not a learned experience generator or unsupervised reliability estimator.
Selection uses labeled held-out probes accessible to every control. Four later
tickets measure nuisance-field generalization within four fixed rule cells;
they are not sixteen independent task draws.

Resource inspection before launch found no active Python/MLX training process on
the local 64GiB M1 Ultra. The visible command names this study and evidence output.
One job runs at a time, with a 40GB MLX and 30-minute bound. No sibling processes
or resource notes are modified. Timing is descriptive, not controlled latency.
