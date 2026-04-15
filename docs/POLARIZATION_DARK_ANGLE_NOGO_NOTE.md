# Dark-Angle No-Go on the Current Polarization-Bundle Candidate

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** exact final obstruction after the common connected residual gauge has collapsed to `SO(2)`

## Verdict

The remaining connected common residual gauge is indeed only

`SO(2)`.

But the current exact common objects are all blind to that angle.

Concretely, under the residual dark-plane `SO(2)` action:

- `delta_A1` is invariant;
- the bright pair `u_E, u_T` is invariant;
- the exact Route 2 carrier `K_R` is invariant;
- the exact tensorized action `I_TB` is invariant;
- the exact spacetime carrier `Xi_TB` is invariant.

At the same time, the dark complement itself moves nontrivially.

So the current atlas does **not** contain enough exact structure to derive a
canonical dark-angle section or a distinguished connection on that last
`SO(2)` bundle.

## Input sharpening

The glue pass already established that the strongest shared candidate is

`P_glue^cand := (Pi_A1, B_R, O_glue)`

with

`B_R := (K_R, I_TB, Xi_TB)`

and exact common connected residual gauge

`SO(2)`.

That reduced the obstruction from a generic missing full bundle to a single
dark-plane angle.

## Exact invariance of the current common data

The support-side residual `SO(2)` rotates only the dark complement plane.
It leaves the Route 2 bright block untouched.

Because the current exact carrier is

`K_R(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T)`,

and because `delta_A1`, `u_E`, and `u_T` are all unchanged under the dark-plane
rotation, the carrier itself is unchanged.

Then the current exact tensorized action

`I_TB(f, a ; j) = I_R(f ; j) + 1/2 ||a - vec K_R(q)||^2`

is also unchanged.

Finally, the current exact spacetime carrier

`Xi_TB(t ; q) = vec K_R(q) \otimes exp(-t Lambda_R) u_*`

is unchanged as well, because it factors through `K_R`.

So every exact common object currently available factors through data that are
invariant under the residual `SO(2)`.

## Exact no-go

This gives the sharp no-go:

> No canonical dark-angle section or distinguished connection can be derived
> from the current exact common bundle data alone, because every exact common
> object is invariant under the residual dark-plane `SO(2)` action.

Equivalently:

> the current atlas has reduced the gravity obstruction to one angle, but it
> has not supplied any exact angle-sensitive observable or transport law.

## What is now actually missing

The missing primitive is therefore no longer a generic bundle or frame object.
It is specifically:

> an exact angle-sensitive primitive on the dark complement plane.

Examples of the kind of thing that could close this gap:

- a canonical axial phase convention;
- an angle-sensitive support observable;
- an angle-sensitive curvature-localization observable;
- a connection law whose holonomy detects the dark-plane angle.

Without one of those, the current atlas cannot fix the final `SO(2)` freedom.

## Bottom line

The common residual gauge has collapsed to one angle, but the current exact
candidate data are completely blind to that angle.

So the honest frontier is now:

- **not** a missing full canonical `3+1` bundle;
- **not** a missing generic connection;
- **exactly** a missing angle-sensitive primitive on the dark complement plane.
