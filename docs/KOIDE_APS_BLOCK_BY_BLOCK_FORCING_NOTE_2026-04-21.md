# Delta Support Route Block-by-Block Forcing: APS η = 2/9 Verification

**Date:** 2026-04-21
**Status:** Strong executable support verification of the ambient APS route.
**Runner:** `scripts/frontier_koide_aps_block_by_block_forcing.py` — 29/29 PASS.
All checks are executable symbolic or numeric computations; no literal
`True` placeholders remain.

---

## Statement

Every building block of the ambient `η = 2/9` derivation via APS
topological robustness is verified executable on the admitted
Cl(3)/Z³ topological route — no hidden internal choice is made within that
route. This note does not by itself prove the remaining physical bridge
identifying the selected-line Brannen phase with the ambient APS invariant.

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

## ABSS applicability (every prerequisite is executable)

- **(h1)** PL smoothability obstruction groups π_i(PL/O) = 0 for
  i ≤ dim(PL S³ × R) = 4. The runner checks the standard table
  {π_0 = π_1 = π_2 = π_3 = π_4 = 0} (Cerf–Munkres), making the
  obstruction vanish by enumeration.
- **(h2)** S³ is parallelizable (as SU(2) Lie group) — TS³ is globally
  trivialized by three linearly-independent left-invariant fields. The
  runner exhibits these three fields as quaternion imaginary units and
  checks rank = 3. Then w_2(S³) = 0 ⟹ spin exists. Uniqueness follows
  from H^1(S³ × R; Z_2) = 0, which the runner derives from the known
  homology of S³ (simply connected ⟹ H_1 = 0).
- **(h3)** Morse-Bott is checked via `det(R_normal − I) = 3 ≠ 0`
  computed symbolically from (ω − 1)(ω² − 1) = 3.
- **(h4)** C_3 ⊂ SO(3) lifts to SU(2) as an explicit unit quaternion
  `q = cos(π/3) + sin(π/3) · (1,1,1)/√3 ·(i,j,k)`. The runner verifies
  (i) |q|² = 1, (ii) q³ = −1, confirming the 2:1 double cover.
- **(h5)** Composite: (h1) ∧ (h2) ∧ (h3) ∧ (h4) all verified
  executively, so the ABSS fixed-point formula applies.

## Why this answers the reviewer question "is η = 2/9 a choice?"

**No hidden internal choice is made on this route.** The retained kinematics fix p = 3 (from
C_3[111] cubic rotation) and the tangent weights (1, 2) (from
eigenvalues (ω, ω²)). The ABSS formula is a mathematical theorem.
The core identity (ζ − 1)(ζ² − 1) = 3 is an exact algebraic fact.

There is no alternative consistent construction under the admitted topological
data that would give a different ambient `η` value. The remaining open issue is
the physical-observable bridge `delta_physical = eta_APS`.
