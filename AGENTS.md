# Experience selection

Read [README.md](README.md) first. This independent ancillary study owns its
methods, workload discovery, implementation, evidence and publication. The root
owns theory and synthesis through its [study map](../../construct-2/studies/README.md)
and [ancillary-study approach](../../construct-2/notes/ANCILLARY_STUDY.md).

Investigate which experience is useful for an update and when abstention helps.
Begin with a bounded comparison using a functioning acquisition regime. Source
reliability, learner state and downstream utility may differ; none substitutes
for measuring the others. Read the closest primary methods and record exact
versions and reused code revisions. Follow the root's
[source guidance](../../construct-2/AGENTS.md#research-sources) for arXiv access,
caching and rate limits.

## Research practice

- Keep loss and starting state matched when comparing sources, or explicitly
  factor their effects. Distinguish useful behavior from lower training loss,
  dynamic selection from the best fixed source, and selection quality from
  savings due to fewer updates. Retain no-update and accessible-evidence
  comparisons appropriate to the claim.
- Workload discovery and acquisition calibration are legitimate local work.
  A negative result alone is not a stop condition. When a learner has not
  acquired its development cases, pursue bounded diagnostic comparisons that
  distinguish plausible causes or establish a functioning learning regime.
  Finite gradients and exact resets establish mechanics, not acquisition.
- Preserve failed attempts and consequential method changes. Use fresh
  evaluation material for claims developed through exploration, with the
  selection rule fixed before that evaluation. Report component success,
  information access and costs at the level the evidence supports.
- Close on explanatory progress, a demonstrated limitation or an actual
  resource constraint. Neither a neural win nor a dynamic-selector advantage
  is required. Listing possible causes alone is insufficient diagnosis;
  indefinite search for a winning configuration is not expected.
- Keep code, methods, outputs and publication in this directory. Preserve
  identifiable revisions in Git. Source studies are read-only; copy reusable
  components with provenance and use new experimental cases. Do not wait for
  concurrent studies to complete before developing this investigation.

## Model resources

- Dedicated Mac Studio M1 (64 GB unified memory), serving over Tailscale through
  Docker Model Runner (preferred).
  `https://mac-studio-7hr7.taile71f88.ts.net/engines/v1/chat/completions`
- Local open-weight models with `docker model`
- OpenAI models with `codex`
- SpaceXAI models with `agent`

The procedure-transfer diagnosis demonstrates a native MLX route on the Mac
Studio for adapter gradients and full teacher token distributions. Verify the
selected mechanism's gradient, mutable-state and teacher access as applicable;
a chat endpoint alone establishes none of these capabilities. Preparation has
not tested resource availability. Coordinate heavy jobs with other investigators
using the shared Mac Studio and avoid interfering with active runs; independent
development and analysis can proceed concurrently without a central scheduler.

## Dependency management

- Use `uv` for Python package and project management.
- Use Docker and Compose/Dockerfiles for supporting resources when needed.
