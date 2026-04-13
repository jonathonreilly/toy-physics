# CPT Exact Preservation in the Cl(3) Staggered Framework

## Status

EXACT theorem on finite lattice. All checks pass (PASS=53 FAIL=0).

## Theorem / Claim

**Theorem (CPT Invariance).**
The staggered Cl(3) Hamiltonian on Z^3 with periodic boundary conditions
is exactly CPT-invariant: [CPT, H] = 0. All CPT-odd SME coefficients
vanish identically.

**Discrete symmetry pattern:**

| Symmetry | Action on H | Status |
|----------|-------------|--------|
| C        | H -> -H     | NOT a symmetry of H (spectral flip) |
| P        | H -> -H     | NOT a symmetry of H (spectral flip) |
| T        | H -> H      | IS a symmetry (H is real) |
| CP       | H -> H      | IS a symmetry |
| CT       | H -> -H     | NOT a symmetry |
| PT       | H -> -H     | NOT a symmetry |
| CPT      | H -> H      | IS a symmetry (EXACT) |

This pattern matches the Standard Model: C and P are individually
violated, CP is preserved at tree level, and CPT is exactly preserved.

## Assumptions

1. Cl(3) staggered framework on Z^3 with periodic boundary conditions.
2. Even lattice size L (required for parity to be well-defined).
3. No additional interactions beyond the free staggered Hamiltonian.

## What Is Actually Proved

### Exact (theorem-grade):

1. **C operator**: The sublattice parity epsilon(x) = (-1)^{x1+x2+x3}
   is a real, diagonal, involutory operator satisfying C H C = -H exactly.

2. **P operator**: Spatial inversion x -> -x mod L is a real, involutory
   permutation satisfying P H P = -H exactly.

3. **T operator**: Complex conjugation acts trivially on H because all
   staggered phases and hoppings are real: T H T^{-1} = H* = H.

4. **CPT combined**:
   - CPT * H * (CPT)^{-1} = C * P * H * P * C = C * (-H) * C = -(-H) = H.
   - [CPT, H] = 0 verified numerically to machine precision on L = 4, 6, 8.
   - All residuals are exactly 0.00e+00 (not just small -- identically zero).

5. **SME coefficients**: The CPT-odd part of H vanishes identically:
   - H^{odd} = (H - CPT*H*(CPT)^{-1})/2 = 0.
   - All direction-resolved a_mu coefficients = 0.
   - The Frobenius norm ||H^{odd}|| = 0 at every lattice size tested.

6. **Taste-space verification**: CPT invariance verified at 7 BZ points
   including all high-symmetry points and a generic point.

7. **Cl(3) automorphism**: The combined CP operator maps each KS gamma
   to minus itself (G_mu -> -G_mu), acting as the grading automorphism
   of the Clifford algebra. (CP)^2 = I.

## What Remains Open

1. Extension to the interacting theory (gauge fields, Yukawa couplings).
   The free-field CPT theorem proved here is necessary but not sufficient
   for the full interacting framework.

2. CP violation from CKM-type phases. The free staggered Hamiltonian has
   exact CP, but physical CP violation requires complex phases in the
   interaction sector. The framework must accommodate this without
   breaking CPT.

3. Connection to the CPT theorem in continuum QFT (Jost 1957, Streater-
   Wightman). The lattice proof is self-contained but the relationship
   to the axiomatic continuum proof should be clarified.

## How This Changes The Paper

This is a clean exact result that can appear in the paper's symmetry
section. The statement is:

> The staggered Cl(3) Hamiltonian on Z^3 is exactly CPT-invariant.
> C and P individually map H -> -H, while T acts trivially on the real
> Hamiltonian. The product CPT preserves H identically. All CPT-odd
> Standard-Model Extension coefficients vanish.

This is a useful structural consistency check: any framework claiming
to reproduce SM physics must have exact CPT. The Cl(3) staggered
framework achieves this automatically from the reality of the staggered
phases and the algebraic structure of C and P.

The individual C and P violation (both send H -> -H) is also
physically correct: it reflects the chiral nature of the staggered
fermion, which is the lattice origin of parity violation.

## Commands Run

```
python3 scripts/frontier_cpt_exact.py
# Exit code: 0
# PASS=53  FAIL=0
```
