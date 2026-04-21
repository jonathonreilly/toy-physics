# I2/P Block-by-Block Forcing: APS η = 2/9 Verification

**Date:** 2026-04-21
**Status:** Retained-forced verification of the I2/P APS closure.
**Runner:** `scripts/frontier_koide_aps_block_by_block_forcing.py` — 34/34 PASS.

---

## Statement

Every building block of the δ = 2/9 rad derivation via APS
topological robustness is verified forced by the retained Cl(3)/Z³
axioms — no choice is made anywhere; every piece is determined by
the retained kinematic structure.

## Forced building blocks

| # | Block | Forced by |
|---|---|---|
| (a) | C_3[111] = 2π/3 rotation about (1,1,1)/√3 | Retained Z³ cubic kinematics; Rodrigues formula = cyclic permutation matrix P |
| (b) | Eigenvalues (1, ω, ω²) on R³ | det(R − λI) = 1 − λ³ uniquely; no other root of unity triple possible |
| (c) | Fixed locus: body-diagonal, codim-2 on S³ | rank(R − I) = 2 |
| (d) | Tangent weights (1, 2) mod 3 | Forced by transverse eigenvalues (ω, ω²) |
| (e) | ABSS equivariant fixed-point formula applies | Spin structure on S³ exists (π_1 = 0, w_2 = 0); PL-smoothable (Cerf, dim ≤ 6); normal Hessian non-degenerate (Morse-Bott) |
| (f) | Core algebraic identity (ω − 1)(ω² − 1) = 3 | Exact algebraic fact for primitive cube root of unity |
| (g) | Result: η = (1/3)(1/3 + 1/3) = 2/9 | Unique computation from (a)–(f) |
| (h) | Alternative weights/p give different η | Ruled out by retained (p, a, b) = (3, 1, 2) |

## Specific symbolic verifications

- **(a1)** Rodrigues rotation at 2π/3 about (1,1,1)/√3 **equals** the
  cyclic permutation P = [[0,0,1],[1,0,0],[0,1,0]] symbolically.
- **(b1)** Characteristic polynomial of R is exactly `1 − λ³`,
  factoring uniquely as (1 − λ)(ω − λ)(ω² − λ).
- **(c2)** Rank of (R − I) is 2, forcing fixed locus to be 1-dim
  (the body-diagonal line).
- **(f1)** (ω − 1)(ω² − 1) = 3 exactly (symbolic verification).
- **(g)** Alternative weight choices: η(1, 1, 3) = 1/9 ≠ 2/9,
  η(2, 2, 3) = 1/9 ≠ 2/9, only η(1, 2, 3) = η(2, 1, 3) = 2/9 — and
  only (1, 2) is consistent with the retained C_3 rotation eigenvalues.

## ABSS applicability

- **(h1)** PL S³ is smoothable (Cerf's theorem for dim ≤ 6).
- **(h2)** Spin structure on S³ × R exists and is unique up to
  isomorphism (S³ simply connected, w_2 = 0).
- **(h3)** Fixed locus is Morse-Bott: normal eigenvalues (ω, ω²) are
  non-unit, so the rotation is non-degenerate on the normal bundle.
- **(h4)** C_3 ⊂ SO(3) lifts to Spin(3) = SU(2), preserving spin
  structure.
- **(h5)** All ABSS prerequisites verified → formula applies.

## Why this answers the reviewer question "is η = 2/9 a choice?"

**No choice is made.** The retained kinematics fix p = 3 (from
C_3[111] cubic rotation) and the tangent weights (1, 2) (from
eigenvalues (ω, ω²)). The ABSS formula is a mathematical theorem.
The core identity (ζ − 1)(ζ² − 1) = 3 is an exact algebraic fact.

There is no alternative consistent construction under the retained
axioms that would give a different η value.
