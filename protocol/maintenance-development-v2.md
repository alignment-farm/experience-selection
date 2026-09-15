# Maintenance development v2 — ticket-diversity diagnosis

V1's joint training nearly memorized the 16 training examples at 256 updates but
only completed 2/8 new-ticket workflows. Preserve v1 and first inspect its 512
endpoint. V2 holds task, objective, model, initialization and prompt fixed while
increasing nuisance-ticket diversity: 16 training replicas per rule (128 records)
instead of two, joint checkpoints 512 and 1024. Alder construction stays128.
Seed101/data2026091501; prior development tickets are not fresh evaluation.
This tests whether the low new-ticket score reflects an inadequate sampling
regime rather than inability to represent all eight workflows. The next bounded
intervention if needed removes the irrelevant identifier from the input in both
training and evaluation; that would explicitly narrow the input claim.
No recurrent selector claim is made until acquisition works.
