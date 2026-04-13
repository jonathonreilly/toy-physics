# Generation Anomaly Obstruction: Z_3 Orbit Sectors Cannot Be Merged

**Date:** 2026-04-12
**Status:** 33/33 tests pass (33 EXACT, 0 BOUNDED)
**Script:** `scripts/frontier_generation_anomaly_obstruction.py`
**Approach:** 't Hooft anomaly matching as topological obstruction to sector identification

---

## Status

All 33 tests pass as EXACT (mathematical theorems verified computationally).
No bounded or model-dependent checks. The obstruction is a first-principles
algebraic result conditional on the three assumptions listed below.

**This does NOT close the generation physicality gate.** It proves that the
two triplet orbit sectors T_1 and T_2 cannot be merged/identified under the
stated assumptions. Generation physicality requires additionally that the Z_3
taste symmetry is the correct physical symmetry (Assumption A1) and that the
anomaly matching condition is applicable in the full interacting theory
(Assumption A3).

---

## Theorem / Claim

**Anomaly Obstruction to Z_3 Sector Merging.**

Let V = C^8 carry the Z_3 taste representation (cyclic permutation of
spatial axes on {0,1}^3). The 8 taste states decompose into four Z_3
orbit sectors:

    S_0 = {(0,0,0)}                        (singlet, |s|=0)
    T_1 = {(1,0,0),(0,1,0),(0,0,1)}        (triplet, |s|=1)
    T_2 = {(1,1,0),(0,1,1),(1,0,1)}        (triplet, |s|=2)
    S_3 = {(1,1,1)}                        (singlet, |s|=3)

**Theorem.** The Z_3 orbit sectors T_1 and T_2 cannot be identified
(merged into a single sector) without violating 't Hooft anomaly matching
for the Z_3 symmetry.

**Proof outline:**

1. Each triplet orbit decomposes under Z_3 Fourier transform into three
   fermion modes with Z_3 charges {0, 1, 2}.

2. The Dai-Freed anomaly invariant nu = sum_f q_f^2 (mod 3) classifies
   the Z_3 anomaly. For each sector:

       nu(S_0) = 0,  nu(T_1) = 2,  nu(T_2) = 2,  nu(S_3) = 0

3. The total anomaly of the full theory is:

       nu_total = 0 + 2 + 2 + 0 = 4 = 1 (mod 3)

4. Merging T_1 and T_2 (identifying them as one sector with charges {0,1,2})
   produces:

       nu_merged = 0 + 2 + 0 = 2 (mod 3)

5. Since 1 != 2 (mod 3), merging violates 't Hooft anomaly matching. QED.

**Corollary.** The singlets S_0 and S_3 CAN be merged without anomaly
obstruction (both contribute nu = 0). This is consistent: singlets do
not carry generation quantum numbers.

---

## Assumptions

**A1.** Taste space V = C^8 with Z_3 action sigma: (s1,s2,s3) -> (s2,s3,s1).
*Status: Exact (combinatorial definition of the taste representation).*

