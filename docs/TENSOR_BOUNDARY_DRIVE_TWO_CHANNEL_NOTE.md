# Two-Channel Law for the Tensor Boundary Drive

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_boundary_drive_two_channel.py`  
**Status:** exact/bounded positive narrowing on the exact star-supported source class

## Purpose

The previous tensor-support notes reduced the remaining microscopic source law
to two aligned bright source directions:

- an aligned quadrupole channel `E_x`
- an aligned shift channel `T1x`

Those results were phrased using the derived ratio

- `c_eta = eta_floor_tf / |I_scalar|`

This note sharpens the frontier by moving one level closer to the tensor lift
itself. The primary observable is now the tensor boundary drive

- `eta_floor_tf`

rather than the derived ratio `c_eta`.

## Setup

On the exact seven-site star support, decompose the support source into the
adapted basis

- `A1(center) ⊕ A1(shell) ⊕ E1 ⊕ E2 ⊕ T1x ⊕ T1y ⊕ T1z`

and define the aligned/orthogonal `E` directions

- `E_x = (sqrt(3) E1 + E2) / 2`
- `E_perp = (-E1 + sqrt(3) E2) / 2`

The runner fixes the scalar `A1` support sector and probes the non-scalar
directions at amplitudes `0.02`, `0.05`, `0.10`.

The baseline scalar-sector values are:

- `eta_floor_tf = 4.581254153227e-03`
- `I_scalar = -1.373250680187`
- `c_eta = 3.336065453544e-03`

## Exact irrep isotropy of the scalar action

The scalar action does not distinguish directions within the same support irrep:

- `max |dI(E_x) - dI(E_perp)| = 4.441e-16`
- `max |dI(T1x) - dI(T1y)| = 2.220e-16`
- `max |dI(T1x) - dI(T1z)| = 2.220e-16`

So the scalar denominator in `c_eta` is already exactly irrep-isotropic on the
audited exact source class.

## Bright/dark structure of the tensor boundary drive

The tensor boundary drive `eta_floor_tf` is not irrep-isotropic. It is bright
only on the aligned channels `E_x` and `T1x`.

Representative values at amplitude `0.10`:

- `d eta_floor_tf(E_x) = -1.845401009408e-05`
- `d eta_floor_tf(E_perp) = -6.580967715220e-11`
- `d eta_floor_tf(T1x) = +3.079285105345e-05`
- `d eta_floor_tf(T1y) = -5.473297397945e-08`
- `d eta_floor_tf(T1z) = -5.473299005167e-08`

So the current tensor lift is already effectively two-channel at the level of
the boundary drive itself:

- one aligned quadrupole channel `E_x`
- one aligned shift channel `T1x`

with the orthogonal `E` and transverse `T1` directions numerically dark.

## Near-affine bright-channel response

The bright-channel response of `eta_floor_tf` is already close to affine in the
tested amplitude window:

- `beta_E_x = -1.846980757627e-04`
- `beta_T1x = +3.076797305061e-04`

Fit quality:

- `E_x` max residual `2.455e-08`, slope variation `5.596e-03`
- `T1x` max residual `3.866e-08`, slope variation `5.339e-03`

So the remaining gravity frontier is no longer best phrased as a generic tensor
completion law for `c_eta`. It is more cleanly phrased as a two-channel law for
the tensor boundary drive `eta_floor_tf`.

## What this changes

Before this note, the sharpest open target was:

- derive the exact transfer coefficients for the aligned channels `E_x` and
  `T1x` into the tensor boundary drive

After this note, that statement becomes more precise:

- the scalar action is already exact and irrep-isotropic
- the open problem sits entirely in the numerator
- the remaining theorem target is therefore:
  - derive the exact `E_x` and `T1x` transfer law for `eta_floor_tf`
  - then recover `c_eta` as a derived ratio

## Current best gravity read

The strongest honest statement now is:

> on the exact star-supported source class, the scalar action is exactly
> irrep-isotropic, while the tensor boundary drive `eta_floor_tf` is a
> two-channel bright observable of the aligned support-irrep directions `E_x`
> and `T1x`, with bounded affine response in the tested amplitude window.

This still does **not** close full nonlinear GR. But it reduces the remaining
microscopic tensor-lift law to the smallest concrete object seen so far:

- one exact scalar denominator
- one two-channel tensor numerator
