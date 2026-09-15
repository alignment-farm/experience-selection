# Maintenance result tables

Generated from independently audited raw runs. These tables do not themselves label development as fresh.

## evidence/maintenance-development-v3

| Arm | Complete uses | Final complete | Retained | Gained | Lost | Updates | Virtual updates | Scoring forwards |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| none | 6/18 | 2/8 | 6 | 0 | 0 | 0 | 0 | 0 |
| incoming | 6/18 | 2/8 | 0 | 6 | 6 | 384 | 0 | 0 |
| fixed25 | 7/18 | 3/8 | 2 | 5 | 4 | 384 | 0 | 0 |
| fixed50 | 10/18 | 4/8 | 4 | 6 | 4 | 384 | 0 | 0 |
| fixed75 | 16/18 | 8/8 | 10 | 6 | 0 | 384 | 0 | 0 |
| mir50 | 7/18 | 2/8 | 1 | 6 | 6 | 384 | 24 | 768 |
| explicit | 18/18 | — | — | — | — | 0 | 0 | 0 |

### Costs by deployed branch

| Arm | Training input / target tokens | Virtual input / target tokens | Scoring input / target tokens | Use prompt / output tokens | Measured training / virtual / scoring / use seconds |
|---|---:|---:|---:|---:|---|
| none | 0 / 0 | 0 / 0 | 0 / 0 | 1697 / 90 | 0.00 / 0.00 / 0.00 / 4.04 |
| incoming | 37768 / 1920 | 0 / 0 | 0 / 0 | 1697 / 90 | 76.79 / 0.00 / 0.00 / 4.28 |
| fixed25 | 37789 / 1920 | 0 / 0 | 0 / 0 | 1697 / 90 | 76.69 / 0.00 / 0.00 / 4.28 |
| fixed50 | 37812 / 1920 | 0 / 0 | 0 / 0 | 1697 / 90 | 76.75 / 0.00 / 0.00 / 4.29 |
| fixed75 | 37840 / 1920 | 0 / 0 | 0 / 0 | 1697 / 90 | 76.63 / 0.00 / 0.00 / 4.30 |
| mir50 | 37826 / 1920 | 2351 / 120 | 75726 / 3840 | 1697 / 90 | 76.56 / 4.77 / 106.68 / 4.37 |

Explicit archive: peak serialized bytes 11616; lookup comparisons 67; lookup + execution seconds 0.000078.

### Episode pairs

| Arm | Episode | Retained | Gained | Lost | Failed both |
|---|---:|---:|---:|---:|---:|
| none | 1 | 2 | 0 | 0 | 2 |
| none | 2 | 2 | 0 | 0 | 4 |
| none | 3 | 2 | 0 | 0 | 6 |
| incoming | 1 | 0 | 2 | 2 | 0 |
| incoming | 2 | 0 | 2 | 2 | 2 |
| incoming | 3 | 0 | 2 | 2 | 4 |
| fixed25 | 1 | 1 | 1 | 1 | 1 |
| fixed25 | 2 | 1 | 1 | 1 | 3 |
| fixed25 | 3 | 0 | 3 | 2 | 3 |
| fixed50 | 1 | 1 | 1 | 1 | 1 |
| fixed50 | 2 | 1 | 3 | 1 | 1 |
| fixed50 | 3 | 2 | 2 | 2 | 2 |
| fixed75 | 1 | 2 | 1 | 0 | 1 |
| fixed75 | 2 | 3 | 2 | 0 | 1 |
| fixed75 | 3 | 5 | 3 | 0 | 0 |
| mir50 | 1 | 1 | 1 | 1 | 1 |
| mir50 | 2 | 0 | 3 | 2 | 1 |
| mir50 | 3 | 0 | 2 | 3 | 3 |

