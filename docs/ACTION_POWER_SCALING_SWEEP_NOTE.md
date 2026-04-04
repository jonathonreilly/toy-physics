# Action Power Scaling Sweep Note

**Date:** 2026-04-04  
**Status:** bounded fixed-family sweep on the retained 3D ordered-lattice valley family

## Artifact chain

- Script: [`scripts/action_power_scaling_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/action_power_scaling_sweep.py)
- Log: [`logs/2026-04-04-action-power-scaling-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-action-power-scaling-sweep.txt)

This is a bounded replay on one fixed family:

- 3D ordered dense lattice
- `h = 0.5`, `W = 10`, `L = 12`
- kernel `1/L^2` with `h^2` measure
- field `f = s / r`
- action family `S = L(1-f^p)`

## Frozen replay

| `p` | `F~M` | Distance tail | Read |
|---|---:|---:|---|
| `0.50` | `0.50` | `z>=5: -0.78` | sub-linear valley branch |
| `0.75` | `0.75` | `z>=4: -0.76` | sub-linear valley branch |
| `1.00` | `1.00` | `z>=4: -1.00` | Newtonian-like row on this family |
| `1.50` | `1.50` | `z>=5: -2.20` | super-Newtonian row |
| `2.00` | `2.00` | `z>=5: -3.54` | steeper super-Newtonian row |

Born stays machine-clean (`2.18e-15`) for every tested power.
All tested valley powers stay `7/7` TOWARD on the measured `z=2..8` window.

## Safe interpretation

The strongest retained claim from this sweep is:

- on this fixed family, the mass-scaling exponent tracks the weak-field power
  `p` in the action: `F~M = p`

The distance-tail behavior is also systematic, but the safest wording is
weaker:

- on this fixed family, the tail steepens as `p` increases
- `p = 1` gives a Newtonian-like `1/b` row on this family
- the broader tail law is empirical and approximate here, not a universal
  theorem

## What this does not prove

- It does **not** prove a universal distance-law formula across graph families.
- It does **not** prove that `-(2p-1)` is exact on the retained family.
- It does **not** settle the irregular-geometry / spent-delay lane.
- It does **not** derive the action power uniquely from the axioms.

## Bottom line

This sweep strengthens the action-law story, but in a bounded way:

- `F~M = p` is now artifact-backed on one retained ordered-lattice family
- the distance tail clearly responds to `p`, but the exact tail formula
  remains a family-level empirical fit rather than a theorem
