# Tensor Drive Reduces to Two Aligned Source Channels

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_support_irrep_selectivity.py`  
**Status:** bounded positive narrowing on the exact star-supported source class

## Purpose

The support-irrep channel scan already showed that the remaining tensor-drive
coefficient is naturally organized in support-irrep coordinates:

- `E` lowers `c_eta`
- `T1` raises `c_eta`

This note asks the sharper question:

> do all directions inside those irreps really matter, or does the current
> tensor orientation only see a smaller aligned channel set?

## Aligned `E` and `T1` channels

On the seven-site star support, define:

- the aligned `E` quadrupole direction
  `E_x = (sqrt(3) E1 + E2) / 2`
- the orthogonal `E` direction
  `E_perp = (-E1 + sqrt(3) E2) / 2`
- the three `T1` directions
  `T1x`, `T1y`, `T1z`

The runner holds the scalar `A1` support sector fixed and probes those
non-scalar channels at equal amplitudes.

## Response pattern

At amplitudes `0.02`, `0.05`, `0.10`:

- `E_x` gives a real negative shift in `c_eta`
- `T1x` gives a real positive shift in `c_eta`
- `E_perp` is dark to numerical precision
- `T1y`, `T1z` are dark to numerical precision

Representative values:

- `amp = 0.10`
  - `dE_x = -1.344148401856e-05`
  - `dE_perp = -3.350484714757e-09`
  - `dT1x = +2.237563218605e-05`
  - `dT1y = -8.723375982504e-08`
  - `dT1z = -8.723377152792e-08`

So the current tensor-drive observable is already effectively two-channel on
the audited exact source class.

## Nearly linear channel response

The aligned channels are also nearly linear in amplitude:

- aligned-`E_x` slope variation: `5.400716e-03`
- aligned-`T1x` slope variation: `3.627463e-03`

So the support-irrep organization is not just qualitative. It is already close
to an affine transfer law in these aligned source coordinates.

## What this changes

Before this note, the remaining gravity target was:

- derive the exact `E` and `T1` transfer coefficients into the tensor boundary
  drive

After this note, the target is sharper:

- derive the exact transfer coefficients for the aligned channels
  `E_x` and `T1x`

That is a more precise and smaller theorem target.

## Current best gravity read

The strongest honest statement now is:

> on the exact star-supported source class, the remaining tensor-drive law is
> effectively two-channel in the current orientation: one aligned quadrupole
> `E_x` channel and one aligned shift `T1x` channel. The orthogonal `E` and
> transverse `T1` directions are dark to numerical precision.

This still does **not** close full nonlinear GR. But it cuts the remaining
microscopic source law down to the smallest concrete channel set seen so far.
