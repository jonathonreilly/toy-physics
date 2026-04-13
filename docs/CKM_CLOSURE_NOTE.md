# CKM Closure: Full Derivation Chain from Z_3 + EWSB

**Date:** 2026-04-12
**Status:** BOUNDED -- complete derivation chain, no Higgs Z_3 charge needed
**Script:** `scripts/frontier_ckm_closure.py`
**Prior work cited:**
- `scripts/frontier_ckm_from_z3.py` (eps = 1/3, FN charges, sin theta_C)
- `scripts/frontier_ckm_with_ewsb.py` (EWSB C3 -> Z_2 breaking, 29/29 exact)
- `scripts/frontier_ckm_higgs_from_vev.py` (democratic VEV, no definite Z_3 charge)
- `scripts/frontier_ckm_dynamical_selection.py` (FN charges from Z_3 directional sums)

---

## Status

BOUNDED. The full CKM derivation chain is assembled from Z_3 group structure
and EWSB. The Higgs Z_3 charge blocker identified in review.md is irrelevant:
the Higgs VEV has no definite Z_3 charge (democratic decomposition, weight
1/3 on each charge). The chain produces the correct CKM hierarchy and
order-of-magnitude values for all elements, but precise values depend on
undetermined O(1) Yukawa coefficients. The lane remains bounded, not closed.

---

## Theorem / Claim

**Claim (CKM from Z_3 + EWSB, no Higgs Z_3 charge):**

The CKM matrix structure follows from two algebraic inputs:

1. The Z_3 symmetry of the 3D staggered lattice, which gives:
   - Froggatt-Nielsen parameter eps = 1/|Z_3| = 1/3 (exact)
   - FN charges q_up = (5,3,0), q_down = (4,2,0) from directional Z_3 sums
   - CP phase delta = 2 pi/3 from Z_3 eigenvalue spacing (exact geometry)

2. EWSB via the quartic selector, which gives:
   - C3 -> Z_2 breaking: one axis (weak) distinguished from the other two
   - 1+2 mass split in generation space (exact)
   - Off-diagonal mixing structure from Z_2 breaking

The Higgs Z_3 charge (the blocker in review.md finding 3) does not enter.
The Higgs VEV decomposes democratically into Z_3 charges 0, 1, 2 with
equal weight 1/3 each (proved algebraically in frontier_ckm_higgs_from_vev.py).

---

## Assumptions

1. Cl(3) on Z^3 as the physical theory (framework premise).
2. Z_3 taste symmetry of the 3D staggered lattice.
3. Quartic selector EWSB (V_sel = 32 sum_{i<j} phi_i^2 phi_j^2).
4. Froggatt-Nielsen parametrization of the mass matrices.
5. O(1) Yukawa coefficients (not derived; this is the remaining bounded input).

No lattice size L. No gauge coupling value. No Higgs Z_3 charge.

---

## What Is Actually Proved

### Exact results (no free parameters):

1. **eps = 1/3** from Z_3 group order. The Z_3 generator has eigenvalues
   1, omega, omega^2 with omega = exp(2 pi i/3). The mixing amplitude
   between adjacent Z_3 sectors is 1/|Z_3| = 1/3. (Step A, 4 exact checks.)

2. **Democratic VEV decomposition.** The VEV direction (1,0,0) in the Z_3
   eigenbasis has equal weight 1/3 on each charge. There is no definite
   Higgs Z_3 charge. (Step A, 1 exact check; proved in frontier_ckm_higgs_from_vev.py.)

3. **C3 -> Z_2 breaking from EWSB.** The quartic selector V_sel = 0 at axis
   directions, V_sel > 0 off-axis. EWSB selects one axis (weak), leaving
   a Z_2 residual permuting the other two. (Step C, 7 exact checks;
   confirmed 29/29 in frontier_ckm_with_ewsb.py.)

