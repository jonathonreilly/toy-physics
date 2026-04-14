# A1-Background Ratio Scan for the Last Tensor Coefficient Gap

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_a1_background_ratio_scan.py`  
**Status:** bounded positive narrowing

## Purpose

The local two-channel Jacobian note already showed:

- exact bright-channel selection (`E_x`, `T1x`)
- exact dark-channel annihilation
- one remaining mismatch in the bright coefficients after the exact shell
  amplitude law is factored out

This note asks whether that last mismatch is at least organized by one scalar
parameter of the `A1` background, rather than by a generic new tensor law.

## A1 background manifold

On the scalar `A1` support surface, write

- `q_A1(r; Q) = Q * (e0 + r s) / (1 + sqrt(6) r)`

with:

- fixed total charge `Q`
- variable shell-versus-center ratio `r = s / e0`

The runner scans:

- `Q = 1`
- `r in {0.50, 0.75, 1.00, 1.25, 1.50, 1.75}`

and measures the two bright local coefficients of the tensor boundary drive.

## Result

Both bright coefficients vary smoothly and monotonically with the single scalar
ratio `r`.

Representative values:

- `r = 0.50`
  - `beta_E_x = -2.282158833643e-05`
  - `beta_T1x = +3.037549045204e-05`
  - `beta_T1x / (-beta_E_x) = 1.330998088488`
- `r = 1.75`
  - `beta_E_x = -1.908676090523e-05`
  - `beta_T1x = +3.179985108345e-05`
  - `beta_T1x / (-beta_E_x) = 1.666068498544`

So the last coefficient gap is not behaving like an uncontrolled family label.
It is naturally organized by one scalar `A1` background parameter.

## What this changes

Before this note, the sharpest gravity read was:

- one last `A1`-background renormalization law is missing

After this note, that statement becomes more precise:

- the missing law is not a generic functional on the tensor source data
- it is best understood as one scalar renormalization function on the
  `A1` background manifold, i.e. one function of `r = s/e0`

## Current best gravity read

The strongest honest statement now is:

> the remaining full-GR gap on the audited restricted class is no longer a
> generic tensor completion problem. After exact shell-amplitude normalization
> and exact local two-channel selection, the last missing piece is one scalar
> renormalization law on the `A1` background manifold.
