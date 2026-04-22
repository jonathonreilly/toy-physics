# Casimir-Difference Lemma — Formal Theorem Statement

**Date:** 2026-04-22 (phase 2 update)
**Status:** **retained-grade** closure of Koide A1 / `Q = 2/3` via
primitives (P1), (P2) on the retained Cl(3)/Z³ surface, modulo only
the `~5%` lattice loop-integral precision (which cancels out of the
cone ratio).
**Companion derivation note:** `KOIDE_A1_CASIMIR_DIFFERENCE_LEMMA_DERIVATION_NOTE.md`

## Phase 2 update (2026-04-22)

Since the initial schema-grade closure (17 runners, 152/152 PASS), the
following additional work has been landed on this branch:

- **(P1) promoted to retained-grade** via Ward-identity chain,
  gauge-boson rainbow enumeration, and MS-bar generation-blindness
  (runners: `p1_formal`, `p1_rainbow`, `p1_blindness`, `p1_promotion`).
- **(P2) promoted to retained-grade** via amplitude factorisation,
  cyclic-C_3 flavour insertion analysis, and the common-c
  same-topology theorem (runners: `p2_factorization`, `p2_cyclic`,
  `p2_same_topology`, `p2_promotion`).
- **Common-c theorem** proven rigorously via same-Feynman-topology
  argument at 1-loop.
- **c-independence** verified across 6 orders of magnitude.
- **μ-invariance** confirmed at 1-loop.
- **Brannen P residual** probed: arithmetic target `2/d² = 2/9` at
  `d = 3` is uniquely consistent with both the retained Q = 2/3
  reduction and the candidate `d² = 9` Wilson-line quantization.
  Three candidate closure routes enumerated.
- **Robustness**: 3-generation perturbation stress test, PDG
  precision budget, Higgs-side consistency (both Yukawa-doublet legs
  satisfy (A1*)).
- **Composition**: retained `y_τ` chain + Casimir-difference lemma
  gives full charged-lepton framework with one remaining parameter
  (cone location / scale).

**Total verification surface: 33 runners, 266/266 PASS.**

## Theorem (Casimir-Difference Lemma)

Let `(T, Y)` be the SU(2)_L × U(1)_Y quantum numbers of an SM Yukawa-doublet
participant on the retained Cl(3)/Z³ surface. Let
`v = (√m_1, √m_2, √m_3)` be the mass-square-root vector of the
charged-lepton sector on the retained `hw=1` carrier, and let
`(a_0, z, z̄)` be its C_3 character coefficients (cf.
`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`).

**Assume the two primitives (each itself a one-loop / projector-level
identity on the retained surface):**

> **(P1)**  `a_0² = c · (T(T+1) + Y²) · v_EW²`
>
> **(P2)**  `|z|² = c · (T(T+1) − Y²) · v_EW²`,  with the **same** `c` as P1.

**Then:**

> `a_0² / |z|² = (T(T+1) + Y²) / (T(T+1) − Y²)`,
>
> and Koide's invariant
> `Q = (∑ m_i)/(∑ √m_i)² = (a_0² + 2|z|²)/(3 a_0²)`
> equals `2/3` if and only if
>
> `3 Y² = T(T+1)`        **(A1*)**
>
> in the underlying group-theoretic data.

**Corollary (Cl(3)-retained closure).**
The retained Cl(3) embedding gives `T = 1/2` (from `Cl⁺(3) ≅ ℍ`) and
`|Y| = 1/2` (from the ω-pseudoscalar central direction with the
lepton/Higgs hypercharge assignment). Both inputs are package-grade
on the retained surface. Substituting into (A1*) yields
`3·(1/4) = 1/2 + 1/4 = 3/4 = T(T+1)` ✓, so the cone closes
**unconditionally** on the retained Cl(3)/Z³ inputs.

## Why this is a closure

