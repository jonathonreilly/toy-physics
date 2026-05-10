# 3+1D Periodic Chiral Sign Windows: Wrap and Recurrence Scale

**Date:** 2026-04-09
**Last sync:** 2026-05-10 — table regenerated from the live runner output and pinned by explicit assertions in the runner (no behavior change to the underlying sweep).
**Status:** bounded — finite-volume periodic-recurrence sweep on the 3+1D
chiral sign windows; the sweep table and ratio observations are exact for
the runner's parameter ranges, but a closed-form recurrence-scale law for
arbitrary `(n, L)` is not derived here

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

The classical and phase-kill columns are identical in this sweep, so they
share a single AWAY column below. Coherent evolution shifts the fine
structure (a few rows that are AWAY classically become TOWARD coherently
and vice versa), but the broad sign-window structure persists in both.

The runner enforces the AWAY-window sets below as explicit `assert` checks.

| n | delta = 3/n | classical / phase-kill AWAY rows, L | classical AWAY in lambda = L/n | coherent AWAY rows, L | coherent AWAY in lambda = L/n |
| --- | --- | --- | --- | --- | --- |
| 15 | 0.2000 | 14, 16, 18 | 0.933, 1.067, 1.200 | 16, 18, 20 | 1.067, 1.200, 1.333 |
| 21 | 0.1429 | 12, 18, 20 | 0.571, 0.857, 0.952 | 12, 28 | 0.571, 1.333 |
| 23 | 0.1304 | 12, 18, 20, 28 | 0.522, 0.783, 0.870, 1.217 | 12, 28 | 0.522, 1.217 |
| 25 | 0.1200 | 20, 28 | 0.800, 1.120 | 14, 28 | 0.560, 1.120 |
| 31 | 0.0968 | 28 | 0.903 | 16, 20 | 0.516, 0.645 |

## Interpretation

The main control parameter is not the raw layer count `L`, but where `L` sits relative to the box size:

1. `delta = 3/n` shrinks from `0.20` to `0.0968` across the sweep, yet the sign windows remain.
2. The stable feature is the wrap fraction `lambda = L/n`, not the physical offset alone.
3. The broad AWAY regions cluster near the first half-wrap (`lambda ~ 0.5`),
   late pre-recurrence (`lambda ~ 0.8-0.95`), and post-recurrence
   (`lambda > 1`) regimes.
4. The `L = 28` point is diagnostic but mode-dependent. Classically it is
   AWAY for `n in {23, 25}` (post-recurrence, `lambda > 1`) and TOWARD for
   `n = 21` (also post-recurrence) and `n = 31` (still pre-recurrence,
   `lambda = 0.903`). Coherently it is AWAY for `n in {21, 23, 25}` and
   TOWARD for `n = 31`. The classical column therefore does not collapse
   onto a single post-recurrence sign on this sweep, even though the
   coherent column does.

So the 3+1D sign problem is best read as a finite-volume wrap/recurrence
effect on a periodic cubic lattice. The geometry-driven bands are present
in both the coherent and classical/phase-kill modes, but the fine
structure (in particular the `L = 28` row) shifts with mode rather than
collapsing to a single recurrence sign.
