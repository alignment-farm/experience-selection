# Partial acquisition development v1

2026-09-14. Exploratory; fixed before execution. Preserve first-phase evidence.
Two regions share two channels and outputs, but have opposite correct mappings:
coast copper→heron/violet→otter; inland copper→otter/violet→heron.
Both experience sources are correct. A source contains observations for one region.
This is a new synthetic task, not additional first-phase tickets.

Use the unchanged pinned runtime/model/environment. Answer-only CE including EOS,
AdamW .0005, batch one, new optimizer for every branch, rank8 q/v LoRA in eight
final layers. No teacher distribution required. Seed 71; data seed 20260914501.
Two training tickets (8 cases), one disjoint verification ticket (4 cases), four
disjoint later evaluation tickets (16 cases). Verify ticket disjointness.

Construct two states independently from identical base initialization by 64 updates
on coast-only or inland-only observations. Save and evaluate at 8,16,32,64 updates.
The final state is the starting point for all source contrasts. Acquisition of the
exposed region requires 8/8 later cases; partiality requires an error elsewhere.
If acquisition fails, diagnose with a bounded additional comparison before closure.

At each state obtain four labeled verification responses, then fix a simple gap
decision before any candidate outcome: none if all agree; source for the region
with more errors; balanced mixture on a tie. This is an exploratory policy.
All controls have access to the same two pools, labels, and verification feedback.
The mixture includes all training labels; probe tickets are used for decisions,
not silently added to any update. Give the context reference both pools and probes.

Train coast-only, inland-only and balanced-mixture branches from exactly matched
state hashes for 64 steps, evaluate at 8,16,32,64 on all train and later cases.
Each single-region order shuffles all its four cases once per cycle; mixture
alternates one coast and one inland example using those same region orders.
No update and all-accessible-evidence-in-context are references at each state;
also evaluate base with and without evidence. Evidence is removed in trained tests.
All source checkpoints are saved and exact token replay checked after reload.
Record per-region accuracy, raw tokens, loss/gradient, input/target tokens, generation
tokens/time, hashes, and frozen-base/reset checks. Outcomes, not loss, select duration.

Bound: 512 optimizer steps, 40GB MLX allocation, 30 minutes. Inspect shared activity
before launch. The study's command identifies its output; do not stop others' jobs.
Use these data to choose a short strong fixed-source/mixture schedule and policy;
fix both before fresh seeds/tickets. A useful null must explain measured source
effects and successful acquisition, not merely a floor or ceiling.
