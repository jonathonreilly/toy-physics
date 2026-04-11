# Two-Body Attraction Retained Note

**Date:** 2026-04-11
**Status:** bounded-retained on frontier; not promoted
**Script:** `frontier_two_body_attraction.py`

## What This Script Does

Measures mutual gravitational acceleration between two Gaussian wavepackets
on a Wilson 3D open-BC lattice using SHARED vs SELF_ONLY Hartree subtraction.
The observable is the second time-derivative of packet separation, with
self-gravity contraction cancelled by the subtraction.

## Audited Surface

- **Geometry:** one fixed open cubic lattice, `side=20`
- **Placement:** x-axis centered, one family only
- **Primary separation sweep:** `G=5`
- **Corroborating fixed-distance check:** `G=2` at `d=6`
- **Nonlinear follow-up:** `G=10` enters noisy regime
- **Screening:** `mu^2=0.001` (screening length 31.6 sites)
- **Evolution:** `expm_multiply` (exact unitary, not Crank-Nicolson)
- **Other:** `MASS=0.3`, `WILSON_R=1.0`, `DT=0.08`, `N_STEPS=15`, `SIGMA=1.0`

## Results on This Surface

### `G=5` separation sweep

- **Mutual acceleration sign:** all 25 phase-jitter repeats attractive
  (`5` separations × `5` phase-jitter repeats)
- **Individual CoM:** both packets approach each other in all 25 configs
- **Distance law:** early-time `|<a_mutual>| ~ d^{-1.966}` with `R^2=0.9998`
  on the all-attractive separations only

### `G=2` corroborating check

- fixed-`d=6` follow-up remains attractive on the same surface
- this is corroboration only, not a second full separation-law sweep

## What This Does NOT Establish

1. **Cross-geometry robustness:** the 5 seeds are phase-jitter repeats on ONE
   fixed lattice with ONE placement family. This shows a deterministic signal
   on this surface, not cross-graph robustness.

2. **Both-masses law:** the script uses equal-mass packets only. The earlier
   `frontier_newton_both_masses.py` showed that varying both inertial masses
   produces a `CV=35-38%` normalized impulse and fails action-reaction on
   every grid row. The common Wilson-gap slowdown dominates the
   shared-minus-self residual when both masses vary.

3. **Full Newton closure:** `F ∝ M₁M₂/r²` requires both the distance law
   AND the mass law. The distance law is clean on this surface; the mass law
   is not retained.

4. **Staggered direct-CoM closure:** this is Wilson fermions only. The primary
   staggered architecture already has bounded retained trajectory/force
   companions, but it still does not have a retained direct-CoM
   self-consistent two-body closure.

## Relationship to Prior Wilson Notes

This script supersedes the older `frontier_wilson_two_body_open.py` result
(which gave `|a_mut| ~ d^{-3.4}` at `mu^2=0.22`) by using the corrected
low-screening surface. The exponent softening from -3.4 → -1.97 as μ²
decreases from 0.22 → 0.001 is documented in `WILSON_TWO_BODY_OPEN_NOTE`
and is consistent with the Newton systematic sweep
(`frontier_newton_systematic.py`: mean -1.979±0.008).

The staggered two-body lane (`TWO_BODY_MUTUAL_ATTRACTION_NOTE`) remains
separate: that lane found a narrow periodic resonance window at `mu^2=0`
but no broad mutual-attraction closure. The Wilson open-BC result is
structurally different (open boundaries, Hartree two-orbital, larger lattice).

## Honest Retained Statement

> On the audited open Wilson surface (`side=20`, `G=5`, `mu^2=0.001`),
> two-orbital Hartree dynamics produces a robust mutual attraction channel
> with an early-time `|a_mutual| ~ d^{-1.97}` fit (`R^2=0.9998`) across the
> all-attractive separations. Both packets approach each other, and the signal
> is deterministic across phase-jitter repeats on this fixed surface. This
> result is bounded to one geometry, one placement family, equal masses only,
> and Wilson fermions. The both-masses law remains unresolved.

## What Would Upgrade This

1. Cross-placement sweep (y-axis, diagonal, off-center placements)
2. Cross-size sweep (side=15, 25 on the same low-screening surface)
3. A clean both-masses observable that suppresses the common slowdown mode
4. Staggered reproduction (requires filtering parity oscillation from CoM)
