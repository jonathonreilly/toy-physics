# CKM Higgs Z_3 Charge from Quartic Selector VEV

**Date:** 2026-04-12  
**Status:** BOUNDED -- L-independent framework established, charge = 1 not singled out  
**Script:** `scripts/frontier_ckm_higgs_from_vev.py`  
**Supersedes:** the staggered mass operator route (proved dead in `CKM_HIGGS_Z3_UNIVERSAL_NOTE.md`)

---

## Status

The quartic selector VEV route provides an L-independent algebraic framework
for the Higgs--Z_3 connection. The physical Higgs decomposes democratically
into Z_3 charges 0, 1, and 2 with equal weight 1/3. It does NOT single out
charge 1. The CKM lane remains **bounded**.

---

## Theorem / Claim

**Theorem (Higgs Z_3 decomposition from VEV):**

Let V_sel = 32 sum_{i<j} phi_i^2 phi_j^2 be the quartic selector on the
3-component scalar field. Let sigma: (phi_1, phi_2, phi_3) -> (phi_2, phi_3, phi_1)
be the Z_3 generator.

Then:

(i) V_sel has exactly 3 global minima on the unit sphere: the axis
    directions e_1, e_2, e_3.

(ii) EWSB selects one axis, say e_1 with VEV phi = (v, 0, 0). The Z_3
     action maps this to (0, 0, v) and (0, v, 0), cyclically permuting
     the 3 degenerate vacua.

(iii) The physical Higgs (radial mode h = phi_1 - v) decomposes in the
      Z_3 eigenbasis as:
        phi_1 = (h_0 + h_1 + h_2) / sqrt(3)
      where h_q has Z_3 charge q. All three components have equal VEV:
        <h_0> = <h_1> = <h_2> = v / sqrt(3)

(iv) The tree-level Yukawa mass matrix is rank 1: M = (y v / sqrt(3)) J_3,
     giving one massive generation (the top) and two massless generations.

**Corollary:** The Higgs does not carry a definite Z_3 charge. The CKM
mass hierarchy must arise from radiative corrections, not from a
tree-level Z_3 charge selection.

---

## Assumptions

1. The quartic selector V_sel = 32 sum_{i<j} phi_i^2 phi_j^2 is the correct
   potential determining EWSB (from the graph-shift selector derivation).
2. The Z_3 symmetry acts as the cyclic permutation of the 3 scalar components.
3. Standard EWSB: one axis minimum is selected, breaking Z_3 -> trivial.
4. The Yukawa coupling is y * phi_1 * psi_bar * psi in the selected vacuum.

No lattice size L, no gauge coupling, no fitted parameters.

---

## What Is Actually Proved

1. **Quartic selector minima are purely algebraic.** V_sel = 0 at axis
   directions, V_sel > 0 elsewhere on the unit sphere. No L-dependence.

2. **Z_3 permutes the 3 degenerate vacua.** The VEV (v,0,0) is NOT
   Z_3-invariant. Z_3 is spontaneously broken by EWSB.

3. **Democratic Z_3 decomposition.** The VEV direction phi_1 decomposes
   into Z_3 eigenstates with equal weight 1/3 for each charge. This is
   exact linear algebra on the 3x3 cyclic permutation matrix.

4. **L-independence.** No lattice size enters at any step. This contrasts
   sharply with the staggered mass operator route, which depends on L mod 6.

5. **Rank-1 tree-level mass matrix.** The democratic Higgs VEV gives a
   mass matrix proportional to J_3 (all-ones), with one nonzero eigenvalue
   m_top = y v sqrt(3) and two zero eigenvalues.

6. **Yukawa selection rule is democratic.** Since all <h_q> are equal,
   the Z_3 selection rule does not distinguish any particular charge
   difference. All Yukawa couplings are equally allowed.

---

## What Remains Open

1. **Charge 1 not singled out.** The VEV route gives equal weight to all
   Z_3 charges. To derive the specific CKM pattern, one needs the
   radiative corrections to the mass matrix, not just the tree-level Higgs
   Z_3 charge.

2. **Radiative hierarchy.** The two lighter generations get masses from
   loop corrections. The loop structure depends on gauge boson exchange
   between Z_3 sectors, which IS sensitive to charge differences. But
   computing this requires a full 1-loop calculation on the staggered
   lattice.

3. **Quantitative CKM.** The Cabibbo angle, V_cb, V_ub, and the CP phase
   all require the off-diagonal structure of the radiative mass matrix.
   This is not computed here.

4. **Key reframing.** The question "what Z_3 charge does the Higgs carry?"
   was based on an incorrect expectation. The correct framework is:
   - Tree level: rank-1 mass matrix (top only)
   - Radiative: Z_3-sensitive loop corrections generate hierarchy
   - CKM: off-diagonal radiative corrections generate mixing

---

## How This Changes The Paper

- CKM remains **bounded lattice support, not a quantitative CKM theorem**
- The staggered mass operator route is confirmed dead (previous note)
- The VEV route provides an L-independent algebraic framework
- The Higgs Z_3 charge question is reframed: the relevant object is the
  tree-level + radiative mass matrix structure, not a single charge quantum
  number
- The rank-1 tree-level result (one massive generation) is a structural
  prediction that matches the SM hierarchy qualitatively
- Paper-safe wording unchanged: "bounded lattice support"

---

## Commands Run

```
python3 scripts/frontier_ckm_higgs_from_vev.py
```

Exit code: 0  
Result: PASS = 16, FAIL = 0
