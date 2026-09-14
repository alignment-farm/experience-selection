# Experience selection

**First phase accepted; independent follow-up commissioned, 14 September 2026.**
Start with [FOLLOWUP.md](FOLLOWUP.md): in partially acquired states, when does
choosing experience help beyond abstention and shorter training? The investigator
owns the next experiments; preparation of this handoff did not launch them.

The completed [findings](FINDINGS.md) are preserved with [reproduction instructions](notes/reproduction.md), [primary methods and provenance](sources/README.md), and [audited metrics](evidence/publication-metrics/metrics.json).

In a synthetic routing workload, checked labels improve the base learner from 30/48 to 48/48 fresh requests but add no accuracy after acquisition. Self-training reaches 24/48 from base; deliberately opposite labels reach 0/48. A supervised agreement gate matches always-checked training at 96/96 across three seeds and two starting states while halving subsequent updates at the fixed 128-step budget. This is not a general compute advantage: the frozen base with examples also reaches full accuracy, and the fresh 32-step diagnostic checkpoints succeed with fewer updates than the gate.

The study preserves development, a prospectively fixed fresh evaluation, all source checkpoints, exact reset/reload checks, the failed initial audit and its repair, and shared-resource timing limits. The first phase closes on measured source/state effects and the limits of supervised abstention. The original brief below records the study's starting question and scope; FOLLOWUP.md supplies the current direction.


**Which experience should an agent use for an update, and when should it
abstain, given source reliability and its current learned behavior?** This
project investigates the training value of experience for Construct-2's
[S1 question](../../construct-2/studies/README.md#s1-can-an-agent-choose-which-experience-to-train-on-during-an-episode).
It can proceed independently of the concurrent retention and changed-goal
studies. The ancillary investigator owns its workload, methods and experiments.

## Start here

Choose a promising existing learner, establish useful acquisition locally,
and run a bounded comparison of candidate updates and no update on a motivated
workload. Discover conditions in which the comparison can distinguish useful,
redundant or harmful learning. Diagnose uninformative comparisons and publish
the evidence. Develop a selection policy only when the observed differences
give it something useful to choose.

The initial deliverable is an inspectable `FINDINGS.md`, supported by local
methods, saved outputs, analysis and reproduction instructions. A separate
manuscript is optional. No numerical budget or frozen protocol is imposed by
this brief; size the first comparison to the available resources and revise
methods when the evidence warrants it.

## Starting evidence

The earlier [update-source-selection investigation](../update-source-selection/README.md)
established reproducible adapter updates, but its final full-history comparison
scored 24/24 for every source and no update. Lower loss and changed generation
did not demonstrate different source utility or a working selector. Its central
lesson is that a source's reliability and its value as training material are
different properties.

The [procedure-transfer diagnosis](../procedure-transfer/DIAGNOSIS.md)
provides a functioning acquisition lead and a reason to consider learner state.
Changing loss direction from the same failed weights repaired routing; reverse
KL preserved training recall when started from an already acquired imitation
checkpoint, despite failing to acquire those calls from the base. These are
local objective and initialization effects, not evidence for a source selector.
Both selected successful students also routed 48/48 fresh development inputs
correctly despite incomplete identifier production. A well-measured learned
component may therefore be a useful starting point without requiring perfect
whole-call performance.

The diagnosis's evidence and audit are pinned at
`c183674bcecf9346d84e233aa5c084b1a9acb3ac`; inspect its
[reproduction note](../procedure-transfer/notes/reproduction.md) and record exact
revisions of any reused code or checkpoints. Keep the source projects read-only
and create new development and evaluation cases here. Reuse of that learner is
an option, not a commitment to another routing study.

## Experimental direction

Start by testing downstream utility directly. Candidate material could include
observations, checked corrections, the learner's own attempts or summaries of
the same experience. Relevant circumstances could include already acquired
knowledge, a current error or a new relation. These are possible
contrasts, not a required factorial design or a claim that usefulness will vary.

For source comparisons, keep the update objective and starting learner matched,
or explicitly separate their effects. Changing source, loss and initialization
together would leave source usefulness unidentified. Record what information
each candidate contains and what reliability evidence is actually available to
the learner. A checked label or privileged teacher can diagnose a failure, but
its information and cost must be disclosed.

Include no update and an accessible-evidence reference. Compare later useful
behavior, including after removing the teaching material where retention is
claimed. A placement or savings claim needs a workload with meaningful reuse,
context or retrieval costs and an explicit account of evidence access. Do not
manufacture an advantage by silently depriving the reference of information.

If candidate utilities differ, ask whether observable conditions predict those
differences. Compare any resulting policy with the strongest fixed source chosen
on development material. Distinguish adaptive choice from choosing one source
that is generally best, and from merely doing fewer updates. Charge selection,
verification and training costs; a matched update-count comparison can help
separate selection quality from abstention savings. Complexity should follow
evidence that a simpler policy leaves useful decisions unresolved.

A floor or ceiling is a reason to examine the workload, learner and available
information. Local discovery and diagnostic interventions do not require a
root permission gate. Stop on explanatory progress, a demonstrated limitation
or a concrete resource constraint, without requiring a neural advantage,
dynamic-selector advantage or indefinite search. Preserve failed attempts and
use fresh evaluation material to test a claim developed through exploration.

## Closest research leads

The root's [paper map](../../construct-2/studies/README.md#3-paper-map-what-we-can-build-on)
records reading scope and overlap. Recheck primary methods relevant to the
chosen experiment before claiming a contribution:

- [aTTT, 2607.03441v1](https://arxiv.org/html/2607.03441v1) (P3): candidate
  update sources and existing controls; online selection is a stated open lead.
- [Self-Guided TTT, 2607.09415v1](https://arxiv.org/html/2607.09415v1) (P13):
  selection of training spans when the current question is already known.
- [VANE, 2608.09448v2](https://arxiv.org/html/2608.09448v2) (P14): validation
  and rollback of candidate updates in a different modality.
- [SEAL, 2506.10943v2](https://arxiv.org/html/2506.10943v2) (P4): learning to
  generate adaptation data using post-update task performance.

These are starting leads from the root, not a new literature review or a novelty
claim. S1 concerns which experience to learn from and whether to update. Later
retention and scoped correction belong to S2; preservation for changed future
goals belongs to S4. Use their eventual publications as evidence without making
their completion a prerequisite for this study.

Resources and working practices are in [AGENTS.md](AGENTS.md). Preparation did
not test endpoints, download models or execute learning experiments.
