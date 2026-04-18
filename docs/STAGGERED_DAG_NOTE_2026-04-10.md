# Staggered Fermion on Layered DAG-Derived Family — Bounded Note

**Date:** 2026-04-10  
**Script:** `frontier_staggered_dag.py`

## Summary

This bounded sibling probe tests whether the staggered force-first lane
survives on a layered acyclic template derived from a causal DAG construction,
rather than only on periodic lattices or undirected cycle-bearing graph
families.

The graph family is intentionally narrow:

- layered acyclic template
- bipartite by layer parity
- nearest-layer forward geometry
- force as the gravity observable
- symmetrized Hermitian transport on the induced layered adjacency

The probe closes `6/6` on three layered configurations under the corrected
parity-coupled attractive sign:

- `(8 layers, width 5)` -> `36` nodes
- `(12 layers, width 4)` -> `45` nodes
- `(6 layers, width 8)` -> `41` nodes

## Battery

| Row | 36-node DAG | 45-node DAG | 41-node DAG |
|---|---:|---:|---:|
| D1 Force TOWARD | `+6.91e-05` | `+2.75e-05` | `+1.25e-04` |
| D2 N-stability | `14/14` | `14/14` | `14/14` |
| D3 Norm | `4.44e-16` | `6.66e-16` | `2.22e-16` |
| D4 Born | `7.81e-16` | `7.73e-16` | `8.92e-16` |
| D5 Forward-depth fraction | `0.1266` | `0.1266` | `0.1266` |
| D6 State families | `3/3` | `3/3` | `3/3` |
| **Score** | **6/6** | **6/6** | **6/6** |

State families tested:

- Gaussian
- color-0
- color-1

## What This Closes

- the staggered structural interaction battery is compatible with layered
  acyclic ordering as a geometry/control surface
- bipartite structure can come from layer parity rather than cubic coordinates
- exact norm and machine-zero linearity survive the layered-template transport
- the retained inward proxy response survives across the tested family set

## What This Does Not Yet Claim

- this is **not** a re-scored replacement for the frozen `29/38` 1D and `28/38`
  3D periodic-lattice full-suite baseline
- it is **not** a proof of genuinely directed-Hamiltonian DAG transport, because
  the live runner symmetrizes the layered adjacency
- it does not add native gauge/current on the acyclic DAG itself
- it does not yet show self-gravity or two-field wave closure on the DAG family

## Bounded Read

The important result is narrower compatibility, not score inflation:

> the staggered force-first lane is not confined to periodic cubic lattices; it
> survives a narrow layered acyclic template with forward-depth bias,
> machine-clean norm/Born, and stable inward proxy response under the prescribed
> attractive sign, even though the live transport operator is still symmetrized
> rather than truly directed.
