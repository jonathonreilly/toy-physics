# Cl(3) → SM Embedding: Master Synthesis Note

**Date:** 2026-04-19
**Status:** reviewed algebraic support synthesis on current `main`; all 95 checks pass; not a new accepted-input memo
**Claim boundary authority:** this note (synthesis); sub-theorems have individual notes
**Script:** `scripts/verify_cl3_sm_embedding.py`

---

## Executive Summary

Starting from the single framework axiom — local algebra `Cl(3)` on spatial substrate
`Z³` — the following algebraic support structure is available on current `main`:

| Structure | Origin | Status |
|-----------|--------|--------|
| SU(2)_weak algebra | `Cl⁺(3) ≅ ℍ` | support |
| U(1)_Y generator | pseudoscalar ω central in Cl(3,0) | support |
| `g₂² = 1/(d+1) = 1/4` | `dim(Cl⁺(3)) = 4` | support |
| `g_Y² = 1/(d+2) = 1/5` | `dim(Cl⁺(3) + {ω}) = 5` | support |
| Y eigenvalues +1/3 / −1 | P_symm base projector | support |
| Y tracelessness (precondition for anomaly cancellation) | `Tr(Y) = 0` | support |
| N_c = 3 | `dim(Z³) = 3` axes | support |
| SU(3)_c algebra | acts on sym 3D base of taste cube | support |
| `[SU(3), SU(2)] = 0` | tensor product base⊗fiber | support |
| `R_conn = 8/9` (leading order) | SU(N_c) adjoint fraction; Fierz confirms | support |
| sqrt(9/8) EW correction | 1/R_conn from Fierz | support |
| 3 generations | Z₃ orbit of hw=1 taste triplet | support |
| hw=1 Y spectrum {+1/3, +1/3, −1} | quark-like × 2 + lepton-like × 1 per orbit | support |
| L-sector det(H_L) ≥ 0 | Kramers degeneracy (T²<0 on chiral L-sector) — necessary but not sufficient for full A-BCC | support |

---

## Four Algebraic Targets Sharpened

### Blocker 1: g₂² = 1/(d+1) — algebraic origin, not direction counting

**Before:** g₂² = 1/(d+1) was taken as a postulate about "gauge directions."

**After:** `Cl⁺(3) ≅ ℍ` has exactly `d+1 = 4` generators `{I, e₁₂, e₁₃, e₂₃}`.
The SU(2) kinetic term normalizes to 1/(number of independent generators) = 1/4.

This is algebraically forced by the quaternionic structure of the even sub-algebra
of Cl(3). No counting or postulate required.

**Authority:** [CL3_SM_EMBEDDING_THEOREM.md](CL3_SM_EMBEDDING_THEOREM.md), Section D.

### Blocker 2: g_Y² = 1/(d+2) — omega central extension

**Before:** g_Y² = 1/(d+2) required an extra input.

**After:** The pseudoscalar `ω = Γ₁Γ₂Γ₃` is central in `Cl(3,0)` with `ω² = −I`.
It is not in `Cl⁺(3)` but is independent of all 4 even-subalgebra generators.
The extension `Cl⁺(3) + span{ω}` has exactly `d+2 = 5` independent elements.

The U(1)_Y coupling normalizes to 1/5 for the same reason g₂² normalizes to 1/4.

**Authority:** [CL3_SM_EMBEDDING_THEOREM.md](CL3_SM_EMBEDDING_THEOREM.md), Sections C, D.

### Blocker 3: R_conn = 8/9 — SU(N_c) Fierz

**Before:** `R_conn = 8/9` was derived geometrically from plaquette geometry, or
stated as a color-projection formula without first-principles derivation.

**After:** N_c = 3 is forced by `dim(Z³) = 3` spatial axes. For SU(3) with T_F = 1/2,
the Fierz completeness relation gives:

