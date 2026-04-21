# PMNS Selector Iter 2: Observable-Principle W[J] with Scalar Casimir Constraint — Negative

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** Honest negative. The pinned point is NOT a constrained
critical point of `W[J] = log|det H|` under any of the four natural
retained scalar Casimirs `{‖J‖_F², Tr(H²), Tr(H), Tr(H³)}`.
**Runner:** `scripts/frontier_pmns_selector_iter2_wdet_constrained.py` —
2 PASS, 5 FAIL (again, the FAILs are the hypothesis being disproven).

---

## Attack

The framework's retained "observable principle" is `W[J] = log|det(H_base + J)|`.
Iter 2 tested whether the physical pinned point
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` is a **constrained**
critical point of `W` on the level set of some natural retained scalar
Casimir of `H` or `J`.

Checked constraints:
- `g1 = ‖J‖_F²` (perturbation Frobenius)
- `g2 = Tr(H²)` (Ad-invariant total Frobenius)
- `g3 = Tr(H)` (linear Ad-invariant)
- `g4 = Tr(H³)` (cubic Ad-invariant)

A point is a constrained critical point of `W` on `{g = const}` iff
`∇W ∥ ∇g`. Numerically: `||(∇W)_⊥|| → 0` where `(∇W)_⊥` is the component
of `∇W` orthogonal to `∇g`.

## Evidence against the hypothesis

At the pinned point:

| Quantity | Value |
|---|---|
| `W[J]` | −0.0417 |
| `det H` | 0.9592 |
| `∇W` | (−1.643, −0.988, +3.461) |
| `‖∇W‖` | 3.957 |

Per-constraint alignment:

| Constraint `g` | `cos(∇W, ∇g)` | `‖(∇W)_⊥‖` |
|---|---:|---:|
| `g1 = ‖J‖_F²` | +0.243 | 3.839 |
| **`g2 = Tr(H²)`** | **+0.693** | **2.853** |
| `g3 = Tr(H)` | −0.415 | 3.600 |
| `g4 = Tr(H³)` | +0.655 | 2.990 |

Best alignment: `Tr(H²)` at **cos(θ) = 0.693** → angle ≈ **46°** off
parallel. None of the four is anywhere close to the < 1e-3 threshold
needed for constrained critical.

## Structural inference

The 4 constraint gradients span all of R³ (4 vectors in a 3-D space),
so there EXISTS some linear combination `g = a·g_1 + b·g_2 + c·g_3 + d·g_4`
with `∇g ∥ ∇W` at the pinned point. The question — whether that
combination has a **framework-natural single-symbol form** — is open
and likely has no clean answer (any single Casimir alone fails badly).

**Working conclusion**: the retained selector is NOT of the form
"extremize log|det H| subject to a single scalar-Casimir constraint."
The selector needs richer structure than Lagrange-multiplier-on-a-scalar.

## What this tells us

1. **Scalar-Casimir variational principles are ruled out** (iter 2's
   negative closes this class).
2. **The best-aligned constraint is `Tr(H²)`**, but it's still 46° off
   — suggestive but not close.
3. **The selector must involve non-scalar structure.** Candidates:
    - Operator-valued constraints (`[H, O] = 0` for some retained `O`,
      i.e., simultaneous eigenvectors).
    - Vector-valued constraints (a specific Hermitian matrix element
      `H_ij = c_ij` for some retained complex numbers).
    - Topological/arithmetic constraints (Brannen-phase = 2/9, APS
      η-invariant = specific, Dedekind-sum = specific).
    - Cross-sector couplings (A-BCC axiomatic derivation pinning a
      sub-manifold).

## Iter 3+ direction

The natural next step is **operator-valued constraint testing**.
Specifically: does the pinned point lie on the intersection of
`{[H, Z_3] = 0}` (but this holds on the whole chart by construction)
with another retained operator-commutation condition? Or does it lie
where the retained `SELECTOR = √6/3` has a specific eigenstructure?

Promoted attack for iter 3: **A4 (Brannen-phase gate)** — compute
`arg(det H) / (2π)` and related APS-like phase invariants of `H` over
the chamber, test whether the level set `phase = 2/9 mod 1` (the
retained I2/P value) intersects the pinned point. This would be a
CROSS-SECTOR forcing law linking I2/P (Brannen phase) to I5 (PMNS
angles).

See `docs/PMNS_SELECTOR_ATTACK_BACKLOG_2026-04-21.md` for the full
candidate list.
