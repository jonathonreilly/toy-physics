# PMNS Selector Iter 1: Doublet-Block AM-GM — Negative

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** Honest negative result. Naive doublet-block AM-GM is NOT the
retained selector for the physical PMNS angle triple.
**Runner:** `scripts/frontier_pmns_selector_iter1_doublet_amgm.py` —
8 PASS, 7 FAIL (the FAIL results are the hypothesis being disproven; the
PASS results are retained-atlas sanity).

---

## Attack

The PMNS angle-triple gate is still open: the 2-real source manifold
`(δ, q_+)` on the live sheet is known, the physical pinned point
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` is known, but the
**framework-native point-selection law** is missing.

Iter 1 hypothesis, parallel to the I1 AM-GM closure:

> The retained selector is the doublet-block AM-GM functional
> `F_d(m, δ, q_+) = log(E_sym_d · E_anti_d)`
> where `K_d = U_Z3^† · H · U_Z3 [1:3, 1:3]` is the 2×2 doublet block,
> and `E_sym_d = (tr K_d)² / 2`, `E_anti_d = Tr(K_d²) − E_sym_d` is its
> Herm_2(C) isotype decomposition.

If this held, the pinned point would be the global AM-GM maximum with
`E_sym_d = E_anti_d`, parallelling I1's `E_+ = E_⊥ ⟹ κ = 2`.

## Evidence against the hypothesis

At the physical pinned point:

| Quantity | Value |
|---|---|
| `E_sym_d` | 0.3212 |
| `E_anti_d` | 0.3122 |
| ratio `E_sym_d / E_anti_d` | **1.029** (expected 1.000 if AM-GM) |
| `|E_sym_d − E_anti_d|` | 0.0091 |
| `∂F_d/∂m` | +0.365 |
| `∂F_d/∂δ` | **−5.95** |
| `∂F_d/∂q_+` | **+4.99** |
| `‖∇F_d‖` | **7.78** |

The ratio is within 3 % of AM-GM equality but the gradient is large,
so the pinned point is NOT a critical point of `F_d`. Bounded 2D and 3D
scans over the chamber place the global maximum of `F_d` at the scan
boundary, not at the pinned point — confirming `F_d` has no retained
interior extremum without an additional constraint.

## Why `F_d` alone can't close the gate (structural reason)

The I1 closure worked because on `Herm_circ(3)` the total Frobenius
`Tr(M²) = E_+ + E_⊥` is a retained Casimir-like invariant that fixes
the sum of isotype energies. AM-GM then forces the maximum at
`E_+ = E_⊥`.

For the doublet block on `H(m, δ, q_+)`, the analogous sum
`Tr(K_d²) = E_sym_d + E_anti_d` is NOT fixed — it varies quadratically
with `(m, δ, q_+)`. Without a retained constraint that fixes
`Tr(K_d²) = N` for some framework-given `N`, `F_d` has no interior
extremum and cannot be the selector.

## What this tells us

1. **The naive I1-style AM-GM doesn't carry over to I5.** The doublet
   block lacks a fixed-Frobenius constraint.

2. **The 3 % `E_sym / E_anti` deviation at pinned is small but real.**
   This is suggestive that AM-GM-like structure is in the ballpark but
   needs a specific retained constraint that would tilt the extremum by
   the right amount.

3. **A successful selector must combine** an energetic functional WITH
   a retained constraint. Candidates for iter 2+:

    - `Tr(H²) = N_retained` for some retained value (e.g. tied to
      `‖H_base‖_F² + ‖J_retained‖_F²`).
    - `det(H) = det(H_base)` (determinant-preserving perturbations).
    - `A-BCC` boundary constraint promoted to an action (distance to
      caustic `q_+ = √(8/3) − δ`).
    - A Koide-like functional on the eigenvalues of `H` rather than on
      isotype energies.
    - A `W[J] = log|det H|` — observable-principle — functional with
      a specific retained `J`.

4. **Frozen slots work correctly** (Part A, 7/7 PASS): `K_01 = a_*`,
   `K_02 = b_*` frozen across 10 random chamber points. The 2-real law
   `q_+ = √(8/3) − (K_11 + K_22)/2` and
   `δ = (Im K_12 + 4√2/3)/√3` holds at the pinned point. The retained
   chart structure is fully verified — the failure is purely in the
   hypothesis about which functional extremizes.

## Iter 2+ direction

Primary candidate for iter 2: **observable-principle functional**
`W[J] = log |det(H_base + J)|` with `J = m·T_m + δ·T_Δ + q_+·T_q`,
combined with a retained constraint that fixes the scale of `J`
(e.g. `‖J‖_F² = ‖J_*‖_F²` where `‖J_*‖_F²` is given by the retained
`a_*`, `b_*` norms). If `W[J]` has a critical point at the pinned
`(m_*, δ_*, q_+*)`, the gate closes.

See `docs/PMNS_SELECTOR_ATTACK_BACKLOG_2026-04-21.md` for the full
candidate list and decision logic.
