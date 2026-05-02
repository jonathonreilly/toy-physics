# Hadronic Electric Charges Q_p = +1, Q_n = 0 from Quark Hypercharges

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on cycle 18 EWSB
pattern. NOT proposed_retained.
**Primary runner:** `scripts/frontier_hadronic_charges_from_quark_y.py`

## 0. Statement

**Theorem.** Given quark electric charges Q_u = +2/3, Q_d = −1/3 (from
cycle 18 Q = T_3 + Y/2 + LHCM-derived Y values) and SM quark constituent
content of nucleons:
- proton p = uud
- neutron n = udd

then Q_p = +1 and Q_n = 0 exactly.

**Proof.** 
```text
Q_p  =  Q_u + Q_u + Q_d  =  2/3 + 2/3 − 1/3  =  3/3  =  +1  ✓
Q_n  =  Q_u + Q_d + Q_d  =  2/3 − 1/3 − 1/3  =  0/3  =  0   ✓
```

These match the SM observed nucleon charges exactly.

## 1. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 18 (Q = T_3 + Y/2) + admitted nucleon constituent
  content (p = uud, n = udd, standard SM convention).
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 2. What this closes

Hadronic electric charges Q_p = +1, Q_n = 0 as exact rational identities
extending cycle 18 to the nucleon sector.

## 3. Cross-references

- Cycle 18 / PR #281 — EWSB pattern Q = T_3 + Y/2
- Cycle 6 / PR #262 — LHCM atlas (quark Y values)
