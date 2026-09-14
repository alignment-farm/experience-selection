# Development and consequential changes

The development protocol and runner were committed at cdf4f92 before generation.
128 CE steps acquired16/16 training and16/16 new development requests;32 did not.
The gate protocol was committed at89f6bd2 after checked128 succeeded in both states
but before the final acquired opposite branch finished. The strongest source was
already at ceiling in both states. No remaining branch could surpass that accuracy.
The three-seed execution/freshness wrapper was committed at5c282b1.

First saved-record audit failed before any confirmatory run: Transformers5 returns
BatchEncoding by default from apply_chat_template, whereas MLX's wrapper returns
input_ids. Printed comparison showed identical actual token lists. The independent
auditor now explicitly requests return_dict=False. Original failed audit log is
preserved at evidence/development-v1-audit.log; no model result changed or reran.

The initial base-none evaluation is repeated later when traversing the base state.
The auditor verifies matching tokens/cases then excludes those32 repeated records
from statistical denominators. All raw observations remain saved. Source checkpoints
are reloaded within the experiment and the first training input is regenerated;
these14 repetitions per run are verification only.

All three fresh seeds completed under the frozen protocol. During inspection of
prespecified32-step checkpoints, all fresh checked branches were also at ceiling,
unlike development. This limits the fixed128-step gate's cost advantage; the final
publication explicitly reports the cheaper192-update shorter fixed schedule.
No follow-up tuning or fresh neural evaluation was performed after this observation.
