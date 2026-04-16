# Baryogenesis Higgs-Doublet Multiplicity Note

**Date:** 2026-04-16
**Status:** bounded/open support target on `main`
**Script:** `scripts/frontier_baryogenesis_higgs_doublet_multiplicity.py`

## Safe statement

Yes, the current framework surface already contains a same-surface candidate
for the required `n=4` scalar multiplicity.

The exact real selector manifold by itself leaves only two orthogonal real
directions, but the Higgs / Coleman-Weinberg lane already fixes the physical
electroweak scalar content as one derived Higgs doublet:

- `n_H = 1` Higgs doublet from the `G_5` condensate
- `n_Higgs = 1` radial mode
- `n_Goldstone = 3`

So the physical scalar multiplicity used on the Higgs/CW surface is

`n_scalar = n_Higgs + n_Goldstone = 4`.

That is exactly the multiplicity needed by the selector-portal baryogenesis
route.

## Why this is not the same count as the real selector manifold

The graph-first selector manifold is the right surface for deriving:

- the selected Higgs axis
- the exact quartic selector
- the portal/self ratio

On that real manifold, choosing one axis leaves only two orthogonal real
directions.

The finite-temperature scalar multiplicity relevant to the Higgs/CW potential
is counted after electroweak completion, where the framework already uses one
derived Higgs doublet with one radial mode and three Goldstones.

So:

- selector manifold: portal structure
- Higgs-doublet completion: thermal scalar multiplicity

These are complementary, not contradictory, statements.

## Existing derived inputs on `main`

The current repo already records all of the following:

1. `n_H = 1` Higgs doublet from the `G_5` condensate in the EW/Yukawa bridge
2. `n_Higgs = 1`, `n_Goldstone = 3` in the Higgs/CW effective-potential
   runners
3. `kappa_sel = 6 lambda_H` from the exact graph-first quartic selector
4. `n_eff * xi_screen ~= 3.77 - 3.80` from the selector multiplicity/screening
   note

Putting these together gives the scalar-side baryogenesis condition

`4 * xi_screen >= 3.77 - 3.80`

so the required screening survival is

- `xi_screen >= 0.949` on the 2-loop Higgs support route
- `xi_screen >= 0.943` on the full 3-loop Higgs route

## Main consequence

This closes the multiplicity loophole.

The scalar-side baryogenesis lane no longer needs:

- an unexplained extra-doublet insertion
- an ad hoc doubling beyond the current framework surface

The current same-surface Higgs/CW package already carries the needed `n=4`
scalar multiplicity. So the only remaining scalar-side open object is the
finite-`T` screening survival factor.

## What this closes

This note closes the following question:

> "Does the required scalar multiplicity have to be added by hand, or is it
> already on the current framework surface?"

Answer:

- it is already on the current framework surface as the derived one-Higgs-doublet
  scalar content

## What remains open

This note does **not** yet determine:

- the actual finite-`T` screening factor on the retained surface
- whether Goldstone contributions survive daisy resummation strongly enough
- the nonperturbative transition strength
- the sphaleron rate
- transport / diffusion
- a derived `eta`

So the scalar-side baryogenesis lane is now reduced to:

- derived portal
- derived multiplicity
- one remaining open screening survival factor

## Validation

- [frontier_baryogenesis_higgs_doublet_multiplicity.py](./../scripts/frontier_baryogenesis_higgs_doublet_multiplicity.py)
- [BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md](./BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md)
- [BARYOGENESIS_SELECTOR_PORTAL_NOTE.md](./BARYOGENESIS_SELECTOR_PORTAL_NOTE.md)

Current runner state:

- `frontier_baryogenesis_higgs_doublet_multiplicity.py`: expected `PASS>0`,
  `FAIL=0`
