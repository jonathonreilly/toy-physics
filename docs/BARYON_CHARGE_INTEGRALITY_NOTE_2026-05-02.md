# Baryon Charge Integrality Q_baryon = N_u − 1 from Quark Hypercharges

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem extending cycles 18, 23.
NOT proposed_retained.
**Primary runner:** `scripts/frontier_baryon_charge_integrality.py`

## 0. Statement

**Theorem.** Given quark electric charges Q_u = +2/3, Q_d = −1/3 (cycle 18)
and SM convention that baryons consist of 3 quarks (in a color-singlet
combination), all baryons composed of u and d quarks have integer
electric charge:

```text
Q_baryon  =  N_u Q_u  +  N_d Q_d           (with N_u + N_d = 3)
            =  N_u · (2/3)  +  (3 − N_u) · (−1/3)
            =  (2 N_u − (3 − N_u)) / 3
            =  (3 N_u − 3) / 3
            =  N_u − 1.
```

For N_u ∈ {0, 1, 2, 3}: Q_baryon ∈ {−1, 0, +1, +2} — all integers.

## 1. Specific baryons

| Baryon | Constituents | N_u | Q (computed) | Q (observed) |
|---|---|---|---|---|
| Δ⁻ | ddd | 0 | −1 | −1 ✓ |
| n | udd | 1 | 0 | 0 ✓ |
| p | uud | 2 | +1 | +1 ✓ |
| Δ⁺⁺ | uuu | 3 | +2 | +2 ✓ |

## 2. Quark color singlet condition

The 3-quark composition is forced to be a SU(3)_color singlet (totally
antisymmetric in color indices) for hadronic stability — a separate
admitted convention beyond Q derivation.

## 3. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 18 (Q = T_3 + Y/2) + admitted hadron 3-quark
  color-singlet composition (standard SM/QCD convention).
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 4. Cross-references

- Cycle 18 / PR #281 — EWSB pattern Q = T_3 + Y/2
- Cycle 23 / PR #286 — Q_p = +1, Q_n = 0
- Cycle 6 / PR #262 — LHCM atlas (quark Y values)
