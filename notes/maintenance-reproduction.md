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
