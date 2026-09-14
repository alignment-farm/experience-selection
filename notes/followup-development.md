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

## Development v1 completed

Source commit bf8e820;512 updates,248.33 seconds,9.61GB peak MLX. Raw-record audit
passes hashes, decoding, prompt reconstruction, outcome scoring, labeled-probe
decisions before candidates, matched reset hashes,32 checkpoint token replays and
frozen-base/logit-reset invariants. The audit is CPU-only.

Both state64 constructions acquired the exposed region8/8 and scored0/8 on the
other. The gap policy correctly identified the missing region in both states.
Every single-region source scored8/16 at every tested duration8,16,32,64: the
gap source eventually moved all eight successes to the formerly wrong region,
while the already-known source preserved the original successes. Thus a source
can be correct and teach its component without improving balanced downstream
utility. The held-out errors alone do not identify a safe isolated update.

Balanced mixture totals across both states:16/32 at8,8/32 at16,16/32 at32,21/32
at64. The last value comprises8/16 from coast-state and13/16 from inland-state.
No joint acquisition yet. Preserve the0/16 transient coast-mixture16 result.
The all-evidence context reference scored20/32 across partial states; base context
scored12/16, so no general information-placement advantage is established.

Development v2 extends the identical trajectories to128/256 updates and adds
base-mixture to diagnose insufficient duration versus prior specialization.
This is a bounded calibration, not a fresh test. Protocol committed before launch.
At v1 completion the waiting retention study began its own development job;
v2 is prepared while this study yields the GPU.
