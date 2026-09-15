# Maintaining complete behavior through recurring learning

15 September 2026. Third phase commissioned for independent ancillary execution.
Preparing this handoff has not run experiments.

**Can selection that anticipates update damage maintain complete behavior under
recurring learning better, or at lower useful cost, than strong fixed mixtures?**

The accepted [follow-up](FOLLOWUP_FINDINGS.md),
`dee1e3159ed0105f6a090c65b72f57cbc386fb10`, found that current-error targeting
replaced an acquired routing rule while a fixed mixture learned both rules.
Mixture and selection had equal update counts and aggregate training tokens.
This motivates anticipating damage to existing behavior and measuring the cost
of maintaining it through repeated use. The root's
[program note](../../construct-2/notes/LEARNING_MAINTENANCE.md) connects the studies;
this brief is sufficient to proceed if that note is absent in another checkout.

## Competing explanations

Selection may protect behavior that a proposed update would damage, preserving
complete task success with less rehearsal. Alternatively, a development-tuned
fixed mixture may provide the same protection, while prediction and verification
make selection more expensive. Both learned approaches may require enough
maintenance that a competent explicit-evidence approach remains more useful.

[MIR (P22)](sources/followup-rehearsal/README.md) is a relevant existing lead:
it selects replay using predicted loss increases after a virtual update. It has
not been implemented here. The investigator chooses an existing or adapted
method, checks its closest primary implementation, and records the actual
differences. A predicted loss increase is a candidate signal; complete behavior
supplies the outcome it must help predict.

## Empirical direction

Broaden beyond the four-cell, two-region routing component. Include at least one
task with multiple dependent decisions or consequential changes to resulting
state. A small sandbox workflow with prerequisites, resource eligibility and
state changes is one optional lead. The investigator owns the task design;
earlier routing can calibrate machinery but cannot supply the main result.

Apply the same complete-task success criterion to learned and explicit arms,
including the required resulting state. Component scores can diagnose failure
without replacing that criterion. Establish functioning acquisition on local
development material and preserve bounded diagnosis when it fails. Record what
each starting learner has acquired, whether it was inherited or constructed,
and the associated cost and provenance. Pair outcomes before and after updates
so retained successes, newly acquired successes and lost behavior remain visible.

Keep historical experience valid throughout this study. Incoming experience can
teach additional compatible behavior; actual revision of the rules belongs to
S2. Choose independent data and methods, without waiting for another study's
next results.

Vary a consequential recurrence, use-frequency or replay-budget condition. Tune
a strong fixed mixture and sensible training duration on development material.
Compare it with the selected method under disclosed budget and information
access. Include a competent explicit-evidence comparison; an arm that performs
no maintenance updates may provide a useful reference. Give controls comparable
verification information and archive access. Match the relevant training resource when
attributing gains to selection, and report any remaining differences.

S5 measurement is active in this phase: track acquisition, repeated use and
maintenance alongside end-to-end complete-task quality. Charge virtual updates,
verification, archive construction/access, rehearsal, retrieval and subsequent
generation. Keep resource units separate: optimizer updates, input/output tokens,
storage and measured time are not interchangeable. Separate executing a chosen
policy from the expense of running every counterfactual branch. A useful-cost
advantage requires comparable complete behavior over the observed sequence.

Fix selection and evaluation choices before fresh tests of developed claims.
An informative null can explain when a simple mixture suffices or why selection
overhead consumes its savings. Diagnose acquisition failures and unexplained
floors or ceilings within the available resources. Neither a selection win nor
indefinite search is required.

## Resources and publication

The investigator owns methods, workload discovery, resource sizing and routine
execution under [AGENTS.md](AGENTS.md), including shared-device coordination.
Publish a separate findings note with local evidence and reproduction details.
Preserve both accepted publications, completed handoffs, protocols and evidence.
