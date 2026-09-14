# Reproduction

Use Apple Silicon with at least 16 GB free memory; recorded runs used a 64 GiB M1
Ultra. Do not overlap with another heavy GPU job. All commands run from this study.

```
uv sync --python 3.14.7 --extra adaptation --frozen
uv run --no-sync python -c 'from huggingface_hub import snapshot_download; snapshot_download("Qwen/Qwen3-4B-Instruct-2507", revision="cdbee75f17c01a7cc42f958dc650907174af0554", local_dir="models/qwen3-4b-instruct", allow_patterns=["*.json", "*.safetensors", "*.jinja", "*.txt"])'
uv run --no-sync python scripts/experiment.py --output evidence/NEW-DEVELOPMENT
uv run --no-sync python scripts/analyze.py evidence/NEW-DEVELOPMENT
```

The model may instead be supplied by a symlink to the exact existing frozen model;
resource() verifies every hash against the owned model reference. No source-study
checkout is otherwise required. Model weights and environments are Git-ignored;
adapters, raw records and source snapshots are preserved. Output directories must
be new; failed attempts must not be overwritten. The script saves SHA256SUMS even
on failure. Acquisition and source checkpoints are evaluated at 32 and 128 steps;
the final source evaluation budget can be fixed by --steps for later protocols.

The copied runtime includes unused reverse-KL and teacher helpers; these runs use
only hard-label CE with native LoRA gradients. They do not rely on a chat API or
claim to exercise teacher-distribution access. The acquired starting state is
trained locally for 128 updates and charged separately. Every candidate starts
with a new optimizer, so this comparison does not test keeping optimizer momentum.

For the fixed prospective comparison, after development reading and without
changing protocol/policy-v1.md:

```
uv run --no-sync python scripts/run_confirmatory.py
uv run --no-sync python scripts/supplemental_audit.py evidence/policy-v1-47 evidence/policy-v1-53 evidence/policy-v1-59 --output evidence/NEW-SUPPLEMENTAL
```

The batch wrapper uses the committed evidence names and deliberately rejects
existing outputs. On a fresh checkout that already contains evidence, reproduce
individual runs with new names, then audit each new run and pass those new paths
to policy_report.py. For example:

```
uv run --no-sync python scripts/experiment.py --output evidence/NEW-47 --seed 47 --data-seed 20260914101 --protocol protocol/policy-v1.md --policy
uv run --no-sync python scripts/analyze.py evidence/NEW-47
```

Repeat with53/20260914201 and59/20260914301. Policy report accepts any list of run
paths and a new --output directory. The script's `development` split denotes the
prospectively reserved evaluation split for these three frozen runs. Seed43 is
exploratory only. Current tokenizer audit explicitly requests a list return type;
the initial failed audit log is retained for provenance.

For the completed bundle, rebuild derived aggregate metrics and the publication
using new output paths (the metrics script refuses existing output):

```
uv run --no-sync python scripts/publication_metrics.py --output evidence/NEW-METRICS
uv run --no-sync python scripts/render_findings.py --metrics evidence/NEW-METRICS/metrics.json --output NEW-FINDINGS.md
```

`scripts/publication_metrics.py` reads the audited three-run results and
`scripts/render_findings.py` renders FINDINGS.md from those metrics. The numeric
report includes the prespecified 32-step diagnostic outcomes as a limitation of
claims about the 128-step gate. `scripts/supplemental_audit.py` independently checks
self-output decoding, equal-label checkpoint equivalence and decision chronology.
