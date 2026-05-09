# Edge Deletion Boundary: Gravity Sign Flip

**Date:** 2026-04-04
**Status:** support - structural or confirmatory support note
**Primary runner:** scripts/edge_deletion_boundary_sweep.py

## Result

| Keep fraction | TOWARD | Mean delta |
|---|---|---|
| 100% | 12/12 (100%) | +0.001083 |
| 90% | 11/12 (92%) | +0.000699 |
| **80%** | **5/12 (42%)** | **-0.000049** |
| 70% | 5/12 (42%) | -0.000453 |
| 50% | 2/12 (17%) | -0.000545 |

The gravity sign flips between 90% and 80% edge retention.
At 80%: coin-flip (42% TOWARD). Below 80%: predominantly AWAY.

## Correction

The earlier claim "gravity survives 70% edge deletion" was from
a single seed. The 12-seed sweep shows 70% is AWAY-dominated (42%).

The graph is NOT irrelevant to gravity. Edge connectivity has a
sharp threshold at ~85% retention. Below it, gravity flips.

## Safe wording

"On the tested 3D ordered-lattice family with valley-linear action,
gravitational attraction (TOWARD) requires at least ~85% of the
standard dense-lattice connectivity. Below this threshold, the
gravity sign becomes seed-dependent and predominantly AWAY."
