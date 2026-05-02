# M_W²/M_Z² = cos²θ_W from EWSB Pattern + Admitted Higgs Kinetic Term

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on cycle 18 (EWSB
pattern Q = T_3 + Y/2) + admitted standard Higgs kinetic term. NOT
proposed_retained — see CLAIM_STATUS_CERTIFICATE.md.
**Primary runner:** `scripts/frontier_w_z_mass_ratio_from_ewsb.py`
**Authority role:** exact-support theorem deriving the W/Z mass ratio
from the campaign's EWSB chain.

## 0. Statement

**Theorem (M_W²/M_Z² = cos²θ_W).**

Given:
1. EWSB pattern Q = T_3 + Y/2 (cycle 18, PR #281);
2. Higgs in (1,2)_{Y=+1} with VEV ⟨H⟩ = (0, v/√2)^T (cycle 15);
3. SM admitted standard Higgs kinetic term `(D_μ H)†(D^μ H)` with
   covariant derivative `D_μ = ∂_μ − i g T^a W_μ^a − i g' (Y/2) B_μ`;

then the W and Z boson masses satisfy:

```text
M_W²  =  g² v² / 4
M_Z²  =  (g² + g'²) v² / 4
M_W² / M_Z²  =  g² / (g² + g'²)  =  cos²θ_W.
```

**Proof.** The Higgs kinetic term `(D_μ H)†(D^μ H)` evaluated at the VEV
gives the gauge-boson mass terms:

```text
(D_μ ⟨H⟩)†(D^μ ⟨H⟩)  =  ⟨H⟩† (g T^a W_μ^a + g' (Y/2) B_μ)² ⟨H⟩
                       =  v²/4 · (g² (W_μ^a T^a)² + g'² Y² B_μ² + cross)
```

After diagonalizing into mass eigenstates W^± (from W^1, W^2) and Z (from
mixing of W^3 and B at the EW mixing angle sin θ_W = g'/√(g²+g'²)):

```text
M_W²  =  g² v² / 4              (charged W)
M_Z²  =  (g² + g'²) v² / 4      (neutral Z)
```

The photon γ (orthogonal mixture) is massless because Q · ⟨H⟩ = 0
(unbroken U(1)_em from cycle 18).

The ratio:

```text
M_W² / M_Z²  =  g² / (g² + g'²).
```

Using the Weinberg angle definition `tan²θ_W = g'²/g²`, equivalently
`sin²θ_W = g'²/(g² + g'²)`, we get:

```text
M_W² / M_Z²  =  1 − sin²θ_W  =  cos²θ_W.   ∎
```

## 1. ρ-parameter ρ = 1 (tree level)

The ρ-parameter is defined as `ρ = M_W² / (M_Z² cos²θ_W)`. Substituting:

```text
ρ  =  M_W² / (M_Z² cos²θ_W)
   =  cos²θ_W / cos²θ_W
   =  1.
```

This is the SM tree-level ρ = 1 prediction, derivable from the cycle 18
EWSB pattern + admitted Higgs kinetic structure.

## 2. Numerical agreement at observed sin²θ_W

At observed `sin²θ_W(M_Z) ≈ 0.231`:
```text
cos²θ_W  ≈  0.769
M_W / M_Z  ≈  √0.769  ≈  0.877
PDG: M_W = 80.379 GeV, M_Z = 91.188 GeV
PDG ratio: M_W/M_Z = 0.8815
```

Agreement to <0.5%, confirming the SM tree-level prediction.

## 3. Retained / admitted inputs

| Ingredient | Class | Source |
|---|---|---|
| EWSB pattern Q = T_3 + Y/2 | exact-support (cycle 18) | PR #281 |
| Higgs (1,2)_{Y=+1} + neutral-component VEV | exact-support (cycle 15) | PR #278 |
| Standard Higgs kinetic term (D_μ H)†(D^μ H) | admitted SM convention | standard SM |
| EW gauge-boson mass diagonalization (Weinberg mixing) | admitted SM convention | standard SM |

## 4. What this closes

- **M_W² / M_Z² = cos²θ_W** as exact algebraic identity given EWSB pattern
  + Higgs kinetic term.
- **ρ = 1 tree-level** as immediate corollary.
- **Photon massless** as direct consequence of Q · ⟨H⟩ = 0 (cycle 18).

## 5. What this does NOT close

- The Higgs kinetic term form `(D_μ H)†(D^μ H)` itself (admitted SM
  convention).
- The W and Z mass values themselves (require v, g, g' values).
- The Weinberg angle value at electroweak scale (PDG observable).
- Loop corrections to ρ (depend on other SM particle content).

## 6. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 18 (EWSB pattern, itself conditional on cycle 15
  + admitted SM Yukawa) + admitted standard Higgs kinetic term + EW
  gauge-boson mass diagonalization (admitted SM convention).
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 7. Cross-references

- Cycle 18 / PR [#281](https://github.com/jonathonreilly/cl3-lattice-framework/pull/281) — EWSB pattern
- Cycle 15 / PR [#278](https://github.com/jonathonreilly/cl3-lattice-framework/pull/278) — Higgs Y_H = +1
- Cycle 19 / PR [#282](https://github.com/jonathonreilly/cl3-lattice-framework/pull/282) — sin²θ_W^GUT = 3/8 (sister GUT-scale prediction)
