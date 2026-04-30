# DM Neutrino `v_even` Bosonic Normalization Theorem

**Date:** 2026-04-15  
**Status:** support - structural or confirmatory support note
transfer coefficients  
**Script:** `scripts/frontier_dm_neutrino_veven_bosonic_normalization_theorem.py`

## Framework sentence

In this note, “axiom” means only the single framework axiom `Cl(3)` on `Z^3`.
Everything else is a derived atlas row.

## Question

After the weak even swap-reduction theorem, the exact current even leg is

`[E1, E2]^T = v_even tau_+`

with

- `tau_+ = tau_E + tau_T`
- `v_even = (v_1, v_2)^T`.

Can the coefficient vector `v_even` itself be fixed from the single axiom plus
the current atlas?

## Bottom line

Yes, canonically.

The two exact even channels

- `E1 = delta + rho`
- `E2 = A + b - c - d`

have canonical Frobenius-dual target generators

- `F1 = (1/2) T_delta + (1/4) T_rho`
- `F2 = A_op + (1/4) b_op - (1/2) c_op - (1/2) d_op`.

These are isospectral to scaled copies of the unique traceless row generator
on the exact 2-row weak source factor:

- `F1 <-> sqrt(3/8) Z_row`
- `F2 <-> (3/sqrt(8)) Z_row`

with

`Z_row = diag(1,-1)`.

Under the unique additive CPT-even bosonic source-response generator, this
fixes the even coefficient vector to

`v_even = (sqrt(8/3), sqrt(8)/3)`

on the source-oriented branch convention.

Equivalently:

`E1 = sqrt(8/3) tau_+`

`E2 = (sqrt(8)/3) tau_+`.

## Exact even channel representatives

The active Hermitian basis entering these channels is Frobenius-orthogonal:

- `A_op`
- `b_op`
- `c_op`
- `d_op`
- `T_delta`
- `T_rho`.

So the exact Riesz/Frobenius dual representatives of the two scalar channels
are:

`F1 = (1/2) T_delta + (1/4) T_rho`

because

`<H, F1>_F = delta + rho = E1`,

and

`F2 = A_op + (1/4) b_op - (1/2) c_op - (1/2) d_op`

because

`<H, F2>_F = A + b - c - d = E2`.

So the even channels are not just coordinate names. They are exact scalar
observables with canonical target generators.

## Exact source-side row factor

The weak even swap-reduction theorem already proved that the exact current
source carrier factors through the symmetric source combination

`tau_+ = tau_E + tau_T`

and that the live source geometry is the exact 2-row factor of

`K_R(q) = [1, delta_A1(q)]^T [u_E(q), u_T(q)]`.

On that exact row factor, the unique traceless Hermitian generator is

`Z_row = diag(1,-1)`.

So the single-axiom source side now offers one exact canonical even generator.

## Spectral match

The target generators have exact spectra:

- `spec(F1) = {-sqrt(3/8), 0, +sqrt(3/8)}`
- `spec(F2) = {-3/sqrt(8), 0, +3/sqrt(8)}`.

The source row generator has

- `spec(Z_row) = {-1, +1}`.

Therefore:

- `F1` is isospectral to `sqrt(3/8) Z_row`
- `F2` is isospectral to `(3/sqrt(8)) Z_row`

up to the same null-multiplicity issue already handled in the `c_odd`
theorem.

## Bosonic normalization law

Let

`W[J] = log|det(D+J)| - log|det D|`

be the unique additive CPT-even scalar generator.

Then on scalar baselines:

- `F1` and `sqrt(3/8) Z_row` have the same exact bosonic source-response
- `F2` and `(3/sqrt(8)) Z_row` have the same exact bosonic source-response.

So the scalar source amplitude `tau_+` is related to the channel amplitudes by

`sqrt(3/8) E1 = tau_+`

`(3/sqrt(8)) E2 = tau_+`.

Hence

`E1 = sqrt(8/3) tau_+`

`E2 = (sqrt(8)/3) tau_+`.

This is exactly

`v_even = (sqrt(8/3), sqrt(8)/3)`.

## What this closes

This closes the even transfer coefficients.

The branch can no longer honestly say:

- “the odd coefficient is closed, but the even coefficient vector is still open”

The sharper statement is:

- the odd coefficient is closed: `c_odd = +1`
- the even coefficient vector is closed:
  `v_even = (sqrt(8/3), sqrt(8)/3)`

So the transfer coefficients are now fully fixed on the current exact
single-axiom transfer bundle.

## What this does not close

This note does **not** derive:

- the selector amplitude `a_sel`
- the symmetric weak source amplitude `tau_+`
- the full leptogenesis benchmark after rewriting the kernel in terms of the
  exact transfer law

So this is a coefficient-normalization theorem, not yet a full benchmark
rebuild theorem.

## Benchmark consequence

The benchmark remains

- `eta = 1.81e-10`
- `eta / eta_obs ~= 0.30`

for a precise reason: the current benchmark runner still uses the older reduced
kernel. This theorem closes the transfer coefficients, not yet the source
amplitude law or the full rewritten kernel.

## Command

```bash
python3 scripts/frontier_dm_neutrino_veven_bosonic_normalization_theorem.py
```
