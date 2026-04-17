# Staggered Backreaction Green-Closure Note

**Date:** 2026-04-10  
**Status:** retained narrow positive

## Question

Can a genuinely nonlocal graph-native Green map close the endogenous-field
force-scale gap on the retained cycle-bearing bipartite families, while still
transferring to one layered holdout and preserving the retained force battery?

## Harness

- Script:
  [`frontier_staggered_backreaction_green_closure.py`](../scripts/frontier_staggered_backreaction_green_closure.py)
- Families:
  - bipartite random geometric, `n=36`
  - bipartite growing, `n=48`
  - layered bipartite DAG-compatible, `n=36` holdout
- Observable:
  - force `F = < -dPhi/dd >`
- Retained checks:
  - zero-source exactness
  - source-response linearity
  - two-body additivity
  - inward retained proxy sign under the prescribed attractive coupling
  - norm stability
- Frozen field maps:
  - `screened_poisson` baseline
  - `geodesic_yukawa(mu=1.50, eps=0.10)`
  - `resistance_yukawa(mu=1.50, eps=0.10)`

## Exact Results

### Holdout-Aware Winner

The promoted graph-native map is `resistance_yukawa`.

- cycle-bearing mean gap, raw: `9.889e-02`
- cycle-bearing mean gap, fitted: `9.688e-02`
- layered holdout gap, raw: `1.680e-02`
- layered holdout gap, fitted: `3.714e-03`
- cycle-only fitted gain: `0.980`

Against the screened graph-Poisson baseline:

- baseline cycle-bearing mean gap: `8.899e-01`
- baseline layered holdout gap: `8.759e-01`
- raw cycle-bearing improvement factor: `9.00x`
- raw holdout improvement factor: `52.13x`

### Frozen Comparison

| Mapping | Gain | Raw cycle gap | Cal cycle gap | Raw holdout gap | Cal holdout gap |
|---|---:|---:|---:|---:|---:|
| `resistance_yukawa` | `0.980` | `9.889e-02` | `9.688e-02` | `1.680e-02` | `3.714e-03` |
| `geodesic_yukawa` | `0.958` | `1.004e-01` | `9.605e-02` | `2.267e-02` | `2.103e-02` |
| `screened_poisson` | `9.476` | `8.899e-01` | `1.358e-01` | `8.759e-01` | `1.809e-01` |

### Retained Checks

For the promoted `resistance_yukawa` map:

- source-response `R²` min / mean: `0.9978 / 0.9989`
- two-body residual max: `3.063e-16`
- minimum inward proxy count: `3/3`
- norm drift max: `7.772e-16`

Family-level calibrated gaps:

- bipartite random geometric: `1.322e-01`
- bipartite growing: `6.151e-02`
- layered holdout: `3.714e-03`

## Readout

- The scale blocker is not just a missing Poisson normalization.
- A direct nonlocal Green map closes the force scale on the retained
  cycle-bearing families by nearly an order of magnitude.
- That closure transfers cleanly to the layered holdout; unlike the earlier
  gain-only closure, the holdout does not blow up.
- The fitted gain sits near `1`, so the promoted map is already close to the
  correct force scale before any cycle-only calibration.

## Interpretation

- The retained structural interaction battery survives the promoted nonlocal
  field map.
- Effective-resistance distance is the cleanest graph-native metric in this
  frozen comparison.
- The next open seam is no longer the raw source-to-field scale on this small
  retained set. It is self-consistent endogenous refresh:
  the promoted cycle-bearing mean self-gap is still `1.036e+00`.

## Next Step

- Keep `resistance_yukawa` as the source-sector closure baseline for this
  staggered graph lane.
- Attack the one-step self-refresh gap directly, rather than reopening local
  source-preconditioner sweeps.
