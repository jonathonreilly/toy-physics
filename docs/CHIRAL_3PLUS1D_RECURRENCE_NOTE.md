# 3+1D Periodic Chiral Sign Windows: Wrap and Recurrence Scale

**Date:** 2026-04-09  
**Status:** Diagnosed, not resolved

This note reduces the 3+1D periodic chiral sign windows to dimensionless finite-volume scales. The sweep was run with the periodic architecture in [`scripts/frontier_chiral_3plus1d_decoherence_sweep.py`](../scripts/frontier_chiral_3plus1d_decoherence_sweep.py) using:

`d = 3` source-mass offset, `theta0 = 0.3`, `strength = 5e-4`, and `n in {15, 21, 23, 25, 31}`, `L in {12, 14, 16, 18, 20, 28}`.

## Geometry

Use:

`delta = d / n = 3 / n`

`lambda = L / n`

`w = 2L / n`

Here `lambda ~ 1/2` is the first half-box wrap, and `lambda ~ 1` is the first full recurrence of the periodic box.

The field is built with a minimum-image distance, so the source already couples to its periodic images. The sign windows therefore reflect finite-volume geometry and recurrence, not just a local `1/r` perturbation.

## Observed Windows

Classical and phase-kill agree exactly on the sign pattern in this sweep, so the broad windows survive full decoherence. Coherent evolution adds a few extra narrow AWAY pockets, but it does not remove the main bands.

| n | delta = 3/n | classical / phase-kill AWAY windows, in lambda = L/n | coherent AWAY windows, in lambda = L/n |
| --- | --- | --- | --- |
| 15 | 0.2000 | 0.933, 1.067, 1.200, 1.333 | 1.067, 1.200, 1.333 |
| 21 | 0.1429 | 0.571, 0.857, 0.952, 1.333 | 0.571, 1.333 |
| 23 | 0.1304 | 0.522, 0.783, 0.870, 1.217 | 0.522, 1.217 |
| 25 | 0.1200 | 0.560, 0.800, 1.120 | 0.560, 1.120 |
| 31 | 0.0968 | 0.903 | 0.516, 0.645 |

## Interpretation

The main control parameter is not the raw layer count `L`, but where `L` sits relative to the box size:

1. `delta = 3/n` shrinks from `0.20` to `0.0968` across the sweep, yet the sign windows remain.
2. The stable feature is the wrap fraction `lambda = L/n`, not the physical offset alone.
3. The broad AWAY regions cluster near the first half-wrap (`lambda ~ 0.5`), late pre-recurrence (`lambda ~ 0.8-0.95`), and post-recurrence (`lambda > 1`) regimes.
4. The `L = 28` point is especially diagnostic: for `n = 21, 23, 25` it is already post-recurrence (`lambda > 1`) and remains AWAY in the classical/phase-kill columns, while for `n = 31` it is still pre-recurrence (`lambda = 0.903`) and is TOWARD.

So the 3+1D sign problem is best read as a finite-volume wrap/recurrence effect on a periodic cubic lattice. Coherence changes the fine structure, but the geometry-driven bands survive even after phases are removed.
