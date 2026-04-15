# Finite-Rank Lambda Bypass Test

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_finite_rank_lambda_bypass.py`  
**Status:** no bypass; the finite-rank widening route inherits the same one-parameter ambiguity

## Verdict

The finite-rank/class-expansion route does **not** canonically fix `lambda`.
The widening side gives a stronger support block and a better source-to-metric
theorem, but it still stops at the same normalized weight-1 multiplicity
freedom:

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

So the answer is negative:

> the widening route does not eliminate the `lambda` ambiguity; it carries the
> same residual `SO(2)` phase orbit forward.

## What the finite-rank route does fix

The widening route does fix a lot of structure exactly:

- the support-irrep frame
  `A1(center) ⊕ A1(shell) ⊕ E ⊕ T1`;
- the exact scalar active-quotient law through total charge `Q_eff`;
- the exact bilinear Route-2 carrier
  `K_R(q) = [[u_E, u_T], [delta_A1 u_E, delta_A1 u_T]]`;
- the scalar/isotropic finite-rank source-to-metric reduction.

That is enough to enlarge the source side and to get a clean scalar exterior
theorem. It is not enough to pick a preferred point in the weight-1
multiplicity circle.

## Why the widening route still leaves `lambda` free

The finite-rank support canonical frame only fixes a block decomposition, not
a fully rigid polarization bundle. The exact support-side freedom is still
the orthogonal freedom on the dark complement:

- `O(1)` on `E_perp`
- `O(2)` on the dark `T1` plane

The bright carrier coordinates `u_E` and `u_T` are exact, but the tensorized
Route-2 action is Euclidean and therefore blind to orthogonal reparameter-
izations of that bright block. Rotating the bright basis simply moves along
the same normalized circle family; it does not select a canonical angle.

In other words:

- the widening route gives a canonical block frame;
- it does not give a canonical bright-basis origin;
- therefore it cannot fix the `lambda` angle.

## Why the source-to-metric theorem does not help

The exact finite-rank source-to-metric theorem is scalar. Its exact outputs
depend on the renormalized scalar source charge and on the scalar boundary
action, not on a phase choice in the bright multiplicity space.

So the widened source-to-metric side is theta-blind:

- it sees `Q_eff`;
- it sees the stationary scalar boundary action;
- it does not see a canonical weight-1 section selector.

That is the same failure mode as the phase-lift route: the observable surface
is orbit-valued, not section-valued.

## Consequence

The finite-rank widening route inherits the same one-parameter ambiguity:

- the exact support geometry leaves a residual `O(2)` phase orbit in the
  bright sector;
- the tensorized action is orthogonally invariant on that sector;
- the scalar source-to-metric theorem does not choose a phase section.

So there is no finite-rank bypass of `lambda` in the current atlas. To fix
`lambda`, we would need a new selector primitive that is not present in the
current widening stack, most plausibly a time-sensitive or curvature-local
connection choice.

## Bottom line

The widening route is better organized than the direct phase-lift route, but
it does **not** remove the `lambda` ambiguity.

It inherits the same exact one-parameter freedom, so the finite-rank/class-
expansion path is not a bypass.
