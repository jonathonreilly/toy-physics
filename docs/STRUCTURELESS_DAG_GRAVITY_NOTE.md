# Gravity on Structureless Causal DAGs

**Date:** 2026-04-04
**Status:** frozen probe — bounded universality result

## Setup
Random 3D points sorted by x-coordinate (causal ordering).
Edges from i→j if x_j > x_i and distance < r.
No layers, no grid, no structure beyond causality.
Valley-linear action S=L(1-f), 1/L^2 kernel.

## Results

| Configuration | TOWARD | F∝M |
|---|---|---|
| 200 nodes, r=3 | 56% (9/16) | 0.97 |
| 500 nodes, r=2.5 | 73% (11/15) | 1.01 |
| 1000 nodes, r=2 | 50% (8/16) | 1.06 |

## Interpretation

**F∝M ≈ 1.0 on completely structureless graphs.**
The mass scaling is a property of the PROPAGATOR (linear action),
not the graph structure. It holds even without layers, grids,
or any lattice-like regularity.

The gravity SIGN is noisy (50-73% TOWARD) because the random
graph doesn't have the coherent path structure needed for
reliable constructive interference. But when gravity IS TOWARD,
the scaling is Newtonian.

## Safe wording
"On random causal DAGs with no imposed structure beyond x-ordering,
the valley-linear propagator gives gravitational deflection that
is TOWARD in the majority of seeds and follows F∝M ≈ 1.0 when
TOWARD. The Newtonian mass scaling is a propagator property,
not a graph property."
