# Evolving Network Prototype V5 Note

**Date:** 2026-04-04  
**Status:** bounded Gate B prototype, modest improvement over v4 but still mixed

## One-line read

This v5 pass tests a tighter structured-connectivity rule than v4:

- local drift on the same layered 3D grid labels
- narrow cross-shaped fixed-offset connectivity
- KNN recomputed from the same grown positions as the control

The point is to see whether a more explicit structured backbone improves the
Gate B lane beyond the mixed crystal-like v4 result.

## Primary artifact

- Script: [`scripts/evolving_network_prototype_v5.py`](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v5.py)
- Log: [`logs/2026-04-04-evolving-network-prototype-v5.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v5.txt)

## Frozen replay result

The frozen replay lands as a modest but not decisive improvement over v4:

| architecture | toward | mean delta | F~M |
|---|---:|---:|---:|
| ordered lattice | `66.7%` | `+0.000010` | `0.66` |
| cross growth | `77.8%` | `+0.000011` | `0.76` |
| KNN control | `66.7%` | `+0.000012` | `0.66` |

Pairwise read:

- `Δtoward = +0.11` for cross growth vs KNN
- `Δmean_delta = -0.000001` for cross growth vs KNN
- `ΔF~M = +0.09` for cross growth vs KNN

## Safe interpretation

- The fixed-offset cross rule is explicit and reviewable.
- The control is fair: KNN on the same grown positions.
- The structured row improves the toward count and the local F~M slope.
- It does **not** cleanly beat the control on mean delta, so this is not a
  Gate B win.

## What this means for Gate B

This is still useful because it tightens the bottleneck:

- position noise is not the main failure mode
- a narrower structured backbone can beat KNN on the main toward count
- but the full dynamics signal remains mixed, so Gate B is still open

That makes v5 a bounded incremental advance, not a solved dynamics theorem.

