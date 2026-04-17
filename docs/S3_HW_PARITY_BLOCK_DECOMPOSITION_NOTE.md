# S_3 Decomposition of the Hw-Parity Blocks

**Status:** AIRTIGHT — refines S_3 Invariant Operator Dimension with
an explicit block-by-hw-parity structure.
**Runner:** `scripts/frontier_s3_hw_parity_block_decomposition.py` (20/20 PASS)

## Classical results applied

- **Restriction of a G-representation to an invariant subspace**
  (standard rep theory; Serre, *Linear Representations of Finite
  Groups*, ch. 1).
- **Schur's lemma applied block-wise** to the restricted rep on each
  Z_2-grading component V_±.
- **Isotypic-multiplicity formula** dim End(V)^G = Σ m_i² applied on
  each block.

## Framework-specific step

- Combining the Batch 2 hw-parity projectors Π_± with the Batch 2
  S_3 decomposition, showing that S_3 commutes with Π_± and hence
  acts on each 4-dim block V_±; the restricted S_3 rep on each
  block is 2·A_1 ⊕ E.

## Theorem

Let Π_± = (1 ± Q) / 2 be the hw-parity projectors on C^8 (with
Q = S_1 S_2 S_3). Then:

1. **Per-block S_3 decomposition:** each 4-dim block V_± = Π_± C^8
   decomposes under S_3 as
   ```
   V_± ≅ 2·A_1 ⊕ E
   ```
   corresponding to one singleton S_3-orbit on Hadamard labels plus
   one three-orbit.

2. **Refined invariant-operator dimensions** (Schur's lemma):
   ```
   dim End(V_+)^{S_3}       = 2² + 1² = 5
   dim End(V_-)^{S_3}       = 2² + 1² = 5
   dim hom(V_+, V_-)^{S_3}  = 2·2 + 1·1 = 5
   dim hom(V_-, V_+)^{S_3}  = 2·2 + 1·1 = 5
   ```
   Total: 20, matching the S_3 Invariant Operator Dimension Theorem.

3. **Parity-preservation split:** among the 20 S_3-invariant operators,
   exactly 10 preserve hw-parity (in End(V_+) ⊕ End(V_-)) and exactly
   10 swap hw-parity (in hom(V_+, V_-) ⊕ hom(V_-, V_+)).

## Proof

(1) S_3 permutes Hadamard labels. Each parity block has 4 labels
forming (1 singleton) + (1 three-orbit) under S_3. The singleton is
A_1; the three-orbit is the standard permutation rep A_1 ⊕ E. Sum:
2·A_1 ⊕ E. Verified by explicit character computation on each block:
χ(e) = 4, χ(2-cycle) = 2, χ(3-cycle) = 1. Peter-Weyl decomposition
gives m(A_1) = 2, m(A_2) = 0, m(E) = 1.

(2) By Schur's lemma, for G-representations V = ⊕_r m_r V_r and
W = ⊕_r n_r V_r,
```
dim hom(V, W)^G = Σ_r m_r n_r.
```
Substituting the multiplicities from (1) yields the block dimensions.
Sum 5+5+5+5 = 20.

(3) Immediate from the partition 20 = (5+5) + (5+5).

QED.

## Reusability

Refines the S_3 Invariant Operator Dimension Theorem with an explicit
block structure. Useful when cataloguing operators that are
simultaneously S_3-invariant AND have a specific hw-parity profile
(preserving or swapping). Natural applications:

- Mass-matrix structures that respect axis symmetry
- CP-even / CP-odd operator classifications
- Effective interaction vertices with specific parity properties

## Verification

```bash
python3 scripts/frontier_s3_hw_parity_block_decomposition.py
# Expected: TOTAL: PASS=20, FAIL=0
```
