# Baryogenesis Finite-`T` Reduction Note

**Date:** 2026-04-16
**Status:** bounded/open finite-temperature reduction note
**Script:** `scripts/frontier_baryogenesis_finite_t_reduction.py`

## Safe statement

Yes, the correct standard for this lane is **derive first, compute second**.

On the current `main` package surface, the right next step is not to pretend a
full nonperturbative electroweak transition computation already exists. It is
to derive the finite-temperature control object from the already-promoted
zero-temperature package, while making the remaining imported thermal ansatz
explicit.

That is what this note does.

## What is derived here

From the promoted `main` package we already have:

- `v = 246.2828 GeV`
- `g_1(v) = 0.464376` in GUT normalization
- `g_2(v) = 0.648031`
- `y_t(v) = 0.9176`
- Higgs routes
  - `m_H(2-loop support) = 119.77 GeV`
  - `m_H(full 3-loop) = 125.10 GeV`

These package values determine the zero-temperature effective parameters:

- the Standard-Model hypercharge coupling `g_Y = sqrt(3/5) g_1`
- the Higgs quartic `λ = m_H^2 / (2 v^2)`

Those are framework-side inputs.

## What remains imported

This note then places those derived package values into the standard textbook
high-temperature one-order-parameter reduction

`V_eff(φ,T) = D (T^2 - T_0^2) φ^2 - E T φ^3 + λ φ^4 / 4`

with the usual one-loop bosonic cubic term.

That thermal reduction is **not** yet derived from the lattice axioms. It is a
bounded imported control ansatz used only to sharpen what the future same-surface
finite-`T` computation must reproduce or avoid.

## Main result

Using the promoted package values, the imported one-doublet gauge-cubic
reduction gives

- `v_c / T_c = 2E / λ`

and lands at:

- `v_c/T_c ≈ 0.160` on the `m_H = 119.77 GeV` support route
- `v_c/T_c ≈ 0.147` on the `m_H = 125.10 GeV` canonical route

So the minimal gauge-cubic finite-temperature reduction undershoots the
historical route anchor

`v(T_c)/T_c ~ 0.52`

by a factor of about `3.2` to `3.5`.

## Consequence

If the older taste-scalar baryogenesis route is real, it cannot come from the
minimal one-doublet gauge cubic alone.

It would require at least one of:

- extra bosonic cubic enhancement from additional taste-scalar structure
- effective quartic suppression near the transition
- a genuinely non-minimal finite-`T` lattice potential not captured by the
  imported one-loop high-`T` reduction

That is already a meaningful derivation-side discriminator.

## Why this is useful

This note turns the vague EWPT task

> "compute the transition somehow"

into the sharper question

> "what same-surface finite-`T` mechanism enhances the minimal gauge-cubic
> control ratio by roughly a factor `3` to `4`?"

That is much closer to a theorem program.

## Derived package values used

The runner uses:

- `v = 246.2828 GeV`
- `g_Y(v) = sqrt(3/5) g_1(v) = 0.3597`
- `g_2(v) = 0.6480`
- `y_t(v) = 0.9176`
- `λ(119.77 GeV) = 0.11825`
- `λ(125.10 GeV) = 0.12901`

## Imported finite-`T` reduction used

The runner uses the standard textbook one-loop high-`T` coefficients:

- `D = (2 m_W^2 + m_Z^2 + 2 m_t^2 + m_H^2) / (8 v^2)`
- `E = (2 m_W^3 + m_Z^3) / (4 π v^3)`
- `v_c / T_c = 2E / λ`

These are explicitly **not** promoted as framework-derived theorems here.

## What this closes

This note closes the next derivation-side question:

> "What does the current promoted zero-temperature package imply for the
> simplest finite-`T` control ratio?"

Answer:

- the minimal gauge-cubic reduction gives `v_c/T_c ≈ 0.15`, not `0.52`
- so the open EWPT route must explain an enhancement of about `3x` to `4x`

## What this does not close

This note does **not** claim:

- a same-surface finite-temperature derivation
- a lattice-derived sphaleron rate
- a lattice-derived transport solution
- a derived `η`

## Validation

- [frontier_baryogenesis_finite_t_reduction.py](./../scripts/frontier_baryogenesis_finite_t_reduction.py)
- [BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md](./BARYOGENESIS_EWPT_WASHOUT_TARGET_NOTE.md)

Current runner state:

- `frontier_baryogenesis_finite_t_reduction.py`: expected `PASS>0`, `FAIL=0`
