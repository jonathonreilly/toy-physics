# C₃[111] Cyclic-Permutation Action on All BZ Corners

**Status:** AIRTIGHT — pure combinatorial permutation algebra
**Runner:** `scripts/frontier_c3_cyclic_action_bz_corners.py` (32/32 PASS)
**Reusability:** high — extends main's hw=1 observable theorem to the full
8-dim taste cube; provides foundation for axis-cycle / Z_3 arguments.

## Classical results applied

- **Orbit–stabilizer theorem for finite group actions** (Burnside;
  textbook group theory, e.g. Dummit–Foote, *Abstract Algebra*,
  §4.1).
- **Cyclic-group action on a finite set** with orbit sizes dividing
  the group order |Z_3| = 3 (so orbits have size 1 or 3).
- **Conjugation action on generators**: U S_μ U^{-1} = S_{σ(μ)} is
  the standard "automorphism of the generating set" pattern.

## Framework-specific step

- Identification of the body-diagonal [111] axis cycle as the
  unitary U on C^8 = (C²)^⊗³ cyclically permuting the three tensor
  factors, and the corresponding orbit structure 1 + 3 + 3 + 1 on
  the 8 taste-cube basis states.

## Theorem

Let U be the unitary on C^8 = (C²)⊗³ implementing the axis cycle
(α_1, α_2, α_3) ↦ (α_3, α_1, α_2) on computational-basis labels.
Then:

1. U is unitary with U³ = I. Eigenvalues are {1, ω, ω²} with ω = exp(2πi/3).
2. U permutes the 8 computational-basis vectors with orbit structure
   1 + 3 + 3 + 1:
   - Fixed points: |000⟩ (hw=0), |111⟩ (hw=3).
   - Two 3-cycles: {|100⟩, |010⟩, |001⟩} (hw=1) and {|110⟩, |011⟩, |101⟩} (hw=2).
3. U commutes with each Hamming-weight projector; equivalently, U
   preserves the hw-sector decomposition C^8 = C^1 ⊕ C^3 ⊕ C^3 ⊕ C^1.
4. U conjugates the cube-shift operators cyclically:
   U S_μ U⁻¹ = S_{cyclic(μ)}.
5. The restriction of U to the hw=1 triplet {|100⟩, |010⟩, |001⟩}
   reproduces the 3-cycle X_1 → X_2 → X_3 → X_1 used in
   `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` on main.

## Proof

All parts by direct computation. σ : (α_1, α_2, α_3) ↦ (α_3, α_1, α_2)
is a permutation of {0,1}³ of order 3; U is the corresponding permutation
matrix on C^8. Eigenvalues of an order-3 unitary are roots of x³ − 1.
Hamming weight is preserved because σ just relabels bit positions.
Cube-shift transformation follows from tensor-position permutation:
S_μ has σ_x in position μ, and U⁻¹ → position cyclic(μ)⁻¹ = μ', so
U S_μ U⁻¹ has σ_x in position σ(μ). Explicit verification of the
hw=1 restriction matches the cycle already on main.

QED.

## Reusability

Cited wherever:
- Axis-cycle / C₃[111] arguments extend beyond the hw=1 triplet
- Z_3-center-phase analyses (CP phase structure)
- Block-diagonal structure of C_3-invariant operators
- Orbit-type classification of operators on C^8

## Verification

```bash
python3 scripts/frontier_c3_cyclic_action_bz_corners.py
# Expected: TOTAL: PASS=32, FAIL=0
```
