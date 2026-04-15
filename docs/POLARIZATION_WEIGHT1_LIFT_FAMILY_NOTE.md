# Weight-1 Lift Family for the Dark-Phase Curvature Map

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** exact remaining ambiguity after the support dark phase and the universal weight decomposition are both in hand

## Verdict

After the latest reductions, the remaining curvature-side ambiguity is a
single parameter.

Why:

1. the support dark phase is one exact `SO(2)` weight-1 doublet;
2. the universal complement contains two exact `SO(2)` weight-1 doublets;
3. any covariant linear lift from one weight-1 doublet into the direct sum of
   two weight-1 doublets is an equivariant mixing family.

After fixing overall normalization, that family is exactly:

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

So the remaining universal ambiguity is a single mixing parameter `lambda`
between the two universal weight-1 sectors.

## Input facts

From the support-side phase primitive:

- the residual connected gauge is `SO(2)`;
- the exact support dark pair `D_R = (d_y, d_z)` carries charge `1`;
- the exact dark phase `vartheta_R` exists wherever `rho_R != 0`.

From the universal-side weight decomposition:

- there are two exact weight-1 doublets on the universal complement;
- there is a separate weight-2 shear sector, which is excluded by covariance.

So the only representation-theoretically allowed target is the direct sum of
the two weight-1 universal doublets.

## Exact lift family

Let `D` denote the support dark doublet. Then every normalized equivariant lift
into the two universal weight-1 sectors is of the form

`L_lambda(D) = (cos(lambda) D, sin(lambda) D)`.

This is exact because each component transforms with the same `SO(2)` weight.

The family is normalized:

`||L_lambda(D)|| = ||D||`.

So once the overall scale is fixed, the only remaining freedom is `lambda`.

## Consequence

This is much sharper than the older bundle obstruction.

The remaining phase-to-curvature ambiguity is no longer:

- a generic projector bundle
- a generic connection
- a generic complement section

It is:

> one mixing parameter `lambda` between two exact universal weight-1 sectors.

That matches the holonomy audit, which found that flatness and singular-set
structure still leave a free holonomy normalization parameter.

## Bottom line

The all-out push now isolates the gravity frontier to:

> determine the canonical value of the single mixing parameter `lambda`, or
> prove that the current atlas cannot fix it.
