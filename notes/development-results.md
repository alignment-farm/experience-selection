# Development results (not fresh policy evaluation)

Run evidence/development-v1, execution cdf4f92; saved and audited atddc687f.
Each entry below is correct routing on16 development requests at128 updates.

| Starting state | No update | Checked examples in context | Checked labels | Self answers | Opposite labels |
|---|---:|---:|---:|---:|---:|
| Base |10|16|16|8|0|
| Acquired with128 checked updates |16|16|16|16|0|

Acquisition at32:8/16 train and8/16 development; at128:16/16 on each.
All32-step checkpoints retained. The acquired opposite32 branch scores2/16 training
and0/16 development. This is an actual harmful update from functioning weights.
Base self labels contain13 `heron` and3 `otter` answers: all8 teal labels correct,
only3/8 amber labels correct. Their measured reliability is11/16; later task utility
is8/16, below no-update10/16. This is not evidence for all forms of self-training.

Self and checked sources contain exactly the same labels after acquisition, while
their names differ. Their recorded first and last training losses also match.
Checked source reliability stays16/16 across learner states while its incremental
utility changes from+6/16 to0/16 on this split. Wrong labels are a stress test and
not a model of a naturally occurring source or a test of reliability estimation.

The301.166-second run uses896 optimizer steps. Individual128-step update blocks
cost15.42–17.34 seconds; the rest includes generation, model loading, hashes,
resets and audits. Peak MLX allocation9.612 GB decimal. All608 response records
are retained;32 repeated base records are excluded from accuracy denominators.
The runner verifies14 first-case checkpoint reloads, exact reset logits and frozen
base hashes. The independent audit verifies prompts, decoding, labels, update
orders, costs and saved evaluation counts. The first audit's return-type error
and its fix are documented in development.md and both logs are retained.
