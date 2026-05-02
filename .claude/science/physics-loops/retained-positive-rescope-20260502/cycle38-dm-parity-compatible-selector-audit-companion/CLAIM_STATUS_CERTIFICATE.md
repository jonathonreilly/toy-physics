# Cycle 38 Claim Status Certificate — DM Parity-Compatible Selector Audit Companion (Pattern B)

**Block:** physics-loop/dm-parity-compatible-selector-audit-companion-block38-20260502
**Runner:** scripts/audit_companion_dm_parity_compatible_selector_exact.py (PASS=11/0)
**Target row:** dm_neutrino_source_surface_parity_compatible_observable_selector_theorem_note_2026-04-17 (claim_type=positive_theorem, audit_status=audited_conditional, td=89, load_bearing_step_class=A)

## Block type

**Pattern B — audit-acceleration runner.** This block does NOT introduce a new
claim row, a new source note, or a new positive theorem. It contributes a
focused exact-precision verification companion to the existing parity-compatible
observable-selector row, providing audit-lane evidence at sympy `Rational`
exact precision for the algebraic-calculus content (curvature isotropy +
minimizer location).

## What the companion verifies

1. **Determinant law symbolic verification.** Using the parent's stated
   `det(D + J_act) = A B^2 - (A + 2B)(delta^2 + q_+^2) - 6 delta^2 q_+ + 2 q_+^3`,
   compute `W_D = log det(D + J_act) - log det(D)` symbolically.

2. **Curvature isotropy.** `-d^2 W_D / d delta^2 |_(0,0) = -d^2 W_D / d q_+^2 |_(0,0)
   = 2(A + 2B)/(A B^2)` and `-d^2 W_D / d delta d q_+ |_(0,0) = 0`
   exact.

3. **Concrete `(A, B) = (1, 1)`:** isotropic coefficient `= 6` exact.

4. **Unique minimizer** on `q_+ = sqrt(8/3) - delta`:
   `delta_* = sqrt(8/3)/2 = sqrt(6)/3` exact (sympy `solve` of stationary
   condition).

5. **Strict convexity:** `d^2(action)/d delta^2 = 4 > 0`.

6. **Consequence at minimizer:** `q_+* = sqrt(6)/3`, `rho_* = sqrt(6)/3`.

7. **Parent row class-(A) ledger check.**

## Claim-Type Certificate (Pattern B)

```yaml
target_claim_type: meta  # audit-companion runner; not a claim row
proposed_load_bearing_step_class: A
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
audit_required_before_effective_retained: true  # parent row only; companion is meta
bare_retained_allowed: false
```

## 7-criteria check (adapted for Pattern B)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES |
| 2 | No new claim rows or new source notes introduced | YES |
| 3 | No load-bearing observed/fitted/admitted | YES (purely symbolic differentiation + sympy.solve) |
| 4 | Parent row's deps unchanged by this block | YES |
| 5 | Runner verifies parent's load-bearing step at exact precision | YES |
| 6 | Review-loop disposition | proposed pass as audit-companion meta artifact |
| 7 | PR body says audit-lane to ratify | YES |

## Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No admitted unit conventions load-bearing on retention.
- No same-surface family arguments.

## Audit-graph effect

This companion is **meta**. The parent's audit_conditional verdict
identifies the upstream observable-principle / active-affine source /
parity-compatible diagonal baseline / half-plane-chamber authorities as
the unratified deps. None of those gaps are addressed here; the
companion verifies the local class-(A) algebraic-calculus content at
exact symbolic precision.

## What this proposes

A standalone audit-companion runner that complements the existing primary
runner by providing exact symbolic verification of the curvature isotropy
and minimizer location. The block proposes nothing about any
retained-status change; the audit lane is the authority for that.
