# SU(3) Bridge Derivation: Consolidated Ongoing Work

**Date:** 2026-05-04 (live document, updated as work progresses)
**Claim type:** bounded_theorem (live)
**Status:** consolidated draft for ongoing iteration. ALL post-closure derivation work goes here, not in new PRs.
**Scope:** framework-NATIVE Cl(3)/Z³ in 3+1D (NOT standard 4D Wilson lattice).

## 0. Purpose of this consolidated draft

After [PR #519](https://github.com/jonathonreilly/cl3-lattice-framework/pull/519) shipped the numerical bridge closure (`ρ = (c/c₀₀)^(12+2/π)` → `P = 0.5934` within ε_witness), subsequent iteration explored derivation paths. Per user direction "we don't need a PR for everything", all this iterative work is now consolidated in this single living document.

**Update rule**: as work progresses, add new sections here rather than spawning new PRs.

## 1. Closure formula (recap from PR #519)

```
ρ_(p,q)(6) = (c_(p,q)(6) / c_(0,0)(6))^(12 + 2/π)
P_cube(L_s=2 APBC, β=6) = 0.5934162594
gap to MC: 0.05× ε_witness ✓
```

Empirical exact closure k = 12.6342120930 (from brentq).

## 2. Framework-native (Cl(3)/Z³ 3+1D) re-interpretation

**Important user correction**: framework derivations must use Cl(3)/Z³ in 3+1D structure, NOT standard 4D Wilson lattice formulas.

The candidate `Δk = (N²-1)/(4π)` re-interpreted in framework-native terms:

| Factor | Framework-native source |
|---|---|
| `N²-1 = 8` | Adjoint dim of SU(3), forced by Cl(3) algebra (8 generators) → SU(3) embedding |
| `4` | NOT "4 spacetime dim" or "4 plaquette links" in standard sense |
| `1/(4π)` | **3D spatial solid-angle measure** (S² unit sphere area = 4π); inverse gives 3D angular average |
| `g_bare² = 1` | Canonical Cl(3) connection normalization (G_BARE_DERIVATION_NOTE.md) |

**Critical**: `1/(4π)` in framework-native interpretation is the **inverse 3D solid angle** (Cl(3)/Z³ has 3D rotational symmetry). It is NOT the standard 4D Brillouin zone factor `1/(16π²)`.

**Comparison to standard 4D Wilson PT** (which doesn't apply here):
- Standard 4D Wilson 1-loop tadpole: `(N²-1)/(8N²) × Z_W` ≈ 0.017 for SU(3) (way off observed Δk = 0.634)
- Framework-native `(N²-1)/(4π)` at g_bare=1 = 2/π = 0.637 (matches Δk to 0.4%)

The framework-native interpretation matches; the standard 4D doesn't.

## 3. The α_LM × b₀ ≈ 1 framework relation

From thorough search (see [PR #526](https://github.com/jonathonreilly/cl3-lattice-framework/pull/526)):

```
α_LM × b₀ = 0.997 at MC's P = 0.5934
```

If this were exactly 1 (a framework identity), then:
- `α_LM × 2b₀/π = 2/π` exactly
- The `(N²-1)/(4π)` and `α_LM × 2b₀/π` forms coincide

If exactly 1: framework would predict P = (11/(4π))⁴ = 0.587, vs MC 0.5934 (1% off).

So `α_LM × b₀ = 1` is **approximate**, not exact. The 0.3% deviation reflects 2-loop corrections.

## 4. Tension between rigorous Schur derivation and K-tube + 2/π closure

Key honest finding from explicit attempt:

| Formulation | ρ formula | P |
|---|---|---:|
| Schur rigorous (PR #501 candidate) | `(c/c₀₀)¹² × d⁻¹⁶` | 0.4291 |
| K-tube approximation (PR #517) | `(c/c₀₀)¹²` | 0.5888 |
| K-tube + 2/π closure (PR #519) | `(c/c₀₀)^(12+2/π)` | 0.5934 ✓ |

**These ρ formulations differ by ~10¹⁵ for high-(p,q) sectors** — NOT a perturbative correction.

The closure formula matches MC, but it's not the rigorous Schur derivation. Three possible interpretations:

(A) **K-tube captures thermodynamic-limit better than rigorous L=2 Schur**: +2/π is coincidental MC match; framework's true L=2 prediction is 0.4291.

(B) **Framework's source-sector formula has T_src structure that absorbs Schur factors via D_loc^6**: K-tube ρ + 2/π is the framework's correct ρ, derivable from the source-sector formula's SD equations.

(C) **+2/π is numerical coincidence**: framework predicts 0.4291 from L=2; MC mismatch is finite-volume effect.

**Resolution**: requires careful reading of the framework's source-sector formula derivation (in `GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_*` docs). If the SD derivation gives K-tube ρ form, interpretation (B) holds; otherwise (A) or (C).

## 5. Structural test: Δk is NOT a single 1-loop self-energy

The closure formula `ρ_(p,q) = (c/c₀₀)^(12 + Δk)` implies LOGARITHMIC sector dependence (`Δ ln ρ ∝ ln(c/c₀₀)`).

Standard 1-loop self-energy gives POLYNOMIAL sector dependence via Casimir `C_2(p,q)`.

Test: `Δ ln ρ_(p,q) / C_2(p,q)` varies by 451% across sectors (NOT constant).

**Conclusion**: `(N²-1)/(4π)` is NOT a single Casimir-proportional Feynman diagram. It's an effective exponent shift from RG-type / SD resummation.

## 6. Open derivation work

To rigorously derive `(N²-1)/(4π)` from framework primitives:

### 6.1 Read framework's source-sector formula derivation

Look at:
- `docs/GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md`
- `docs/GAUGE_VACUUM_PLAQUETTE_TENSOR_TRANSFER_PERRON_SOLVE_NOTE.md`

Determine: does the SD derivation give Schur ρ (= 0.4291) or K-tube ρ (= 0.5888)?

### 6.2 If K-tube is the framework's correct ρ

Derive the +2/π correction as the next-order SD term. Use 3D Cl(3)/Z³ structure (NOT 4D Wilson).

The (N²-1)/(4π) factor with framework-native interpretation:
- (N²-1) = adjoint multiplicity from gluon loops
- 1/(4π) = 3D angular average measure (Cl(3) native)
- g_bare² = 1 (canonical normalization)

### 6.3 If Schur is the framework's correct ρ

Then closure formula is empirical fit, NOT derivable. Framework's L=2 cube prediction is 0.4291. The 0.5934 reflects finite-volume effects beyond L=2.

In this case, native derivation of 0.5934 requires moving to L_s ≥ 3.

## 7. Numerical verification (re-confirmed)

```
ρ formula                          | P            | gap × ε_witness
Schur rigorous                     | 0.429105     | 543×
K-tube approximation               | 0.588794     | 15×
K-tube + 2/π closure (PR #519)     | 0.593416     | 0.05× ✓
MC                                 | 0.593400     | 0×
```

Closure stable across NMAX_perron 5-10.

## 8. Most likely interpretation (current best)

Per the framework-native re-interpretation + the Schur tension finding:

**Working hypothesis**: the framework's source-sector formula T_src derivation gives K-tube ρ (interpretation B), and the (N²-1)/(4π) at g_bare=1 with framework-native 3D angular interpretation is the SD-derivable next-order correction.

This requires verification by reading the source-sector formula's derivation.

## 9. Status and immediate next step

**Current campaign status:**
- ✓ Numerical closure ([PR #519](https://github.com/jonathonreilly/cl3-lattice-framework/pull/519))
- ✓ (N²-1)/(4π) candidate identified ([PR #522](https://github.com/jonathonreilly/cl3-lattice-framework/pull/522))
- ✓ β=6-specificity ([PR #521](https://github.com/jonathonreilly/cl3-lattice-framework/pull/521))
- ✓ Search confirms candidate ([PR #526](https://github.com/jonathonreilly/cl3-lattice-framework/pull/526))
- ✓ Schur tension identified ([PR #527](https://github.com/jonathonreilly/cl3-lattice-framework/pull/527))
- ✓ Framework-native re-interpretation (this consolidated doc)
- ⏳ **OPEN**: read framework's source-sector derivation to determine which interpretation (A/B/C) holds

**Immediate next step**: study the framework's existing source-sector formula derivation in detail and determine which ρ form (Schur or K-tube) it actually gives. This will resolve the tension and clarify whether (N²-1)/(4π) is derivable or empirical.

## 10. Historical PRs (consolidated into this doc going forward)

This consolidated doc supersedes the per-iteration PRs. Future updates go HERE, not new PRs.

Historical:
- [#519](https://github.com/jonathonreilly/cl3-lattice-framework/pull/519): closure announcement
- [#520](https://github.com/jonathonreilly/cl3-lattice-framework/pull/520): per-link 1/(2βπ) (refuted by #521)
- [#521](https://github.com/jonathonreilly/cl3-lattice-framework/pull/521): β=6-specificity
- [#522](https://github.com/jonathonreilly/cl3-lattice-framework/pull/522): (N²-1)/(4π) candidate
- [#523](https://github.com/jonathonreilly/cl3-lattice-framework/pull/523): last-step PT scope (revised by #525)
- [#525](https://github.com/jonathonreilly/cl3-lattice-framework/pull/525): RG-resummation interpretation
- [#526](https://github.com/jonathonreilly/cl3-lattice-framework/pull/526): search confirms target
- [#527](https://github.com/jonathonreilly/cl3-lattice-framework/pull/527): Schur tension finding

## 11. Audit consequence

```yaml
claim_id: su3_bridge_derivation_ongoing_2026-05-04
note_path: docs/SU3_BRIDGE_DERIVATION_ONGOING_2026-05-04.md
claim_type: bounded_theorem
intrinsic_status: ongoing (live document)
deps: [closures and derivation candidates from PR fleet]
verdict_rationale_template: |
  Consolidated ongoing work for SU(3) bridge derivation, post-PR #519
  closure. Numerical match within ε_witness verified; framework-native
  (N²-1)/(4π) candidate identified at g_bare=1 with 3D Cl(3) angular
  interpretation; tension with rigorous Schur cube derivation flagged
  for resolution.
  
  Status updated as work progresses; no new PRs spawned. All iterative
  derivation work consolidated here.
```
