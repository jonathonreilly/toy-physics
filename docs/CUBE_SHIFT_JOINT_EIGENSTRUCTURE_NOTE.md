# CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM: Cube-Shift Joint Eigenvalue Structure on C^8

**Status:** AIRTIGHT — pure linear algebra + Z_2³ character theory
**Runner:** `scripts/frontier_lego_A_cube_shift_eigenstructure.py` (69/69 PASS)
**Reusability:** high — cited wherever cube-shift eigenstructure is used

## Theorem

Let S_1, S_2, S_3 be the canonical one-step axis shifts on C^8 = (C²)^⊗3,
defined by
```
S_1 = σ_x ⊗ I ⊗ I,   S_2 = I ⊗ σ_x ⊗ I,   S_3 = I ⊗ I ⊗ σ_x.
```
Then:

1. Each S_μ is Hermitian and involutive (S_μ² = I). Eigenvalues are ±1.
2. [S_i, S_j] = 0 for all i, j.
3. The three operators admit a simultaneous eigenbasis on C^8
   consisting of 8 one-dimensional joint eigenspaces, indexed by
   s = (s_1, s_2, s_3) ∈ {±1}³.
4. The joint eigenstate with eigenvalue triple s is
   ```
   |ψ_s⟩ = (1/√8) Σ_{a ∈ {0,1}³} (∏_μ s_μ^{a_μ}) |a_1 a_2 a_3⟩.
   ```
5. The 8 joint eigenstates form an orthonormal basis of C^8
   (the Z_2³ Hadamard / character transform).

## Proof

1. Each S_μ is a tensor product of σ_x and two I's. σ_x is Hermitian
   and σ_x² = I; tensor products preserve these.
2. σ_x and I commute in disjoint tensor factors:
   [σ_x ⊗ I ⊗ I, I ⊗ σ_x ⊗ I] = σ_x·I⊗I·σ_x⊗I² − I·σ_x⊗σ_x·I⊗I² = 0.
3. Commuting Hermitian operators on finite-dim space always admit a
   simultaneous eigenbasis (standard spectral theorem).
4. Direct substitution: S_μ |ψ_s⟩ = s_μ |ψ_s⟩ verified by expansion.
5. Character orthogonality Σ_a (∏_μ s_μ^{a_μ}) (∏_μ s'_μ^{a_μ}) = 8 δ_{s,s'}
   is the standard orthogonality relation for Z_2³ characters χ_s(a)
   = ∏_μ s_μ^{a_μ}.

QED.

## Relation to main

The V_sel selector derivation note (`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`)
uses properties (1) and (2) (Hermiticity and commutativity) as standing
facts. CUBE-SHIFT JOINT-EIGENSTRUCTURE THEOREM extends the standing facts with (3)-(5), providing the
explicit joint eigenbasis and its character-orthogonality proof.

## Reusability

Cited wherever downstream work involves:
- Joint-eigenbasis parameterization of C^8
- Z_2³ character / Hadamard transform on the taste cube
- Basis translation between the computational basis |a⟩ and the
  momentum-like basis |ψ_s⟩
- Spectral decomposition of operators that are polynomials in the S_μ

## Scope

Pure linear algebra on C^8. No downstream physics claim is made.

## Verification

```bash
python3 scripts/frontier_lego_A_cube_shift_eigenstructure.py
# Expected: TOTAL: PASS=69, FAIL=0
```
