# K_R Tensor Carrier Vanishes on A1 Backgrounds

**Status:** AIRTIGHT — pure S_3 representation theory
**Runner:** `scripts/frontier_KR_A1_vanishing_proof.py` (30/30 PASS)
**Method:** Schur orthogonality theorem

## Theorem

On the seven-site star support, the tensor carrier
```
K_R(q) = (u_E(q), u_T(q), δ_A1(q) u_E(q), δ_A1(q) u_T(q))
```
with
```
u_E(q) = ⟨E_x, q⟩        (inner product with E irrep bright mode)
u_T(q) = ⟨T1_x, q⟩       (inner product with T1 irrep bright mode)
δ_A1(q) = A1 scalar coordinate
```
satisfies
```
K_R(q) = 0  for every q ∈ A1 subspace.
```

## Proof

The seven-site star has 7-dim S_3 representation decomposing into:
- 2 × A1 (trivial, 1-dim each): center + symmetric arms
- 1 × E (2-dim doublet): axis quadrupoles
- 1 × T1 (3-dim axis vector): axis differences

Dimension check: 2(1) + 2 + 3 = 7 ✓

**Schur orthogonality** (textbook): distinct irreps of a finite group
are orthogonal in any representation they both appear in.

For q ∈ A1, q is orthogonal to every vector in E and T1 irreps.
Therefore:
```
⟨E_x, q⟩ = 0
⟨T1_x, q⟩ = 0
```
Both components u_E(q) and u_T(q) of K_R vanish. The remaining
components δ_A1(q) u_E(q) and δ_A1(q) u_T(q) are products with
u_E and u_T, hence also zero. Therefore K_R(q) = 0.

## Verification

The runner explicitly constructs all 7 basis vectors, verifies
S_3 orthogonality (Schur theorem), and evaluates K_R on a family
of A1 backgrounds including:
- q = A1_center
- q = A1_arms  
- q = arbitrary linear combinations
- q = canonical q_A1(r) family (r = 0, 0.5, 1, √6)

All give K_R = 0 to machine precision.

Non-A1 perturbations (E_x, T1_x) give nonzero K_R as expected,
confirming the vanishing is specific to A1.

## Scope

This note proves ONLY the algebraic vanishing K_R(A1) = 0. The
APPLICATION of this result in downstream CKM arguments (selecting
1/√6 over 1/√7 in the |V_ub| amplitude) is a separate structural
identification and is NOT claimed here.

## What this is NOT

Not a derivation of V_ub. Not a derivation of the CP phase δ. Not
a derivation of any CKM magnitude. Just the algebraic theorem that
K_R restricted to A1 is identically zero.
