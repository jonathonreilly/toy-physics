# Universal GR Lambda Bypass on `PL S^3 x R`

**Status:** support - lambda-bypass candidate
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal bypass route / candidate note  
**Purpose:** attack whether `lambda` is an artifact of the current phase-lift
architecture by staying on the direct universal tensor action / quotient-kernel
route

## Verdict

The current direct universal route does **not** collapse onto the same
`lambda` ambiguity as the phase-lift architecture.

The direct universal route can be written as a lambda-free `A1`-anchored
action/quotient-kernel candidate:

`S_GR^bypass[h] := 1/2 * D^2 W[g_*](Pi_A1 h, Pi_A1 h)`.

Here:

- `W[J] = log|det(D+J)| - log|det D|` is the exact scalar observable
  generator;
- `Pi_A1` is the exact rank-2 invariant projector onto lapse and spatial
  trace;
- `g_*` is the lifted `PL S^3 x R` background source;
- the quotient kernel is the exact symmetric `3+1` Hessian restriction on
  the `A1` block.

This candidate is exact as a construction and it never introduces the
phase-lift mixing family `L_lambda`. So, at the level of the direct universal
action/quotient-kernel route, `lambda` is bypassed rather than chosen.

## Why this bypass is clean

The previous `lambda` obstruction came from the phase-lift architecture:

- support dark phase `vartheta_R`;
- universal weight-1 multiplicity space;
- normalized lift family `L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

That family is specific to matching the support phase into the universal
weight-1 sectors.

The direct universal route does not need that matching step if one works only
with the `A1`-anchored tensor action candidate. On that route:

1. the scalar observable generator is exact;
2. the `PL S^3 x R` kinematic lift is exact;
3. the symmetric `3+1` quotient kernel is exact;
4. the `Pi_A1` section is exact and canonical;
5. no `lambda` parameter is required to define the candidate action.

So the strongest concrete bypass candidate is:

> the exact `A1`-projected tensor action on the direct universal route.

## What remains open

This bypass does **not** close full GR.

The remaining obstruction is different from the phase-lift `lambda` family:

- the complementary `E \oplus T1` channels still form an `SO(3)` orbit
  bundle;
- the current atlas still lacks a covariant `3+1` curvature-localization
  operator `Pi_curv`;
- the invariant `A1` core is canonical, but the complement is still frame
  dependent.

So the direct universal route bypasses `lambda`, but it still stops at the
same final type of missing object as before:

> a canonical curvature-localization bundle / distinguished connection for
> the complement.

## Honest status

The current direct universal route is:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- lambda-free in the action/quotient-kernel candidate;
- still blocked at the curvature-localization level.

So the answer to the bypass question is:

> yes, the direct universal action route bypasses `lambda` entirely at the
> `A1`-anchored candidate level, but it does so by shifting the remaining
> obstruction to the complement frame bundle rather than closing full GR.
