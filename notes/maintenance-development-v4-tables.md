# Maintenance result tables

Generated from independently audited raw runs. These tables do not themselves label development as fresh.

## evidence/maintenance-development-v4

| Arm | Complete uses | Final complete | Retained | Gained | Lost | Updates | Virtual updates | Scoring forwards |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| fixed75 | 18/18 | 8/8 | 12 | 6 | 0 | 768 | 0 | 0 |
| mir50 | 17/18 | 8/8 | 10 | 7 | 1 | 768 | 48 | 1536 |
| mir75 | 18/18 | 8/8 | 12 | 6 | 0 | 768 | 48 | 1536 |
| explicit | 18/18 | — | — | — | — | 0 | 0 | 0 |

### Costs by deployed branch

| Arm | Training input / target tokens | Virtual input / target tokens | Scoring input / target tokens | Use prompt / output tokens | Measured training / virtual / scoring / use seconds |
|---|---:|---:|---:|---:|---|
| fixed75 | 75673 / 3840 | 0 / 0 | 0 / 0 | 1697 / 90 | 153.48 / 0.00 / 0.00 / 4.30 |
| mir50 | 75666 / 3840 | 4711 / 240 | 151460 / 7680 | 1697 / 90 | 153.74 / 9.55 / 214.15 / 4.39 |
| mir75 | 75729 / 3840 | 4714 / 240 | 151460 / 7680 | 1697 / 90 | 152.19 / 9.51 / 212.34 / 4.36 |

Explicit archive: peak serialized bytes 11616; lookup comparisons 67; lookup + execution seconds 0.000078.

### Episode pairs

| Arm | Episode | Retained | Gained | Lost | Failed both |
|---|---:|---:|---:|---:|---:|
| fixed75 | 1 | 2 | 2 | 0 | 0 |
| fixed75 | 2 | 4 | 2 | 0 | 0 |
| fixed75 | 3 | 6 | 2 | 0 | 0 |
| mir50 | 1 | 1 | 2 | 1 | 0 |
| mir50 | 2 | 3 | 3 | 0 | 0 |
| mir50 | 3 | 6 | 2 | 0 | 0 |
| mir75 | 1 | 2 | 2 | 0 | 0 |
| mir75 | 2 | 4 | 2 | 0 | 0 |
| mir75 | 3 | 6 | 2 | 0 | 0 |

