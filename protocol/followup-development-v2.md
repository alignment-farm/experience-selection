# Partial acquisition duration diagnosis v2

2026-09-14. Development v1 is preserved. After coast-only construction learned its
exposed region 8/8, gap-only updates replaced its learned mapping (0/8 coast,
8/8 inland by step32). A balanced mixture reached only 8/16 at64; a transient
step16 checkpoint scored0/16. This does not establish a functioning joint regime.

Retain exactly the same seed71, data seed20260914501, model, loss, optimizer,
state64 construction, sources and ordering. Extend source duration to256 and
evaluate64,128,256. Prefix orders and reset states match v1 exactly; verify the
repeated64 checkpoints against v1. Add balanced-mixture acquisition from base
at the same durations. The intervention separates short duration from the effect
of single-region prior acquisition. All data remain exploratory.

No policy tuning on fresh cases. Same four labeled probes and gap policy as v1.
Do not interpret training loss as acquisition. Require8/8 train and16/16 later
for full joint acquisition; report both regions even where total is unchanged.
The shortest duration that achieves the maximum aggregate later performance for
the strongest fixed source across both partial states is the candidate fresh
primary duration. Keep shorter diagnostic checkpoints visible.

Bound:1920 updates (2×64 construction +7×256),40GB MLX,30 minutes. Includes
all three sources from each partial state and mixture from base. A fresh evaluation
will be separately committed after this diagnosis, preserving unsuccessful runs.
