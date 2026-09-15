# Maintenance methods and measurement

## Task and complete behavior

Owned dispatch sandbox, eight rule cells: four sites (alder, birch, cedar, dune)
and two parcel kinds (copper, violet). Each cell specifies an eligible resource
(heron/otter) and mandatory preparation (scan/seal). The learner emits three
space-separated actions: reserve the resource, prepare, ship. Reserve decrements
that inventory; preparation requires a reservation; shipment requires both the
eligible resource and correct preparation and clears the reservation. Success
requires the complete expected state, including both inventories, preparation,
cleared reservation and shipment, with no invalid action. Component scores only
diagnose errors. The independent bounded trace check exhausts every sequence of
length0–4 over the five action words and an invalid word.

Each dispatch starts with stock1 for both resources and no other state. State is
consequential within a dispatch; inventories do not persist between dispatches.
The task has eight input cells and four valid action traces, not eight independent
real-world tasks. Rules stay valid forever. Random ticket strings are irrelevant,
but included in every learned prompt. Training and later tickets are disjoint.
New-ticket evaluation tests nuisance invariance on these same eight cells, not
novel business rules or broad workflow generalization.

## Learner and learning

Qwen/Qwen3-4B-Instruct-2507 revision
cdbee75f17c01a7cc42f958dc650907174af0554; existing native runtime and uv.lock.
MLX-LM86b48c461feebf87c58788655b7e57b5574b9e6d; exact installed packages and all
model file hashes in each resource.json. Native LoRA rank8/scale2 on q/v
projections in the final8 layers, dropout0. AdamW .0005, no weight decay, batch1.
Answer-token CE includes EOS. Every target is5 tokens. Greedy generation capped
at16 tokens; the emitted trace is executed by the sandbox. Each request uses a
fresh prompt with no teaching examples or previous request history.

Alder-only construction uses128 updates from newly initialized LoRA on the same
frozen pretrained base. All policy branches restore identical constructed weights;
optimizers reset at each arrival. Later states intentionally diverge as consequences
of policy history. Starting-state cost is charged to each deployed learned policy,
although the paired experiment constructs it once. No earlier study's adapters or
cases are inherited. The calibration's joint-acquisition adapter is not used to
smuggle future-site experience into recurring comparisons.

Development established joint acquisition using16 tickets/cell and1024 updates.
The two-ticket512 attempt memorized16 training examples but completed3/8 unseen
tickets. Sixteen-ticket512 achieved4/8; at1024 it achieved8/8 and128/128 training.
These interventions establish a functioning regime; they do not separately prove
that ticket diversity is necessary at1024.

## Policies and information

Arrival prefix birch, cedar, dune introduces compatible rules. Later recurrences
repeat those sites. After each arrival evaluate all seen sites, paired before and
after updating. The primary complete-use total counts post-update outcomes. Those
counts contain repeated use of the same cases and are not independent samples.

Incoming-only uses its site pool. Fixed25/50/75 use the named fraction of updates
on old-site replay, with the remainder incoming. Shuffled within-pool orders are
seeded, repeated as needed and shared as prefixes where counts permit. No-update
keeps the initial alder state. Stop75 is identical to fixed75 for three arrivals,
then freezes on a fixed schedule irrespective of measured acquisition. It does
not get a hidden fresh-outcome gate. Its lower update count is a separate control.

MIR50/75 use the same respective quotas. Every16 actual updates, clone current
AdamW state, make one virtual update on the next incoming example, score a seeded
sample of at most16 old-site archive records before/after, rank their mean target
CE increases, and cycle through the top half at replay slots. Ties use record
index. Restore exact weights and verify the live optimizer is untouched and the
next actual incoming update exactly matches virtual weights. No-update is not a
MIR decision: this selector always updates during its scheduled learning arrivals.

This is a MIR-inspired block adaptation, not a replication of the NeurIPS2019
image-classifier experiments. The author implementation uses SGD, random buffer
subsampling and combined incoming/replay gradients; ours uses AdamW, sequential
single-example updates and blockwise selection. Versioned source inspection and
license are in sources/maintenance-mir. No author code is imported. We do not use
historical-minimum loss, reservoir replacement or teacher distributions.

All policies can access the same successful training traces and paired labeled
verification results. MIR's operative signal uses training-archive labels only;
it never selects on later-case results. Before-update generations are paired
research diagnostics, not necessary deployment calls for these fixed policies
or the MIR loss scorer. Source labels and the sandbox checker are privileged,
correct synthetic supervision. Human annotation or real-world verification costs
were not measured.

The explicit reference scans the same checked in-memory archive by the structured
(site,kind) key, retrieves the successful action trace and executes it in the same
sandbox. The key schema and the ticket's irrelevance are designed knowledge, not
learned by this reference. No future-site record is accessible before arrival.
This is a competent structured lookup, not a test of general language retrieval.
Archive construction, serialized bytes, lookup comparisons, action-token counts
and observed lookup-plus-execution time are measured. Python object overhead,
persistent-disk access and real annotation costs are not included in those units.

## Costs and audit

Match actual optimizer steps and target tokens when comparing selection quality;
retain exact input-token differences caused by ticket and source composition.
Report actual steps separately from virtual steps, scored forwards, model prompt
and completion tokens, archive bytes, adapter bytes and measured seconds. Token
counts are not FLOPs. Whole-selection time includes copying, hashing, scoring,
virtual training, ranking and restore; its component timings must not be added
again. Shared-device timings are descriptive, not isolated latency benchmarks.

Distinguish deploying one policy from actually executing every counterfactual
branch, checkpoint audit and before-update diagnostic. Separate initial acquisition,
subsequent maintenance and repeated-use generation. A useful-cost advantage needs
comparable complete behavior; lower loss or fewer updates alone cannot establish it.

Runs preserve exact code/protocol/lock snapshots, configuration, model hashes,
tokenized examples, every training/virtual update, candidate scores/selections,
raw generations, complete states, evaluated adapters and SHA256 manifests. The
CPU auditor independently reconstructs expected traces and final states, decodes
tokens and regenerates prompts, checks disjoint tickets, source orders/quotas,
matched starts, selection membership, exact-reset/reload records and aggregate
costs. Native checks establish frozen-base invariants and exact greedy token replay
for one saved generation per evaluated adapter. They do not re-execute every
counterfactual update in the CPU audit.
