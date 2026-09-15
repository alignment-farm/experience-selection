# Recurrent comparison design — development draft

Not a frozen fresh protocol. Start only after the diversity diagnosis establishes
functioning joint acquisition. Keep failed attempts and tune on development only.

All arms independently construct alder from identical base LoRA initialization.
The compatible incoming sequence is birch, cedar, dune, birch, cedar, dune. At
each episode measure complete action execution immediately before and after
updates on all sites observed so far. Each dispatch starts with its own full
inventory and must reach its specified final state; this is not one persistent
inventory across all dispatches. No historical rule becomes invalid.

Compare no update, incoming only, fixed replay fractions25/50/75%, and the
MIR-inspired method initially at50%. Tune duration and the strongest fixed ratio
on development complete-use totals, breaking ties by final completeness then
fewer updates. If selection50% is poor at low replay, add75% under the same budget
to distinguish selection quality from insufficient rehearsal. No adaptive win
is needed. No-update abstains unconditionally; the selector itself does not gate
updates in this phase.

All methods can access the same checked archive of successful training traces
and the same before-update verification cases/results. Fixed policies don't need
to run virtual updates. Selector scores labeled examples from the old-site
archive. It does not see later-case outcomes while selecting. Each16-update block
uses one incoming virtual AdamW step with copied current optimizer state, scores
up to16 seeded candidate records before/after, takes the largest loss increases,
and cycles through the top half on replay slots. Restore weights and check that
the real next incoming step reproduces the virtual weights exactly. The real
optimizer resets at episode boundaries for every learned policy.

A competent explicit arm keeps checked (site,kind,actions) records, matches the
site/kind key and replays the three-action trace into the identical sandbox. It
has no learned acquisition/update cost, but archive construction, bytes, lookup
comparisons, read time and action output are charged separately. This structured
lookup exploits an observed sufficient key; no general natural-language retrieval
claim follows. No future-site archive rows may be read before arrival.

Resource units: actual and virtual optimizer steps, separately scored forward
passes and their input/target tokens, archive rows/bytes, lookup comparisons,
verification/use generations and prompt/output tokens, measured time. Acquisition
cost belongs to each deployed learned branch but is paid once in the paired
experiment. Counterfactual arm execution and diagnostic verification are reported
separately. Exact step and target-token matching matters for attribution;
input-token variation is retained and disclosed. Per-episode pairing reports
retained, gained, lost, failed-both. Repeated-use aggregates count repeated cases,
not independent task samples. Development versus fresh evaluations remain distinct.
