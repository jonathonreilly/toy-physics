# 3+1D Chiral Mixing Period Note

**Date:** 2026-04-09  
**Status:** Diagnosed, not universal
**Claim type:** bounded_theorem

## Summary

The 3+1D periodic chiral sign windows live on the local coin-mixing timescale, but they are not explained by a single fixed `pi/theta0` alias.

The bad windows move with lattice size `n`, and the same windows survive in the classical and phase-kill limits. That means the sign problem is encoded in the local coin + shift dynamics, not only in coherent phase interference.

## Evidence

- Ran [scripts/frontier_chiral_3plus1d_decoherence_sweep.py](../scripts/frontier_chiral_3plus1d_decoherence_sweep.py) with `theta0=0.3`, `strength=5e-4`, `n in {15,21,23,25,31}`, and `L in {12,14,16,18,20,28}`.
- Coherent AWAY windows were size-dependent:
  - `n=15`: `L=16,18,20`
  - `n=21`: `L=12,28`
  - `n=23`: `L=12,28`
  - `n=25`: `L=14,28`
  - `n=31`: `L=16,20`
- Classical and phase-kill columns were identical, and both kept AWAY windows. Decoherence does not remove the sign windows on this periodic architecture.
- The flat mixing period is `pi/theta0 = 10.4719755` layers.
- The field-shifted local angle is only slightly smaller:
  - source site: `theta_eff = 0.29995161`, period `10.473665`
  - mass site: `theta_eff = 0.29850000`, period `10.524599`
  - the full field shift changes the local period by only `0.0526` layers at the mass, far too small to explain the observed multi-layer window drift.
- A simple phase model `sign ~ sin(2 L theta0 + phi)` only partially fits the coherent signs, and the best `phi` changes with `n`:
  - `n=15`: best match `5/6`, `phi ≈ 0.000`
  - `n=21`: best match `4/6`, `phi ≈ 2.969`
  - `n=23`: best match `4/6`, `phi ≈ 2.969`
  - `n=25`: best match `5/6`, `phi ≈ 1.769`
  - `n=31`: best match `4/6`, `phi ≈ 0.000`

## Interpretation

The local coin angle sets the resonance scale, but the periodic lattice supplies an additional size-dependent phase offset. The observed bad windows are therefore better described as geometry-shifted mixing resonances than as a universal `pi/theta0` rule or a field-only phase shift.

The field-coupled `theta_eff` matters, but only as a small perturbation on top of the periodic wrap/return geometry. The sign windows are real, but they are not pinned by `theta0` alone.

## Bottom Line

The 3+1D periodic chiral walk has genuine sign windows on the local mixing period, but the bad windows are not fixed by `pi/theta0` and are not removed by classicalization. They track a size-dependent resonance phase that the periodic geometry introduces, with only a minor correction from the field-shifted mixing angle.

## Registered runner artifacts

The n/L decoherence sweep has a live runner in-tree. The separate
predictive recurrence/phase-offset law remains open:

- Live runner: `scripts/frontier_chiral_3plus1d_decoherence_sweep.py`
  (registered as the runner path for this CID).
- Runner cache: `logs/runner-cache/frontier_chiral_3plus1d_decoherence_sweep.txt`
  (registered cached stdout; exit_code=0, status=ok).

The remaining item is structural rather than registration: a predictive
recurrence/phase-offset law across lattice sizes is not derived here. The
bounded read above stays as a geometry-dependent resonance boundary, not a
closed period theorem.