4. **delta_CP = 2 pi/3 as the natural scale.** The angular spacing between
   adjacent Z_3 eigenvalues is exactly 2 pi/3 = 120 deg. This is the
   maximal CP phase from Z_3 geometry. (Step F, 1 exact check.)

5. **CKM hierarchy ordering.** The FN charge structure forces
   |V_us| >> |V_cb| >> |V_ub|. This is structural, not fitted. (Step E.)

6. **CKM unitarity.** The reconstructed matrix is exactly unitary.
   (1 exact check, ||VV^dag - I|| < 10^{-15}.)

### Bounded results (depend on O(1) Yukawa coefficients):

7. **sin(theta_C) = 0.225 +/- 0.05** from FN with eps = 1/3 and Z_3
   charges. Median from Monte Carlo over O(1) coefficients. PDG 0.2243
   is within the range. (Step B, 2 bounded checks.)

8. **|V_cb| ~ 0.04** from Z_2 breaking + FN charges. PDG 0.0422 is
   within the Monte Carlo range [0.02, 0.08]. (Step D, 1 bounded check.)

9. **|V_ub| ~ 0.005** from the product |V_us| x |V_cb|. PDG 0.00394
   is within the range [0.002, 0.015]. (Step E, 1 bounded check.)

10. **delta_CP within factor 2 of PDG.** The Z_3 value 120 deg vs PDG
    68.5 deg. The physical phase is reduced from the Z_3 maximum by
    O(1) Yukawa effects. (Step F, 1 bounded check.)

11. **Jarlskog J within order of magnitude.** J_Z3 ~ 3.8 x 10^{-5} vs
    PDG 3.08 x 10^{-5}. (Step G, 1 bounded check.)

### Script scorecard: PASS=20 FAIL=0 (14 exact, 6 bounded)

---

## What Remains Open

1. **O(1) Yukawa coefficients.** The FN framework determines the parametric
   SCALING of CKM elements (powers of eps = 1/3) but not the O(1)
   prefactors. Deriving these requires computing the full Yukawa matrix
   from the lattice action, which has not been done.

2. **Precise delta_CP.** The Z_3 prediction 120 deg is 75% larger than
   PDG 68.5 deg. Closing this gap requires the O(1) Yukawa structure.

3. **Radiative corrections to the mass hierarchy.** The tree-level mass
   matrix is rank 1 (one massive generation from democratic VEV). The
   lighter generations get masses from radiative corrections. The loop
   structure is computable in principle but has not been calculated.

4. **Continuum limit.** All lattice computations are at finite L.
   The continuum/thermodynamic limit has not been taken.

---

## How This Changes The Paper

The Higgs Z_3 charge was listed as the live blocker for CKM closure
(review.md finding 3: "CKM remains bounded until the Higgs Z_3 charge is
L-independent"). This note shows that blocker is irrelevant:

- The Higgs has no definite Z_3 charge (democratic VEV, proved algebraically).
- The CKM derivation chain uses eps = 1/3 from the Z_3 GROUP ORDER,
  not from any Higgs Z_3 charge.
- The EWSB C3 -> Z_2 breaking is algebraic (quartic selector), not
  dependent on any L-specific Z_3 charge assignment.

The CKM lane remains BOUNDED (not closed) because the O(1) Yukawa
coefficients are not derived. But the NATURE of the remaining gap has
changed: it is no longer "Higgs Z_3 charge not universal" but rather
"O(1) coefficients not computed." This is a standard FN limitation,
not a framework-specific blocker.

Paper-safe wording:

> The Z_3 taste symmetry and EWSB quartic selector determine the CKM
> hierarchy and CP phase scale. The Froggatt-Nielsen parameter eps = 1/3
> and the charge assignments q_up = (5,3,0), q_down = (4,2,0) are derived
> from the lattice Z_3 structure. Precise CKM values remain bounded by
> undetermined O(1) Yukawa coefficients.

---

## Commands Run

```
python3 scripts/frontier_ckm_closure.py
# Exit code: 0
# PASS=20 FAIL=0 (14 exact, 6 bounded)
```
