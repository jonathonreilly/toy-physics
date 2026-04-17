# Symmetry Spectrum Mirror Compare Note

**Date:** 2026-04-03  
**Status:** diagnostic complete, bounded small-N support only

This note records the detector-response singular-spectrum diagnostic for the
mirror families against matched random baselines.

Script:
[`scripts/symmetry_spectrum_mirror_compare.py`](/Users/jonreilly/Projects/Physics/scripts/symmetry_spectrum_mirror_compare.py)

## Question

Does the two-slit detector response retain a near-rank-2 structure, i.e.
two near-degenerate singular directions, long enough to explain the mirror
decoherence result?

The diagnostic uses the 2-column detector response matrix

`R = [psi_A(detectors), psi_B(detectors)]`

with each branch response normalized to unit norm.

## Setup

- `k = 5.0`
- `16` seeds
- `NPL_HALF = 25` for the mirror families (`50` total nodes per layer)
- matched random baselines use the same total per-layer node count
- `N = 15, 25`

## Results

### `N = 15`

| family | dTV | pur_cl | Born | `s2/s1` | eff rank |
|---|---:|---:|---:|---:|---:|
| random-2layer | `0.079±0.024` | `0.971±0.014` | FAIL | `0.092±0.027` | `1.175±0.050` |
| mirror-2layer | `0.029±0.009` | `0.996±0.002` | FAIL | `0.039±0.011` | `1.077±0.022` |
| random-chokepoint | `0.898±0.049` | `0.893±0.044` | `2.92e-16` | `0.889±0.049` | `1.967±0.027` |
| mirror-chokepoint | `0.972±0.012` | `0.577±0.020` | `5.84e-16` | `0.919±0.035` | `1.988±0.006` |

### `N = 25`

| family | dTV | pur_cl | Born | `s2/s1` | eff rank |
|---|---:|---:|---:|---:|---:|
| random-2layer | `0.097±0.031` | `0.962±0.020` | FAIL | `0.135±0.042` | `1.239±0.065` |
| mirror-2layer | `0.081±0.030` | `0.980±0.011` | FAIL | `0.079±0.025` | `1.150±0.046` |
| random-chokepoint | `0.670±0.047` | `0.870±0.044` | `4.61e-16` | `0.636±0.051` | `1.860±0.038` |
| mirror-chokepoint | `0.801±0.070` | `0.733±0.049` | `6.54e-16` | `0.773±0.067` | `1.909±0.057` |

## Narrow Read

- The original mirror family does **not** support a strong near-rank-2 story
  in this diagnostic. Its `s2/s1` is lower than the matched random baseline at
  both tested sizes.
- The mirror-chokepoint family **does** support a near-rank-2 / near-degenerate
  leading-pair story at the retained small-N pocket:
  - `s2/s1` is high and the effective rank is close to `2`
  - it is also Born-clean at machine precision
  - it keeps the strong gravity and decoherence pocket from the retained note
- However, that support is bounded to the small-N pocket. The strict mirror
  chokepoint lane fails at `N >= 40`, so this is not yet a scalable
  rank-protected architecture.

## Interpretation

The review-safe conclusion is:

- **Supported, but bounded:** the mirror-chokepoint pocket at `N = 15, 25`
  really does look like a near-rank-2 symmetry-protected transfer response.
- **Heuristic only:** the original mirror family does not give the same
  support cleanly enough to claim a general symmetry-protected rank story.
- **Not yet scalable:** the rank-2 story is real in the small retained pocket,
  but it has not yet been extended past the `N = 25` chokepoint window.

So the cleanest current statement is:

> Mirror symmetry can produce a genuine near-rank-2 signature, but only in the
> strict chokepoint pocket and only at small `N`. Outside that pocket, the rank
> story is heuristic rather than a retained large-N mechanism.
