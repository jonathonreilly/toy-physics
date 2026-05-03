# Claim Status Certificate — Cycle 21

## Cycle metadata

- **slug**: pmns-branch-selector-2026-05-03
- **branch**: physics-loop/pmns-branch-selector-2026-05-03
- **base**: origin/main
- **note**: docs/PMNS_BRANCH_SELECTOR_CP_SHEET_BLINDNESS_NOTE_2026-05-03.md
- **runner**: scripts/frontier_pmns_branch_selector.py

## Status fields

```yaml
actual_current_surface_status: open
target_claim_type: open_gate
conditional_surface_status: bounded-support
hypothetical_axiom_status: null
admitted_observation_status: null
claim_type_reason: |
  Stretch-attempt cycle on the branch-selector residual. The cycle
  produces a NEGATIVE STRUCTURAL RESULT: the entire current Branch-B
  selector bank (min-info, observable-relative-action, transport-
  extremal, continuity-closure) is CP-sheet blind, hence cannot
  uniquely select a baryogenesis witness. By exclusion, Branch A
  (one-flavor reduced surface) is selected as the framework-native
  branch — but only modulo the audit ratification of the CP-sheet
  blindness theorem (P4) and the cycle-18 structural decomposition
  (P2). This is a sharpening of cycle 09 Obstruction 2, NOT a closing
  derivation.
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## V1-V5 Promotion Value Gate

| # | Question | Pass/Fail |
|---|----------|-----------|
| V1 | Closes/sharpens cycle 09 Obstruction 2 by EXCLUDING all four Branch-B selectors via CP-sheet blindness | PASS |
| V2 | New synthesis of cycle 18 (Branch A decomposition) + retained CP-sheet blindness + four candidate selectors → uniqueness exclusion theorem | PASS |
| V3 | Audit lane does not have this synthesis; the parity argument is in P4 but not connected to the branch-selector ambiguity | PASS |
| V4 | Five-route portfolio + symbolic parity verification across four selectors + Route-E counterfactual is substantive | PASS |
| V5 | Different from cycle 09 (near-fit catalogue), cycle 12 (cp1/cp2 = -√3 partial), cycle 18 (structural decomposition); cycle 21 does branch-selector LAW analysis | PASS |

All five gate questions pass.

## Dependencies

- (P1) cycle 06 Majorana null-space — retained
- (P2) cycle 18 structural decomposition — bounded_theorem (audit
  ratification pending)
- (P3) H-source-surface chart constants — support-grade
- (P4) CP-sheet blindness theorem — audited_conditional retained
- (P5) Four candidate selectors — support-grade
- (P6) cycle 09 transport-status — audited_conditional retained

## Open imports

None new. The cycle inherits the already-named obstructions:
- cycle 09 O1 / cycle 12 R2 / cycle 15 R1 (Y₀² = (G_weak²/64)²)
- cycle 09 O3 (α_LM mass scale)
These are NOT consumed as derivation inputs in cycle 21; they are
recorded in the note's "Inherited obstructions" section.

## Forbidden-import discipline

- η_obs (= 6.12 × 10^{-10}) used only as comparator.
- m_β not used.
- Σ m_ν not used.
- No PDG values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No same-surface family arguments.
- y_0 (G_weak): named obstruction inherited; not new.
- α_LM: named obstruction inherited; not new.

## Review-loop disposition

`pass` (self-review). Independent audit-lane ratification still
required. The note explicitly says so.

## What this cycle does NOT claim

- Does NOT promote any selector to retained.
- Does NOT close cycle 09 Obstruction 2 by constructing a positive
  selector — sharpens it into a structural exclusion of the entire
  current Branch-B selector bank.
- Does NOT consume η_obs as derivation input.
- Does NOT promote PMNS chart constants (γ, E₁, E₂) to retained.
- Does NOT close the right-sensitive 2-real Z_3 doublet-block
  selector law — that is the residual remaining open.
