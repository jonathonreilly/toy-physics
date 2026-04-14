# Local Two-Channel Jacobian and the Remaining Background-Normalization Gap

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_local_two_channel_jacobian.py`  
**Status:** exact/bounded narrowing; exact local channel law, exact obstruction to closure from the current retained shell stack alone

## Purpose

The previous tensor notes reduced the remaining gravity gap to two aligned
source channels in the current tensor orientation:

- `E_x`
- `T1x`

The next honest question is whether that already closes the tensor transfer on
the retained stack, or whether one more microscopic coefficient law is still
missing.

This note works directly around the scalar `A1` baselines of the two audited
restricted families:

- exact local `O_h`
- finite-rank

and studies the local Jacobian of the tensor boundary drive `eta_floor_tf`.

## Exact local channel structure

On both audited `A1` baselines, the centered local Jacobian is already
two-channel:

- `beta(E_x)` is nonzero
- `beta(T1x)` is nonzero
- `beta(E_perp)`, `beta(T1y)`, `beta(T1z)` vanish to numerical precision

So the open gravity gap is no longer channel selection.

It is already exact locally that the tensor boundary drive sees only:

- one aligned quadrupole direction
- one aligned shift direction

## Stable bright coefficients

The bright coefficients are stable across the audited epsilon window
`eps = 0.0025, 0.005, 0.01`.

### Exact local `O_h` A1 baseline

- `beta_E_x = -4.905638666959e-05`
- `beta_T1x = +6.930845030727e-05`

### Finite-rank A1 baseline

- `beta_E_x = -1.858381249251e-04`
- `beta_T1x = +3.058844111459e-04`

So there is a real local response law, not just a coarse finite-amplitude fit.

## What the retained shell law does and does not fix

The retained reduced-shell toolbox already fixes the exact anisotropic shell
amplitude scale

- `A_aniso = c_aniso * Q`

with one exact lattice constant `c_aniso`.

Normalizing the local bright coefficients by that exact amplitude materially
narrows the family mismatch:

- raw relative difference in `beta_E_x`: `2.788791e+00`
- raw relative difference in `beta_T1x`: `3.413320e+00`
- `A_aniso`-normalized relative difference in `gamma_E = beta_E_x / A_aniso`:
  `1.051230e-01`
- `A_aniso`-normalized relative difference in `gamma_T = beta_T1x / A_aniso`:
  `4.270730e-02`

So the retained shell law is clearly relevant. But it still does **not** close
the bright coefficients exactly across the two audited `A1` baselines.

## Exact remaining obstruction

This gives the new exact obstruction:

> the current retained shell toolbox fixes the local bright-channel selection
> exactly and materially narrows the coefficient mismatch via the exact shell
> amplitude `A_aniso`, but it still does not determine the two bright local
> transfer coefficients exactly across the audited scalar `A1` baselines.

So the remaining full-GR gap is now even smaller than before:

- not generic tensor completion
- not generic `E ⊕ T1`
- not even generic aligned two-channel selection
- but one last **A1-background renormalization law** for the local bright
  coefficients of `eta_floor_tf`

## Current best gravity read

The strongest honest statement now is:

> around the retained scalar `A1` surface, the local tensor-boundary-drive law
> is exactly two-channel in the aligned source directions `E_x` and `T1x`.
> The remaining open piece is one background-renormalization law for their
> coefficients; the exact reduced shell amplitude law narrows that mismatch but
> does not yet fix it.
