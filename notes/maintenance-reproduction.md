# Maintenance reproduction (in development)

Use the existing `uv.lock`, exact Qwen3-4B model revision and native setup from
[the follow-up](followup-reproduction.md). No sibling checkpoints are used.
Recheck active Python/MLX jobs before every run; yield to existing work.
Run paths must be new. Scripts save source snapshots, protocol, configuration,
all tokenized examples, responses, updates, evaluated adapters and SHA256 manifests.

```sh
uv run --no-sync python scripts/maintenance_task_check.py
uv run --no-sync python scripts/maintenance_experiment.py --output evidence/NEW-MAINTENANCE-V1
uv run --no-sync python scripts/maintenance_audit.py evidence/NEW-MAINTENANCE-V1 --output evidence/NEW-MAINTENANCE-V1-AUDIT
uv run --no-sync python scripts/maintenance_experiment.py --output evidence/NEW-MAINTENANCE-V2 --replicas 16 --joint-checkpoints 512 1024 --protocol protocol/maintenance-development-v2.md
```

V1 source snapshot has the original, unexecuted recurrent draft. Subsequent code
corrects virtual optimizer state and caps candidate scoring. No recurrent data
have yet been used to choose these implementation corrections. Model runtime is
unchanged; every run's resource.json checks all model file hashes.

## Completed replay composition development

```sh
uv run --no-sync python scripts/maintenance_experiment.py --output evidence/NEW-MAINTENANCE-V3 --mode recur --replicas 16 --sequence birch cedar dune --steps 128 --protocol protocol/maintenance-development-v3.md
uv run --no-sync python scripts/maintenance_audit.py evidence/NEW-MAINTENANCE-V3 --output evidence/NEW-MAINTENANCE-V3-AUDIT
uv run --no-sync python scripts/maintenance_report.py evidence/NEW-MAINTENANCE-V3-AUDIT/metrics.json --output NEW-MAINTENANCE-V3-TABLES.md
uv run --no-sync python scripts/maintenance_coverage.py evidence/NEW-MAINTENANCE-V3 --output NEW-MAINTENANCE-V3-COVERAGE.json
```

Current recurrent code omits the redundant base/future-site training diagnostics
that V3 executed. It retains all primary before/after evaluations and updates.
Use the run-owned script snapshot for that exact diagnostic count. SHA-check the
initial adapter when comparing these versions. Future runs also accept
`--later-replicas` (default1), without changing training pools or policy inputs.

## Completed duration/replay-budget diagnosis

V4 completed and passed its audit. Reproduce to a new output path:

```sh
uv run --no-sync python scripts/maintenance_experiment.py --output evidence/NEW-MAINTENANCE-V4 --mode recur --replicas 16 --sequence birch cedar dune --steps 256 --arms fixed75 mir50 mir75 --protocol protocol/maintenance-development-v4.md
```

Optional independent plotting environment (no change to learner lock):

```sh
uv run --no-project --with matplotlib==3.11.2 --with numpy==2.5.3 python scripts/maintenance_plot.py evidence/NEW-MAINTENANCE-V3-AUDIT/metrics.json --output evidence/NEW-MAINTENANCE-V3-FIGURE --title 'Development: complete dispatch workflows (128 updates per arrival)'
```

## Frozen fresh cohort (execution in progress)

Policy and protocol fixed at `ba91a06`. Analysis/publication commits do not change
the run-owned policy snapshots; the cohort audit compares them to that commit.
Check that the shared GPU is free before launching one visible sequential batch.
The following new prefix avoids overwriting the original fresh evidence:

```sh
uv run --no-sync python scripts/run_maintenance_fresh.py --mir-arm mir75 --protocol protocol/maintenance-fresh-v1.md --prefix NEW-MAINTENANCE-FRESH
uv run --no-sync python scripts/maintenance_audit.py evidence/NEW-MAINTENANCE-FRESH-103 evidence/NEW-MAINTENANCE-FRESH-107 --output evidence/NEW-MAINTENANCE-FRESH-AUDIT
uv run --no-sync python scripts/maintenance_cohort.py evidence/NEW-MAINTENANCE-FRESH-AUDIT/metrics.json --output evidence/NEW-MAINTENANCE-FRESH-COHORT
```

The selected method and both seeds are fixed, not automatically retuned from the
new run's outcomes. Any execution failure remains visible and stops the batch.
