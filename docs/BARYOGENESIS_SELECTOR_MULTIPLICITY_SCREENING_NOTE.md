# Baryogenesis Selector Multiplicity / Screening Note

**Date:** 2026-04-16
**Status:** bounded/open support target on `main`
**Script:** `scripts/frontier_baryogenesis_selector_multiplicity_screening.py`

## Safe statement

The exact selector portal result does **not** close baryogenesis by itself.

What it does close is the next boundary question:

> once the portal scale is fixed by the exact graph-first quartic surface,
> what multiplicity and screening budget must the finite-`T` scalar sector
> satisfy to keep the old taste-scalar route alive?

The answer is now explicit.

## Exact selector multiplicity

On the exact graph-first selector surface, choosing one axis as the Higgs
direction leaves exactly two orthogonal real scalar directions.

Write

`phi = (v + h, s_2, s_3)`.

Then the exact selector quartic around the chosen axis contains

- one Higgs-axis fluctuation `h`
- two orthogonal real selector modes `s_2`, `s_3`

and no additional orthogonal directions on that real selector manifold.

So the exact real selector multiplicity is

`n_real = 2`.

## One-mode contribution with the derived selector portal

The previous note derived

`kappa_sel = 6 lambda_H`.

For one real scalar mode with

`m_s^2(h) = (kappa_sel / 2) h^2`,

the undressed one-loop cubic contribution is

`Delta E_1 = 1/(12 pi) * (kappa_sel / 2)^(3/2)`.

So the full unscreened scalar contribution can be written as

`Delta E_scalar = n_eff * xi_screen * Delta E_1`

where:

- `n_eff` is the effective real scalar multiplicity participating in the high-`T`
  cubic term
- `xi_screen <= 1` is the survival factor after thermal screening / daisy effects

## Exact requirement

Matching the previously derived target

`Delta E_target = E_required - E_gauge`

gives the exact condition

`n_eff * xi_screen = Delta E_target / Delta E_1`.

On the current promoted package surface this becomes:

- `n_eff * xi_screen = 3.7969` on the `m_H = 119.77 GeV` support route
- `n_eff * xi_screen = 3.7700` on the `m_H = 125.10 GeV` canonical route

So the old route requires an effective unscreened multiplicity of almost `4`
real scalar modes.

## Consequence for the exact selector manifold

The exact real selector surface gives only

`n_real = 2`.

Even with no screening at all (`xi_screen = 1`), that would give only

- `52.7%` of the required enhancement on the 2-loop Higgs support route
- `53.0%` of the required enhancement on the full 3-loop route

So the exact real selector manifold by itself cannot close the old
taste-scalar baryogenesis route.

## Conditional route-history rescue

If the route-history phrase "2HDM-like taste-scalar spectrum" is interpreted as
an effective

`n_eff = 4`

real scalar multiplicity, then the selector portal can work only if screening
is extremely mild:

- `xi_screen >= 0.949` on the 2-loop Higgs support route
- `xi_screen >= 0.943` on the full 3-loop route

So the remaining open question is not portal size anymore. It is whether the
finite-`T` theory supplies both:

1. an effective doubling from the exact real `n=2` selector surface to roughly
   `n_eff = 4`
2. a screening penalty smaller than about `5%` to `6%`

The current Higgs/CW surface does supply one derived Higgs doublet with
`1+3` scalar content, but the matching boundary note shows that this does
**not** by itself justify reusing the selector coefficient across all four
modes. That boundary is recorded in
[BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md](./BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md).

## Why this matters

This is a substantial narrowing of the baryogenesis lane.

Before:

- missing EWPT strength
- missing portal scale
- vague taste-scalar route

Now:

- portal scale is derived: `kappa_sel = 6 lambda_H`
- the exact real selector surface alone is not enough
- the only live scalar-side loophole is an additional doubling mechanism with
  very mild screening

That is a much sharper scientific target.

## What this closes

This note closes the following question:

> "Given the exact selector portal, does the exact real selector manifold
> already provide enough scalar cubic strength?"

Answer:

- no
- it provides only about half the required enhancement
- any surviving old route must therefore rely on additional finite-`T`
  multiplicity and almost no screening

## What remains open

This note does **not** yet determine:

- whether the required doubling mechanism exists on the retained finite-`T`
  surface
- whether daisy screening is indeed that mild
- the nonperturbative transition strength
- the sphaleron rate
- transport / diffusion
- a derived `eta`

## Validation

- [frontier_baryogenesis_selector_multiplicity_screening.py](./../scripts/frontier_baryogenesis_selector_multiplicity_screening.py)
- [BARYOGENESIS_SELECTOR_PORTAL_NOTE.md](./BARYOGENESIS_SELECTOR_PORTAL_NOTE.md)
- [BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md](./BARYOGENESIS_HIGGS_DOUBLET_MULTIPLICITY_NOTE.md)

Current runner state:

- `frontier_baryogenesis_selector_multiplicity_screening.py`: expected
  `PASS>0`, `FAIL=0`