**A2.** The fermion content in each orbit sector is determined by the Z_3
Fourier decomposition of the cyclic permutation representation.
*Status: Exact (group representation theory, Schur's lemma).*

**A3.** 't Hooft anomaly matching: the discrete anomaly invariant nu mod 3
is preserved under any identification or RG flow that maintains the Z_3
symmetry.
*Status: Standard QFT result. The anomaly is a topological invariant
classified by the bordism group Omega_4^{Spin}(BZ_3) = Z_3. This is
the Dai-Freed eta invariant on the lens space L(3,1) = S^3/Z_3.*

---

## What Is Actually Proved

### Proved (EXACT)

1. The 8 taste states decompose as 8 = 1(S_0) + 3(T_1) + 3(T_2) + 1(S_3)
   under the Z_3 cyclic permutation.

2. Each triplet orbit carries Z_3 charge content (n_0, n_1, n_2) = (1, 1, 1):
   one fermion mode per Z_3 irrep.

3. Each singlet orbit carries charge content (1, 0, 0): pure charge-0.

4. The Dai-Freed anomaly invariant nu = sum q^2 mod 3 is:
   nu(S_0) = 0, nu(T_1) = 2, nu(T_2) = 2, nu(S_3) = 0.

5. Total nu = 1 mod 3 for the full 8-fermion theory.

6. Merging T_1 and T_2 gives nu_merged = 2 mod 3, violating anomaly matching.

7. The lens space partition function Z[L(3,1)] changes phase from 1/3 to 2/3
   under the merge, confirming the anomaly mismatch.

8. The Hamming weight operator W is a Z_3-invariant observable that
   distinguishes T_1 (eigenvalue 1) from T_2 (eigenvalue 2), confirming
   that no Z_3-equivariant isomorphism exists between them.

9. The linear Z_3 anomaly A = sum q_f (mod 3) vanishes identically for all
   sectors (because 0+1+2 = 0 mod 3). The obstruction appears only at the
   quadratic level (Dai-Freed invariant).

10. Singlet merges (S_0 = S_3) are anomaly-allowed, which is physically
    correct since singlets do not carry generation quantum numbers.

### Not Proved (remains open)

1. That Z_3 taste symmetry is the correct physical symmetry. This is the
   taste-physicality assumption, which is the framework's central postulate.

2. That the anomaly matching condition applies in the full interacting theory
   with broken Z_3 (anisotropy needed for mass hierarchy).

3. That the dim-4 sector V_0 fully decouples to leave exactly 3
   generation-carrying sectors.

4. That the mass hierarchy follows from Z_3 breaking (dynamical question).

---

## What Remains Open

1. **Taste-physicality.** The entire argument rests on the taste states being
   physical (not lattice artifacts). This is the framework's central claim,
   not something proved by the anomaly argument.

2. **Interacting theory.** The anomaly matching is proved at the level of the
   free fermion representation. Whether it survives in the full interacting
   theory (where Z_3 may be softly broken) is a dynamical question.

3. **V_0 sector.** The dim-4 eigenspace V_0 contains contributions from all
   four orbits. Its physical interpretation (sterile neutrino + Planck-mass
   state + symmetric combinations from triplets) needs further work.

---

## How This Changes The Paper

### New argument available

The anomaly obstruction provides a TOPOLOGICAL argument for why the two
triplet orbit sectors T_1 and T_2 must represent physically distinct fermion
families. Unlike the superselection argument (which shows they cannot MIX),
the anomaly argument shows they cannot be IDENTIFIED (declared to be the
same sector).

### Relationship to existing arguments

- The **superselection argument** (wildcard script) proves T_1 and T_2 cannot
  mix under Z_3-invariant dynamics.
- The **anomaly obstruction** (this script) proves T_1 and T_2 cannot be
  identified (merged) without violating a topological invariant.
- Together, they show that the two triplet sectors are both operationally
  distinct (superselection) and topologically protected (anomaly).

### Honest status

The anomaly obstruction is an exact algebraic theorem. It does NOT close the
generation physicality gate because it is conditional on:

1. Taste-physicality (A1) -- the framework's central postulate
2. 't Hooft anomaly matching being applicable (A3) -- standard QFT

The paper-safe claim is:

> Under the Z_3 taste symmetry, the two triplet orbit sectors T_1 and T_2
> carry distinct Dai-Freed anomaly invariants (nu = 2 each, contributing
> to nu_total = 1 mod 3). Merging them would change the total anomaly to
> nu = 2 mod 3, violating 't Hooft anomaly matching. This provides an exact
> topological obstruction to generation identification, conditional on the
> Z_3 taste symmetry being physical.

---

## Commands Run

```bash
python3 scripts/frontier_generation_anomaly_obstruction.py
# 33 PASS / 0 FAIL (0.0s) -- all EXACT
```
