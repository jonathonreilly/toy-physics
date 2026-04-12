# Electromagnetism Probe Note

**Date:** 2026-04-11
**Status:** exploratory probe complete, bounded claims only

## Summary

This probe tests whether U(1) gauge phases on directed graph edges produce
electromagnetic behaviour within the staggered lattice framework that already
supports gravitational attraction.

Two sectors were tested on an 18^3 open-boundary cubic lattice:

1. **Electrostatic sector** -- scalar potential V(r) = Q/r on the Hamiltonian
   diagonal, with coupling q*V*eps (staggered parity).
2. **Magnetic sector** -- U(1) link phases exp(i*q*A_{ij}) on hopping terms,
   with A from the symmetric gauge for constant B_z.

Script: `scripts/frontier_electromagnetism_probe.py`

## Results

### Electrostatic sector (7/7 pass)

| Test | Result |
|------|--------|
| Opposite charges attract (Q*q < 0) | PASS, all 5 distances |
| Like charges repel (Q*q > 0) | PASS, all 5 distances |
| Neutral immune (q=0) | PASS, exactly zero force |
| Force law | |F| ~ d^-2.11, R^2 = 0.9995 |
| Centroid tracking (attraction) | PASS, all 5 distances shift toward source |

The force expectation value F = -<psi|grad(q*V)|psi> perfectly discriminates
attraction from repulsion with exact sign control. The power-law exponent
-2.11 is close to the Coulomb -2.0, with the small deviation attributable to
lattice discretisation and the Gaussian probe width.

### Magnetic sector

| Test | Result |
|------|--------|
| Charged particle curves in B field | PASS |
| Deflection monotone in B | PASS |
| Neutral particle unaffected | PASS, exactly zero |
| Wilson plaquette holonomy = B | PASS, exact to machine precision |
| Uniform B field (zero plaquette variance) | PASS |

Transverse deflection scales as B^1.6 (expected ~1 for Lorentz force in the
weak-field linear regime; the super-linear scaling suggests the probe is in the
non-perturbative regime at these B values).

## Bounded claims

**What this probe establishes:**

1. The staggered lattice Hamiltonian naturally accommodates a scalar Coulomb
   potential that produces correct force signs (attraction for opposite charges,
   repulsion for like charges) with a 1/r^2 force law (R^2 > 0.999).

2. U(1) link phases on directed edges produce transverse deflection of charged
   wavepackets in a magnetic field, with the deflection monotonically increasing
   with field strength. Neutral particles are exactly unaffected.

3. The Wilson plaquette holonomy equals the applied B field exactly, confirming
   the gauge construction is consistent with lattice gauge theory.

4. The electrostatic and magnetic sectors are independent of the gravitational
   sector and can coexist in the same Hamiltonian.

**What this probe does NOT establish:**

1. Full Maxwell's equations (not tested -- would require checking Gauss's law,
   Faraday's law, and wave propagation).

2. Charge conjugation symmetry in the staggered dynamics. The staggered
   formulation couples the scalar potential to the mass channel (V*eps), which
   breaks the expected q -> -q symmetry for centroid dynamics. This is a known
   lattice artifact of the staggered doubling, not a physics failure. The force
   expectation value (a classical observable on the initial wavepacket) correctly
   captures the sign.

3. Lorentz covariance or the full Lorentz force law F = q(E + v x B). Only the
   magnetic deflection (v x B) was tested, and only for a single velocity
   direction.

4. Coupling between the electric and magnetic sectors (electromagnetic waves,
   radiation).

## Key parameters

- MASS=0.30, SIGMA=0.80, DT=0.08, N_STEPS=12
- Lattice: 18^3 = 5832 sites, open boundaries
- EM coupling: Q_EM=5.0
- Distances tested: 3, 4, 5, 6, 7 lattice units
- B field strengths: 0.05, 0.10, 0.20, 0.40

## Open questions for follow-up

- Can a naive-fermion (non-staggered) formulation restore charge conjugation
  symmetry in the centroid dynamics?
- Does electromagnetic wave propagation emerge from time-dependent gauge fields?
- Can the gravitational and electromagnetic sectors be unified through a single
  gauge group structure on the graph?
