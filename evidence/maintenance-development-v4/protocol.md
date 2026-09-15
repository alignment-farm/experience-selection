# Maintenance development v4 — duration and matched replay fraction

V3's audited128-update results over three arrivals: fixed25=7/18, fixed50=10/18,
fixed75=16/18, MIR50=7/18. Fixed75 ends8/8 with no lost workflows. MIR50 loses6,
ends2/8. Native virtual steps match actual next steps exactly, and optimizer
state is isolated. The short-budget result does not separate insufficient replay
fraction from ranking quality relative to the strongest fixed75.

Hold seed101, data2026091501,16 training replicas,128-update alder construction,
three arrivals birch/cedar/dune and later cases fixed. Run256 updates/arrival for
fixed75,mir50,mir75. This tests sensible duration for the strongest fixed source
and ranks replay at its75% fraction, with equal actual updates/target tokens.
Choose best MIR fraction by complete uses, then final completeness, then lower
replay fraction. Retain all outcomes; no fresh evaluation or promotion yet.

Base/state diagnostic-generation reduction described in the development log;
check state128 adapter SHA against V3. Primary evaluations and training identical
in definition. Complete-selection timer includes virtual/scoring/copy/reset/ranking.

For subsequent fresh recurrence, add stop75: same fixed75 training for the first
three arrivals, then unconditionally freeze. This is a prospectively fixed
schedule, not an acquisition guarantee or a gate using fresh labels. It tests
whether repeated arrivals on already observed immutable rules need any further
maintenance. Score failures if its acquisition prefix is incomplete. Do not charge
its smaller update count as evidence for damage-aware selection. A recurrent
fresh protocol and seeds will be committed after this development comparison.
