# Lensing Adjoint Kernel Reduced Model

**Date:** 2026-04-09
**Status:** retained NEGATIVE (bounded) - the exact edge-level first-order observable is real, but a one-term-per-layer surrogate is far too lossy to explain the retained lensing fingerprint.

## Setup

Reference mechanism target:

> `kubo_true(b) = sum_e c_e / r_e(b)`

with fixed signed edge coefficients `c_e` from the free propagator and
detector adjoint, and all `b` dependence entering through the field
distance factor `r_e(b)`.

Tested bounded reduction:

> `kubo_red(b) = sum_l C_l / r_l(b)`

where each layer keeps:

- one signed coefficient `C_l`
- one effective signed geometry point `(x_l, z_l)`

This is a reduced surrogate only. It is not a derivation.

Run used for the retained check:

- `T_phys = 15`
- `H = 0.35`
- `Fam1`, `seed = 0`
- `drift = 0.20`, `restore = 0.70`
- `beta = 0.8`
- `b in {3, 4, 5, 6}`

Frozen artifact:

- [2026-04-09-lensing-adjoint-kernel-reduced-model-h035.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-09-lensing-adjoint-kernel-reduced-model-h035.txt)

Script:

- [lensing_adjoint_kernel_reduced_model.py](/Users/jonreilly/Projects/Physics/scripts/lensing_adjoint_kernel_reduced_model.py)

## Result

The exact edge replay is correct.

- At `b = 3`, the harness spot-check gives:
  - `true_kubo = +5.972756`
  - `exact_edge = +5.972756`
  - `|Delta| = 4.228e-13`

So the factorization

> `kubo_true(b) = sum_e c_e / r_e(b)`

is not heuristic at this setup. It is an exact replay of the
first-order observable.

The one-term-per-layer reduction fails badly.

| Model | slope | R^2 | mean rel err | max rel err |
| --- | ---: | ---: | ---: | ---: |
| exact_edge | -1.2692 | 0.9366 | 0.00% | 0.00% |
| layer_signed | -0.0782 | 0.4678 | 98.00% | 98.88% |
| layer_abs | -0.8358 | 0.9978 | 100.44% | 100.50% |

Per-point behavior:

- `layer_signed` stays near `+0.06` for all `b`, missing the observed
  scale by almost two orders of magnitude
- `layer_abs` gives the wrong sign and still misses the magnitude by
  about 100%

## Interpretation

This closes the simplest reduced-model mechanism attempt.

What survives:

- the exact edge-level first-order response really does factor into
  fixed coefficients times the field denominator
- all `b` dependence is carried by the sampling of `1 / r_e(b)` against
  those fixed coefficients

What fails:

- compressing each layer to a single signed weight plus one effective
  geometry point
- compressing each layer to a single absolute-geometry point

So the retained mechanism gap is now narrower:

> the `b` law is not just "a broad layer kernel sampled against `1/r`"
> if each layer is reduced to one number and one centroid.

The response remains edge-distributed within layers. Signed cancellation
structure inside a layer matters materially.

## What this does not claim

- not a derivation of the `~ -1.43` reference slope
- not a failure of the exact edge-level factorization
- not an `H = 0.25` result

This is a bounded negative on the first reduced surrogate only.

## Best next move

If this lane continues, the next model has to keep more internal
structure than one centroid per layer. The cheapest plausible upgrade is
either:

1. two-moment per-layer compression
2. coarse `(x,z)` binning of the signed edge coefficients

The exact edge replay stays as the literal reference object.
