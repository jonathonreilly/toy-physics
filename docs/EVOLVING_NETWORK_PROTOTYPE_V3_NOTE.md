# Evolving Network Prototype V3 Note

**Date:** 2026-04-04 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded Gate B control audit; cleaner control discipline relative to v2 but not a closed dynamics result and not a tier-ratified Gate B claim.

## One-line read

This v3 pass improves the *control design* relative to v2: the imposed
comparator now preserves a source-to-detector backbone corridor instead of
carving out a center band.

That makes the comparison cleaner and more reviewable, but it still does **not**
close Gate B. In the frozen sweep, the imposed comparator remains methodologically
negative because its detector purity is still `nan` even though the backbone is
preserved.

## Primary artifact

Script:

- [`scripts/evolving_network_prototype_v3.py`](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v3.py)

Log:

- [`logs/2026-04-04-evolving-network-prototype-v3.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v3.txt)

## What v3 changes relative to v2

v2 used a same-budget imposed band that was too destructive:

- it removed too much of the post-barrier structure
- detector signal often collapsed to `nan`
- the control was not clearly connectivity-preserving

v3 instead:

- builds a greedy backbone spine through the same DAG family
- protects a narrow corridor around that spine
- leaves a longer detector-side tail untouched
- spends the removal budget outside that protected corridor where possible

That is a better public imposed control because it answers a fair
question:

- what happens if the control preserves a visible source-to-detector route?

## Retained result

The audit retains two things:

1. The generated rule still creates a real geometric gap signal.
2. The imposed control now preserves the backbone corridor, with `spine_ok = 1.00`
   across the frozen sweep.

The frozen rows also show:

- generated purity remains finite and below baseline in places
- imposed gap remains finite, so the control is not just collapsing the graph
- `imposed_pur` is still `nan` in this sweep

So the methodological improvement is real, but the imposed control still does
**not** deliver a retained detector-side purity result.

## What this means for Gate B

This is the correct level of claim for v3:

- the control is now fairer and more connectivity-preserving than v2
- the comparison is easier to defend under review
- the result is still negative or inconclusive on the imposed side

That means Gate B remains open.

## What is not retained

- Gate B is solved
- the imposed control is a positive comparator
- the v3 audit closes the dynamics question
- the current control proves a generated-geometry advantage over the imposed lane

## Safe public summary

Use this note to explain the control discipline:

- same graph family
- same generated pruning rule
- imposed control protects a backbone corridor instead of a central band
- detector signal is still the blocker on the imposed side
- the best current outcome is methodological cleanup, not a positive Gate B win

## Audit boundary (2026-04-28)

The earlier Status line read "public Gate B control audit, not a
`proposed_promoted` dynamics result". The audit-lane parser caught the
literal token even though the sentence asserts the opposite. The Status
line has been rephrased.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: the queued `proposed_promoted` status is contradicted by the
> source note and by the v3 runner; the control is cleaner, but the
> detector-side purity comparison is still undefined and the
> self-regulating rule still does not converge. Why this blocks: a
> promoted Gate B dynamics result requires a measurable
> generated-vs-imposed comparator and stable rule behavior, while this
> packet only shows that the imposed control preserves a backbone
> corridor before losing finite detector purity.

## What this note does NOT claim

- A closed Gate B dynamics result.
- A finite imposed-side detector purity (`pur_cl = nan` on the imposed
  side in the frozen sweep).
- A stable fixed point under the self-regulating rule.
- A positive generated-vs-imposed comparator outcome.

## What would close this lane (Path A future work)

Reinstating a closed Gate B dynamics result would require:

1. A registered runner with finite imposed `pur` so the
   generated-vs-imposed comparator is defined.
2. Explicit pass thresholds for the generated-vs-imposed comparator.
3. A self-regulating rule that converges to a stable fixed point under
   stated thresholds, asserted across seeds and layer sizes.
