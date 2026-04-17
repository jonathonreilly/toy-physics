# Hw-Graded Decomposition of End(C^8)^{S_3}

**Status:** airtight (Grind Program, Batch 5)
**Runner:** `scripts/frontier_s3_invariant_hw_graded_decomposition.py` (21/21 PASS)

## Framework object

The Batch 3 S_3-Invariant Operator Dimension theorem establishes
dim_C End(C^8)^{S_3} = 20 on the taste cube C^8 = (C²)^⊗³. The
Hamming-weight grading C^8 = V_0 ⊕ V_1 ⊕ V_2 ⊕ V_3 (dimensions
1 + 3 + 3 + 1) is preserved by the S_3 action, inducing a grading
on the invariant commutant.

## Theorem

The 20-dim S_3-invariant commutant decomposes by Hamming-weight
transitions as

    End(C^8)^{S_3}  =  D  ⊕  O

where

1. **D = hw-preserving S_3-invariants** (block-diagonal in hw):

        dim_C D  =  Σ_k dim_C End(V_k)^{S_3}  =  1 + 2 + 2 + 1  =  6.

   The contribution from each hw block V_k = m_{A_1}^{(k)} · A_1
   ⊕ m_E^{(k)} · E is m_{A_1}^{(k),2} + m_E^{(k),2}, giving
   1² + 0² = 1 for V_0, 1² + 1² = 2 for V_1 and V_2, 1² + 0² = 1
   for V_3.

2. **O = hw-changing S_3-invariants** (ordered pairs with j ≠ k):

        dim_C O  =  Σ_{j ≠ k} dim_C Hom(V_j, V_k)^{S_3}  =  14.

   The one-way (j < k) tally is
        (0,1): 1   (0,2): 1   (0,3): 1
        (1,2): 2   (1,3): 1   (2,3): 1
   summing to 7, doubled by the two orderings for a total of 14.

3. dim_C End(C^8)^{S_3} = 6 + 14 = 20, matching Batch 3.

4. Hermitian real dim preserves the split: 6 + 14 = 20 real
   parameters (6 hw-diagonal, 14 hw-off-diagonal).

## Proof sketch

(1)–(2) are Schur's lemma applied to each isotypic pair. Within a
single hw block V_k, commuting operators are determined by one
scalar per irrep, giving m_{A_1}^{(k),2} + m_E^{(k),2} complex
degrees of freedom. Between V_j and V_k, the dimension of the
intertwiner space is m_{A_1}^{(j)} · m_{A_1}^{(k)} + m_E^{(j)} ·
m_E^{(k)}. The isotypic multiplicities (m_{A_1}^{(k)}, m_E^{(k)})
= (1, 0), (1, 1), (1, 1), (1, 0) for k = 0, 1, 2, 3 follow from the
Batch 2 S_3 Axis-Permutation Decomposition of the Taste Cube. (3)
is arithmetic. (4) uses that the commutant is *-closed under
Hermitian conjugation.

## Verification

The runner (a) confirms that each of the two S_3 generators
(τ = (12) and σ = (123)) commutes with every hw projector Π_k
(Part 1), (b) recovers the isotypic multiplicities on each V_k via
the trace of the trivial-rep projector (Part 2), (c) solves the
commutator system on the 20-dim hw-diagonal subspace and confirms
a 6-dim null space, (d) solves it on the 44-dim hw-off-diagonal
subspace and confirms a 14-dim null space, (e) solves it on the
full 64-dim End(C^8) and confirms the 20-dim Batch 3 total.

## Reusability

- Refines the Batch 3 dim-20 theorem into an hw-graded structure.
- Separates mass-matrix-like (hw-preserving) operators from
  transition-like (hw-changing) operators within the S_3-invariant
  algebra.
- Used when a framework operator is known to respect hw grading
  (e.g. gauge operators preserving particle content) or to change
  hw by a specific amount (e.g. Yukawa-like hw-1 transitions).
- Companion to the Batch 3 S_3 Hw-Parity Block Decomposition
  (which splits 20 = 10 + 10 by hw-parity); this theorem splits
  20 = 6 + 14 by hw grading.