```
∑_a T^a_{ij} T^a_{kl} = (1/2)δᵢₗδₖⱼ − (1/(2N_c))δᵢⱼδₖₗ
```

The adjoint (non-singlet) fraction of the N_c×N_c matrix algebra is:
```
R_conn = (N_c²−1)/N_c² = 8/9
```

This is the leading-order algebraic value; O(1/N_c^4) ~ 1.2% corrections are bounded in
`RCONN_DERIVED_NOTE.md`. The sqrt(9/8) EW-color correction follows at the same order.

**Authority:** [CL3_COLOR_AUTOMORPHISM_THEOREM.md](CL3_COLOR_AUTOMORPHISM_THEOREM.md), Section D.

### Blocker 4: L-sector det(H_L) ≥ 0 — Kramers degeneracy

**Before:** `det(H) > 0` for the bilinear condensate operator was imposed as a
positivity assumption.

**After:** On the chiral L-sector `{|000⟩, |011⟩, |101⟩, |110⟩}`, the SU(2)
generators `J_i = (i/2)eᵢⱼ` satisfy an anti-unitary time-reversal symmetry
`T = J₂ · K` (K = complex conjugate) with:

```
T² = J₂ · J₂* = −(1/4)I₄ < 0
```

Kramers theorem for T² < 0: every eigenvalue of any Hermitian operator in this
sector must be doubly degenerate. Therefore any H_L in the span of L-sector SU(2)
generators has paired eigenvalues, and `det(H_L) = λ₁²λ₂² ≥ 0`.

The L-sector determinant positivity is a theorem on that restricted algebraic class.

**Scope boundary:** Kramers establishes `det(H_L) ≥ 0` on the chiral L-sector.
This is a **necessary but not sufficient** condition for full A-BCC (physical-sheet
selection C_base vs C_neg). The physical-sheet choice requires additional observational
grounding — two Sylvester-inertia basins (C_base signature (1,0,2) and C_neg signature
(2,0,1)) are both geometrically valid; T2K/NOvA exclusion of C_neg is the current
operational closure. Axiom-native derivation of the physical-sheet selector remains
open. See `DM_LEPTON_SYNTHESIS_NOTE_2026-04-19.md` §2.3.

**Authority:** [CL3_SM_EMBEDDING_THEOREM.md](CL3_SM_EMBEDDING_THEOREM.md) and
`scripts/verify_cl3_sm_embedding.py` Section J.

---

## Algebraic Structure Map

```
Z³ spatial substrate
    │
    ├─ 3 coordinate axes ──────────────────────────────► N_c = 3
    │       │                                                │
    │   staggered doubling                            SU(3)_c Fierz
    │       │                                                │
    │   taste cube C^8 = (ℂ²)^{⊗3}                  R_conn = 8/9
    │       │                                         sqrt(9/8) correction
    │       │
    │   local algebra Cl(3) on C^8
    │       │
    │       ├─ Cl⁺(3) = {I,e₁₂,e₁₃,e₂₃} ≅ ℍ
    │       │       │                    │
    │       │   su(2) generators      dim = 4 = d+1
    │       │   J_i = (i/2)eᵢⱼ            │
    │       │       │               g₂² = 1/(d+1)
    │       │   fiber realization
    │       │   Jf_i = I₄⊗σᵢ/2
    │       │       │
    │       │   [Y, Jf_i] = 0 ─────────► SU(2)×U(1) gauge structure
    │       │
    │       ├─ pseudoscalar ω = Γ₁Γ₂Γ₃
    │       │       │
    │       │   [ω, Γᵢ] = 0  (central)
    │       │   ω ∉ Cl⁺(3)
    │       │   dim(Cl⁺(3)+{ω}) = 5 = d+2
    │       │       │
    │       │   g_Y² = 1/(d+2)
    │       │
    │       └─ base/fiber split of C^8
    │               │
    │           P_symm (6D) + P_antisymm (2D)
    │               │
    │           Y = (+1/3)P_symm + (−1)P_antisymm
    │               │
    │           Tr(Y) = 0
    │
    └─ S₃ axis permutations
            │
        Z₃ cyclic subgroup
            │
        hw=1 orbit: {e₁,e₂,e₃}
            │
        3 generation candidates
        (identical SU(2)×U(1) charges)
```

