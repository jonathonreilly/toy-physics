# Staggered Layered Gauge Engineering Note

**Date:** 2026-04-10  
**Status:** proposed_retained layered-cycle engineering probe

This note freezes the first explicit layered-cycle geometry probe for the
staggered graph lane.

## Question

Can we build a layered bipartite graph with an explicit, well-conditioned loop
structure that produces a native gauge/current win on the same staggered
transport law, without falling back to 1D helpers or proxy rows?

## Harness

- Script:
  [`frontier_staggered_layered_gauge_engineering.py`](../scripts/frontier_staggered_layered_gauge_engineering.py)
- Observable: ground-state persistent-current span over `phi in [0, 2pi]`
- Operator: native staggered Hamiltonian with flux threaded through the
  detected cycle edge
- Retained side battery: Born/linearity, norm, force sign, `F∝M`, achromatic
  force, equivalence, robustness

## Families

- `layered_bipartite_dag_s13_n36`: acyclic control, `gauge=N/A`
- `layered_bipartite_dag_s29_n55`: sparse layered holdout, cycle-bearing but
  weak current
- `layered_brickwall_open`: engineered layered plaquette geometry
- `layered_brickwall_wrap`: engineered layered cylinder geometry

## Exact Results

| Family | n | cycle | Retained | Force | F∝M | Achrom | Equiv | Robust | J span | J resid | Gauge |
|---|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| layered bipartite DAG `s13` | 36 | no | `8/8` | TOWARD | `1.000` | `1.699e-16` | `1.683e-16` | `3/3` | `N/A` | `N/A` | `N/A` |
| layered bipartite DAG `s29` | 55 | yes | `7/8` | TOWARD | `1.000` | `1.126e-16` | `0.000e+00` | `3/3` | `4.769e-06` | `6.748e-20` | FAIL |
| layered brickwall open | 48 | yes | `8/8` | TOWARD | `1.000` | `2.646e-16` | `2.245e-16` | `3/3` | `2.285e-03` | `7.589e-18` | PASS |
| layered brickwall wrap | 48 | yes | `8/8` | TOWARD | `1.000` | `2.223e-16` | `1.023e-16` | `3/3` | `2.157e-03` | `8.674e-19` | PASS |

## Readout

- The acyclic layered DAG control is correctly `N/A` for gauge/current.
- The sparse layered holdout still fails the gauge threshold.
- The engineered layered plaquette geometries close the native gauge/current
  probe cleanly.
- The best current span in this probe comes from `layered_brickwall_open`, and
  the most explicit loop-basis geometry is `layered_brickwall_wrap`.

## Interpretation

- Native gauge/current closure is possible on a layered graph when the loop
  geometry is made explicit and well-conditioned.
- The original sparse layered DAG-like holdout is therefore better treated as a
  negative control for gauge/current, not as a barrier to the staggered
  transport law itself.
- Force remains the primary gravity observable; current is the gauge observable.

