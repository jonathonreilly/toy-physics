# `S^3` + Anomaly-Forced Time: Dynamics-Route Audit

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** Route-2 action student  
**Scope:** exact action/variational bridge from the retained `S^3 +`
anomaly-forced-time stack to GR-like dynamics on `PL S^3 x R`

## Verdict

**The route is kinematically exact but dynamically blocked.**

The current retained stack gives a clean background candidate:

- `S^3` topology is exact on the physical lattice
- anomaly-forced time is exact as a single-clock theorem
- the natural lift is `PL S^3 x R`

Those are real theorem-grade ingredients. They are already reusable tools.

But the current atlas does **not** yet contain an exact action or
variational theorem that turns that background into GR-like dynamics.

## What the retained stack already supplies

### 1. Exact spatial topology

[`S3_GENERAL_R_DERIVATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/S3_GENERAL_R_DERIVATION_NOTE.md)
shows that the cone-capped cubical ball is PL homeomorphic to `S^3` for all
`R >= 2`. So the spatial compactification surface is not a guess.

### 2. Exact single-clock time

[`ANOMALY_FORCES_TIME_THEOREM.md`](/Users/jonreilly/Projects/Physics/docs/ANOMALY_FORCES_TIME_THEOREM.md)
shows that anomaly cancellation plus chirality plus the codimension-1
Cauchy requirement force a single temporal dimension. So the time factor is
also exact.

### 3. Exact microscopic shell action on the current strong-field class

[`OH_SCHUR_BOUNDARY_ACTION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/OH_SCHUR_BOUNDARY_ACTION_NOTE.md)
derives the exact Schur-complement boundary energy on the current
strong-field source classes. That is a genuine microscopic action object, but
it is a static shell-boundary action, not yet a `PL S^3 x R` dynamics action.

## Why that still does not close Route 2

The current retained stack gives:

- an exact spatial background
- an exact temporal background
- an exact static shell boundary action on the strong-field class

It does **not** yet give one of the following exact Route-2 objects:

1. an exact discrete action on `PL S^3 x R` whose Euler-Lagrange equations
   are the GR metric equations
2. an exact spacetime-lift observable that reconstructs the metric dynamics
3. a uniqueness theorem that forces the Einstein dynamics as the only
   compatible lift

That is the sharp missing step.

## Cleanest possible action-route candidate

The strongest action-style candidate in the retained stack would be:

- lift the exact shell Schur boundary action slice-by-slice along the
  anomaly-forced time direction
- promote that slice action to a transfer-matrix or discrete variational
  principle on `PL S^3 x R`
- show the resulting stationarity condition reproduces the GR field law

That would be the right exact route if it exists.

The blocker is that the atlas does not yet provide the missing theorem that
identifies such a transfer-matrix lift as exact.

## Sharp blocker

The current route-2 stack is exact in its ingredients, but only **kinematic**
when combined:

- `S^3` closes the spatial topology
- anomaly-forced time closes the clock structure
- the Schur boundary action closes the static shell law

None of those alone gives a theorem-grade 4D action on `PL S^3 x R`.
The current shell action remains a static boundary action on the retained
strong-field class, not a full spacetime dynamics action.

So the route is blocked because the atlas lacks an exact dynamics bridge:

> an exact `PL S^3 x R` action, observable, or uniqueness theorem that
> produces GR-like dynamics without importing a new dynamical postulate.

## Runnable summary

The companion runner confirms:

- `S^3` topology is closed
- anomaly-forced time is exact
- the shell boundary action is exact on the current strong-field class
- the atlas still does not contain an exact route-2 dynamics bridge

That is the route-2 result today.

## Bottom line

Route 2 is a clean axiom-first **kinematic** spacetime lift, but it is not
yet a theorem-grade **action** route to full GR.

The exact missing object is one of:

1. a `PL S^3 x R` discrete action
2. a spacetime-lift observable
3. a uniqueness theorem for the compatible dynamics

Until one of those appears, Route 2 stays dynamically blocked.
