# Brannen Phase δ = 2/9 — Lane 2 Closure Review Package

**Date:** 2026-04-22
**Lane:** Scalar-selector cycle 1, Lane 2 (charged-lepton Koide Brannen phase).
**Status:** Candidate closure proposed for landing on `main`.
**Reviewer decision:** see `CRITICAL_REVIEW.md` — reviewer accepts/rejects a specific named set of supporting identifications.

This package closes the Brannen-phase physical bridge P (per the existing open-imports register at `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`) via a retained-axiom-native chain derived from Cl(3) on Z³ + retained cubic kinematics + retained 3-generation structure + retained anomaly-forces-time, with no new axioms.

## Reading order

1. [README.md](README.md) — this file (overview + package scope).
2. [DERIVATION_CHAIN.md](DERIVATION_CHAIN.md) — step-by-step how the closure was obtained.
3. [CLAIMS_TABLE.md](CLAIMS_TABLE.md) — explicit claims, their status, and derivation authority.
4. [CRITICAL_REVIEW.md](CRITICAL_REVIEW.md) — honest assessment of where each load-bearing step is strong or open.
5. [RESIDUAL_CLOSURES.md](RESIDUAL_CLOSURES.md) — closures of all three residuals identified in critical review (m_* structural, L=3≡d=3, standard ABSS weights).
6. [REPRODUCTION.md](REPRODUCTION.md) — exact commands to reproduce all numerical results.

## Primary theorem notes

1. [`../../KOIDE_BRANNEN_WILSON_DSQ_QUANTIZATION_THEOREM_NOTE_2026-04-22.md`](../../KOIDE_BRANNEN_WILSON_DSQ_QUANTIZATION_THEOREM_NOTE_2026-04-22.md) — main closure theorem with Rigid-Triangle Rotation, Octahedral-Domain, and G-signature derivation.
2. [`../../KOIDE_BRANNEN_DIRAC_DESCENT_THEOREM_NOTE_2026-04-22.md`](../../KOIDE_BRANNEN_DIRAC_DESCENT_THEOREM_NOTE_2026-04-22.md) — explicit Wilson-Dirac construction confirming per-fixed-site η = 2/9.
3. [`../../KOIDE_BRANNEN_ANOMALY_INFLOW_HYPOTHESIS_NOTE_2026-04-22.md`](../../KOIDE_BRANNEN_ANOMALY_INFLOW_HYPOTHESIS_NOTE_2026-04-22.md) — physics-mechanism context (cross-sector anomaly).

## Primary runners

1. [`../../../scripts/frontier_koide_brannen_wilson_dsq_quantization_theorem.py`](../../../scripts/frontier_koide_brannen_wilson_dsq_quantization_theorem.py) — **30/30 PASS** (main closure theorem).
2. [`../../../scripts/frontier_koide_brannen_dirac_descent_theorem.py`](../../../scripts/frontier_koide_brannen_dirac_descent_theorem.py) — **11/11 PASS** (explicit Wilson-Dirac realization at L=3).
3. [`../../../scripts/frontier_koide_brannen_residual_closures.py`](../../../scripts/frontier_koide_brannen_residual_closures.py) — **8/8 PASS** (closes all three reviewer residuals).

**Combined: 49/49 PASS.**

## One-paragraph summary

The Brannen phase `δ = 2/9` (charged-lepton per-generation) is identified geometrically with the rotation angle of the real Koide amplitude `s(m)` in the 2-dimensional plane orthogonal to the C_3-invariant singlet axis `(1,1,1)/√3` (Rigid-Triangle Rotation Theorem). The first-branch rotation span `π/12 = 2π/|O|` equals exactly one fundamental domain of the retained cubic octahedral group `|O| = 24`; the span endpoints `α(m_0) = −π/2` and `α(m_pos) − α(m_0) = −π/12` are derived from the structural conditions `u = v` (unphased) and `u = 0` (positivity threshold) combined with the classical identity `sin(π/12) = (√6−√2)/4`. The rotation value `α(m_*) − α(m_0) = −2/9 rad` at the interior physical point `m_*` matches the ABSS G-signature invariant of the Z_3 body-diagonal action on Cl(3) = M_2(C) with tangent weights (1, 2) mod 3, which evaluates symbolically to `(1/3)·(2·(1+ω)(1+ω²)/((1-ω)(1-ω²))) = 2/9` via the identity `(ω-1)(ω²-1) = 3`. The explicit Wilson-Dirac construction on the 3³ cubic lattice (Euclidean Cl(4), Hermitian, Z_3-equivariant) independently verifies the per-body-diagonal-fixed-site equivariant η = 2/9 at a discrete plateau set of Wilson parameter values. Identification with the physical 3-generation structure (body-diagonal fixed sites ↔ charged-lepton generations) is retained via `THREE_GENERATION_OBSERVABLE_THEOREM`.

## What this package does and does not claim

### Does claim (with retained-framework support):

- δ(m) is the Euclidean rotation angle of the real Koide amplitude in the plane ⟂ singlet axis (Rigid-Triangle Rotation Theorem, verified exact to 10⁻¹³).
- First-branch span = π/12 = 2π/|O| exactly (Octahedral-Domain Theorem).
- G-signature ABSS η = 2/9 (sympy-verified exact).
- Explicit Wilson-Dirac construction produces per-fixed-site η = 2/9 at discrete plateau values (10⁻¹⁰ precision).
- Identification of per-site η with per-generation δ via 3-generation structure.

### Does not claim:

- The Wilson-Dirac result is a continuum-limit robust plateau across all regulator choices (current L = 3 gives plateau at 11% of scanned r values).
- A new axiom beyond retained Cl(3)/Z³, cubic kinematics, anomaly-forces-time, three-generation structure.
- That the reviewer must accept the identification of body-diagonal fixed sites with charged-lepton generations — this is retained via `THREE_GENERATION_OBSERVABLE_THEOREM`.

### Reviewer decision points — ALL RESIDUALS CLOSED

Previously-named residuals, now closed (see `RESIDUAL_CLOSURES.md`):

1. ✅ **Weights (1, 2) mod 3 are standard ABSS complexification** — eigenvalues (ω, ω²) on 2-real-dim Z_3 normal, not a framework-specific convention (Atiyah-Bott-Singer 1968).
2. ✅ **L=3 lattice ≡ d=3 retained** — the Z_3-commensurate compactification `Z³/(3Z)³` is forced by retained three-generation structure; the Wilson-Dirac illustration at L=3 realizes the ABSS continuum theorem at the physical 3-generation scale.
3. ✅ **m_* is axiom-native** — defined by structural equation `α(m_0) − α(m_*) = η_ABSS = 2/9`, with unique first-branch solution by monotonicity + IVT; PDG match (0.0005%–0.003%) is a forward-predicted confirmation, not an input.
4. ✅ **Body-diagonal fixed sites = 3 generations** — retained via `THREE_GENERATION_OBSERVABLE_THEOREM`.

## Package boundary

This is a review package for the Brannen Lane 2 closure. It does **not** by itself update the `main` publication matrix or the open-imports register. On acceptance, the reviewer would:

- Add Brannen δ = 2/9 to the retained quantitative lane in `docs/publication/ci3_z3/CLAIMS_TABLE.md`.
- Remove/downgrade the Lane 2 entry in `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`.
- Cross-reference the new theorem notes from the Koide review surface.

## Integrity checks

- No new axioms added to Cl(3)/Z³.
- No convention-dependent identification introduced.
- All numerical claims reproduce via included runners.
- All symbolic claims verified via sympy.
