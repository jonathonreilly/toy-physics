# Baryogenesis EWPT/Washout Target Note

**Date:** 2026-04-16
**Status:** bounded/open support target on `main`
**Script:** `scripts/frontier_baryogenesis_ewpt_washout_target.py`

## Safe statement

The current `main` package does not yet compute the electroweak transition,
sphaleron rate, or baryon transport coefficients needed for baryogenesis.

What it **can** now state exactly is the quantitative target that any future
same-surface EWPT/washout computation must hit:

`η_obs = J_CKM * ε_EWPT`

with

- `η_obs = 6.12e-10`
- `J_CKM = 3.331e-5`
- `ε_EWPT = η_obs / J_CKM = 1.837e-5`.

So the remaining baryogenesis gap is no longer a vague missing mechanism. It is
one explicit electroweak efficiency bridge of order `10^-5` sitting on top of
the already-retained weak CP source.

## Role in the package

This note is the quantitative companion to
[BARYOGENESIS_CLOSURE_GATE_NOTE.md](./BARYOGENESIS_CLOSURE_GATE_NOTE.md).

The closure-gate note says what is still missing qualitatively:

- not baryon violation
- not weak CP violation
- only the EWPT / transport bridge

This note says what that missing bridge must do numerically.
The exact flavor-factorized form of that bridge is recorded in
[BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md](./BARYOGENESIS_JARLSKOG_FACTORIZATION_NOTE.md).

The next derivation-side reduction step is now recorded in
[BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md](./BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md).

## Exact input surface

The target uses only quantities already fixed on the current package surface:

1. promoted CKM closure package
2. observed baryon-to-photon ratio `η_obs`
3. standard BBN bookkeeping already used in the bounded cosmology companion

No additional flavor fit or extra model parameter is introduced here.

## Main target

### 1. CKM-source normalization

From the promoted CKM package,

- `|V_us| = 0.22727`
- `|V_cb| = 0.04217`
- `|V_ub| = 0.003913`
- `δ = 65.905°`
- `J = 3.331e-5`.

This gives the already-retained weak CP source scale.

### 2. Required electroweak efficiency

With

`η_obs = 6.12e-10`

the required net electroweak conversion factor is

`ε_EWPT = η_obs / J = 1.837e-5`.

This factor is intentionally agnostic about the detailed microscopic split
between:

- transition strength,
- sphaleron suppression,
- wall transport / diffusion,
- freeze-out timing.

It is the exact missing multiplicative bridge on the current package surface.

### 3. Historical route anchor

The current cosmology route still carries the older bounded target

`v(T_c)/T_c ~ 0.52`

for the taste-scalar electroweak transition.

This note does **not** promote that number to a retained theorem. It records
its honest role:

- it is a historical partial-washout anchor,
- it lies below the textbook strong no-washout benchmark `v/T ~ 1`,
- it remains useful only as a route target for the future same-surface EWPT
  computation.

## Why this matters

This target note upgrades the baryogenesis lane in one specific way:

- before: "η is missing because baryogenesis is open"
- now: "η is missing because one electroweak bridge of size `1.837e-5` has
  not yet been computed on the retained surface"

That is materially tighter. It tells future work exactly what to compute and
what number the result must reproduce.

The finite-`T` reduction note then asks the sharper follow-up question:

> what finite-temperature control ratio does the already-promoted zero-`T`
> package imply before any genuine same-surface EWPT computation is done?

## Relation to cosmology

The bounded cosmology companion already uses

`η -> Ω_b -> R -> Ω_DM -> Ω_m -> Ω_Λ`.

So if a future same-surface EWPT computation produces

`η_pred = J * ε_EWPT_pred`

with `η_pred ≈ 6.12e-10`, the remaining matter-content bridge behind the
bounded `Ω_Λ` lane closes immediately.

## What this closes

This note closes the quantitative targeting question:

> "What exact number must the open baryogenesis computation reproduce?"

Answer:

`ε_EWPT = 1.837e-5`

relative to the already-promoted CKM weak CP source.

## What this does not close

This note does **not** claim:

- a first-principles EWPT effective potential
- a first-principles sphaleron rate
- a first-principles diffusion/transport system
- a derived `η`
- a promoted cosmology closure

## Validation

- [frontier_baryogenesis_ewpt_washout_target.py](./../scripts/frontier_baryogenesis_ewpt_washout_target.py)
- [BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md](./BARYOGENESIS_FINITE_T_REDUCTION_NOTE.md)

Current runner state:

- `frontier_baryogenesis_ewpt_washout_target.py`: expected `PASS>0`, `FAIL=0`
