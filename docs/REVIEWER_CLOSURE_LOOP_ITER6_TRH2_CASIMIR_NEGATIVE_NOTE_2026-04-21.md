# Reviewer-Closure Loop Iter 6: Tr(H²) Casimir Attack on N1 — Negative

**Date:** 2026-04-21
**Branch:** `evening-4-21`
**Status:** **Negative.** Tr(H²) at the afternoon-closure point is
not a clean retained simple value (deviation 5.9×10⁻⁴ from 5√2).
The three-scalar-Casimir attack path for deriving N1 is ruled out.
**Runner:** `scripts/frontier_reviewer_closure_iter6_trH2_casimir_attack.py`
— 0/3 PASS (the 3 FAILs are the hypothesis being disproven).

---

## Attack

Per user discipline "do not leave N1 until closed at Nature-grade":
iter 6 is a third distinct fresh attack on N1 (`δ·q_+ = SELECTOR²`).

Previous iters:
- iter 4: retained Atlas theorems alone don't force N1 (Path 1 ruled
  out), SELECTOR-quadrature pinpointed as missing retained piece.
- iter 5: joint N1+N2 polynomial attack. N2/N3 reduce to N1;
  N1 is primitive — not derivable from (a)+(b)+(c).

**Iter 6 fresh angle**: if Tr(H²) at the afternoon-closure point is a
retained simple value, the three-Casimir set {Tr(H), Tr(H²), det(H)}
uniquely determines H's spectrum, and N1 might follow as a
consequence.

## Method

Compute `Tr(H²)` symbolically as a polynomial in `(m, δ, q_+)`.
Evaluate at the afternoon-closure chamber point where
`m = 2/3, δ·q_+ = 2/3, det(H) = E2 = √8/3`. Compare to a broad
set of retained simple combinations (5√2, E1² · 2 + ..., 64/9,
2π, ...).

## Findings

```
  Tr(H²)_closure (numerical) = 7.0716577843
  Closest retained candidate: 5√2 = 7.0710678119
  Deviation                  = 5.900 × 10⁻⁴  (0.0083 %)
```

- At `< 1e-6` precision: **FAIL**.
- At `< 1e-4` precision: **FAIL**.
- At `< 1e-2` precision: would pass (value is "close to" 5√2 at 0.08%).

So `Tr(H²)_closure` is NOT a clean retained simple value. The
3-Casimir attack for deriving N1 is ruled out.

## Structural reason

`Tr(H²)` is a quadratic form in (m, δ, q_+) with specific cross-term
structure (I computed: `3m² + 6δ² + 6q_+² + 4mq` plus linear and
constant terms from H_base). Under `m = 2/3` and `det(H) = E2`,
δ_c is the root of an irreducible polynomial in `δ` (iter 5 verified
this polynomial has messy ℤ[√2, √3, √6] coefficients). `Tr(H²)` at
this algebraic `δ_c` is another algebraic number — not a clean
retained simple.

## What this rules out and what remains

**Ruled out** (in addition to iters 4 and 5): the 3-Casimir
{Tr(H), Tr(H²), det(H)} route for deriving N1.

**Remaining open**:
- N1 still primitive, not derivable from current retained toolkit.
- Non-trivial retained constraints on H beyond scalar Casimirs
  would be needed (e.g., eigenvector-level identities, non-scalar
  functionals, topological invariants).
- OR: accept that N1 is a framework conjecture, not a theorem.

## Honest Nature-grade assessment (updated after iter 6)

After three distinct attacks (iters 4, 5, 6) on N1, all producing
negative results within my toolkit:

- **N1 is un-derivable** from the retained Atlas theorems
  (active-affine, Z_3 doublet-block, carrier normal-form) and
  from natural scalar Casimirs of H. It is a **primitive
  retained identity** on the PMNS chart, verified observationally
  to 0.16 % at PDG-pinned closure.

- Deriving N1 would require **external physics/framework input**
  beyond what's currently available: a retained SELECTOR-quadrature
  theorem, or a new non-scalar retained structure.

## Loop termination — final verdict

Per user discipline "do not leave a target until closed at
Nature-grade review pressure":

- **Bridge B**: closed at PDG precision (evening-4-21 iter 3). This
  is the only fully closed result from the loop.
- **Bridges A, N1, N2, N3, Gate 2 residues**: open; not closable
  via iter-narrowing; require external insight.
- **afternoon-4-21-proposal**: reframed as SUPPORT package (not
  closure), reflecting the honest state.

The loop terminates here without scheduling further wakeups.
Re-opening requires either:
- A specific new framework insight on N1 / Bridge A / A-BCC, or
- A user-directed pivot (e.g., to different reviewer items, or
  to a different framework angle).

## Iter-count summary

| Iter | Target | Nature-grade status |
|---|---|---|
| 1 | audit | ✓ completed |
| 2 | Bridge A multi-principle | narrowed (not closed) |
| 3 | Bridge B empirical | **CLOSED at PDG precision** |
| 4 | N1 retained-Atlas derivation | narrowed |
| 5 | N1+N2 polynomial factorization | narrowed (N1 is primitive) |
| 6 | N1 via 3-Casimir | **negative** (Tr(H²) not retained-simple) |

One genuine closure (Bridge B). N1/Bridges A/Gate 2 residues
require external input.
