# CKM Higgs Z_3 Charge: Obstruction to L-Independence

**Date:** 2026-04-12  
**Status:** BOUNDED -- sharp obstruction proved  
**Script:** `scripts/frontier_ckm_higgs_z3_universal.py`  
**Blocker addressed:** "the Higgs Z_3 charge step is still finite-size / L=8 anchored and not yet universal"

---

## Status

The Higgs Z_3 charge delta = 1 is **not** L-independent. The obstruction
is sharp, analytic, and threefold. The CKM lane remains **bounded**.

---

## Theorem / Claim

**Theorem (Higgs Z_3 charge obstruction):**

Let eps(x) = (-1)^{sum_mu x_mu} be the staggered mass operator on a
d-dimensional cubic lattice with L sites per direction. Define Z_3 taste
projectors psi_z(x) = (1/sqrt(L^d)) prod_mu omega^{z_mu x_mu} with
omega = exp(2 pi i / 3).

Then for any even L:

  (i) |<z+delta|eps|z>| is identical for delta_total = 1 and
      delta_total = 2. The mass operator does not prefer either Z_3 charge.

  (ii) For L divisible by 6, all Z_3 transition elements vanish exactly.

  (iii) For L not divisible by 6, magnitudes are O(1/L^d) and vanish
        in the continuum limit.

**Corollary:** The staggered mass operator does not carry a well-defined
Z_3 charge. The claim "Higgs Z_3 charge = 1" cannot be derived from the
Z_3 decomposition of eps(x).

---

## Assumptions

The proof uses only:
1. The standard staggered lattice mass operator eps(x) = (-1)^{sum x_i}
2. Z_3 Fourier analysis on a periodic lattice
3. Elementary properties of geometric sums

No model assumptions, no gauge coupling, no fitted parameters.

---

## What Is Actually Proved

1. **The 1D transition element factorizes analytically.** For each
   direction, the matrix element <z+delta|eps|z> is a geometric sum
   with phase phi_delta = pi(3 - 2 delta)/3.

2. **phi_1 and phi_2 have equal magnitude (pi/3).** Therefore |T(delta=1)|
   = |T(delta=2)| exactly, for all L. This is a consequence of complex
   conjugation symmetry: phi_2 = -phi_1.

3. **For L divisible by 6, sin(L pi/6) = 0.** Therefore all transition
   elements vanish. The mass operator is Z_3-neutral.

4. **The L=8 "confirmation" was a false positive.** The existing script
   checked `charge_1_mag > max(charge_0_mag, charge_2_mag)`, which is
   True because charge_1 = charge_2 > charge_0. But charge_1 is NOT
   greater than charge_2. The result was a tie, not delta = 1.

5. **The d-dimensional result factorizes.** The 3D transition element is
   the product of 1D elements over the three directions. Verified by
   direct lattice computation at L = 4 and L = 8.

6. **Verified numerically at L = 4, 6, 8, 10, 12, 16, 20, 24, 30, 36, 48**
   in d = 3 dimensions. S(delta=1) = S(delta=2) at every size.
   All transitions vanish at L = 6, 12, 24, 30, 36, 48.

---

## What Remains Open

The staggered mass operator route is blocked. Four potential alternative
routes to a Higgs Z_3 charge derivation:

1. **Gauged staggered action:** Coupling to SU(2)_L might break the
   delta=1 / delta=2 degeneracy. Not developed.

2. **EWSB pattern:** The specific Higgs VEV structure might select
   delta=1. Not developed.

3. **Anomaly/consistency constraints:** Combining anomaly cancellation
   with Yukawa sector constraints. Existing analysis showed anomaly
   cancellation alone is insufficient.

4. **Alternative Higgs identification:** Perhaps the Z_3 charge comes
   from a different lattice object. Not developed.

The CKM lane cannot advance beyond bounded status until one of these
alternatives succeeds.

---

## How This Changes The Paper

- CKM remains **bounded lattice support, not a quantitative CKM theorem**
- The specific blocker is now precisely documented: the staggered mass
  operator is Z_3-neutral in the continuum limit and has no charge
  preference at any finite L
- The existing claim in `frontier_ckm_interpretation_derivation.py` that
  "delta=1 CONFIRMED" at L=8 is superseded by this analysis
- Paper-safe wording is unchanged: "bounded lattice support"

---

## Commands Run

```
python3 scripts/frontier_ckm_higgs_z3_universal.py
```

Exit code: 0  
Result: PASS = 8, FAIL = 0
