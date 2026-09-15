# MIR implementation inspection, 15 September 2026

Author repository https://github.com/optimass/Maximally_Interfered_Retrieval,
HEAD resolved to `35eda78bcdd35025b16b0b1039a926d34aad4851`. Cached files downloaded
from raw.githubusercontent.com at that exact revision. Proceedings method §3.1
and Algorithm 1 read from the already cached NeurIPS 2019 PDF in
../followup-rehearsal/. No new arXiv request. `utils.py:get_future_step_parameters`
uses a copied model and one SGD step. Author code is cached for inspection, not
imported into this study. License preserved. Local implementation is independently
written using this study's existing native runtime at dee1e3159ed0105f6a090c65b72f57cbc386fb10.

Local adaptation: answer-token CE for multi-action text; one virtual AdamW
step with cloned current optimizer state, every 16 actual updates, on the next incoming example; rank a seeded sample of at most 16 records from the
old-site archive by post-minus-pre loss and cycle through its top half for
replay. Restore exact adapter weights, leave actual optimizer untouched. No
reservoir replacement, image classifier, joint minibatch, historical minimum loss,
or teacher distribution. Actual updates alternate incoming and selected replay
according to a fixed ratio. This is MIR-inspired block replay, not a replication
of published MIR. The virtual step uses the actual optimizer moments; its separate copy is discarded.
Exact weight restore and an unchanged actual optimizer-state digest are checked.
The fresh-AdamW draft was corrected before any recurrent run.
`mir.py:retrieve_replay_update` was read in full, including descending loss-delta
ranking, excluded current task, reservoir sampling and the summed new/replay gradients.
