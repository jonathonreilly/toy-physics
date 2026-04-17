# Hamming-Distance Selection Rule for BZ-Corner Transitions

**Status:** AIRTIGHT — plane-wave algebra + Hamming-weight induction
**Runner:** `scripts/frontier_hamming_distance_selection_rule.py` (473/473 PASS)
**Reusability:** high — universal selection rule for polynomial operator
products on Z_L³ acting on BZ corners.

## Theorem

Let Z_L³ (L even) be the periodic cubic lattice, with BZ corner states
|X_α⟩ (α ∈ {0,1}³). Define the site-phase operators on C^{L³} by
```
(P_μ ψ)(x) = (−1)^{x_μ} ψ(x)   for μ ∈ {1, 2, 3}.
```

Then:

1. **Matrix element factorization:**
   ```
   ⟨X_β | P_μ | X_α⟩ = δ_{α ⊕ β, e_μ}
   ```
   (nonzero iff α and β differ only in the μ-th coordinate).

2. **Linear combinations:** for V = Σ_μ c_μ P_μ,
   ```
   ⟨X_β | V | X_α⟩ = c_μ δ_{α ⊕ β, e_μ}
   ```
   V connects α to β only if H(α ⊕ β) = 1, where H denotes Hamming weight.

3. **k-fold products:**
   ```
   ⟨X_β | P_{μ_1} ... P_{μ_k} | X_α⟩ = δ_{α ⊕ β, ⊕_i e_{μ_i}}
   ```
   The minimum k such that a product of k site-phase operators (in any
   direction choice) connects α and β equals the Hamming distance
   H(α ⊕ β).

4. **Consequence for hw=1 generation mixing:**
   The three hw=1 BZ corners {(1,0,0), (0,1,0), (0,0,1)} have pairwise
   Hamming distance exactly 2. Therefore single site-phase operators
   cannot mediate hw=1 ↔ hw=1 transitions; at least 2 insertions are
   required.

## Proof

1. Direct plane-wave algebra:
   ```
   ⟨X_β | P_μ | X_α⟩ = (1/L³) Σ_x (−1)^{β·x} · (−1)^{x_μ} · (−1)^{α·x}
                      = (1/L³) Σ_x (−1)^{(α + β + e_μ)·x}
                      = ∏_ν [(1/L) Σ_{x_ν} (−1)^{(α+β+e_μ)_ν · x_ν}]
   ```
   Each inner sum is 0 (if the coefficient is odd; L even) or 1 (even).
   So the matrix element is nonzero iff α + β + e_μ ≡ 0 mod 2, i.e.,
   α ⊕ β = e_μ.

2. By linearity from (1).

3. By induction on k. The product P_{μ_1} ... P_{μ_k} acts as multiplication
   by ∏_i (−1)^{x_{μ_i}} = (−1)^{(Σ_i e_{μ_i}) · x}. By the same
   character-orthogonality argument as (1), matrix element is nonzero
   iff α + β = Σ_i e_{μ_i} mod 2, i.e., α ⊕ β = ⊕_i e_{μ_i} (XOR of
   the chosen directions). The minimum |μ| achieving any given target
   α ⊕ β is the Hamming weight of α ⊕ β.

4. By enumeration: (1,0,0) ⊕ (0,1,0) = (1,1,0), Hamming weight 2.
   Similarly for the other two pairs.

QED.

## Reusability

Cited wherever downstream work makes claims about:
- Gauge-mediated transitions between BZ corners (the "single-link"
  gauge coupling in staggered fermion actions corresponds at the
  momentum-π modes to the P_μ operators analyzed here).
- Selection rules on lattice operator products.
- Minimum-order conditions for hw-sector-changing transitions.
- Taste-changing interactions in staggered fermion analysis.
- Framework-internal proofs that specific operator classes do NOT
  connect specific corner pairs.

## Scope caveats

The theorem is about products and linear combinations of the specific
site-phase operators P_μ defined above. Extensions to non-site-phase
operators (e.g., operators with non-constant phase profiles in position)
require separate analysis.

## Verification

```bash
python3 scripts/frontier_hamming_distance_selection_rule.py
# Expected: TOTAL: PASS=473, FAIL=0
```
