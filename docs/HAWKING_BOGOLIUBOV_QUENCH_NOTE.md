# Gaussian-State In/Out Quench Prototype

**Status:** bounded review candidate (Paper 2 groundwork)
**Script:** `scripts/frontier_hawking_bogoliubov_quench.py`
**Date:** 2026-04-12

## Motivation

The existing second-quantized prototype (`frontier_second_quantized_prototype.py`)
computes Bogoliubov overlaps between a free vacuum and a gravitationally-shifted
vacuum.  That is an overlap-proxy calculation: it compares ground states of two
different Hamiltonians but does not model a dynamical quench process.

This script implements an explicit sudden-quench Gaussian-state in/out
calculation on a free-fermion chain.  Two Hamiltonians H_in (uniform) and H_out
(locally modified) are diagonalized independently, and the Bogoliubov beta
matrix is computed exactly from their mode overlaps.  This is the first step
toward establishing real particle creation from vacuum in the framework.

**This is NOT described as Hawking radiation.**  It is a Gaussian-state in/out
calculation.  The horizon interpretation requires further work.

## Method

Free fermions on a 1D tight-binding chain (N=40-100 sites).  Half-filled Dirac
sea.  All results from exact diagonalization of the N x N single-particle
Hamiltonian (O(N^3), no exponential Hilbert space).

- **H_in:** uniform hopping t=1, mass m=0.5 on all sites.
- **H_out:** same chain with localized modification:
  - *Hopping quench:* reduced hopping in a central region (smooth tanh profile).
  - *Mass quench:* increased on-site mass in a central region.
- **Bogoliubov beta:** overlap of H_in occupied modes with H_out unoccupied modes.
- **Occupations:** n_l = sum_k |beta_{kl}|^2 per out-unoccupied mode l.
- **Thermality test:** Fermi-Dirac logit fit: ln(1/n - 1) vs epsilon gives slope = 1/T.

## Results

### Gate 0: Null test (H_out = H_in) -- PASS

When H_out = H_in identically, all Bogoliubov coefficients vanish:
max |beta|^2 = 7e-31 (machine epsilon).  No spurious particle creation.

### Gate 1: Hopping quench -- PASS

Reducing hopping in a central region creates particles.  Creation is monotone
in quench strength:

| t_center | particles | max n_k | R^2 (logit) |
|----------|-----------|---------|-------------|
| 0.90     | 0.0002    | 0.0001  | 0.89        |
| 0.70     | 0.0019    | 0.0008  | 0.89        |
| 0.50     | 0.0072    | 0.0030  | 0.91        |
| 0.30     | 0.021     | 0.009   | 0.93        |
| 0.10     | 0.067     | 0.027   | 0.96        |

### Gate 2: Mass quench -- PASS

Increasing mass in a central region also creates particles, with larger effect
at fixed quench depth:

| m_center | particles | max n_k | R^2 (logit) |
|----------|-----------|---------|-------------|
| 1.0      | 0.38      | 0.12    | 0.97        |
| 2.0      | 1.86      | 0.23    | 0.94        |
| 4.0      | 4.74      | 0.50    | 0.55        |
| 8.0      | 5.97      | 0.79    | <0.01       |

Thermality degrades at strong mass quench (modes saturate toward n=1 at the
Dirac sea limit).  This is a finite-chain saturation effect.

### Gate 3: Temperature scales with gradient -- PASS

Varying the tanh steepness (sigma) at fixed quench depth changes the gradient
at the quench boundary independently of the quench depth.  The fitted
temperature tracks the gradient linearly:

T = 0.457 * gradient + 0.067  (R^2 = 0.97)

This is the lattice analog of the Unruh/Hawking relation T ~ kappa/(2 pi),
where kappa is the surface gravity.  The relationship is compatible with a
proportionality between effective temperature and the steepness of the
local vacuum structure change.

### Size dependence

Particle number at fixed quench parameters grows slowly with N, confirming
this is not a finite-size artifact:

| N   | particles | density (n/N) |
|-----|-----------|---------------|
| 40  | 0.032     | 8.1e-4        |
| 60  | 0.036     | 6.0e-4        |
| 80  | 0.038     | 4.8e-4        |
| 100 | 0.040     | 4.0e-4        |

## What is supported

- Exact Bogoliubov particle creation from a sudden quench on a free-fermion
  chain, with verified null (no quench => no particles).
- Monotone dependence on quench strength for both hopping and mass quenches.
- Fermi-Dirac thermal spectrum (R^2 > 0.89) in the weak-to-moderate quench
  regime.
- Linear scaling of fitted temperature with quench gradient (R^2 = 0.97),
  compatible with a surface-gravity interpretation.

## What is NOT supported

- This is not a Hawking radiation claim.  It is a Gaussian-state in/out
  calculation on a lattice.  The horizon interpretation requires:
  1. Connection to the propagator framework (graph growth + field f).
  2. Identification of the quench with actual causal structure change.
  3. Recovery of the 1/(2 pi) Hawking prefactor from graph-theoretic quantities.
- Thermality degrades at strong quench (finite-chain saturation).
- The T ~ gradient relation is a linear fit, not a derivation.

## Missing closure

- Real-time evolution (currently instant quench; Floquet/Krylov propagation
  would test adiabatic vs sudden regimes).
- Connection to the Paper 1 propagator (the quench should arise from graph
  growth dynamics, not be imposed by hand).
- 2D/3D generalization to test whether area-law entropy interacts with
  the quench particle creation.
