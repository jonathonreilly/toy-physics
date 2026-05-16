# Assumption / Import Ledger

**Date:** 2026-05-16
**Loop:** koide-l5-spectral-triple-20260516

## Retained primitives (load-bearing OK)

These are audit-ratified retained-grade primitives on main. They may be used
as proof inputs:

| Primitive | Note | Role |
|---|---|---|
| Q(v) = 2/3 ⟺ NSC | `koide_q_two_thirds_z3_character_norm_split_recasting_theorem_note_2026-05-10` | scalar-eigenvalue ↔ Fourier-coefficient equivalence |
| Q(v) = 2/3 ⟺ LCC | `koide_lightcone_primitive_theorem_note_2026-05-10` | scalar ↔ operator-coefficient equivalence on Z_3-equivariant H |
| {H, Γ_χ} = 0 + λ ≠ 0 ⟹ ⟨v\|Γ_χ\|v⟩ = 0 | `koide_anticommuting_operator_derivation_theorem_note_2026-05-10` | algebraic implication; 2-dim characterization of such H |
| Z_3 character grading Γ_χ = (2/3)J − I | (same as above) | grading on the 3-generation triplet |
| 2-dim family H = (1/3)(1⊗h + h⊗1), Σh=0 | (same as above) | explicit parametrization of all anti-commuting Hermitian H on R³ |

## Imports that would need explicit ledger entry if used

These are admitted-context imports that the user wants AVOIDED in the
retained tier. If any agent or cycle uses one of these, it must be flagged
as `bounded_theorem` (import-bearing ceiling), not positive_theorem.

| Import | Where it would enter | Why it limits status |
|---|---|---|
| Lepton mass values (m_e, m_μ, m_τ from PDG) | Validation that v is the physical eigenvector | PDG numerical input — not retained |
| Standard Connes spectral triple axioms (orientability, finite-summability, etc.) | Used as comparator/grammar for the construction | external math import — bounded ceiling unless re-derived |
| Spectral action principle (Chamseddine-Connes 1996) | Justification for the bosonic action `Tr f(D²/Λ²)` | external math import — bounded ceiling unless re-derived |
| Real structure J on the finite spectral triple | Connes' reality axiom for KO-dimension | external math import — bounded ceiling |
| Charge conjugation / KO-dimension labels | Standard NCG machinery | external math import — bounded ceiling |
| Foot 1994 (Q = 2/3 prediction) | Comparator only | external comparator — never load-bearing for proof |

## Counterfactual pass (per assumption-import-audit.md reference)

For each hidden assumption in the spectral-triple route, ask: "what if this
is wrong, and what direction does the alternative open?"

### CF-1: γ-grading = Γ_χ assumption

**Assumption:** the spectral-triple γ-grading IS exactly the Z_3 character
grading Γ_χ = (2/3)J − I.

**What if wrong:** the grading is a different Z_2-grading (e.g., chirality
on a 2-spinor, or KO-dimension grading mod 2). Then the anti-commutation
constraint changes — Dirac would anti-commute with the new γ, not with Γ_χ.

**Direction:** might suggest H is constructed first (Z_2-graded), then
projected to the Z_3-equivariant subspace and only then asked to satisfy
LCC. Two-step structure.

### CF-2: D acts on R³ assumption

**Assumption:** the Dirac D acts on the same 3-dim space R³ as the
generation triplet.

**What if wrong:** D acts on a larger Hilbert space H = R³ ⊗ H_extra where
H_extra is a "spinor" or "KO" factor. Then Γ_χ ⊗ γ_KO is the grading. The
anti-commuting H on R³ is the Schur complement / partial-trace of D over
H_extra.

**Direction:** opens "tensored" constructions — Cl(3) Dirac on R³⊗C^2 or
R³⊗H_KO with appropriate γ.

### CF-3: Dirac is finite assumption

**Assumption:** D is a finite Hermitian matrix on a finite-dim Hilbert
space.

**What if wrong:** D is an unbounded operator on infinite-dim Hilbert space
(continuous spatial Dirac), with the 3-gen triplet only the finite
internal index. Then the anti-commuting H on R³ is the matrix part of a
direct-product Dirac D = D_x ⊗ I + I ⊗ H.

**Direction:** opens "Chamseddine-Connes" style infinite-dim spectral
triples where the finite part is just one factor of the construction.

### CF-4: 3-generation triplet is R³ vs C³

**Assumption:** the 3-gen triplet is real (R³), so Hermitian = real
symmetric, and h is a real 3-vector with Σh=0.

**What if wrong:** the 3-gen triplet is C³ (with complex structure), so
Hermitian includes complex H, and h is a complex 3-vector with Σh=0. The
search space is then 4-dim (2 complex parameters), not 2-dim.

**Direction:** opens the complex case. The retained Level 4 theorem
applies to BOTH real and complex Hermitian H. The 2-dim claim is for the
real case; complex case has 4-dim search space.

### CF-5: γ-grading order (Z_2 vs Z_3)

**Assumption:** γ is Z_2-graded (γ² = I), as in standard spectral triples.

**What if wrong:** γ is Z_3-graded (γ³ = I, e.g., R itself). Then
anti-commutation generalizes to "γ-twisted" commutation: D γ = ω γ D for
some ω. This is the "twisted spectral triple" / "modular spectral triple"
generalization.

**Direction:** opens twisted/modular spectral triple constructions. Could
be more natural for Z_3-equivariant systems. The retained Level 4 theorem
does NOT cover this case — only standard Z_2 anti-commutation.

## Counterfactual pass — implications

The 5 counterfactuals open 5 distinct routes for the agent fan-out:

- CF-1 → Agent on alternative γ-gradings + Schur complement to Γ_χ-anti-commuting H
- CF-2 → Agent on tensored R³⊗H_extra construction (Connes-Lott style)
- CF-3 → Agent on infinite-dim Chamseddine-Connes route
- CF-4 → Agent on complex 4-dim Hermitian H (broader search space)
- CF-5 → Agent on twisted/modular spectral triples (Z_3-twisted Dirac)

These map well to the 5-agent parallel attack pattern (special-forces).
