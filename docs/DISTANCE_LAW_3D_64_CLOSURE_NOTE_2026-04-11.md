# 3D Path-Sum Distance Continuation Note

**Date:** 2026-04-11  
**Status:** proposed_retained narrowly as a bounded continuation note; not full Newton closure

## Artifact chain

- [`scripts/distance_law_3d_64_closure.py`](../scripts/distance_law_3d_64_closure.py)
- commit `4af00dc5b7a65e1ffc2fe11f7271292727bacfa5`

## Scope

This note records a single 3D path-sum distance-law continuation on a
64^3 lattice. It is best read as a bounded numerical extension of the
existing path-sum distance-story line, not as a universal theorem and not as
a replacement for the Wilson-lane control work.

## Retained result

The retained signal is:

- grid sweep: `31^3, 40^3, 48^3, 56^3, 64^3`
- far-field exponent on the largest grid: `alpha = -1.023 +/- 0.012`
- finite-size extrapolation: `alpha_inf = -0.976 +/- 0.019`
- mass linearity on the largest grid: spread `< 0.1%`

That is consistent with a Newtonian `1/r^2` force law at the level of a
bounded numerical continuation, with the usual finite-size caveats.

## Why this stays bounded

The note does not close the stronger claims that would let this replace the
existing retained story:

- it uses one point-mass source family on one 3D lattice geometry
- it uses Dirichlet boundaries, so boundary sensitivity is still part of the
  readout
- it does not provide a frozen/static-source control family
- it does not show architecture portability beyond this path-sum setup
- it does not establish the full two-body `M_1 M_2` law

## Mainline read

Safe mainline phrasing:

- the 64^3 path-sum run is a strong bounded continuation of the
  path-sum distance story
- it supports a near-Newton continuum trend on this surface
- it should not be cited as full Newton closure

## Blockers for stronger promotion

1. Add a matched frozen/static-source control on the same 64^3 surface.
2. Re-run the same continuation under a second boundary condition or
   control surface.
3. Bridge the continuation to the existing Wilson / two-body mass-law lane
   before treating it as architecture-independent.

## Bottom line

Retain this as a narrow continuation note. Promote the distance-law trend,
not the stronger Newton-closure story.
