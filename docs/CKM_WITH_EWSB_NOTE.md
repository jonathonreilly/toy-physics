# CKM Inter-Valley Scattering with EWSB

**Script:** `scripts/frontier_ckm_with_ewsb.py`
**Status:** 15/15 checks pass (all bounded or supporting exact checks)
**Lane status:** BOUNDED -- does not close CKM

## Status

BOUNDED. EWSB provides the structural C3 -> Z_2 breaking that was
missing from the bare inter-valley computation, but the quantitative
CKM hierarchy does not emerge from this mechanism alone.

## Theorem / Claim

**Exact structural result:**

On the staggered lattice Z^3_L, the EWSB term H_EWSB = y*v*Gamma_1
breaks the C3[111] permutation symmetry of the three BZ corners
X_1=(pi,0,0), X_2=(0,pi,0), X_3=(0,0,pi) down to Z_2:

- X_1 (the "weak" corner, aligned with VEV direction) is distinguished
- X_2, X_3 (the "color" corners) remain equivalent under residual Z_2

This is algebraic and L-independent.

**Bounded computational result:**

The inter-valley scattering amplitudes T_ij = <psi_i|H|psi_j> split
into two classes after EWSB:

- T_12, T_13 (involving the weak corner)
- T_23 (color-color)

The free-field ratio is <|T_weak|>/|T_color| ~ 0.70, with weak-corner
amplitudes *suppressed* (not enhanced). With gauge fluctuations, the
ensemble average ratio is ~1.70 but with standard deviation ~2.05,
meaning the effect is not statistically robust at L=6 with 10 configs.

**Negative result on quantitative CKM:**

The extracted V_CKM from this mechanism does NOT reproduce the PDG
hierarchy. The CKM elements do not order as |V_us| >> |V_cb| >> |V_ub|.

## Assumptions

1. Staggered lattice Z^3_L with L=6
2. SU(3) gauge links near identity (epsilon=0.3)
3. Wilson taste-breaking term with r=1
4. EWSB coupling y*v as a free parameter (scanned 0 to 1)
5. Gaussian wave packets at BZ corners
6. Quenched gauge approximation

## What Is Actually Proved

1. **EXACT:** EWSB breaks C3 -> Z_2 in the BZ corner structure.
   The weak corner X_1 is algebraically distinguished from X_2, X_3.

2. **EXACT:** In the free field with EWSB, |T_12| = |T_13| (Z_2 residual)
   and |T_12| != |T_23| (C3 broken). This is L-independent.

3. **COMPUTED:** The free-field C3 breaking ratio is ~0.70 and stable
   across L=4,6,8. The weak-corner amplitudes are suppressed, not
   enhanced, in the free field.

4. **BOUNDED:** With gauge fluctuations, the ensemble-averaged ratio
   shifts to ~1.70 but with large variance, indicating that gauge
   effects dominate over the structural EWSB splitting at this
   lattice size and coupling.

5. **NEGATIVE:** The extracted V_CKM does not match PDG values
   quantitatively. The hierarchy |V_us| >> |V_cb| >> |V_ub| is
   not reproduced by this mechanism.

## What Remains Open

1. **Higgs Z_3 charge L-independence** -- the primary blocker for the
   entire CKM lane (per review.md)

2. **Quantitative CKM mechanism** -- EWSB + inter-valley scattering
   provides the right symmetry breaking (C3 -> Z_2) but not the right
   quantitative hierarchy. The mechanism may require:
   - Radiative corrections (loop-level effects)
   - Proper continuum limit / thermodynamic limit
   - Different treatment of up vs down sectors
   - Or a fundamentally different route

3. **y*v as a model input** -- the EWSB coupling strength is not derived

4. **Continuum limit** -- L=6 is far from the thermodynamic limit

## How This Changes The Paper

This note is a bounded strengthening of the CKM lane:

- It identifies the structural mechanism (EWSB breaks C3 -> Z_2) that
  was missing from the bare computation
- It confirms that the bare computation's negative result was due to
  the missing EWSB, not a fundamental obstruction
- It shows that the structural breaking alone does not quantitatively
  reproduce CKM

The CKM lane remains BOUNDED per review.md. This note does not
upgrade the lane status.

Safe paper use: cite as evidence that the EWSB symmetry-breaking
pattern (C3 -> Z_2) is consistent with the CKM structure, while noting
that quantitative closure requires additional work.

## Commands Run

```
python3 scripts/frontier_ckm_with_ewsb.py
# Exit code: 0
# PASS=15 FAIL=0
```
