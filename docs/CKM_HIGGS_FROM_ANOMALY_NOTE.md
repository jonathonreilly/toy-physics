# CKM Higgs Z_3 Charge from Anomaly Cancellation

**Date:** 2026-04-12
**Status:** BOUNDED -- anomaly route blocked, lane remains open
**Script:** `scripts/frontier_ckm_higgs_from_anomaly.py`
**Blocker addressed:** "the Higgs Z_3 charge step is still finite-size / L=8 anchored and not yet universal"

---

## Status

The anomaly cancellation route to deriving the Higgs Z_3 charge delta_H
is **blocked**.  The CKM lane remains **bounded**.

---

## Theorem / Claim

**Claim (Anomaly non-constraint on Higgs Z_3 charge):**

Let the three SM generations carry Z_3 charges {0, 1, 2} from the
staggered lattice orbit decomposition.  Let the Higgs field carry Z_3
charge delta_H in {0, 1, 2}.

Then:

  (i)   All discrete Z_3 anomaly conditions (Z_3-grav^2, Z_3^3 cubic,
        Z_3-SU(2)^2, Z_3-SU(3)^2) cancel trivially for any delta_H,
        because they involve only fermion charges and
        sum(0 + 1 + 2) = 3 = 0 mod 3.

  (ii)  The Higgs is a scalar and does not enter discrete anomaly
        triangles (which require chiral fermion loops).

  (iii) Gauge invariance of the Yukawa psi_L H psi_R fixes the Higgs
        SU(2) x U(1) quantum numbers (doublet, Y=1) but does NOT
        constrain the discrete Z_3 charge delta_H.

  (iv)  delta_H = 0 is excluded phenomenologically (gives V_CKM = I,
        no quark mixing).

  (v)   delta_H = 1 and delta_H = 2 give the same |V_CKM|^2 and are
        related by the Z_3 outer automorphism (charge conjugation).
        They are physically indistinguishable from CKM magnitude
        measurements.

**Corollary:** Anomaly cancellation does not select the Higgs Z_3
charge.  The CKM lane cannot be closed via this route.

---

## Assumptions

The argument uses only:

1. Three SM generations with Z_3 charges {0, 1, 2} (from orbit algebra)
2. Standard discrete Z_3 anomaly conditions
3. The fact that scalars do not contribute to chiral/discrete anomalies
4. Gauge invariance of the Yukawa coupling under SU(2) x U(1)
5. The observation that V_CKM is not the identity

No model assumptions, no finite-size effects, no fitted parameters.

---

## What Is Actually Proved

1. **Z_3 anomaly conditions are trivially satisfied.**  For generation
   charges {0, 1, 2}, all anomaly sums are proportional to
   0 + 1 + 2 = 0 mod 3.  This holds for any fermion multiplicity
   structure and is independent of delta_H.

2. **Scalars do not enter discrete anomaly conditions.**  The anomaly
   triangle involves chiral fermion loops.  The Higgs (spin 0) has no
   chiral index and does not appear in the anomaly sum.

3. **Four indirect routes are blocked:**
   - (a) Mixed Z_3 x Z_3 anomaly with Higgs: no scalar chiral anomaly.
   - (b) 't Hooft anomaly matching across EWSB: Z_3 is broken by the
     Higgs VEV (if delta_H != 0), so matching does not apply.
   - (c) Z_3 as remnant of U(1): in the lattice framework, Z_3 is a
     taste symmetry, not a broken U(1) remnant.
   - (d) Gravitational anomaly: involves only fermion zero modes.

4. **Gauge invariance constrains SU(2) x U(1) charges, not Z_3.**
   The Higgs must be an SU(2) doublet with Y = 1 for the Yukawa to be
   gauge-invariant.  But all three values of delta_H give gauge-invariant
   Yukawa couplings with rank-3 texture matrices.

5. **delta_H = 1 and delta_H = 2 are physically degenerate.**
   They are related by the Z_3 outer automorphism (alpha -> -alpha mod 3),
   which is equivalent to charge conjugation.  The physical CKM
   observables |V_ij|^2 are the same for both.

---

## What Remains Open

The anomaly route is blocked.  The CKM lane remains bounded.

Four potential routes to deriving delta_H (or bypassing it):

1. **Gauged staggered action:** Coupling to SU(2)_L gauge fields might
   break the delta=1/delta=2 degeneracy through the gauge-taste
   interaction structure.  Not developed.

2. **EWSB pattern:** The specific Higgs VEV structure on the lattice
   might select a preferred delta_H.  Not developed.

3. **Lattice CP structure:** A lattice mechanism that breaks the Z_3
   outer automorphism (distinguishes omega from omega*) would lift the
   degeneracy.  This would require a CP-odd lattice observable.

4. **Alternative Higgs identification:** Perhaps delta_H comes from a
   different lattice object than the staggered mass operator.

---

## How This Changes The Paper

- CKM remains **bounded lattice support, not a quantitative CKM theorem**
- The anomaly route is now documented as blocked, joining the staggered
  mass operator route (CKM_HIGGS_Z3_UNIVERSAL_NOTE.md)
- The blocker is sharpened: not only is the staggered mass operator
  Z_3-neutral, but anomaly cancellation provides no alternative path
  because scalars are invisible to discrete anomalies and the fermion
  anomalies are trivially satisfied
- Paper-safe wording is unchanged from review.md

---

## Commands Run

```
python3 scripts/frontier_ckm_higgs_from_anomaly.py
```

Exit code: 0
Result: PASS=22 FAIL=0 BOUNDED=0
