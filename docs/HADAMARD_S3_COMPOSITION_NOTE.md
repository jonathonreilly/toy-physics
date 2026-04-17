# Hadamard Basis: Simultaneous T_μ Eigenbasis + S_3 Label Action

**Status:** AIRTIGHT — composes Batch 1 (cube-shift + intertwiner) and
Batch 2 (S_3 decomposition + hw-parity).
**Runner:** `scripts/frontier_hadamard_s3_composition.py` (117/117 PASS)

## Theorem

Let |ψ_s⟩ = (1/√8) Σ_α (∏_μ s_μ^{α_μ}) |α⟩ for s ∈ {±1}³ be the
Hadamard basis of C^8. Let |ψ_s^lattice⟩ be its image in the BZ-corner
subspace of C^{L³} under the intertwiner Φ. Then:

1. **Simultaneous T_μ eigenbasis:** S_μ |ψ_s⟩ = s_μ |ψ_s⟩ on C^8 and
   T_μ |ψ_s^lattice⟩ = s_μ |ψ_s^lattice⟩ on BZ corners.

2. **Hw-parity diagonalization:** the operator Q = S_1 S_2 S_3 (or
   T_1 T_2 T_3 on BZ corners) has eigenvalue s_1 s_2 s_3 ∈ {±1} on
   |ψ_s⟩. The projectors Π_± = (1 ± Q)/2 each have rank 4.

3. **S_3 label action:** U(π) |ψ_s⟩ = |ψ_{π · s}⟩ where
   (π · s)_μ = s_{π^{-1}(μ)}.

4. **Hw-parity is S_3-invariant:** the product s_1 s_2 s_3 is invariant
   under permutations of its factors; hence U(π) commutes with Π_±.

## Proof

1. Direct substitution + Cube-Shift Joint-Eigenstructure Theorem.
2. Product of single-factor eigenvalues.
3. Direct computation using the Hadamard formula + U(π) action on
   computational basis: U(π) relabels α by π, which by substitution
   of variables relabels s by π.
4. The product s_1 s_2 s_3 is a symmetric polynomial in its factors,
   hence invariant under any permutation.

QED.

## Composition role

Composes:
- Cube-Shift Joint-Eigenstructure Theorem (Batch 1)
- Site-Phase / Cube-Shift Intertwiner Theorem (Batch 1)
- S_3 Taste-Cube Decomposition (Batch 2)
- Hamming-Weight Parity Conservation (Batch 2)

into a unified block-diagonalization picture where each hw-parity
block is a 4-dim S_3-invariant subspace.

## Reusability

- Block-diagonalizes hw-parity-preserving operators in a canonical
  orthonormal basis
- Makes S_3 symmetry manifest as label permutation for calculations
  in the Hadamard basis
- Connects C^8 (abstract cube) and C^{L³} (lattice) pictures while
  respecting both S_3 and hw-parity

## Verification

```bash
python3 scripts/frontier_hadamard_s3_composition.py
# Expected: TOTAL: PASS=117, FAIL=0
```
