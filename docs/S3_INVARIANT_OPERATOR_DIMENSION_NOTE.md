# Dimension of S_3-Invariant Operators on C^8

**Status:** AIRTIGHT — Schur's lemma applied to the S_3 decomposition of C^8
**Runner:** `scripts/frontier_s3_invariant_operator_dimension.py` (14/14 PASS)

## Classical results applied

- **Schur's lemma** (Schur 1905; Serre, *Linear Representations of
  Finite Groups*, ch. 2): for a finite group G and a G-module V with
  isotypic decomposition V = ⊕ m_i · ρ_i,
  dim_C End(V)^G = Σ_i m_i².
- **Character-theoretic classification of S_3 irreps**: the three
  irreps A_1 (trivial), A_2 (sign), E (2-dim standard) have
  dimensions 1, 1, 2.

## Framework-specific step

- Using the Batch 2 S_3 Axis-Permutation Decomposition
  C^8 ≅ 4·A_1 ⊕ 2·E as the input to Schur's lemma, giving
  4² + 0² + 2² = 20.

## Theorem

Let C^8 = (C²)⊗³ carry the S_3 axis-permutation action. Then
```
dim_C End(C^8)^{S_3} = 20.
```

## Proof

By the S_3 Taste-Cube Decomposition Theorem, C^8 ≅ 4·A_1 ⊕ 2·E as
S_3 representations (no A_2 component). By Schur's lemma, for any
G-representation V = ⊕_r m_r · V_r,
```
dim End(V)^G = Σ_r m_r².
```
Here m_{A_1} = 4, m_{A_2} = 0, m_E = 2, giving
```
dim End(C^8)^{S_3} = 4² + 0² + 2² = 20.
```

Verified numerically via the group-averaging projector
P(X) = (1/|S_3|) Σ_π U(π) X U(π)^†, which has rank 20.

QED.

## Examples of S_3-invariant operators

- Identity I_8
- Sum of cube-shifts S_1 + S_2 + S_3
- Product S_1 S_2 S_3 (= hw-parity operator up to sign)
- Each Hamming-weight projector P_hw for hw ∈ {0, 1, 2, 3}
- Hw-parity projectors Π_± = (1 ± S_1 S_2 S_3) / 2
- Arbitrary polynomials in the above

## Reusability

- Classifies which operators on C^8 can be S_3-symmetric
- Used in constructing S_3-invariant Hamiltonians, Yukawa matrices,
  CP-even operators
- Constrains framework claims that invoke S_3 symmetry: any such
  observable lives in this 20-dim algebra

## Verification

```bash
python3 scripts/frontier_s3_invariant_operator_dimension.py
# Expected: TOTAL: PASS=14, FAIL=0
```
