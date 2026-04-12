# Diagnosis: T-kappa Sign Reversal in 3D Bogoliubov Quench

**Status:** Root cause identified. The sign reversal is physical, not a bug.

## The Problem

The 3D spherical quench (scripts/frontier_hawking_3d_quench.py) produces:

| Relation     | Slope sign | R^2  | Hawking expectation |
|-------------|-----------|------|---------------------|
| T vs kappa  | NEGATIVE (-0.43)  | 0.98 | Positive            |
| T vs 1/R_h  | POSITIVE (+0.10)  | 0.86 | Positive            |

In Hawking physics, T = kappa/(2 pi) with kappa ~ 1/R_h for Schwarzschild.
Both relations should have the same sign. They do not.

## Five Hypotheses Tested

### H1: kappa is computed incorrectly

**Result:** kappa = qs/(2 sigma) exactly (R^2 = 1.000000).

The surface gravity is analytically trivial: a tanh of width sigma has
max gradient qs/(2 sigma). With sigma fixed at 2.0, kappa is just a rescaled
copy of quench_strength. It carries no independent geometric information.

### H2: The spectrum is not thermal

**Result:** The logit R^2 is 0.86-0.91 -- reasonable but not excellent.
The spectrum is approximately thermal at all quench strengths. However, T_logit
DECREASES monotonically from 0.447 (qs=0.1) to 0.358 (qs=0.9) while the
bandwidth simultaneously compresses from 5.50 to 4.68.

### H3: Finite-size contamination

**Result:** The sign is NEGATIVE at all tested sizes (L=8, 10, 12).
The magnitude of dT grows slightly with L but the direction is invariant.
This is not a finite-size artifact.

### H4: Weak-quench perturbative regime

**Result:** The slope is -0.75 at qs in [0.02, 0.30] with R^2 = 0.97.
Even in the weakest quenches accessible on this lattice, the sign is wrong.
The perturbative regime does not fix it.

### H5: Onsite potential quench (redshift analog)

**Result:** T vs kappa_V has slope +0.48 with R^2 = 0.92 -- CORRECT sign.

This is the key finding. Replacing the hopping reduction with an onsite
potential (which shifts eigenvalues like gravitational redshift, rather than
compressing bandwidth) produces the correct Hawking sign.

| Quench type     | T vs kappa slope | Sign    |
|----------------|-----------------|---------|
| Hopping reduction | -0.43        | WRONG   |
| Onsite potential  | +0.48        | CORRECT |

## Root Cause

The sign reversal comes from confusing two distinct physical effects:

**Hopping reduction compresses the bandwidth.** Reducing t inside the sphere
makes the post-quench unoccupied band narrower (from 5.50 at qs=0.1 to 4.68
at qs=0.9). A stronger quench creates more Bogoliubov particles, but they are
spread across a narrower band. The Fermi-Dirac logit fit captures the RATIO of
occupied to unoccupied states -- when more modes are filled in a narrower band,
the logit slope decreases (lower T).

**Gravitational redshift shifts eigenvalues without compressing bandwidth.**
The onsite potential quench shifts the energy spectrum inside the sphere without
changing the connectivity. This is closer to the physical mechanism in Hawking
radiation, where frequencies are redshifted near the horizon.

Key observables vs kappa (hopping quench):

| Observable        | Sign vs kappa | R^2  |
|------------------|--------------|------|
| n_total (particles) | POSITIVE   | 0.86 |
| E_total (energy)    | POSITIVE   | 0.92 |
| E/n (energy/particle)| NEGATIVE  | 0.99 |
| T_fit (logit T)     | NEGATIVE   | 0.98 |
| Bandwidth           | NEGATIVE   | --   |

The fitted T tracks E/n (energy per particle), not the total radiation
intensity. In real Hawking radiation, increasing kappa increases BOTH the
per-quantum energy AND the total flux. In the hopping quench, increasing kappa
increases total flux but DECREASES per-quantum energy because the bandwidth
shrinks.

## Implications

1. The T vs 1/R_h relation has the correct sign because varying R_h at fixed
   quench_strength changes the number of modes near the horizon (a geometric
   effect), not the bandwidth. This is why R_h and kappa give contradictory
   signs -- they probe different physics.

2. The onsite potential quench is a better analog of Hawking radiation than the
   hopping reduction quench. Future work should use potential-based quenches or
   mixed quenches that preserve the bandwidth while creating a mode mismatch.

3. The Fermi-Dirac T is not the Hawking temperature. For the hopping quench,
   n_total ~ kappa^2 (R^2 = 0.998 in weak regime) is the correct perturbative
   scaling, consistent with Bogoliubov coefficient expectations.

## Scripts

- `scripts/frontier_hawking_sign_diagnosis.py` -- all five hypothesis tests
- `scripts/frontier_hawking_3d_quench.py` -- original 3D quench calculation
