# Polarization Lambda from Dark-Phase Holonomy

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** test whether singular-locus regularity, punctured-bundle flatness, or global trivialization can fix the dark-phase holonomy normalization `lambda` after the latest phase-lift reductions

## Verdict

The current atlas does **not** canonically fix `lambda`.

The exact residual freedom remains a one-parameter family of flat dark-plane
connections:

`A_lambda = lambda d vartheta_R`.

The three candidate mechanisms fail in the same way:

1. singular-locus regularity fixes the defect set `Sigma_R`, but not the
   normalization of the connection on its complement;
2. punctured-bundle flatness gives `d A_lambda = 0` for every `lambda`;
3. global trivialization on a cut domain makes `A_lambda` exact, but exactness
   still leaves the coefficient `lambda` free.

So the exact conclusion is the negative one:

> the current atlas does not derive a canonical `lambda`; it leaves a
> one-parameter residual holonomy family.

## Exact setup

The support-side dark pair is

`D_R(q) := (d_y, d_z)`.

The radius/phase decomposition is

`rho_R(q) := sqrt(d_y^2 + d_z^2)`,

`vartheta_R(q) := atan2(d_z, d_y)`.

The singular locus is

`Sigma_R := { q : rho_R(q) = 0 }`.

On the punctured complement

`X_R := { q : rho_R(q) > 0 }`,

the candidate connection family is

`A_lambda := lambda d vartheta_R`.

## Why singular-locus regularity does not fix `lambda`

The singular locus is determined entirely by `rho_R`.

Since `rho_R` does not involve `lambda`, every member of the family
`A_lambda` has the same defect set `Sigma_R`.

So regularity at `Sigma_R` only tells us where the phase is undefined. It
does not choose a preferred normalization of the flat connection on `X_R`.

## Why punctured-bundle flatness does not fix `lambda`

On `X_R`,

`d A_lambda = lambda d^2 vartheta_R = 0`.

So all `lambda` give a flat connection on the punctured complement.

Flatness therefore collapses the curvature, but not the holonomy character.
The family remains distinct through its loop integrals.

For a winding-one loop `gamma`,

`Hol_lambda(gamma) = ∮_gamma A_lambda = 2 pi lambda`.

Different `lambda` give different holonomy characters, so flatness does not
canonically select one value.

## Why global trivialization still does not fix `lambda`

If one cuts the punctured bundle to a simply connected branch domain, then
`vartheta_R` admits a global branch `vartheta_cut`, and on that domain

`A_lambda = d( lambda vartheta_cut )`.

So the connection becomes globally exact on the cut domain for every
`lambda`.

But exactness does not fix the coefficient of the primitive. The same
trivialization supports the entire family, and the current atlas does not
contain any normalization rule that singles out one `lambda` among the
exactly exact primitives.

## Exact holonomy test

The latest phase-lift reductions already establish the stronger support-side
objects:

`B_R^phase = (K_R^phase, I_TB^phase, Xi_TB^phase)`

and the orbit-valued phase-to-curvature correspondence

`[vartheta_R]_{SO(2)} <-> [alpha_curv]_{SO(2)}`.

Those results sharpen the obstruction, but they do not change it:

- the support dark phase exists exactly;
- the common bridge carries it only as an orbit coordinate;
- the shared residual gauge is still `SO(2)`;
- the holonomy normalization `lambda` remains free.

## Bottom line

The current atlas does not derive a canonical `lambda`.

The exact residual freedom is still one-parameter:

`A_lambda = lambda d vartheta_R`.

To fix `lambda`, the atlas would need an additional normalization principle
that is not present in the current phase/holonomy stack.
