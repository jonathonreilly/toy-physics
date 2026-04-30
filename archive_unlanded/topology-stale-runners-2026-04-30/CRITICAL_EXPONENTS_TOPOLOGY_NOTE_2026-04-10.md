# Critical Exponents vs Topology

**Date:** 2026-04-10
**Status:** proposed_retained finite-size scout
**Script:** `frontier_critical_exponents.py`

## Question

Does the self-gravity localization onset show the same fitted exponent on all
admissible graph families, or does the exponent depend on topology?

## Probe

- Evolve staggered self-gravity on representative admissible graph families.
- Use the order parameter `op(G) = max(0, 1 - width_self / width_free)`.
- Fit the onset branch to `op(G) ~ A * (G - G_crit)^beta`.

This is a **finite-size onset characterization**, not a universal critical-law
proof.

## Current outputs

| Family label | Base family | n | G_crit | beta | R² | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `random_geometric_s8` | random geometric | 64 | 18.0 | 0.1744 | 0.8506 | fit |
| `random_geometric_s10` | random geometric | 100 | 10.0 | 0.4600 | 0.9700 | fit |
| `growing_n64` | growing | 64 | 50.0 | 0.6453 | 0.9759 | fit |
| `layered_cycle_8x8` | layered cycle | 64 | 24.0 | 0.1315 | 0.8086 | fit |
| `causal_dag_10x6` | causal DAG | 55 | 28.0 | 0.0769 | 0.9403 | fit |
| `causal_dag_8x8` | causal DAG | 57 | `1.0` | `nan` | `nan` | degenerate |

## Honest reading

- The fitted `beta` values vary substantially across admissible graph families.
- That is evidence for **topology-dependent finite-size onset behavior**.
- It is **not yet** evidence for a new universality class in the strong sense,
  because:
  - the fits are still finite-size and single-geometry representatives
  - one DAG configuration is degenerate
  - there is no proper finite-size scaling collapse yet

## What this closes

- The project no longer needs to assume mean-field exponents by default.
- There is now a concrete, script-backed reason to treat topology as an active
  variable in the localization transition.

## What remains open

1. finite-size scaling on each family, not just one representative graph
2. multi-seed robustness
3. holdout graph families
4. an order parameter that remains clean on both cycle-bearing and DAG-like
   families
