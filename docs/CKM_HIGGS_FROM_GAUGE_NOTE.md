# CKM Higgs from Gauge: Z_3 Charge of the Gamma_5 Condensate

**Date:** 2026-04-12  
**Status:** EXACT obstruction -- Higgs has Z_3 charge 0, not 1  
**Script:** `scripts/frontier_ckm_higgs_from_gauge.py`  
**Blocker addressed:** "the Higgs Z_3 charge step is still finite-size / L=8 anchored and not yet universal"

---

## Status

The Higgs Z_3 charge obstruction is now proved by two independent methods:
1. **Algebraic** (this note): eps(taste) has Z_3 charge 0 by permutation symmetry
2. **Numerical** (existing): eps(x) couples equally to charges 1 and 2 on finite lattices

The CKM lane remains **BOUNDED**.

---

## Theorem / Claim

**Theorem (Higgs Z_3 charge obstruction -- gauge-scalar route):**

In the Cl(3)-on-Z^3 framework:

(a) The natural Higgs candidate is the staggered mass condensate
    `<psi-bar eps psi>`, where `eps(x) = (-1)^{x_1+x_2+x_3}`.

(b) In the taste decomposition, `eps` maps to the diagonal operator
    `eps(taste) = diag((-1)^{a_1+a_2+a_3})` on the 8-dimensional
    KS taste space.

(c) The Z_3 taste symmetry acts by cyclic permutation of the taste
    indices: `(a_1, a_2, a_3) -> (a_3, a_1, a_2)`.

(d) `eps(taste)` is **exactly Z_3-invariant** (charge 0) because the
    exponent `a_1 + a_2 + a_3` is symmetric under cyclic permutations.

(e) The CKM derivation chain requires the Higgs to have Z_3 charge 1.

(f) Therefore the gauge-scalar route to the Higgs Z_3 charge **fails**.

**Proof of (d):**

`(P eps P^{-1})_{b,b} = eps_{P^{-1}b, P^{-1}b} = (-1)^{b_2+b_3+b_1} = (-1)^{b_1+b_2+b_3} = eps_{b,b}.`

The sum `a_1 + a_2 + a_3` is invariant under all permutations of
`(a_1, a_2, a_3)`, so `eps(taste)` is actually S_3-invariant (not
just Z_3-invariant). This is verified numerically for all 6 elements
of S_3.

---

## Assumptions

The proof uses only:
1. The standard KS gamma matrices on the 8-dim taste space
2. The identification of the Higgs with the staggered mass condensate
3. Elementary properties of permutations acting on sums

No model assumptions, no gauge coupling, no fitted parameters, no
finite-size dependence.

---

## What Is Actually Proved

1. **Clifford algebra verified.** The KS gamma matrices G_1, G_2, G_3
   satisfy `{G_mu, G_nu} = 2 delta_{mu,nu} I` on the 8-dim taste space.
   Gamma_5 = i G_1 G_2 G_3 is hermitian with Gamma_5^2 = I.

2. **Z_3 action on KS generators is NOT simple cyclic permutation.**
   The taste permutation `P: (a_1,a_2,a_3) -> (a_3,a_1,a_2)` maps:
   - `P G_1 P^{-1} = D * G_2` (D = diagonal sign matrix from KS phases)
   - `P G_2 P^{-1} = D * G_3`
   - `P G_3 P^{-1} = D' * G_1`
   
   The sign matrices D arise because the KS phases `eta_mu(a)` are
   direction-dependent: `eta_1=1, eta_2=(-1)^{a_1}, eta_3=(-1)^{a_1+a_2}`.

3. **G_123 does NOT have a well-defined Z_3 charge.**
   Because of the sign matrices, `P G_123 P^{-1}` is not proportional
   to `G_123`. The entry-by-entry ratios alternate +1 and -1.
   G_123 decomposes into all three Z_3 sectors.

4. **eps(taste) IS exactly Z_3-invariant (charge 0).**
   `P eps P^{-1} = eps` because `(-1)^{a_1+a_2+a_3}` is symmetric
   under cyclic permutations. This is the physically relevant result.

5. **eps(taste) is S_3-invariant** (all 6 permutations preserve it).

6. **No Cl(3) basis element has pure Z_3 charge 1** under conjugation.
   All generators (G_1, G_2, G_3, G_12, G_13, G_23, G_123) mix under
   Z_3 conjugation. Only I and eps have pure charge 0.

7. **Abstract Clifford argument verified.** G_2 G_3 G_1 = G_1 G_2 G_3
   by anticommutation (two transpositions, net sign +1). All cyclic
   permutations of the triple product equal G_1 G_2 G_3; all
   anti-cyclic permutations equal -G_1 G_2 G_3. But this abstract
   invariance does NOT translate to Z_3-invariance of G_123 in the
   KS basis because the taste permutation introduces sign factors.

---

## What Remains Open

The staggered mass operator route to the Higgs Z_3 charge is blocked.
Four potential alternative routes:

1. **Different Higgs identification:** Perhaps the physical Higgs is
   not the eps(taste) condensate but a different lattice bilinear that
   carries Z_3 charge 1. The individual KS gamma matrices mix under
   Z_3, so charge-1 components exist in the algebra, but selecting
   one requires additional physical input.

2. **Dynamical Z_3 breaking:** Perhaps gauge interactions (SU(2)_L
   coupling) dynamically select charge 1 over charge 2. This would
   require a non-perturbative gauge calculation.

3. **EWSB pattern constraint:** Perhaps the specific SU(2)_L x U(1)_Y
   -> U(1)_EM breaking pattern forces the Higgs to align with a
   charge-1 component.

4. **Anomaly/topological constraint:** Perhaps anomaly cancellation
   or a topological argument fixes the Higgs Z_3 charge. Existing
   analysis showed anomaly cancellation alone is insufficient.

None of these has been developed. The CKM lane remains **bounded**.

---

## How This Changes The Paper

- CKM remains **bounded lattice support, not a quantitative CKM theorem**
- The Z_3 charge obstruction is now proved by two independent methods:
  algebraic (permutation symmetry of the sum) and numerical (equal
  charge-1 and charge-2 couplings on finite lattices)
- The algebraic proof is L-independent and exact, requiring no
  finite-size extrapolation
- An important subtlety is documented: the KS taste permutation does
  NOT simply permute the Cl(3) generators (it introduces direction-dependent
  sign factors from the KS phases)
- Paper-safe wording remains: "bounded lattice support"

---

## Commands Run

```
python3 scripts/frontier_ckm_higgs_from_gauge.py
```

Exit code: 0  
Result: PASS = 25, FAIL = 0
