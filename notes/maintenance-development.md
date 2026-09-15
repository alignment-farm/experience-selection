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
