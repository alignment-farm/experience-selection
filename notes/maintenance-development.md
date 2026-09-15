# Maintenance development log

## V1: acquisition works locally, new-ticket transfer fails

Committed setup9937cc4. Calibration completed185.97s, peak9.62GB,640 actual
updates. Base0/8 later; alder construction64 and128 both2/2 on alder later,
0/6 elsewhere. Joint from base:128 updates1/8 later;256 updates2/8;
512 updates3/8, despite16/16 training completion. Raw responses and all evaluated
adapters retained in evidence/maintenance-development-v1. CPU independent audit
passed, including decoded responses, complete state, frozen base and reload records.
The sequence checker exhaustively checks all traces of length0–4 across8 rules.

V2 is a bounded sampling diagnosis, not a fresh test: increase training replicas
from2 to16 with the same initialization, rules, loss and prompt. Compare512 and
1024 joint updates. This distinguishes insufficient nuisance diversity/duration
from joint representability; no training-loss success substitutes for later tasks.

Before any recurrent run, corrected the MIR draft to clone the actual optimizer
moments for its virtual step. It checks that actual optimizer state is untouched,
weights restore exactly, and the next actual incoming step matches virtual weights.
A seeded candidate sample caps forward-scoring cost at16 records/block, as the
larger-diversity archive otherwise makes selection unnecessarily costly.

## Resource coordination

V1 ended before starting any second job. Sibling retention learner4678 was waiting
and began GPU work after V1; this study yields while preparing diagnostics and
analysis. No sibling process or file is modified.

CPU audit expansion: an initial prompt-reconstruction check failed because this
Transformers version returns BatchEncoding by default. Preserved its failure in
maintenance-development-v1-audit-v2/failure.json; explicit return_dict=False
repairs it. V3 audit passes response, prompt, component and complete-state checks.
This is an auditor bug; no experimental response or checkpoint was altered.
The CPU optimizer test with accumulated AdamW moments passes isolation, exact
restoration and equality between virtual and actual parameter updates.

## V2: a functioning acquisition regime

At512 joint updates the128-record pool gives64/128 train and4/8 later. All later
outputs choose otter, with site-specific preparation, ignoring kind. At1024,
128/128 training and8/8 unseen-ticket workflows succeed. Diverse supervision plus
sufficient duration resolves the floor on this development seed. This is not a
claim that diversity alone suffices: its matched512 outcome remains incomplete.
Alder state64/128 both32/32 train and2/2 later. Replay comparisons may now proceed.

V3 tunes three fixed fractions and MIR50 on the three-arrival prefix at128 updates.
A bounded256-step follow-up will tune duration. Fresh tests will add three recurring
arrivals; all costs and repeated-case dependence will be disclosed.

Before V3, added whole-selection wall timing (including cloning, hashing, scoring,
virtual update, ranking and restoration). Component forward/update times remain
separate and must not be added again to the inclusive selection total.

After V3 launch (its source snapshot preserved), prepared a diagnostic-generation
reduction for subsequent recurrent runs: base scores only later queries; initial
state scores train and later only on alder. This removes gratuitous future-site
training-case generations, not any selector input or primary before/after measure.
Greedy evaluation does not update weights. Check exact initial-state file equality
with V3 before claiming unchanged trajectories. Added configurable later replicas
so fresh claims can use more disjoint tickets without changing training.

## V3: composition matters on complete workflows

Independent audit passes. Total uses over the three arrivals (18 repeated-state
outcomes): none6, incoming6, fixed25 7, fixed50 10, fixed75 16, MIR50 7; explicit18.
Fixed75 ends8/8, retains10 and loses0. Incoming learns6 and loses6; MIR50 likewise
learns6 and loses6. Each updating arm spends384 steps and1920 target tokens.
MIR50 adds24 virtual updates and768 loss-scoring forwards;24 exact virtual/actual
next-step and optimizer-isolation checks pass. Starting checkpoint matches V2
byte-for-byte. Full run728.34s,9.63GB peak. V4 tests256-step duration and MIR75,
matching the strongest fixed replay fraction instead of blaming ranking for an
unmatched rehearsal budget. A fixed post-prefix stop schedule is added for fresh
recurrence, with its lower update count reported separately.

## V4: duration and matched replay-budget diagnosis

Audit passed. At256 updates/arrival, fixed75=18/18, MIR50=17/18, MIR75=18/18;
all end8/8. The shorter failure of MIR50 is not a general selector failure:
longer duration and75% replay suffice for complete development behavior. Fixed75
also suffices without predicting damage. Both choices and primary256 duration
are now frozen for two new initialization/data seeds and a6-arrival recurrence.
The fixed post-prefix stop control separates repeated-update costs from selection.
The reduced diagnostic-generation code produces the same state128 SHA as V3.
V4 completed1019.82 seconds, peak9.63GB. No fresh cases have yet been generated.

## Fresh execution and audit preparation

Fresh policy, protocol and cohort fixed at ba91a06 before any fresh case generation.
Analysis code may advance while the cohort runs; the cohort audit compares every
run-owned task/runtime/experiment snapshot and protocol byte-for-byte to that
commit. The first fresh run started only after the sibling native audit exited.
The auditor's gradient sanity check was corrected prospectively to allow finite
zero gradients at convergence (requiring some nonzero gradients per updating arm),
rather than declaring any zero gradient an execution error. This changes no
behavioral criterion, training, selector, fresh seed or checkpoint choice.

## Fresh cohort completed

Both frozen seeds completed; per-run and cohort audits pass. Fixed75=143/168,
MIR75=151/168, stop75=118/168, none=48/168, explicit=168/168. Fixed and MIR both
end32/32. Seed103 gives all three updating/stopping policies84/84; seed107
accounts for the differences. MIR's acquisition prefix67/72 exceeds fixed55/72,
but recurrence84/96 is below fixed88/96. Stop shares the fixed prefix exactly,
then freezes: seed107 remains5/16 while continued fixed replay reaches16/16.
This identifies the consequence of stopping before complete acquisition without
retuning fresh policies. Initialization and ticket effects are not separated.
All fresh snapshots match ba91a06, ticket sets are disjoint, exact reload and
virtual-step checks pass. Component and complete outcomes, costs and limitations
are published in MAINTENANCE_FINDINGS.md. No additional winning-config search is
needed: the bounded study establishes a local accuracy/work tradeoff and a
state-dependent limitation of the fixed stopping schedule.
