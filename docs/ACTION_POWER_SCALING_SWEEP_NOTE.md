# Action-Power Scaling Sweep

**Date:** 2026-04-04  
**Status:** bounded fixed-family scaling replay

## Artifact chain

- Script: [`scripts/action_power_scaling_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/action_power_scaling_sweep.py)
- Log: [`logs/2026-04-04-action-power-scaling-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-action-power-scaling-sweep.txt)

This is a bounded replay on one fixed retained family:

- 3D ordered dense lattice
- `h = 0.5`, `W = 10`, `L = 12`
- kernel `1/L^2` with `h^2` measure
- field `s/r`
- action family `S = L(1-f^p)`

## Frozen replay

| p | Born | F∝M | Tail |
|---|------|-----|------|
| 0.50 | `2.18e-15` | `0.50` | `z>=5:-0.78` |
| 0.75 | `2.18e-15` | `0.75` | `z>=4:-0.76` |
| 1.00 | `2.18e-15` | `1.00` | `z>=4:-1.00` |
| 1.50 | `2.18e-15` | `1.50` | `z>=5:-2.20` |
| 2.00 | `2.18e-15` | `2.00` | `z>=5:-3.54` |

All tested rows stay `7/7` TOWARD on the fixed `z = 2..8` window.

## Safe read

- On this fixed family, the mass-scaling law is clean: `F∝M = p` across the
  tested sweep.
- Born stays machine-clean across the whole tested power family.
- The distance tail steepens strongly with `p`.
- The distance-tail law is **not** yet a closed theorem. The replay supports a
  strong monotonic steepening pattern, not a unique exact formula.

## What this does and does not support

This sweep supports:

- a bounded one-parameter family of mass-scaling laws on the fixed ordered
  lattice
- a clean separation between sublinear, linear, and superlinear phase-valley
  couplings on that family

This sweep does **not** support:

- a universal tail theorem across architectures
- a unique exact relation like `-(2p-1)` as a retained project-level law
- a derivation of `p=1` from the current axioms alone

The strongest safe summary is:

- `F∝M = p` is the clean retained fixed-family result
- tail steepening with `p` is real
- the precise tail formula still needs either a derivation or a wider
  cross-family replay before promotion
