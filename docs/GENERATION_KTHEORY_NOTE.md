# Generation K-Theory: Equivariant K-Theory Classification Attempt

## Status

**BOUNDED** -- The equivariant K-theory framework K_{Z_3}(T^3) does not
apply to the staggered Cl(3) Hamiltonian because the taste Z_3
permutation is not a dynamical symmetry of H(k) in the Kawamoto-Smit
basis.  The topological distinctness of sectors is already captured by
group theory (Z_3 charges, anomaly obstruction).  Generation physicality
remains open.

## Theorem / Claim

**Attempted claim:** The three Z_3 sectors of the staggered Cl(3)
Hamiltonian carry distinct classes in K_{Z_3}(T^3) = Z^{12}, providing
a topological obstruction to their identification.

**Actual result:** The prerequisite for equivariant K-theory -- that Z_3
acts as a symmetry of the Hamiltonian -- is NOT satisfied.  The
Kawamoto-Smit gamma matrices do not transform under the taste
permutation P: (s1,s2,s3) -> (s2,s3,s1).  Specifically:

- P Gamma_mu P^{-1} does not equal any Gamma_nu or -Gamma_nu.
- P H(k) P^{-1} != H(sigma(k)) at generic momenta.
- [H(k), P] != 0 even at Z_3-invariant momenta k = (a,a,a) (except k=0, pi).

## Assumptions

A1. Taste space V = C^8 with Z_3 action (s1,s2,s3) -> (s2,s3,s1).
    **Status: Exact** (combinatorial definition).

A2. Kawamoto-Smit gamma matrices for the Cl(3) Clifford algebra:
    G1 = sigma_x (x) I (x) I,
    G2 = sigma_y (x) sigma_x (x) I,
    G3 = sigma_y (x) sigma_y (x) sigma_x.
    **Status: Standard** lattice construction.

A3. Bloch Hamiltonian H(k) = sum_mu sin(k_mu) Gamma_mu.
    **Status: Standard** staggered fermion dispersion.

A4. Equivariant K-theory K_G(X) requires a G-action compatible with the
    Hamiltonian (either [H,g]=0 or g H(k) g^{-1} = H(g.k)).
    **Status: Standard** mathematical requirement.

## What Is Actually Proved

1. **EXACT (group theory):** The taste space {0,1}^3 decomposes under
   the Z_3 cyclic permutation into orbits 8 = 1+1+3+3.  The Z_3
   eigenspaces have dimensions (4, 2, 2).  The projectors P_0, P_1, P_2
   are orthogonal and complete.

2. **EXACT (obstruction):** The taste Z_3 permutation P does NOT commute
   with (or equivariantly relate to) the KS Bloch Hamiltonian.
   Numerically verified: ||P H(k) P^{-1} - H(sigma(k))|| ~ 4-6 at
   generic k.  Root cause: the nested KS gamma construction breaks the
   permutation symmetry.

3. **EXACT (conditional):** IF Z_3 were a symmetry of H(k), then
   K_{Z_3}(T^3) = Z^{12} = (Z^4)^3 would classify the system.  The
   invariants per sector would be (rank, three Chern numbers).  All
   Chern numbers vanish for the free staggered fermion.  So the only
   content would be (rank, irrep label) -- identical to what group
   theory already provides.

4. **EXACT (already known):** The sectors carry distinct Z_3 irrep
   labels.  No Z_3-equivariant unitary can map between sectors.  This
   was already established by the anomaly obstruction analysis.

## What Remains Open

1. **Generation physicality:** The gap between "algebraically distinct
   taste sectors" and "physically distinct fermion generations" is not
   closed by K-theory or by any existing analysis.

2. **Is there a different Z_3 action that IS a symmetry of H(k)?**
   The naive taste permutation fails, but there might exist a
   basis-changed or dressed Z_3 action that commutes with the
   Hamiltonian.  This would require finding U such that
   (U P U^{-1}) commutes with H(k) for all k.  This is not
   attempted here.

3. **Interacting theory:** Even if the free-fermion Z_3 could be
   promoted to a symmetry, interactions might break it.

## How This Changes The Paper

This analysis does NOT change the paper's claims.  It confirms that:

- The Z_3 orbit structure is a labeling fact, not a dynamical symmetry.
- The topological distinctness of sectors is already captured by the
  anomaly obstruction (which IS exact).
- The generation physicality gate remains open.

The paper-safe statement is unchanged:

> "exact 1+2 split; bounded 1+1+1 hierarchy model; generation
> physicality still open"

The K-theory attempt is documented as a clean negative result: the
framework does not apply due to the equivariance obstruction, and even
if it did, it would add no new invariants beyond what is already known.

## Commands Run

```
python3 scripts/frontier_generation_ktheory.py
```

Exit code: 0.  PASS=21 FAIL=0.
Exact checks: 19.  Bounded checks: 2.  Obstructions identified: 2.
