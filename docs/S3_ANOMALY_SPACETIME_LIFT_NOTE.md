# `S^3` + Anomaly-Forced Time: Axiom-First Spacetime Lift

**Status:** open - kinematic route with missing dynamic theorem
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Purpose:** route-2 assessment from `FULL_GR_AXIOM_FIRST_PATHS_NOTE.md`

## Verdict

**Kinematically promising, dynamically blocked.**

The current atlas supports a clean axiom-first background candidate:

- `S^3` topology is already closed as a retained `PL S^3` compactification
- anomaly-forced time is already closed as an exact `d_t = 1` result

Together, these give the unique clean background candidate

    PL S^3 x R

for a spacetime lift.

That is a real architecture. It is cleaner than the shell/tensor-boundary
route in one sense: it starts from topology + chirality/time and tries to
build the spacetime background first.

But the current atlas still does **not** contain an exact theorem that turns
that background into the required tensor/metric dynamics. In particular:

- no exact `S^3`-to-curvature law is present
- no exact anomaly-to-Einstein-field-equation derivation is present
- no exact discrete variational action is present for this route

So route 2 is not a full-GR proof path yet. It is a clean kinematic path
with a precise dynamical gap.

## What the route would need

The route becomes theorem-grade only if one can derive at least one of:

1. an exact spacetime-lift observable from the `S^3` + anomaly stack
2. an exact action whose Euler-Lagrange equations give the GR field law on
   the lifted background
3. a uniqueness theorem saying the only compatible dynamical lift is the GR
   one

Without one of those, the route remains a background theorem, not a full
gravity closure theorem.

## Route 2 in context

The current `FULL_GR_AXIOM_FIRST_PATHS_NOTE.md` survey treats this as one of
the top three alternatives because it uses only retained topology and
chirality/time tools. That is still correct.

But the route is now sharper than the survey wording alone suggests:

- `S^3` is exact and reusable
- anomaly-forced time is exact and reusable
- the combined lift `PL S^3 x R` is the right kinematic target
- the missing piece is a genuine dynamical bridge

## Full 10-route survey

Against the current atlas and axioms, the 10 candidate architectures are:

1. Exact support-side tensor observable on `A1 x {E_x, T1x}`.
2. Exact support-side Schur / Dirichlet tensor action.
3. Axiom-first spacetime lift from `S^3` and anomaly-forced time.
4. Observable-principle effective-action route.
5. Gauge-matter-first backreaction route.
6. Exact finite-rank source-to-metric theorem.
7. Direct lattice Green / resolvent route to the full metric.
8. Discrete 4D variational action route.
9. Geometric RG / projective-shape flow route.
10. Obstruction-first theorem with a minimal new primitive.

The current ranking still stands:

1. support-side tensor observable
2. `S^3` + anomaly-forced-time spacetime lift
3. exact finite-rank source-to-metric theorem

## Runner result

The companion runner checks the route ingredients directly on `main`:

- `S^3` compactification theorem is closed
- anomaly-forced time theorem is exact
- the atlas contains both as reusable tools
- the atlas does not yet contain an exact dynamics bridge for this route

That is the sharp blocker.

## Bottom line

Route 2 is **not** a GR closure yet.
It is a clean axiom-first **kinematic** route with a well-defined missing
dynamic theorem.
