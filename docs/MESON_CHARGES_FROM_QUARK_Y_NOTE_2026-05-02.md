# Meson Electric Charge Integrality from Quark Hypercharges

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on cycle 18 + cycle 23.
NOT proposed_retained.
**Primary runner:** `scripts/frontier_meson_charges_from_quark_y.py`

## 0. Statement

**Theorem.** For any meson `q q̄'` (quark-antiquark with two SM up-type
or down-type flavors having Y values from cycle 18), the electric charge
is integer:

```text
Q_meson = Q_q − Q_q' ∈ Z (for q,q' ∈ {u,d,s,c,b,t} where each
                          has Q ∈ {+2/3, −1/3} for up/down type)
```

## 1. Specific mesons

| Meson | Quark | Antiquark | Q (computed) | Q (observed) |
|---|---|---|---|---|
| π⁺ | u | d̄ | 2/3 − (−1/3) = +1 | +1 ✓ |
| π⁻ | d | ū | −1/3 − 2/3 = −1 | −1 ✓ |
| π⁰ | (uū − dd̄)/√2 | (mixture) | 0 | 0 ✓ |
| K⁺ | u | s̄ | 2/3 − (−1/3) = +1 | +1 ✓ |
| K⁰ | d | s̄ | −1/3 − (−1/3) = 0 | 0 ✓ |
| D⁺ | c | d̄ | 2/3 − (−1/3) = +1 | +1 ✓ |
| B⁰ | d | b̄ | −1/3 − (−1/3) = 0 | 0 ✓ |

All up-type (u, c, t) have Q = +2/3; all down-type (d, s, b) have Q = −1/3.

## 2. Why integrality is automatic

Q_q − Q_q' ∈ {0, ±1} because both quarks are in {+2/3, −1/3}, and the
difference is always 0 or ±1. So all neutral mesons have Q = 0 and all
charged mesons have Q = ±1.

## 3. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 18 (Q = T_3 + Y/2) + admitted cross-generation
  universality of Q_u and Q_d (admitted SM convention; not derived from
  graph-first).
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 4. Cross-references

- Cycle 18 / PR #281
- Cycle 23 / PR #286 (nucleon charges)
- Cycle 24 / PR #287 (baryon charge integrality)
