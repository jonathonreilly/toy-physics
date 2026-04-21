# PMNS Selector Iter 4: Operator-Commutation — Mixed, with Key Hint δ · q_+ ≈ 2/3

**Date:** 2026-04-21
**Branch:** `afternoon-4-21`
**Status:** Mixed. Operator-commutation class itself is ruled out (no
retained operator has zero commutator with H_* or a chamber-cutting
zero-set). BUT scalar-invariant scan turned up a **strong hint**:
`δ_* · q_+* = 0.66770` within 0.15 % of the retained I1 value
`Q = 2/3 = 0.66667`. This may be the retained selector — to be verified
at high precision in iter 5.
**Runner:** `scripts/frontier_pmns_selector_iter4_operator_commutation.py` —
0 PASS, 9 FAIL.

---

## Parts A & B: operator-commutation class — negative

Tested 12 retained operators `O ∈ {C, C+C², i(C-C²), T_M, T_Δ, T_Q,
U_Z3, P_0, I-P_0, H_base, diag(1, ω, ω²), T_Δ + i T_Q}` for
`‖[H_*, O]‖_F²`.

- **No operator gives exact commutator = 0** at the pinned point.
  Smallest `O` are the Z_3 projectors `P_0 = J/3` and `I - P_0`, but
  those commutators are **constant across the chamber** (identity-like
  commutation = trivial, not selector).
- **No operator has a chamber-cutting zero-set** through the pinned
  point: ratio (pinned / scan-mean) ≥ 0.32 for all O; smallest is
  `i(C - C²)` at 0.32 (still not an order-of-magnitude suppression).

Operator-commutation selector class is therefore ruled out.

## Part C: scalar-invariant scan — one clear near-hit

Testing 33 natural scalars at the pinned point against retained simple
values `{0, 1, 1/2, 1/3, 2/3, 1/9, 2/9, 4/9, √6/3, 1/√6, √2, √3, √6,
π, π/9, 2π/9, π/3, -1, 1/6, 5/6, 1/√3, 2/√3, √(8/3), √8/3, ...}`:

| Scalar at pinned | Value | Closest retained | \|dev\| | Hit? |
|---|---:|---|---:|---:|
| **`δ_* · q_+*`** | **+0.66770** | **2/3** | **0.0010** | **★** |
| `Σλ / Σ\|λ\|` | +0.1678 | 1/6 | 0.0011 | ★ |
| `SELECTOR · q_+*` | +0.5838 | 1/√3 | 0.0065 | close |
| `Tr(H_*)` | +0.6571 | 2/3 | 0.0096 | close |
| `q_+* + δ_*` | +1.6488 | √(8/3) | 0.0159 | close (= chamber dist) |
| det(H_*) | +0.9592 | √8/3 | 0.0164 | close |
| `K_00 / √Tr(H²)` | +0.5495 | 1/√3 | 0.0278 | near |
| `Q_Koide(\|λ_i\|)` | +0.3771 | π/9 | 0.0281 | near |

Nothing hits the `< 1e-4` threshold at this test's fixed 6-digit
precision of the pinned point. But TWO scalars cluster at ≈ 0.001
deviation:
- **`δ · q_+ = 2/3`** (the retained I1 Koide Q)
- **`Σλ / Σ|λ| = 1/6`** (sum of eigenvalues vs sum of absolute values)

## Why `δ · q_+ = 2/3` is the prime candidate

Three reasons:

1. **Cross-sector connection**: `Q = 2/3` is the retained I1 Koide
   value (from AM-GM on Frobenius isotype energies, landed on
   morning-4-21). If `δ · q_+ = Q` is forced, this is a direct I1 → I5
   retained linkage. The framework headline `Q = 3·δ_Brannen` already
   ties I1 to I2/P; a `δ · q_+ = Q` identity would tie I1 to I5.

2. **Natural codim-1 cut**: on the 2-real `(δ, q_+)` manifold,
   `δ · q_+ = 2/3` is a hyperbola — a 1-real curve through the
   chamber. The level set cuts the chamber to codim-1. Combined with
   one more retained condition it pins the point.

3. **Simplicity and framework-naturalness**: `δ` and `q_+` are the
   chart coordinates themselves (from the retained source-surface
   affine parametrization). Their product being exactly the retained
   I1 scalar is the simplest possible cross-sector identity.

## What's open and the iter 5 plan

The 0.15 % deviation is ABOVE the pinned-point's 6-digit precision
(~1e-6), so this is NOT an exact match at the reported precision.
Three possibilities:

1. **`δ · q_+ = 2/3` is the true selector** and the pinned point as
   reported (6-digit) is slightly off from the exact chamber solution.
   Iter 5: re-pin the chamber under the constraint `δ · q_+ = 2/3`
   and check whether the resulting (sin²θ_12, sin²θ_13, sin²θ_23) are
   within PDG 3σ ranges.
2. **`δ · q_+ = 2/3` is a near-miss**, not exact. Numerical coincidence.
   Iter 5's precision-sharpening test will settle this.
3. **Intermediate: `δ · q_+` is a framework-natural quantity but not
   exactly Q**. Iter 5 may find it equals some related retained value.

**Iter 5 attack**: RE-PIN under `δ · q_+ = 2/3` exactly.

- Replace the 3-equation PMNS angle system with 2 of the PDG angles +
  the constraint `δ · q_+ = 2/3`. Solve for `(m, δ, q_+)` at high
  precision.
- Check: does the resulting solution have all three PMNS angles
  within 3σ of PDG NO central values?
- If YES: `δ · q_+ = 2/3` is likely a retained identity and iter 6
  should pursue its framework-native derivation (by linking to
  I1 Koide AM-GM).
- If NO: the hypothesis is disproven and iter 6 should pivot.

This is the most promising signal in the loop to date. The attacks in
iters 1-3 ruled out natural classes; iter 4's near-hit on `δ · q_+ = Q`
opens the most targeted possible iter-5 test: a single precision
re-pin.
