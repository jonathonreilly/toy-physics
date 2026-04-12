# 3D Bogoliubov Quench with Spherical Horizon -- Scope and Limitations

**Status:** Gaussian-state lattice calculation. NOT a Hawking radiation claim.

## What this computes

A free-fermion tight-binding model on a 3D cubic lattice (side L = 10-14)
undergoes a sudden quench: hopping amplitude inside a sphere of radius R_h
is reduced, creating a "slow zone" where the effective speed of light is lower.
The Bogoliubov coefficients between the pre-quench and post-quench single-particle
bases determine particle creation in the post-quench vacuum as seen by pre-quench
observers.

This is the correlation-matrix method for free fermions: all observables follow
from the N^3 x N^3 single-particle Hamiltonian. There is no exponential Hilbert
space and no many-body entanglement beyond what the Gaussian state encodes.

## What this is NOT

1. **Not quantum gravity.** There is no dynamical spacetime, no Einstein equations,
   no backreaction. The "horizon" is a hand-placed boundary in a hopping profile.

2. **Not Hawking radiation.** Hawking radiation requires a collapsing geometry that
   forms a trapped surface. A sudden quench on a fixed lattice is an analog model
   at best -- comparable to Unruh's sonic analog, not to actual black hole evaporation.

3. **Not a proof of thermality.** Any sudden quench produces Bogoliubov particles.
   Approximate thermal fits to the mode spectrum may reflect the smooth profile shape
   (a tanh has a natural energy scale) rather than deep physics.

4. **Not continuum physics.** Lattice artifacts (finite bandwidth, discrete modes,
   boundary effects) dominate at the system sizes accessible here. Continuum limits
   would require careful extrapolation.

## What it IS

- A concrete numerical test of whether a spherical quench boundary on a 3D lattice
  produces qualitatively different Bogoliubov spectra than the 1D chain version.
- A check of three analog-Hawking scaling relations:
  - T vs surface gravity (hopping gradient at the horizon)
  - T vs 1/R_h (larger horizon = colder, if the analog holds)
  - Spatial localization of particle creation near the horizon
- A stepping stone: if the lattice calculation shows the right qualitative trends,
  it motivates more careful continuum-limit analysis.

## Relation to the 1D chain result

The 1D script (frontier_hawking_bogoliubov_quench.py) found T proportional to
the hopping gradient with R^2 ~ 0.97. However, a 1D chain has no closed horizon
surface. The 3D version tests whether the spherical geometry introduces the
expected 1/R_h dependence that has no 1D analog.

## Lattice sizes and runtime

| L  | N = L^3 | Approx diag time | Notes              |
|----|---------|-------------------|--------------------|
| 8  | 512     | < 1s              | Null test only     |
| 10 | 1000    | ~1s               | Main quench tests  |
| 12 | 1728    | ~5s               | T vs R_h test      |
| 14 | 2744    | ~30s              | If needed          |

Total runtime for the full test suite: approximately 2-5 minutes depending
on hardware.
