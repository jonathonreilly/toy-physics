# Baryogenesis Higgs-Doublet Multiplicity / Matching Boundary Note

**Date:** 2026-04-16
**Status:** bounded/open scalar-surface matching boundary on `main`
**Script:** `scripts/frontier_baryogenesis_higgs_doublet_multiplicity.py`

## Safe statement

Yes, the current framework surface already contains one derived Higgs doublet
with one radial mode plus three Goldstones.

But that does **not** close the old scalar-side baryogenesis route.

The missing step is a matching theorem between two different scalar surfaces:

- the exact selector surface, which fixes the portal coefficient
  `kappa_sel = 6 lambda_H`
- the Higgs/CW one-doublet surface, which fixes the physical `1+3` scalar
  content

Once that matching is done honestly, only the radial Higgs mode carries the
selector coefficient. The three Goldstones do not.

So the old step

`kappa_sel times n=4`

is not framework-derived.

## What is derived here

The current repo already fixes all of the following:

1. one Higgs doublet from the `G_5` condensate
2. one radial Higgs mode plus three Goldstones on the Higgs/CW surface
3. exact selector-portal coefficient

   `kappa_sel = 6 lambda_H`

4. Higgs/CW field-dependent masses

   `m_rad^2(h) = 3 lambda_H h^2`

   `m_G^2(h) = lambda_H h^2`

The exact selector quartic therefore matches the **radial** Higgs coefficient
exactly:

`m_sel^2(h) = 3 lambda_H h^2 = m_rad^2(h)`.

But it does **not** match the Goldstones:

`m_G^2(h) = (1/3) m_sel^2(h)`.

Equivalently, in the baryogenesis `kappa` convention:

- selector / radial mode: `kappa_sel = 6 lambda_H`
- Goldstone modes: `kappa_G = 2 lambda_H`

So the Goldstones are lighter by a factor `3` in `kappa`.

## Exact consequence

If one still uses the same imported one-loop scalar-cubic bookkeeping as the
earlier baryogenesis notes, the matched one-doublet scalar contribution is

`DeltaE_doublet = DeltaE_sel,1 + 3 DeltaE_G,1`

with

`DeltaE_sel,1 prop to (3 lambda_H)^(3/2)`

and

`DeltaE_G,1 prop to (lambda_H)^(3/2)`.

Measured in units of one selector-mode contribution, the exact one-doublet
surface therefore has selector-equivalent multiplicity

`n_equiv = 1 + 1/sqrt(3) = 1.57735...`

not `4`.

That is the exact matching-boundary result.

## Consequence for the old route

The earlier `n=4` rescue used the correct Higgs-doublet multiplicity count, but
it implicitly reused the selector coefficient across all four scalar modes.
That step is not derived from the current same-surface package.

Using the actual one-doublet scalar spectrum instead:

- the unscreened scalar contribution reaches only about `41%` of the old
  target on the current imported one-loop high-`T` ansatz
- the remaining gap is still about `2.4x` even **before** screening

So the scalar-side open question is stronger than “is screening mild enough?”

It is now:

- can the framework derive additional same-surface bosonic structure beyond the
  matched one-doublet spectrum?
- or does the real finite-`T` dynamics differ substantially from the old
  one-loop scalar-cubic route?

## Why this matters

This is a hardening step, not a retreat.

Before this note, the scalar-side lane could be misread as:

- portal derived
- multiplicity derived
- only screening left

After this note, the honest statement is:

- portal derived
- Higgs-doublet multiplicity derived
- exact matching boundary derived
- the naive `n=4` selector rescue is **not** derived

That is a much tighter and more reviewer-safe package surface.

## What this closes

This note closes the following question:

> “Can the exact selector portal simply be combined with the Higgs-doublet
> `1+3` multiplicity to close the scalar-side baryogenesis route?”

Answer:

- no
- the selector coefficient matches only the radial mode
- the actual matched one-doublet scalar package is much weaker than the old
  `n=4` reuse implied

## What remains open

This note does **not** yet determine:

- whether the framework derives an additional finite-`T` scalar sector
- whether a non-minimal or nonperturbative finite-`T` potential replaces the
  old one-loop scalar-cubic bookkeeping
- the actual finite-`T` screening factor on the retained surface
- the nonperturbative transition strength
- the sphaleron rate
- transport / diffusion
- a derived `eta`

So the scalar-side baryogenesis lane is now:

- exact selector portal
- exact Higgs-doublet `1+3` content
- exact matching boundary between those two surfaces
- one remaining real finite-`T` dynamical gap

## Validation

- [frontier_baryogenesis_higgs_doublet_multiplicity.py](./../scripts/frontier_baryogenesis_higgs_doublet_multiplicity.py)
- [BARYOGENESIS_SELECTOR_PORTAL_NOTE.md](./BARYOGENESIS_SELECTOR_PORTAL_NOTE.md)
- [BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md](./BARYOGENESIS_SELECTOR_MULTIPLICITY_SCREENING_NOTE.md)

Current runner state:

- `frontier_baryogenesis_higgs_doublet_multiplicity.py`: expected `PASS>0`,
  `FAIL=0`
