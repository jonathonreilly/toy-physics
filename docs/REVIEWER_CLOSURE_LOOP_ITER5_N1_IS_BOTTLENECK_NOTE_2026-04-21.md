# Reviewer-Closure Loop Iter 5: N1 Is the Primitive Bottleneck

**Date:** 2026-04-21
**Branch:** `evening-4-21`
**Status:** **Honest Nature-grade verdict.** N2 and N3 both reduce
to N1 via polynomial argument; N1 (`δ·q_+ = SELECTOR² = Q_Koide`) is
the primitive retained identity not derivable from the currently
retained Atlas. The afternoon-4-21-proposal should be re-labeled as
a SUPPORT package, not a closure.
**Runner:** `scripts/frontier_reviewer_closure_iter5_n1n2_joint_polynomial_attack.py`
— 4/7 PASS (the 3 FAILs are the hypothesis being disproven, expected).

---

## Context: user-directed discipline

> "We should NOT leave a target until it's derived, closed, retained
> at Nature-grade review pressure — otherwise we keep context-switching
> ourselves to death."

Iter 4 returned "N1 narrowed", which is not closure. Iter 5 is the
last honest attack before declaring N1 un-closable within currently
available retained framework.

## Iter 5 attack: joint N1 + N2 via polynomial factorization

Test whether the afternoon-4-21-proposal's combined consequence
`det(H) = √2·(δ·q_+)` holds as a polynomial identity on the full
`(m, δ, q_+)` chart or reduces under retained constraints.

### Part A — full-chart identity
`det(H) − √2·δ·q_+` is NOT identically zero on the full chart. It's
a non-trivial multinomial residual in (m, δ, q_+).

### Part B — substitute Tr(H) = 2/3 (Identity 1)
Under `m = 2/3`, residual does NOT simplify to zero. It's a non-zero
polynomial in (δ, q_+).

### Part C — substitute Tr(H) = 2/3 + δ·q_+ = 2/3 (Identities 1 + 2)
Under both, `det(H) − E2` becomes a polynomial equation in δ:

```
  det(H(2/3, δ, 2/(3δ))) − √8/3 = 0
```

with specific roots. At δ_* ≈ 0.9331 this holds (afternoon closure).
**N2 (det(H) = E2) is therefore a polynomial root-selection given
N1 + Identity 1**, not an independent primitive identity.

### Part D — honest classification

**N1 is the primitive retained identity** of the afternoon-4-21-proposal.
Everything else reduces to it:

- **N2** (`det(H) = E2`) follows from N1 + `Tr(H) = 2/3` + polynomial
  root-selection.
- **N3** (uniqueness) reduces to finite real-root enumeration of
  the polynomial in δ — algebraically tractable given N1 + Identity 1.

**N1 itself is NOT derivable** from the currently retained Atlas
theorems:
- Active-affine chart gives the `(m, δ, q_+)` parametrization only.
- Z_3 doublet-block gives K-entry inversions, not constraints on `δ·q_+`.
- Carrier normal-form gives `σ sin(2v) = 8/9`, `δ + ρ = √(8/3)` — but
  δ remains a free 1-real parameter after carrier reduction.

**Missing retained piece** (named in iter 4): a SELECTOR-quadrature
identity `δ · q_+ = SELECTOR²` on the `(T_Δ, T_Q)` active directions.
Without it, the afternoon-4-21-proposal cannot be elevated from
SUPPORT to CLOSURE.

## Honest status at Nature-grade pressure

- **N1**: OPEN. Requires a new retained framework identity
  (SELECTOR-quadrature on `T_Δ, T_Q`) OR reformulation of the
  afternoon-4-21-proposal as a SUPPORT package.
- **N2**: derivable FROM N1 + Tr(H) = 2/3 (polynomial argument).
- **N3**: derivable from the same, via finite-root enumeration.

Therefore the REAL remaining open item is N1. N2 and N3 will close
as corollaries once N1 lands.

## Loop-discipline conclusion

Per the user's directive:

- The loop has hit a genuine framework-level blocker on N1.
- Continuing to iter-narrow N1 produces "narrowed" results but
  does NOT close it at Nature-grade.
- The honest Nature-grade response is to **re-label the afternoon-
  4-21-proposal as a SUPPORT package** (observational verification
  + three conjectured retained identities, first-principles
  derivation open), rather than pretend continued iteration
  produces progress.

This aligns with the canonical reviewer's own downgrade of
morning-4-21 to a SUPPORT package pending Bridge A/B physical
arguments.

## Action items

1. **Commit iter 5** with the honest verdict.
2. **Update `afternoon-4-21-proposal`** documentation to reflect
   SUPPORT package status (not closure).
3. **Terminate this loop**. Re-opening requires either:
   - User provides a new framework attack angle for N1
     (SELECTOR-quadrature derivation), or
   - Structural reframing of the proposal.
4. **Backlog is accurate** on what remains open:
   - N1 (primitive)
   - Reviewer Gate 2: A-BCC axiomatic, chamber-wide σ_hier, etc.

## Summary of evening-4-21 loop (iter 1–5)

| Iter | Item | Status at Nature-grade |
|---|---|---|
| 1 | Audit | ✓ completed |
| 2 | Bridge A | narrowed (not Nature-closed) — multi-principle + γ |
| 3 | Bridge B | **closed at PDG precision** (5 decimal agreement) |
| 4 | N1 derivation attempt | narrowed (SELECTOR-quadrature pinpointed) |
| 5 | N1+N2 joint attack | **honest**: N1 is primitive bottleneck; N2/N3 reduce to it |

**Bridge B** is the only item fully closed at Nature-grade. Other items
require either new framework work or honest SUPPORT-package framing.
