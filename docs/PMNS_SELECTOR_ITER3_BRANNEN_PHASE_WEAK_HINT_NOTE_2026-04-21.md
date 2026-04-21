# PMNS Selector Iter 3: Brannen-Phase Gate — Weak Hint, Not Closure

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** Honest partial. No exact Brannen-phase linkage at the
`< 1e-4` threshold, but two independent phases cluster at ~1.4 ° from
simple I2/P-retained values. Not closure; worth following up in later
iterations only if iter 4+ identifies a retained mechanism.
**Runner:** `scripts/frontier_pmns_selector_iter3_brannen_phase_gate.py` —
3 PASS, 3 FAIL.

---

## Attack

Cross-sector I2/P → I5: test whether any natural "intrinsic phase" of
`H(m, δ, q_+)` evaluates to a retained I2/P-associated value
(2/9 rad, 2π/9, π − 2/9, etc.) at the physical pinned point
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`.

12 phase invariants tested:

| Invariant | Value (rad) | Closest retained | \|dev\| |
|---|---:|---|---:|
| P1 `arg(K_12)` | −1.4649 | −4π/9 | 0.0686 |
| P2 `arg(det H)` | ≈ 0 | 2/9 rad | 0.2222 |
| **P3 `arg(K_12/a_*)`** | **−2.8941** | **−(π − 2/9)** | **0.0252** |
| P4 `arg(K_12/b_*)` | −0.4788 | −π/9 | 0.1297 |
| P5 `arg(Pfaffian_d)` | −1.4649 | −4π/9 | 0.0686 |
| P6 `arg(U_e3)` | −π | π − 2/9 rad | 0.2222 |
| P7 `arg(Jarlskog)` | −2.9479 | −(π − 2/9) | 0.0285 |
| **P8 `arg(K_00·conj(a_*+b_*))`** | **−0.6720** | **−2π/9** | **0.0261** |
| P9 `arg(Tr(H T_Δ))` | π | −(π − 2/9) | 0.2222 |
| P10 `arg(Tr(H² T_Δ))` | π | −(π − 2/9) | 0.2222 |
| **P11 `arg(K_01/K_12)`** | **+2.8941** | **+(π − 2/9)** | **0.0252** |
| P12 `arg(K_02/K_12)` | +0.4788 | +π/9 | 0.1297 |

## Evidence against exact closure

- **Best match:** `|dev| = 0.0252 rad ≈ 1.45°.** The `< 1e-4` closure
  threshold is not met.
- **Top-3 matches cluster at ≈ 0.025–0.028 rad** which is suspiciously
  uniform but NOT tighter than the pinned point's intrinsic precision
  (6 digits ≈ 1e-6 rad scale).

## Interesting structural signals

1. **P3 and P11 are the same invariant up to sign:**
   `arg(K_01/K_12) = −arg(K_12/K_01) = −arg(K_12 / a_*)`
   (since `K_01 = a_*` is frozen). Not two independent matches —
   one invariant giving two reports.

2. **P8 is chamber-blind** (neighborhood std = 0.0000):
   `arg(K_00 · conj(a_* + b_*))` is constant across the chamber.
   Decomposing:
   - `K_00 = (1/3) · sum of all H entries = −2√8/9 + m + 2q_+` (REAL and
     changes with `m, q_+`).
   - `arg(a_* + b_*) = arctan(0.5 / 0.6285) = 0.6720` rad, frozen.
   - So P8 = `−arg(a_* + b_*)` (when K_00 > 0), chamber-invariant.
   - Numerical: `a_* + b_* = 0.62854 + 0.50000 i`, so
     `Im(a_*+b_*) = 0.5 = γ` (the retained constant).
     This explicit `Im = γ` link is framework-natural; the deviation
     `arg(a_* + b_*) − 2π/9 = 0.672 − 0.698 = −0.026 rad` lives in the
     frozen-slot structure, NOT in the chamber coordinates.

3. **Frozen-slot structure carries a 2π/9-adjacent angle, but not
   exactly.** Since `a_* + b_* = Re + i γ`, `arg(a_*+b_*)` depends on
   `Re(a_*+b_*)`. Exact `arg = 2π/9` would require
   `Re(a_*+b_*) = γ / tan(2π/9) = 0.5 / 0.8391 = 0.5959` — but the
   actual `Re(a_*+b_*) = 0.6285`. So no exact 2π/9 in the frozen slots.

## What this rules out and what it suggests

**Ruled out** at the `< 1e-4` threshold: direct Brannen-phase gate
linking I5 pinned point to I2/P value via a single phase invariant.

**Structural finding worth keeping:** the frozen slot `a_* + b_*` has
`Im = γ = 1/2` exactly. This is retained framework structure, not a
PMNS selector, but it tells us the Z_3 frozen slots have intrinsic
phase ≈ 2π/9 — close but not forced by I2/P.

**Narrow open question:** does the retained framework definition of
`a_*` and `b_*` (from the chamber-blindness theorem) imply a tighter
relation like `Im(a_* + b_*) = γ` (verified) AND some other phase
identity (unverified)?

## Iter 4+ direction

Iter 3 ruled out the simple Brannen-phase class. Pivoting:

- **A6: simultaneous-eigenvector / operator-commutation attack.** Test
  whether `[H(m, δ, q_+), O] = 0` for some retained operator `O` cuts
  the chamber to a sub-manifold through the pinned point. Candidates
  for `O`: the retained cyclic shift `C`, the Z_3 isotype projectors,
  or specific Cl(3) bivector combinations.

- **A5: A-BCC axiomatic derivation.** Derive A-BCC (`sign det H > 0`)
  from `Cl(3)` on `Z³` rather than from T2K observation. If A-BCC is
  axiomatic, it may come with additional structure that pins the
  point.

See `docs/PMNS_SELECTOR_ATTACK_BACKLOG_2026-04-21.md` (iter log and
next-up section).