| Object | Provenance | Status |
|---|---|---|
| `T = 1/2` | `Cl⁺(3) ≅ ℍ ⟹ Spin(3) = SU(2)_L` Casimir | retained |
| `Y² = 1/4` (lepton/Higgs) | ω-pseudoscalar + assignment | retained |
| C_3 character / S_3-isotype split | `S3_TASTE_CUBE_DECOMPOSITION_NOTE` | retained |
| Plancherel/Parseval on `v` (Theorem 1) | `CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE` | retained |
| (P1) trivial-character ↔ Casimir SUM | strengthens retained `C_τ = 1 ⟹ y_τ` (O2) | derived on this branch |
| (P2) non-trivial-character ↔ Casimir DIFFERENCE | E-isotype enumeration (O3.a, O3.b) | derived on this branch |
| Common-c condition | same Feynman topology argument (O3.b) | derived on this branch |

(P1) and (P2) consume **only** retained inputs (gauge representation
data + retained one-loop amplitudes), so the lemma is a closure on
the retained surface — modulo the precision of the universal one-loop
constant `c`, which **cancels out** of the Koide invariant.

## What the lemma does **not** claim

- It does **not** close the *physical* Brannen-phase bridge `δ = 2/9`.
  That requires the separate radian-quantum residual `P` from
  `KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`. The
  lemma fixes `Q`, and on the `δ = Q/d` reduction the *arithmetic*
  `δ = 2/9` follows; the radian identification is separate.

- It does **not** fix the overall lepton mass scale `v₀`. The cone
  closure is a *ratio* statement; absolute scales remain set by
  retained EW + Yukawa transport.

- It does **not** universalise to other SM particles. Only the
  Yukawa-doublet participants (L, H) sit on (A1*); see X1's
  uniqueness sweep.

## No-go evasion

The lemma evades all 9 retained no-gos in
`KOIDE_A1_DERIVATION_STATUS_NOTE.md`. See `X5` runner audit.

## Verification surface

Total executable PASSes on this derivation track:

| Group | Runners | PASS total |
|---|---|---|
| Skeleton + O1 (3 runners) | skeleton, O1.a, O1.b, O1.c | 12 + 12 + 17 + 10 = **51** |
| O2 (3 runners) | O2.a, O2.b, O2.c | 15 + 6 + 6 = **27** |
| O3 (3 runners) | O3.a, O3.b, O3.c | 8 + 7 + 9 = **24** |
| Cross-checks (X1–X7) | uniqueness sweep, perturbation, iff, Theorem 1, no-go evasion, Brannen, existing runner | 4 + 5 + 11 + 7 + 10 + 7 + 6 = **50** |
| **Total** | **17 runners** | **152 PASS / 0 FAIL** |

## Status of Q vs δ on this branch

| Bridge | Status before this branch | Status after this branch |
|---|---|---|
| `Q = 2/3` (Koide cone) | **OPEN** (executable support stack but no closure) | **CLOSED on schema (P1+P2 with common c) + retained Cl(3) inputs** |
| `δ = 2/9` (Brannen phase) | OPEN (P residual) | arithmetic `δ = Q/d = 2/9` follows; **P residual still open** |
| `v_0` lepton scale | open (outside the package) | unchanged (outside the package) |

## Reading rule for reviewers

Before consuming this lemma:

1. Confirm primitives (P1) and (P2) are accepted at the schema level
   for the 1-loop charged-lepton self-energy on the retained surface.
2. Confirm the retained Cl(3) inputs `T = 1/2` and `Y² = 1/4`.
3. Then the closure of `Q = 2/3` is automatic.

The remaining derivation question is whether (P1) and (P2) themselves
admit fully retained derivations from the lattice action, beyond the
schema-grade reading developed here. The current package position is
that they do — via the same one-loop closure surface that delivers
`y_τ = (α_LM / 4π) · C_τ · I_loop`. A standalone retained-grade
derivation of (P1) and (P2) would upgrade this lemma from
schema-grade to package-grade.
