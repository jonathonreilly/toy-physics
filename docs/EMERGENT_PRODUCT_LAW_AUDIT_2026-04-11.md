# Emergent M1*M2 Product Law Audit

**Date:** 2026-04-11  
**Status:** approved for bounded promotion to `main`
**Primary runner:** scripts/frontier_emergent_product_law.py

## Decision

Promote, but only as a bounded field-linearity result on one audited surface.
Do not read this as full Newton closure.

## Exact Retained Wording

> On the audited open 3D staggered cross-field Poisson surface (`side=14`,
> `G=50`, `mu^2=0.001`), two-orbital Hartree dynamics produces
> `|F| ~ M_A^1.0146 M_B^0.9863` with `R^2 = 0.999993`, and the frozen-source
> control gives `|F| ~ M_A^1.0081 M_B^0.9919` with `R^2 = 0.999998`.

## Why This Is Retainable

The runner does not contain an explicit `M_A * M_B` interaction term. The
source density is linear in each mass, the Poisson solve is linear, and the
force observable carries the test-packet mass linearly. The frozen-source
control stays essentially unchanged, so the retained interpretation is that the
product law is a field-linearity consequence on this audited surface.

## Caveats

1. This is a single open 3D staggered cross-field Poisson surface, not an
   architecture-independent theorem.
2. This is a field-linearity product-law companion, not full Newton closure.
3. The distance law is fixed in this experiment, so the `1/r^2` claim belongs
   elsewhere.
4. The result is not the earlier exact-two-particle toy, which baked the
   product law into the Hamiltonian ansatz.

## Retained Wording For Main

"On the audited open 3D staggered cross-field Poisson surface, the mutual
force scales as `F ~ M_A^alpha M_B^beta` with `alpha = 1.0146` and
`beta = 0.9863` in the dynamic run, and the frozen-source control gives
`alpha = 1.0081`, `beta = 0.9919` with `R^2 > 0.99999`. The bilinear factor is
not explicit in the Hamiltonian, and the product law is retained only as a
bounded field-linearity result on this surface."

## Verdict

**Retainable to `main`: yes, bounded.**
