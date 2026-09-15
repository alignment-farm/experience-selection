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

The retention development completed at568.77 seconds of its own timer, including
150.05 seconds of initial waiting. After observing its complete event and no
active experimental Python process, this study launched followup-development-v2
(PID7177), one1920-update job. The first minute's process inspection shows only
this study's learner. The CPU-only source/PDF reading and evidence audits during
the device wait did not instantiate a learner.

V2 completed after432.49 seconds. Next planned use is one sequential three-run
fresh cohort,4992 optimizer updates in total, approximately20 active minutes based
on development timings. The batch command names run_followup_fresh.py and each
child names its evidence output. The protocol is fixed before launch; recheck
processes before starting. No additional heavy experiments are planned after this
cohort unless a prespecified acquisition failure requires bounded diagnosis.

After the retention acquisition job completed (139.46 seconds), no active learner
was visible and the fresh cohort began under the frozen698d8ca revision. The
visible batch is PID7385, first learner PID7386. A subsequent retention boundary
diagnosis is visible at0% CPU, waiting for this batch; its initial wait does not
establish concurrent GPU use. Do not interpret these process samples as continuous
exclusive-device monitoring. The cohort remains three sequential runs.

Fresh cohort completed:364.89,365.11 and365.55 seconds,1095.54 seconds summed active
run timers,9,612,131,344 bytes peak MLX in each. All gradient work and reloads are
finished. The combined audit is complete; only CPU publication work remains.
The waiting retention boundary diagnosis can use the GPU. No further heavy job
is planned for this follow-up, and no sibling file or process was changed.

2026-09-15 maintenance phase: native local host still mac.lan/M1 Ultra. Process
inspection before calibration found no active Python/MLX learner. Planned first
job: 640 updates and bounded generation, 40 GB MLX ceiling, 3600 s run limit.
No serving process or sibling file changed. Timing remains descriptive.

Maintenance V1 completed185.97s, peak9.62GB. Sibling retention PID4678 was seen
waiting and then actively running; this study yields before V2. CPU-only audit
and task checks completed while yielding. Next intended job is1152 updates for
higher-ticket-diversity acquisition; no background learner is started to wait.

After the sibling PID4678 exited (about19 minutes elapsed for that process),
process inspection found no active learner. Launched maintenance-development-v2:
128 alder updates and1024 joint updates,16 tickets per rule, checkpoints512/1024.
No overlap intentionally introduced. Awaiting yielded time is not experimental
active time and is not included in model latency comparisons.

V2 completed440.61s with9.62GB peak. Yielded to waiting sibling boundary-diagnosis
PID5223; after it exited and no active learner was visible, launched V3:1920
counterfactual maintenance updates plus128 construction updates, three arrivals,
six arms. Prospective protocol committed65c5e49; whole-selection cost timing at
236382b. No other learner was active at launch.

V3 ended728.34s,9.63GB peak. Waiting sibling final learner5507 then became active;
this study yielded. CPU audit and V4 preparation proceed. Next bounded job is
V4:2304 maintenance updates plus128 construction, fixed75/MIR50/MIR75 at256 per
arrival. No model process from this study is currently waiting in the GPU queue.

After sibling final PID5507 exited (about36 minutes total process elapsed,
including its earlier wait), no active learner was visible. Started V4 under
89cf2da/46a7420-era audited code:2304 maintenance updates plus128 construction,
three policies and three arrivals. Prior shared-device wait is excluded from
experimental active timers. Native whole-selection/reset checks remain enabled.
