# Nearest-Neighbor Lattice Refinement Note

**Date:** 2026-04-03  
**Status:** Born-clean positive refinement trend through `h = 0.25`; `h = 0.125` remains unresolved for the raw kernel

This note freezes the canonical raw nearest-neighbor lattice refinement run.
It is intentionally narrow:

- it does **not** claim a full continuum limit
- it does **not** use fan-out normalization or layer normalization
- it keeps the standard linear propagator only

Artifacts:

- [`scripts/lattice_nn_continuum.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_continuum.py)
- [`logs/2026-04-03-lattice-nn-continuum.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-lattice-nn-continuum.txt)

## Canonical Retained Window

The raw NN lattice is Born-clean through the last successful spacing:

| `h` | nodes | gravity | `k=0` | `MI` | `1-pur` | `d_TV` | Born |
|---|---:|---:|---:|---:|---:|---:|---:|
| `2.0` | `441` | `-0.775486` | `0.00e+00` | `0.5558` | `0.4215` | `0.7498` | `2.88e-16` |
| `1.0` | `1681` | `-0.116678` | `0.00e+00` | `0.5022` | `0.4229` | `0.7455` | `6.02e-16` |
| `0.5` | `6561` | `+0.138226` | `0.00e+00` | `0.7420` | `0.4844` | `0.9072` | `2.26e-16` |
| `0.25` | `25921` | `+0.077415` | `0.00e+00` | `0.9470` | `0.4989` | `0.9878` | `3.83e-16` |

Safe read:

- gravity flips sign and becomes positive by `h = 0.5`
- `MI` rises strongly toward `1` by `h = 0.25`
- `1-pur` rises toward `0.5`
- `d_TV` rises toward `1`
- Born stays at machine precision on the retained window
- `k=0` stays exactly zero

## Unresolved Point

The raw kernel overflows at `h = 0.125` in the canonical run.

That means:

- the refinement trend is real on the retained window
- the next finer point is not yet frozen
- a full continuum claim is not review-safe yet

## Safe Conclusion

The correct wording is:

- the nearest-neighbor lattice shows a **Born-clean positive refinement trend through `h = 0.25`**
- the raw kernel has a **computational resolution limit** at finer spacing
- the continuum question remains open

Do **not** promote this note to a full continuum theorem.
