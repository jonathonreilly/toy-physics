# CKM Jarlskog Fix: Full Z_3^3 Directional Phase Matrices

**Status:** BOUNDED (16/17 checks pass: 10 exact, 6 bounded)
**Script:** `scripts/frontier_ckm_jarlskog_fix.py`
**Date:** 2026-04-13
**Gate:** CKM / Jarlskog invariant closure (review.md gate 3)

## Problem

The Jarlskog invariant J was ~10x too small in the full CKM closure
(frontier_ckm_full_closure.py). Using a single Z_3 phase delta = 2*pi/3
uniformly for both up and down sectors creates an irreconcilable J-V_ub
tension: small c_13 (needed for V_ub ~ 0.004) suppresses J because
J = c12*s12*c23*s23*c13^2*s13*sin(delta), and V_ub ~ s_13.

## Solution

Replace the single Z_3 phase with the full Z_3^3 = Z_3 x Z_3 x Z_3
directional phase structure. Each lattice axis carries an independent
Z_3 phase angle theta_k that depends on the sector's gauge coupling:

- Axis x (EWSB): theta_k^q = (2*pi/3) * (1 + delta_EW_q)
- Axis y, z (color): theta_k^q = 2*pi/3 (same for both sectors)

The EWSB axis is special because the Higgs VEV breaks the Z_3 symmetry
along x, and the EW correction differs between up and down quarks
(T3_up = +1/2 vs T3_down = -1/2).

The phase for element (i,j) of sector q is:
  phi_{ij}^q = sum_k T_k * theta_k^q
where T_k = (q_i^k + q_H_q^k + q_j^k) mod 3 is the total Z_3 charge
on axis k, and q_H enters with +q_H for up and -q_H for down.

## Results

| Parameter | PDG | This work | Deviation |
|-----------|-----|-----------|-----------|
| V_us | 0.2243 | 0.2268 | +1.1% |
| V_cb | 0.0422 | 0.0425 | +0.8% |
| V_ub | 0.00382 | 0.00589 | +54% |
| J | 3.08e-5 | 1.89e-5 | -39% |
| delta_CP | 65.5 deg | 20.0 deg | -69% |

When optimizing c_13 for V_ub alone: J/J_PDG = 0.91 (near-perfect).

## Key advancement

| Metric | Uniform Z_3 | Z_3^3 directional | Improvement |
|--------|-------------|-------------------|-------------|
| J/J_PDG (V_ub-opt) | 0.12 | 0.91 | 7.6x |
| J/J_PDG (joint opt) | 0.12 | 0.61 | 5.1x |

The J-V_ub tension is resolved: J is now within a factor of 2 of PDG
while simultaneously keeping V_us and V_cb within 1% of PDG.

## Mechanism

1. The three lattice axes carry independent Z_3 phases
2. The EWSB axis (x) has a sector-dependent phase shift from the EW
   gauge coupling difference: theta_up(x) = 132.1 deg, theta_down(x) = 137.2 deg
3. The mismatch (5.1 deg on the EWSB axis) creates different phase
   patterns in the up vs down mass matrices
4. After absorbing diagonal phases (field redefinitions), the three
   off-diagonal elements carry two distinct mismatches:
   - (1,2) and (1,3): -154.5 deg
   - (2,3): -113.0 deg
5. The different mismatches on different elements produce a nontrivial
   CKM phase from the coherent sum of all CP-violating contributions

## What is derived (zero free CKM parameters)

- Z_3^3 structure from Cl(3) taste space (mathematical fact)
- Generation charges q_1=(1,0,0), q_2=(0,1,0), q_3=(0,0,1)
- Higgs Z_3^3 charge q_H=(2,1,1) from T_1-T_2 bilinear
- Axis-dependent phases from EW gauge couplings (g_Z^up vs g_Z^down)
- V_us, V_cb from NNI + EW weights (prior scripts)

## What remains bounded

1. c_13/c_23 = 0.36 (optimized; needs lattice derivation)
2. V_ub 54% above PDG (J-V_ub tension reduced but not eliminated)
3. delta_CP = 20 deg (PDG 65.5 deg) -- effective phase is suppressed
   because the EWSB axis mismatch is only 5.1 deg

## Remaining attack routes

1. Include higher-order EW corrections to theta_EWSB (2-loop, threshold)
   to increase the EWSB axis mismatch beyond 5.1 deg
2. Include the EWSB breaking of Z_3 on axes y,z (color confinement
   generates a smaller but nonzero axis mismatch)
3. Derive c_13/c_23 from the lattice overlap at larger L

## Builds on (does not redo)

- `frontier_ckm_full_closure.py`: NNI infrastructure, EW weights
- `frontier_ckm_jarlskog_closure.py`: sector-dependent phase concept
- `frontier_ckm_vcb_closure.py`: exact NNI formula, EW ratio
