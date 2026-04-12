# Graviton Mass from Lattice Dispersion and S^3 Topology

**Script:** `scripts/frontier_graviton_mass.py`
**Date:** 2026-04-12
**Status:** PREDICTION -- all observational bounds satisfied

## Question

Does the lattice wave equation on S^3 topology predict a nonzero graviton mass?
If so, is it consistent with LIGO, pulsar timing, and solar system bounds?

## Setup

The framework propagates gravitational waves via the wave equation on a discrete
lattice with spacing a = l_Planck and S^3 spatial topology with radius R = c/H_0
(Hubble radius). Two potential sources of mass gap:

1. **Lattice dispersion:** omega^2 = (2/a^2) sum_i sin^2(k_i a/2)
2. **S^3 topology:** Laplacian eigenvalues lambda_l = l(l+2)/R^2

## Key Results

### 1. Lattice dispersion does NOT give a mass gap

The lattice dispersion satisfies omega(k=0) = 0 exactly. The k^4 correction
modifies the group velocity but preserves masslessness:

    omega^2 = k^2 - (a^2/12) k^4 + O(k^6)

### 2. S^3 topology DOES give a graviton mass

For transverse-traceless (spin-2) graviton modes on S^3, the Lichnerowicz
operator gives eigenvalues lambda_l^TT = [l(l+2) - 2]/R^2 for l >= 2.

The lowest graviton mode (l=2):

    m_g = sqrt(6) * hbar * H_0 / c^2 = 3.52 x 10^-33 eV

### 3. All observational bounds satisfied

| Bound | Upper limit (eV) | Prediction/Bound |
|-------|-------------------|------------------|
| LIGO O3 combined | 1.76 x 10^-23 | 2.0 x 10^-10 |
| LIGO GW170104 | 1.27 x 10^-23 | 2.8 x 10^-10 |
| Pulsar timing | 7.6 x 10^-20 | 4.6 x 10^-14 |
| Solar system | 4.4 x 10^-22 | 8.0 x 10^-12 |
| Weak lensing | 6.0 x 10^-32 | 5.9 x 10^-2 |

Safety margin: prediction is 10^10 below strongest model-independent bound (LIGO).

### 4. UV cutoff from Brillouin zone

Maximum graviton energy at BZ edge: E_max ~ E_Planck.
Group velocity vanishes at BZ edge -- natural UV regulator.
LIGO frequencies are 10^40 below the cutoff.

### 5. Dark energy connection

Yukawa range lambda_g = hbar/(m_g c) = 0.41 R_Hubble.

The graviton mass and cosmological constant come from the SAME S^3 spectrum:
- Lambda <-> l=1 mode: lambda_1 = 3/R^2
- m_g <-> l=2 mode: lambda_2 = 8/R^2

This gives m_g^2 = (8/3) hbar^2 Lambda / c^2. The cosmic coincidence
Lambda ~ m_g^2 ~ H_0^2 is geometric: all set by R_Hubble.

### 6. vDVZ discontinuity does not apply

The graviton mass is topological (from compact S^3 geometry), not Fierz-Pauli
(explicit mass term). Key differences:

- Topological mass preserves diffeomorphism invariance
- The m -> 0 limit (R -> infinity) is smooth
- Extra polarizations are non-normalizable on non-compact space
- Vainshtein radius for the Sun: 2.1 x 10^18 m >> solar system

## Prediction

    m_g = sqrt(6) * hbar * H_0 / c^2 = 3.52 x 10^-33 eV

This is undetectable with current technology (10^10 below LIGO), but represents
a sharp, falsifiable prediction of the framework. Future experiments sensitive
to m_g ~ 10^-33 eV (e.g., cosmological-scale graviton propagation tests)
could in principle test this.

## Dependencies

- `frontier_wave_equation_gravity.py` -- wave equation on lattice
- `frontier_cc_factor15.py` -- S^3 topology and CC eigenvalue
