# Charged-Lepton Charge Universality Q_e = Q_μ = Q_τ = −1

**Date:** 2026-05-02
**Status:** exact algebraic identity / support theorem on cycle 18 +
admitted three-generation matter universality. NOT proposed_retained.
**Primary runner:** `scripts/frontier_lepton_charge_universality.py`

## 0. Statement

**Theorem.** Given STANDARD_MODEL_HYPERCHARGE_UNIQUENESS-derived Y values
(cycle 6 atlas) and admitted SM convention that all 3 generations have
identical Y assignments (cross-generation universality), the charged-lepton
electric charges are:

```text
Q(e_R) = Q(μ_R) = Q(τ_R) = Y/2 = −2/2 = −1.
Q(e_L) = Q(μ_L) = Q(τ_L) = T_3 + Y/2 = -1/2 + (-1)/2 = -1.
```

All three charged leptons have identical charge Q = −1.

## 1. Cross-generation universality

The SM convention is that all three lepton generations (e, μ, τ) have
identical SU(3)×SU(2)×U(1) representation content, hence identical
hypercharges. This is admitted as a SM convention; cross-generation
distinctions appear only in mass/mixing matrices, not gauge charges.

## 2. Status

```yaml
actual_current_surface_status: exact algebraic identity / support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on cycle 18 + admitted three-generation universality.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 3. Cross-references
- Cycle 18 / PR #281
- Cycle 6 atlas / PR #262
