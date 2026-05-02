# Cycle 45 Claim Status Certificate — alpha_s Wilson-Loop Derivation source-note tightening (Pattern C)

**Block:** physics-loop/alpha-s-wilson-loop-tighten-block45-20260502
**Edited file:** docs/ALPHA_S_DIRECT_WILSON_LOOP_DERIVATION_THEOREM_NOTE_2026-04-30.md
**Target row:** alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30 (claim_type=bounded_theorem, audit_status=audited_conditional, td=240, load_bearing_step_class=D)

## Block type

**Pattern C — source-note scope tightening.** Replaces the conflicting
author-side `Status: proposed_retained` paragraph with explicit Type / Claim
scope / Status: audit pending headers; adds an "Out of scope (admitted-context
to this note)" section naming the four upstream/external items the audit
verdict identifies.

The edit is purely structural; no algebraic claim added or removed. No
runner changes.

## Specific edits

1. Replaced `Status: proposed_retained ... pending audit ratification` with
   explicit `Type: bounded_theorem`, `Claim scope` (in-scope: lattice
   Wilson-loop certificate at beta=6; out-of-scope: Sommer scale +
   standard QCD running + threshold matching + sea-quark/full-QCD
   bridge + PDG comparator), and `Status: audit pending` recording the
   `audited_conditional` verdict.

2. Sharpened §"Claim Boundary Pending Audit" to remove
   `proposed_retained` author-side language and clarify that
   `audited_conditional` is the audit-lane verdict.

3. Added new §"Out of scope (admitted-context to this note)" naming:
   - external Sommer scale setting;
   - standard QCD running;
   - threshold matching;
   - sea-quark / full-QCD bridge (verdict's principal gap);
   - PDG comparator `alpha_s(M_Z) = 0.1180 +/- 0.0009` (audit-comparator
     role only, never a derivation input).

## Claim-Type Certificate (Pattern C)

```yaml
target_claim_type: bounded_theorem  # unchanged
proposed_load_bearing_step_class: D  # unchanged
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
adds_new_load_bearing_observed_or_fitted_imports: false
removes_author_side_proposed_retained_label: true
```

## 7-criteria check (adapted)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern C source-note scope tightening) |
| 2 | No new claim rows or new source notes | YES |
| 3 | No new load-bearing observed/fitted/admitted | YES (PDG `0.1180` already present; now explicitly relabeled as audit-comparator only) |
| 4 | Algebraic content preserved | YES (Wilson-loop runner / certificate not modified) |
| 5 | Tightening responds to audit verdict | YES (mirrors verdict's identification of Sommer / running / matching / sea-quark gaps) |
| 6 | Review-loop disposition | proposed pass as scope-tightening edit |
| 7 | PR body says audit-lane to ratify | YES |

## Forbidden imports check

- No PDG observed values added (PDG `0.1180` already present; now
  explicitly relabeled as audit-comparator-only).
- No literature numerical comparators added.
- No fitted selectors added.
- No admitted unit conventions made load-bearing on retention.
- No same-surface family arguments added.

## Audit-graph effect

This tightening is structural source-note edit. It does not by itself
move any ledger row. Removes the author-side `proposed_retained` claim
that conflicts with the `audited_conditional` ledger state.

## What this proposes

A structural rewrite of the `Direct Wilson-Loop alpha_s(M_Z) Derivation
Gate` header, claim-boundary section, and a new out-of-scope section.
Algebraic / lattice content unchanged.
