# Experimental Predictions: Graph-Propagator Gravity vs Smooth GR

**Status**: Honest negative result  
**Script**: `scripts/frontier_experimental_predictions.py`  
**Date**: 2026-04-12

## Summary

Three candidate experimental predictions were computed for the discrete
graph-propagator framework: gravitational decoherence, COW neutron
interferometry phase shift, and BMV entanglement generation. All three
produce lattice corrections proportional to (a/L)^2, where a is the graph
spacing and L is the experimental length scale. For a = l_Planck, none are
remotely detectable.

## Candidate 1: Gravitational Decoherence Rate

The Diosi-Penrose prediction for decoherence of a spatial superposition is
tau ~ hbar / (G m^2 / delta_x). On a discrete graph, the gravitational
self-energy acquires a correction from the lattice Green's function:

    gamma_lattice = gamma_DP * [1 + (pi^2/6) * (a/delta_x)^2]

For MAQRO parameters (m = 1e-15 kg, delta_x = 1 um):
- gamma_DP = 0.63 Hz (tau = 1.58 s)
- Lattice fractional correction at a = l_Planck: 4.3e-58
- Required a for 1% detection: a > 78 nm (= 4.8e27 l_Planck)

**Verdict**: Not testable. The correction is 58 orders of magnitude below
experimental sensitivity.

## Candidate 2: Modified COW Phase Shift

In a COW neutron interferometry experiment, the gravitational phase is
Phi = m g H T / hbar. For a uniform gravitational field, the leading
Euler-Maclaurin lattice correction vanishes (d^2f/dz^2 = 0). The
surviving correction from Earth's field curvature gives:

    delta_Phi_systematic = (a^2/12) * (2g/R_earth) * m * T / hbar

For current COW parameters (H = 2 cm, T = 1 ms):
- Continuum phase: 3116 rad
- Lattice fractional correction at a = l_Planck: 3.4e-76
- Required a for detection (precision 1e-3 rad): a > 0.5 m

**Verdict**: Not testable. This is the weakest candidate because the leading
correction vanishes for uniform fields.

## Candidate 3: BMV Entanglement Phase

The BMV experiment tests whether gravity mediates entanglement between two
masses in superposition. The entanglement phase is:

    Phi = G m^2 T / hbar * (1/d_close - 1/d_far)

On a lattice, 1/r picks up a correction: 1/r -> (1/r)[1 + C_lat*(a/r)^2].

For BMV parameters (m = 1e-14 kg, d = 500 um, T = 2 s):
- Continuum phase: 0.105 rad
- Lattice fractional correction at a = l_Planck: 2.7e-63
- Required a for 1% correction: a > 31 um

**Qualitative prediction**: The framework predicts gravity DOES mediate
entanglement (via Bogoliubov mechanism). This is testable by BMV (~2030)
but is shared by all quantum gravity theories. A negative BMV result would
falsify the framework.

## Cross-Cutting Result

All corrections scale as (a/L)^2. The universal bound: for any experiment
with L > 1 nm and a = l_Planck, the fractional correction is below 4.3e-52.

| Experiment | Required a for detection | a / l_Planck |
|---|---|---|
| Decoherence | 78 nm | 4.8e27 |
| COW phase | 0.5 m | 3.1e34 |
| BMV entanglement | 31 um | 1.9e30 |

## Bounded Claims

1. The framework is empirically indistinguishable from smooth weak-field GR
   at all currently accessible experimental scales (assuming a ~ l_Planck).

2. The one testable prediction (gravity mediates entanglement) is qualitative
   and shared by all quantum gravity theories. It distinguishes quantum
   gravity from classical gravity, not lattice gravity from continuum gravity.

3. A null result in any of the three experiments would constrain a to be
   below the "Required a" values above, but these constraints are far weaker
   than existing bounds on spacetime discreteness from other sources
   (gamma-ray dispersion, atomic spectroscopy).

4. To produce a prediction unique to the lattice structure that is
   distinguishable from smooth GR, one needs either a >> l_Planck (already
   constrained) or experiments at the Planck scale (not foreseeable).

## Numerical Verification

The script includes lattice computations on 1D chains (N=400) confirming
that the discrete propagator matches the continuum expectation to machine
precision for separations >> 1 lattice site, with deviations emerging only
at the lattice scale. The decoherence, COW, and BMV lattice-vs-continuum
ratios all converge to 1.000 as the relevant length scale grows.
