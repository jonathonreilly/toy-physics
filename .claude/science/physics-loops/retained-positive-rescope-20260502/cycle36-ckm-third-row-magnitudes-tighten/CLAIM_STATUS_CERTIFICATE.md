# Cycle 36 Claim Status Certificate — CKM Third-Row Magnitudes source-note tightening (Pattern C)

**Block:** physics-loop/ckm-third-row-magnitudes-tighten-block36-20260502
**Edited file:** docs/CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md
**Primary runner:** scripts/frontier_ckm_third_row_magnitudes.py (PASS=35/0, unchanged)
**Target row:** ckm_third_row_magnitudes_theorem_note_2026-04-24 (claim_type=positive_theorem, audit_status=audited_conditional, td=87, load_bearing_step_class=A)

## Block type

**Pattern C — source-note scope tightening.** This block does NOT introduce a
new claim row, a new positive theorem, or a new runner. It edits the existing
source note to:

1. Replace the conflicting author-side
   `Status: proposed_retained structural-identity subtheorem of the
   proposed_promoted CKM atlas/axiom package` paragraph with explicit
   `Type`, `Claim scope`, and `Status: audit pending` headers that
   record the actual `audited_conditional` audit-lane verdict.

2. Add a new "Out of scope (admitted-context to this note)" section
   explicitly naming the four upstream authority notes the audit
   verdict identifies as the unratified one-hop dependencies, plus
   the exact standard-matrix readout values (audit-comparator-only).

3. Add a runner-flag clarification noting that the runner-emitted flag
   `CKM_THIRD_ROW_ATLAS_IDENTITIES_RETAINED=TRUE` is a runner-level
   diagnostic only; the authoritative retention/conditional status is
   set by the audit lane on the row's `audit_status` and
   `effective_status`, not by the runner flag.

4. Cross-reference the related Pattern A narrow rescope from cycle 19
   (`CKM_MAGNITUDES_STRUCTURAL_COUNTS_NARROW_THEOREM_NOTE_2026-05-02`)
   that carves out the input-supply-free algebra.

The edit is purely structural; no algebraic claim is added or removed. The
primary runner's PASS count is unchanged (35/35).

## Audit verdict that motivates this tightening

The audit-lane verdict on this row reads:

> Issue: The load-bearing step still imports unratified direct
> authority: WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md,
> CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md,
> CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md,
> ALPHA_S_DERIVED_NOTE.md.

The tightening directly mirrors that separation: the in-scope algebraic
substitution is preserved; the four upstream authorities are explicitly
relocated to "Out of scope" admitted-context.

## Specific edits

1. **Header reformatted.** Replaced
   `Status: proposed_retained structural-identity subtheorem...` with
   explicit `Type: positive_theorem`, `Claim scope` (in-scope:
   algebraic substitution producing R1, R2, R3 from parametric inputs;
   out-of-scope: four upstream authorities + exact-standard-matrix
   readouts), and `Status: audit pending` recording
   `audited_conditional`.

2. **Runner-flag clarification** added under §"Reproduction" noting that
   the `CKM_THIRD_ROW_ATLAS_IDENTITIES_RETAINED=TRUE` runner flag is a
   diagnostic only and the audit lane is the authority for retained
   status.

3. **New §"Out of scope (admitted-context to this note)" section** placed
   before "Cross-References", naming the four verdict-identified
   upstream authorities + the exact standard-matrix readout values
   (audit-comparator-only).

4. **§"Cross-References"** extended to include the related Pattern A
   narrow rescope from cycle 19.

The remainder of the source note (Statement, Derivation, Numerical Read,
Relationship To The Existing CKM Package, Boundary) is left structurally
unchanged.

## Claim-Type Certificate (Pattern C)

```yaml
target_claim_type: positive_theorem  # unchanged
proposed_load_bearing_step_class: A  # unchanged
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
adds_new_load_bearing_observed_or_fitted_imports: false
removes_author_side_proposed_retained_label: true  # corrects "proposed_retained" -> "audit pending"
```

## 7-criteria check (adapted for Pattern C)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern C source-note scope tightening) |
| 2 | No new claim rows or new source notes introduced | YES (edits an existing source note only) |
| 3 | No new load-bearing observed/fitted/admitted introduced | YES (no new imports; pre-existing four upstream authorities relocated to "out of scope" admitted-context with explicit role labels) |
| 4 | Algebraic content preserved | YES (primary runner PASS=35/0 unchanged; algebraic substitution producing R1, R2, R3 preserved) |
| 5 | Tightening responds to audit verdict | YES (directly mirrors the verdict's identification of the four upstream authorities) |
| 6 | Review-loop disposition | proposed pass as scope-tightening edit; audit-lane decides whether the row's verdict tightens on the next pass |
| 7 | PR body says audit-lane to ratify | YES (block proposes structural tightening only; explicitly removes the conflicting `proposed_retained` author-side label and adds runner-flag clarification) |

## Forbidden imports check

- No PDG observed values added.
- No literature numerical comparators added.
- No fitted selectors added.
- No admitted unit conventions made load-bearing on retention.
- No same-surface family arguments added.

## Audit-graph effect

This tightening is a structural source-note edit. It does not by itself
move any ledger row. The role is to give the audit lane a cleaner
source-note surface where the in-scope algebraic substitution is
visibly separated from the four audit-pending upstream authorities and
the audit-comparator-only standard-matrix readouts. The runner-flag
clarification removes a potential ambiguity between the runner's local
diagnostic and the audit lane's authoritative status.

## What this proposes

A structural rewrite of the `CKM Third-Row Magnitudes Structural Identities`
header, runner-flag clarification, new "Out of scope" section, and
cross-reference extension. Algebraic content unchanged; primary runner
unchanged.