---

## Numerical Verification Summary

Script: `scripts/verify_cl3_sm_embedding.py`

| Section | Description | Checks | Result |
|---------|-------------|--------|--------|
| A | Cl(3) anticommutation | 7 | 7/7 |
| B | Cl⁺(3) ≅ ℍ, su(2) algebra | 12 | 12/12 |
| C | ω central, dim = d+2 | 7 | 7/7 |
| D | Bare couplings g₂², g_Y² | 5 | 5/5 |
| E | Fiber SU(2) commutes with Y | 7 | 7/7 |
| F | Y eigenvalues +1/3 / −1 | 11 | 11/11 |
| G | S₃ on C^8, hw=1 = 3 gen | 14 | 14/14 |
| H | SU(3)_c, T_F=1/2, Fierz | 6 | 6/6 |
| I | N_c=3, R_conn=8/9 | 7 | 7/7 |
| J | A-BCC Kramers | 19 | 19/19 |
| **Total** | | **95** | **95/95** |

---

## Relation to Existing Framework Documents

| This theorem | Connects to |
|-------------|-------------|
| g₂² = 1/(d+1) | `MINIMAL_AXIOMS_2026-04-11.md`: g₂(v) = 0.6480 |
| g_Y² = 1/(d+2) | `MINIMAL_AXIOMS_2026-04-11.md`: g₁(v) = 0.4644 |
| R_conn = 8/9 | `RCONN_DERIVED_NOTE.md` (now has algebraic backing) |
| sqrt(9/8) | `YT_EW_COLOR_PROJECTION_THEOREM.md` (Fierz confirms) |
| Y = +1/3 / −1 | `NATIVE_GAUGE_CLOSURE_NOTE.md`: abelian factor |
| [SU(3),SU(2)] = 0 | `NATIVE_GAUGE_CLOSURE_NOTE.md`: gauge-structure backbone |
| 3 generations | `MINIMAL_AXIOMS_2026-04-11.md`: three-generation structure |
| L-sector det(H_L) ≥ 0 | Chiral condensate positivity via Kramers (L-sector only) |

---

## What Remains Bounded

The following are NOT claimed by this theorem:

- **Running couplings**: g₂(v), g_Y(v) retain their bridge budgets from
  `YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md`
- **Generation mass splitting**: CKM, Yukawa hierarchy require additional derivation
- **Full anomaly cancellation**: precondition `Tr(Y)=0` is verified; full Green-
  Schwarz mechanism is a separate computation
- **DM sector**: no claims made; DM stack is separately bounded
- **Downstream phenomenology**: all quantitative SM predictions inherit their
  individual note authorities

## Reading Rule

This master note provides the synthesis of the Cl(3) → SM embedding theorem.
This synthesis sharpens four algebraic targets on current `main`. Use the
individual sub-theorem notes as claim boundaries for those support statements.
Do not treat this packet as superseding [MINIMAL_AXIOMS_2026-04-11.md](MINIMAL_AXIOMS_2026-04-11.md),
the retained three-generation matter package, or the public chirality boundary.

Sub-theorem notes (all dated 2026-04-19, status: reviewed support):
- [CL3_SM_EMBEDDING_THEOREM.md](CL3_SM_EMBEDDING_THEOREM.md)
- [CL3_TASTE_GENERATION_THEOREM.md](CL3_TASTE_GENERATION_THEOREM.md)
- [CL3_COLOR_AUTOMORPHISM_THEOREM.md](CL3_COLOR_AUTOMORPHISM_THEOREM.md)
