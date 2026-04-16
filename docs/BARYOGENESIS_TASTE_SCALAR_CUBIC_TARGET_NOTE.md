# Baryogenesis Taste-Scalar Cubic Target Note

**Date:** 2026-04-16
**Status:** bounded/open support target on `main`
**Script:** `scripts/frontier_baryogenesis_taste_scalar_cubic_target.py`

## Safe statement

The next honest step after the finite-`T` reduction note is not to claim a
completed electroweak phase transition computation. It is to derive the exact
extra bosonic cubic strength that any viable taste-scalar EWPT route must add
to the minimal gauge-cubic control potential.

That is what this note does.

It turns the vague statement

> "the taste-scalar sector must strengthen the transition"

into an explicit one-loop high-`T` target relation for the missing cubic term.

## Input surface

This note starts from the current bounded baryogenesis package:

- [BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md](./BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md)
  fixes the historical target `v(T_c)/T_c ~ 0.52`
- [BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md](./BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md)
  shows that the minimal gauge-cubic reduction gives only
  `v_c/T_c ≈ 0.15`

So the missing object is the extra bosonic cubic coefficient

`ΔE = E_required - E_gauge`.

## Imported scalar-cubic ansatz

In the same imported one-loop high-`T` Landau reduction used in the finite-`T`
note, a bosonic mode with field-dependent mass

`m_s^2(phi) = (κ_s / 2) phi^2`

contributes

`E_s = n_s / (12 pi) * (κ_s / 2)^(3/2)`

to the cubic coefficient, where:

- `n_s` is the number of real bosonic degrees of freedom carrying that mass
- `κ_s` is the effective portal/curvature coupling of that mode to the order
  parameter

This is still an imported thermal ansatz, not yet a lattice-derived theorem.
But it converts the open EWPT route into an exact algebraic target.

## Main relation

Let

- `E_gauge` be the gauge-boson cubic coefficient from the finite-`T` reduction
- `E_required = lambda * (v_c/T_c)_target / 2`

with the historical target `(v_c/T_c)_target = 0.52`.

Then the missing taste-scalar sector must satisfy

`sum_i n_i (κ_i / 2)^(3/2) = 12 pi (E_required - E_gauge)`.

On the current promoted package surface this gives:

- `sum_i n_i (κ_i / 2)^(3/2) = 0.8023` on the `m_H = 119.77 GeV` support route
- `sum_i n_i (κ_i / 2)^(3/2) = 0.9077` on the `m_H = 125.10 GeV` canonical route

That is the exact one-loop scalar-cubic target implied by the current package.

## Minimal 2HDM-like interpretation

The old route history described the target as natural for a "2HDM-like
taste-scalar spectrum."

If that phrase means one extra complex `SU(2)` doublet with four real bosonic
degrees of freedom carrying a common effective coupling `κ`, then the target
reduces to

`4 (κ / 2)^(3/2) = 12 pi (E_required - E_gauge)`.

This gives:

- `κ ≈ 0.685` on the `m_H = 119.77 GeV` support route
- `κ ≈ 0.744` on the `m_H = 125.10 GeV` canonical route

Rounded to one significant reviewer-facing window, that is

- `κ ~= 0.69 - 0.74`

So the old route does **not** require a huge or absurd coupling. But it does
require an honest order-1 scalar portal. A weak quartic-scale coupling is not
enough.

## Why multiplicity alone is not enough

If the extra doublet had only Higgs-quartic-scale coupling

`κ ~ lambda_H ~= 0.12 - 0.13`

then its scalar cubic term would supply only about `7%` of the required
enhancement.

Equivalently, at `κ = lambda_H` one would need about `55` real scalar degrees
of freedom to hit the target, which is not compatible with a minimal
2HDM-like route.

So the old route can only work if the taste-scalar sector is not merely
"present," but coupled to the order parameter substantially more strongly than
the Higgs quartic itself.

## Important caution

This target is optimistic.

The relation above uses the undressed one-loop scalar cubic term. Thermal
screening / daisy resummation typically weakens scalar cubic contributions.
So if the same-surface finite-`T` theory includes standard thermal screening,
the true required `κ` would be larger than the values quoted here, not smaller.

## What this closes

This note closes the next derivation-side question:

> "If the older taste-scalar EWPT route is real, what exact scalar-cubic
> relation must it satisfy?"

Answer:

- the route must supply
  `sum_i n_i (κ_i / 2)^(3/2) ~= 0.80 - 0.91`
- a minimal extra-doublet interpretation needs
  `κ ~= 0.69 - 0.74`
- a quartic-scale scalar coupling is decisively too small

## What this does not close

This note does **not** claim:

- that an extra taste-scalar doublet is already derived on the authority path
- a lattice derivation of the finite-`T` scalar effective potential
- a daisy-resummed or nonperturbative thermal calculation
- a derived sphaleron rate or transport system
- a derived `η`

## Validation

- [frontier_baryogenesis_taste_scalar_cubic_target.py](./../scripts/frontier_baryogenesis_taste_scalar_cubic_target.py)
- [BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md](./BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md)

Current runner state:

- `frontier_baryogenesis_taste_scalar_cubic_target.py`: expected `PASS>0`,
  `FAIL=0`
