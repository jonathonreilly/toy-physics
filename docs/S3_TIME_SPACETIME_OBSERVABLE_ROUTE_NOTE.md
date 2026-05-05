# Route 2 Observable Pass: `S^3` + Anomaly-Forced Time

**Date:** 2026-04-14
**Claim type:** open_gate
**Status:** open - exact kinematic lift; no exact dynamics bridge
**Primary runner:** `scripts/frontier_universal_gr_tensor_action_blocker.py`

## Verdict

Exact kinematic lift observable exists. Exact dynamics bridge does not.

The current stack gives two exact ingredients:

- `S^3` compactification;
- anomaly-forced time with `d_t = 1`.

Together they define the clean kinematic background candidate:

```text
PL S^3 x R
```

From the route-2 perspective, the only exact observable one can write from
the current stack is the background-lift selector:

```text
O_lift = 1[S^3 closed] * 1[d_t = 1]
```

On the current atlas, `O_lift = 1`. That is an exact kinematic predicate.
It says the route has a clean spacetime scaffold, but it does not yet give a
GR field law.

## What The Route Supplies

Exact on the current stack:

- `S^3` topology;
- anomaly-forced time;
- the combined lift `PL S^3 x R`;
- a route selector saying the background scaffold is present.

Not exact on the current stack:

- no exact observable that reconstructs curvature or tensor dynamics;
- no exact action on `PL S^3 x R` whose Euler-Lagrange equations give GR;
- no exact uniqueness theorem saying Einstein dynamics is the only compatible
  local lift.

So route 2 is currently a kinematic lift with an exact selector observable,
not a theorem-grade dynamical closure.

## Sharp Blocker

The atlas and route notes are consistent on the negative point:

- topology is not the problem;
- clock structure is not the problem;
- the missing piece is a dynamics carrier.

The remaining theorem would have to be one of:

1. an exact action on `PL S^3 x R`;
2. an exact spacetime-lift observable that reconstructs metric response;
3. a uniqueness theorem forcing Einstein dynamics from the retained lift.

Without one of those, the route cannot underpin a GR field law.

## Relation To Existing Notes

This note preserves the route-2 open gate used by
[`UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md`](UNIVERSAL_GR_TENSOR_ACTION_BLOCKER_NOTE.md).
It is a dependency for the blocker runner, not a closure claim.

The related background note
[`S3_ANOMALY_SPACETIME_LIFT_NOTE.md`](S3_ANOMALY_SPACETIME_LIFT_NOTE.md)
states the broader kinematic route. This note isolates the observable-pass
version: `O_lift = 1` exists, but no metric dynamics bridge follows from it.

## Bottom Line

`S^3` plus anomaly-forced time gives an exact kinematic spacetime lift to
`PL S^3 x R`, but the atlas still lacks an exact observable/action/uniqueness
theorem that turns that lift into Einstein dynamics.
