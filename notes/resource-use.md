# Resource use

2026-09-14: local hostname mac.lan, Apple M1 Ultra, 64 GiB. Before starting,
process inspection found no Python/MLX experimental training process. This study
runs one bounded MLX job at a time with a 40 GB ceiling; no model serving process
is stopped. Active job commands identify this directory and evidence output.
No messages to other investigators were sent. Recheck processes before each run.

During fresh seed47, process inspection found the retention study waiting on this
study's visible batch/experiment processes. Its resource-use note reports a brief
race: it began at20:43:12 UTC after our development run ended; our confirmatory
batch began20:43:33; it observed overlap at20:43:44 and stopped its own partial run.
Its replacement development-v2 is currently waiting (0% CPU, resource_wait events).
We changed none of its files or processes. This overlap was not known at launch;
first fresh-run timing is not evidence of exclusive-machine latency. Accuracy and
exact reset/hash audits remain checked. Our three runs execute sequentially and
are expected to finish roughly15 minutes after batch start; no additional heavy
experiments are planned after that batch. Raw timings are descriptive only.

The three-seed batch completed successfully after936.64 seconds of summed run
timers. All gradient/generation/reload work is finished; remaining work is CPU-only
analysis, documentation and Git preservation. The waiting retention study may use
the GPU. No sibling process was stopped or modified by this study.

Follow-up resumption, 14 September 2026, approximately23:33 UTC: launched the
512-update followup-development-v1 only after inspection found no active learner.
At elapsed202 seconds observed the retention follow-up's scope_experiment.py;
its process is idle and its note says it is waiting for our PID6815 before loading
the model. After v1 completes this study will yield the device for that waiting
development run. The next local diagnosis is1920 updates and will start only after
rechecking that resource. CPU audits and documentation proceed during the wait.
No sibling file or process is modified. Follow-up timings remain descriptive.
