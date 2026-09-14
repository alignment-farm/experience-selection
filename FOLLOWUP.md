# Beyond abstention: selecting useful experience

14 September 2026. Independent continuation is commissioned. This handoff prepares
the next phase; no experiments were launched while writing it.

The accepted [publication](FINDINGS.md),
`dca27dd46b634616e8895e0a137f23225c5dc7cc`, establishes useful supervised
abstention at a fixed 128-step budget. Its decisive qualification is that the
fresh fixed 32-step comparator also scored 96/96 with only 192 subsequent
updates, versus the gate's 384. Including acquired-state construction gives
576 versus 768 total updates. Development had justified choosing 128 steps, but
the fresh result shows why the next comparison needs a well-developed simple
training schedule alongside selection.

**In partially acquired states with competing useful experiences, when does
source selection add value beyond abstention and shorter training?**

The root's [assessment and prospective expectations](../../construct-2/studies/2026-09-14-concurrent-findings.md)
connect this question to the concurrent studies. They supply competing
explanations, not a frozen protocol. Work can proceed independently of those
studies' next results.

## Explanations to distinguish

- **Different remaining gaps favor different experience.** A source useful for
  one partially acquired learner is less useful for another, and observable
  evidence of those gaps helps choose the update.
- **A simple schedule explains the apparent benefit.** One source or fixed
  mixture is generally sufficient; shorter training or abstention captures the
  improvement attributed to selection.
- **Additional supervision explains the gain.** The policy benefits from
  verification information unavailable to its controls, or its checking cost
  outweighs the useful updates it saves.

The previous base/acquired contrast and opposite-label stressor cannot by
themselves decide among these explanations. Acquired self and checked labels
were identical. Develop a workload where candidate experiences can teach
different useful things, rather than making deliberately wrong versus right
labels the entire comparison. Correct observations addressing different
remaining gaps are one possible starting point; the investigator chooses the
mechanism and task.

## Useful experimental contrasts

Compare candidate updates from the same partially acquired starting state on
common later queries, then examine whether their relative utility changes
across states. Distinguish a change in which source helps from changes only in
whether any update is needed. Keep the loss and starting state matched within
source comparisons, or separate their effects explicitly. Training loss and
source correctness remain distinct from later behavioral utility.

Use development material to choose strong fixed-source or fixed-mixture
references and a sensible short training budget. Compare selection with those
references and abstention; match update count or compute where that isolates
the proposed effect. The earlier 32-step success motivates duration calibration,
not a requirement to reuse 32 steps on a new workload. These are discriminating
contrasts to choose among, not a mandatory factorial matrix.

Disclose what verification labels, observations and feedback the selector can
use, and give controls equal access to that information. Include the cost of
constructing learner states, obtaining experience, verification, selection,
training and subsequent use. Retain an accessible-evidence reference for claims
about knowledge placement or useful cost. Fix policy and checkpoint selection
before fresh evaluation of a developed claim; preserve the exploratory cases
and failed attempts separately.

A useful null could show why a simple policy suffices: for example, one source
or mixture repairs the measured gaps across states, and targeted selection adds
no advantage once training duration and information access are matched. Explain
that result with measured contrasts. If initial comparisons only expose failed
acquisition or a floor or ceiling, continue bounded diagnosis rather than treating
that alone as closure. Neither a selector win nor indefinite search is required.

The investigator owns workload discovery, methods, resource sizing and routine
execution under [AGENTS.md](AGENTS.md), including coordination of heavy shared
jobs. Publish the follow-up with local evidence and reproduction instructions.
Preserve the accepted `FINDINGS.md`, completed protocols and evidence as the
record of the first phase.
