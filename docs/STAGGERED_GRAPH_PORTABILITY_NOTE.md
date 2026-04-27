# Staggered Graph Portability Note

**Status:** proposed_retained portability probe

This note freezes the first portability run for the staggered / Kahler-Dirac
lane on non-cubic graph families with the corrected parity-coupled scalar
potential.

## Question

Does staggered transport plus potential gravity survive on:

- bipartite random geometric graphs
- bipartite growing graphs
- layered bipartite DAG-compatible graphs

## Harness

- Script: [`frontier_staggered_graph_portability.py`](../scripts/frontier_staggered_graph_portability.py)
- Battery: Born/linearity, norm, force sign, `F∝M`, achromatic force,
  equivalence, robustness, gauge if cycles exist

## First Retained Run

| Family | n | Born/linearity | norm | force | F∝M | achrom CV | equiv CV | robust | gauge |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bipartite random geometric | 36 | `5.69e-16` | `4.44e-16` | `+3.645e-03` TOWARD | `1.000` | `1.505e-16` | `1.748e-16` | `3/3` | `5.142e-03` PASS |
| bipartite growing | 48 | `5.23e-16` | `9.99e-16` | `+3.647e-03` TOWARD | `1.000` | `1.764e-16` | `2.256e-16` | `3/3` | `9.054e-03` PASS |
| layered bipartite DAG-compatible | 36 | `5.67e-16` | `0.00e+00` | `+3.790e-03` TOWARD | `1.000` | `0.000e+00` | `6.865e-17` | `3/3` | `N/A` |

## Readout

- The retained staggered force battery survives on all three graph families.
- Gauge response appears on the cycle-bearing families and is skipped on the
  DAG-compatible family.
- Force is the primary gravity observable here; centroid-based checks are not
  part of this portability probe.

## Caveat

This is a portability checkpoint, not a new canonical card. The next question is
whether the same mechanism survives larger, less regular graphs and then admits
backreaction.
