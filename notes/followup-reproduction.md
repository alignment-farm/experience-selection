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
checkpoints, exact-token reload checks (one generation per checkpoint) and
SHA256SUMS. Base weights and Python
environments are ignored by Git; the small adapters are committed.

The auditor independently recomputes per-region accuracy from raw decoded answers,
checks matched starting states, decisions before candidate training, case/order
alignment and recorded costs. It reports the computational cost of each deployed
branch separately from actually executing every counterfactual branch and all
diagnostic evaluations. Model time measurements are descriptive and do not justify
an exclusive-device latency or amortization claim.

## Frozen fresh cohort and publication

Fresh policy/duration/cohort were committed at698d8ca before any fresh model run.
The batch refuses existing outputs, so on a checkout containing completed evidence,
use the individual commands with new paths instead of rerunning the batch name.

```sh
uv run --no-sync python scripts/followup_experiment.py --output evidence/NEW-FRESH-73 --seed 73 --data-seed 20260914601 --state-steps 64 --checkpoints 128 256 --protocol protocol/followup-fresh-v1.md
uv run --no-sync python scripts/followup_experiment.py --output evidence/NEW-FRESH-79 --seed 79 --data-seed 20260914701 --state-steps 64 --checkpoints 128 256 --protocol protocol/followup-fresh-v1.md
uv run --no-sync python scripts/followup_experiment.py --output evidence/NEW-FRESH-83 --seed 83 --data-seed 20260914801 --state-steps 64 --checkpoints 128 256 --protocol protocol/followup-fresh-v1.md
uv run --no-sync python scripts/followup_audit.py evidence/NEW-FRESH-73 evidence/NEW-FRESH-79 evidence/NEW-FRESH-83 --output evidence/NEW-FRESH-AUDIT
uv run --no-sync python scripts/followup_report.py --fresh evidence/NEW-FRESH-AUDIT/metrics.json --primary-step 256 --output NEW-FOLLOWUP-FINDINGS.md
```

The report defaults to the committed development audit paths. Supply
`--development-one` and `--development-two` to use newly reproduced audits.
The exact duration-prefix audit is separately reproducible:

```sh
uv run --no-sync python scripts/followup_repeat_audit.py evidence/NEW-DEVELOPMENT-V1 evidence/NEW-DEVELOPMENT-V2 --output evidence/NEW-REPEAT-AUDIT
```

Optional standalone publication figures use a separate plotting environment,
without changing the learner lock. The output records the plotting package versions.

```sh
uv run --no-project --with matplotlib==3.11.2 --with numpy==2.5.3 python scripts/followup_plot.py --fresh evidence/NEW-FRESH-AUDIT/metrics.json --primary-step 256 --output evidence/NEW-FIGURES
uv run --no-sync python scripts/followup_report.py --fresh evidence/NEW-FRESH-AUDIT/metrics.json --primary-step 256 --figure evidence/NEW-FIGURES/source-comparison.svg --output NEW-FOLLOWUP-FINDINGS.md
```

When a figure is supplied, the renderer verifies that its recorded input hash and
primary step match the metrics being published.
