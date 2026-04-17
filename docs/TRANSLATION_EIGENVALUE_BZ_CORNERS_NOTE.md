# Translation-Eigenvalue Theorem on BZ Corners of Z_L³

**Status:** AIRTIGHT — pure plane-wave algebra + discrete Fourier orthogonality
**Runner:** `scripts/frontier_translation_eigenvalue_bz_corners.py` (70/70 PASS)
**Reusability:** high — generalizes the hw=1 translation result of
`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` to the full 8-dim BZ-corner
spectrum.

## Theorem

Let Z_L³ (L even) be the periodic cubic lattice, and let T_μ for μ ∈ {1,2,3}
be the discrete translation on C^{L³} defined by T_μ |x⟩ = |x + e_μ⟩. Let
the BZ corner states be
```
|X_α⟩(x) = (1/√L³) exp(i π α · x) = (1/√L³) (−1)^{α·x}
```
for α ∈ {0,1}³. Then:

1. T_1, T_2, T_3 are unitary and pairwise commute.
2. The 8 BZ corner states {|X_α⟩ : α ∈ {0,1}³} are orthonormal.
3. Each |X_α⟩ is a simultaneous eigenstate of all three translations:
   ```
   T_μ |X_α⟩ = (−1)^{α_μ} |X_α⟩
   ```
4. The 8 distinct sign triples ((−1)^{α_1}, (−1)^{α_2}, (−1)^{α_3}) for
   α ∈ {0,1}³ exhaust the joint-eigenvalue spectrum on the 8-dim
   BZ-corner subspace of C^{L³}.

## Proof

1. Each T_μ permutes L³ lattice sites, so it is a permutation matrix
   (unitary). Translations in different directions commute on the
   commutative lattice Z_L³.
2. ⟨X_α | X_β⟩ = (1/L³) Σ_x (−1)^{(α+β)·x}. Factoring by components,
   each inner sum is 0 (L even, (α+β)_μ odd) or L ((α+β)_μ even).
   Hence ⟨X_α | X_β⟩ = δ_{α,β} for L even.
3. (T_μ |X_α⟩)(x) = |X_α⟩(x − e_μ) = (1/√L³) (−1)^{α·(x−e_μ)}
   = (−1)^{α_μ} · (1/√L³) (−1)^{α·x} = (−1)^{α_μ} |X_α⟩(x).
4. The 8 sign triples in {+1, −1}³ are all distinct, and match the 8
   BZ corners exactly.

QED.

## Relation to main

The note `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` on main gives
```
T_x = diag(−1, +1, +1),   T_y = diag(+1, −1, +1),   T_z = diag(+1, +1, −1)
```
as the translation operators restricted to the hw=1 subspace
{X_1 = (π,0,0), X_2 = (0,π,0), X_3 = (0,0,π)}.

This present theorem is the full 8-dim generalization, covering all
α ∈ {0,1}³ (including hw=0, hw=2, hw=3 corners). The existing hw=1
result is the restriction to Hamming-weight-1 α.

## Reusability

Cited wherever downstream work uses:
- BZ corner states as simultaneous translation eigenstates
- The α ↔ eigenvalue-triple correspondence
- Selection rules based on translation parity signatures
- Extensions from hw=1 generation algebra to other hw sectors

## Scope

Pure math on Z_L³ for L even. No downstream physics claim.

## Verification

```bash
python3 scripts/frontier_translation_eigenvalue_bz_corners.py
# Expected: TOTAL: PASS=70, FAIL=0
```
