# Maintenance development v1 — 2026-09-15

Exploratory acquisition calibration, before recurring comparisons. New dispatch
sandbox: four sites x two parcel kinds, each with an eligible resource and a
mandatory preparation. Three dependent actions must produce the exact required
inventory, reservation, preparation and shipment state. All rules remain valid.
Two training tickets per rule, one disjoint later ticket per rule. Native Qwen3
4B runtime, unchanged LoRA and CE objective. Seed 101, data seed 2026091501.
Construct alder state at 64/128 updates; independently train joint balanced pool
at 128/256/512 updates from the identical base. Save every evaluated checkpoint,
raw generations and state scores. This is development, not a fresh claim.
A competent archive baseline retrieves the successful action trace by site/kind;
it has the same checked training records, with construction/access costs disclosed.
If joint acquisition fails, diagnose duration versus formatting/composition using
component errors and train versus new-ticket results before choosing a policy.
