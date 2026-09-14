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
