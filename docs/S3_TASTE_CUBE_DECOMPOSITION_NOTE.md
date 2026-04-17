# S₃ Axis-Permutation Decomposition of the Taste Cube

**Status:** AIRTIGHT — Peter-Weyl character computation
**Runner:** `scripts/frontier_s3_action_taste_cube_decomposition.py` (57/57 PASS)
**Reusability:** high — characterizes the S_3-irrep content of C^8,
required for any S_3-invariance argument on the taste cube.

## Theorem

The symmetric group S_3 acts on C^8 = (C²)⊗³ by tensor-position
permutations: for π ∈ S_3,
```
U(π) |α_1 α_2 α_3⟩ = |α_{π⁻¹(1)} α_{π⁻¹(2)} α_{π⁻¹(3)}⟩.
```
Then:

1. π ↦ U(π) is a unitary representation of S_3 on C^8.
2. S_3 preserves Hamming weight; the orbit decomposition on the
   computational basis is 1 + 3 + 3 + 1.
3. On the two 1-dim sectors (hw=0 and hw=3), S_3 acts trivially (A_1).
4. On each 3-dim sector (hw=1 and hw=2), S_3 acts as the standard
   permutation representation, decomposing as A_1 ⊕ E.
5. As an S_3 representation,
   ```
   C^8 ≅ 4·A_1 ⊕ 2·E
   ```
   (4 copies of the trivial irrep, 2 copies of the 2-dim standard E;
   the 1-dim sign representation A_2 does NOT appear).

## Proof

Hamming weight is S_3-invariant (permuting bit positions preserves
the bit sum), giving (1) and (2). The 1-dim hw sectors carry A_1 because
they are literally fixed by S_3. For each 3-dim sector, S_3 acts
transitively, giving the natural permutation representation on 3 objects,
which decomposes as A_1 ⊕ E (standard result).

Explicit character computation on C^8:
- χ(e) = 8 (dim C^8)
- χ(2-cycles) = 4 (three 2-cycle elements in S_3, each with trace 4)
- χ(3-cycles) = 2 (two 3-cycle elements, each with trace 2)

Peter-Weyl multiplicities with S_3 character table:
```
m(A_1) = (1/6)(1·8 + 3·4 + 2·2) = 24/6 = 4
m(A_2) = (1/6)(1·8 − 3·4 + 2·2) = 0/6 = 0
m(E)   = (1/6)(2·8 + 0·3·4 − 1·2·2) = 12/6 = 2
```
Total: 4·1 + 0·1 + 2·2 = 8 ✓.

QED.

## Reusability

Cited wherever:
- A framework statement invokes "S_3 axis-permutation symmetry" on
  the taste cube
- Operators are analyzed for S_3 invariance (e.g., V_sel as a
  4·A_1-valued invariant)
- Irrep projectors are needed to block-decompose S_3-symmetric
  computations
- The absence of A_2 component is used (no sign-irrep structure in C^8)

## Relation to main

The V_sel selector derivation note on main uses "S_3 axis symmetry"
implicitly in constructing invariant quartic polynomials. This note
provides the explicit representation-theoretic decomposition that
tells you which operators can be S_3-invariant: the space of S_3-
invariant operators on C^8 is determined by the multiplicity of A_1
in End(C^8) ≅ C^8 ⊗ C^{8*} ≅ (4·A_1 + 2·E) ⊗ (4·A_1 + 2·E).

## Verification

```bash
python3 scripts/frontier_s3_action_taste_cube_decomposition.py
# Expected: TOTAL: PASS=57, FAIL=0
```
