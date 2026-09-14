# Follow-up reproduction

Run from this study on Apple Silicon. See [first-phase setup](reproduction.md)
for `uv sync --python 3.14.7 --extra adaptation --frozen` and exact model download.
Use the unchanged lock and model revision. Each run verifies frozen model hashes.
No sibling study's checkpoints or cases are required. Runtime provenance is in
[sources/README.md](../sources/README.md).

Inspect active Python/MLX jobs before starting. Yield to active shared GPU work;
do not start a polling Python experiment that could cause mutual resource waits.
The experiments bound active execution to30 minutes and peak MLX allocation40GB.
Run sequentially, using fresh output paths; existing paths deliberately fail.

## Exploratory workload and duration diagnosis

```sh
uv run --no-sync python scripts/followup_experiment.py --output evidence/NEW-DEVELOPMENT-V1
uv run --no-sync python scripts/followup_audit.py evidence/NEW-DEVELOPMENT-V1 --output evidence/NEW-AUDIT-V1
uv run --no-sync python scripts/followup_experiment.py --output evidence/NEW-DEVELOPMENT-V2 --checkpoints 64 128 256 --include-base-mixture --protocol protocol/followup-development-v2.md
uv run --no-sync python scripts/followup_audit.py evidence/NEW-DEVELOPMENT-V2 --output evidence/NEW-AUDIT-V2
```

V1 code atbf8e820 did not have the optional base-mixture argument. The current
default retains its behavior. V2 retains seed71, data seed20260914501 and the same
initial/partial states and source orders, and extends duration. Every evidence
directory owns the precise script, task, runtime, protocol and lock that ran.
The audit reconstructs prompts and decoding using only the tokenizer; it does
not load the model and can run while another study uses the GPU.

Evidence includes all model responses (with prompt and output token IDs), labeled
probe decisions, each gradient update, state/source hashes, all evaluated adapter
checkpoints, exact-token reload checks and SHA256SUMS. Base weights and Python
environments are ignored by Git; the small adapters are committed.

The auditor independently recomputes per-region accuracy from raw decoded answers,
checks matched starting states, decisions before candidate training, case/order
alignment and recorded costs. It reports the computational cost of each deployed
branch separately from actually executing every counterfactual branch and all
diagnostic evaluations. Model time measurements are descriptive and do not justify
an exclusive-device latency or amortization claim.
