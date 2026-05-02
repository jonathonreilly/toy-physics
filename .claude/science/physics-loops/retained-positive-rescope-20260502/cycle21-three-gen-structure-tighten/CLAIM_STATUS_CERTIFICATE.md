# Cycle 21 Claim Status Certificate — Three-Generation Structure source-note tightening (Pattern C)

**Block:** physics-loop/three-gen-structure-tighten-block21-20260502
**Edited file:** docs/THREE_GENERATION_STRUCTURE_NOTE.md
**Primary runner:** scripts/frontier_three_generation_observable_theorem.py (PASS=47/0, unchanged)
**Target row:** three_generation_structure_note (claim_type=positive_theorem, audit_status=audited_conditional, td=302)

## Block type

**Pattern C — source-note scope tightening.** This block does NOT introduce a
new claim row, a new positive theorem, or a new runner. It edits the existing
source note for `three_generation_structure_note` to add explicit Type, Claim
scope, and Status headers, and to introduce an "Out of scope (admitted-context
to this note)" section that explicitly separates the in-scope local
algebraic/spectral content (items 1-4) from the two semantic-bridge
conclusions (items 5-6) the audit verdict identifies as depending on
unratified upstream authority rows.

The edit is purely structural; no algebraic claim is added or removed. The
primary runner's PASS count is unchanged (47/47).

## Audit verdict that motivates this tightening

The audit-lane verdict on this row reads:

> Issue: The load-bearing step still imports unratified direct authority:
> THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md, PHYSICAL_LATTICE_NECESSITY_NOTE.md.
> Why this blocks: Under the restricted one-hop audit context, those
> authorities are not retained/audited-clean, so the critical claim
> cannot be ratified as closed even when its local algebra or runner
> checks pass. Repair target: ratify or repair the listed upstream
> theorem/bridge rows ...

The tightening directly responds to this verdict by separating:

- The **in-scope** local algebraic/spectral content (items 1-4: corner/orbit
  algebra `8 = 1 + 1 + 3 + 3`; `hw=1` triplet as lightest nonzero; no-rooting
  on `Cl(3)/Z^3`; no-proper-quotient on `M_3(C)`).
- The **out-of-scope** semantic-bridge claims (items 5-6: physical species
  bridge via observable separation + Hilbert semantics; substrate-level
  physical-lattice reading on accepted one-axiom surface). These depend on
  the unratified upstream rows the verdict identifies and are admitted-context
  to this note.

## Specific edits

1. **Header block reformatted.** Removed `Status: proposed_retained`
   author-side tier (which conflicts with the audit-lane `audited_conditional`
   verdict). Added explicit `Type: positive_theorem`, `Claim scope:`
   identifying in-scope items (1)-(4) and flagging items (5)-(6) as
   out-of-scope, and `Status: audit pending` recording the
   `audited_conditional` ledger verdict and noting that no author-side
   retained-grade tier is asserted in source.

2. **§"Safe statement" retitled to "Safe statement (in-scope)"** and
   reframed to list only the four local algebraic/spectral items (1)-(4).
   The two semantic-bridge items (5)-(6) are removed from this section
   and relocated to the new "Out of scope" section below.

3. **New §"Out of scope (admitted-context to this note)" section** explicitly
   naming the two semantic-bridge claims that the audit verdict identifies as
   depending on unratified upstream authorities:
   - **Physical species bridge** (depends on
     `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`).
   - **Substrate-level physical-lattice reading** (depends on
     `PHYSICAL_LATTICE_NECESSITY_NOTE.md`).

4. **§"Boundary" retitled to "Boundary (in-scope only)"** and reformatted to:
   - rephrase "retained:" bullets as "in-scope:" (consistent with audit-lane
     authority over retained-grade);
   - explicitly list the two semantic-bridge items as "not in-scope; see
     above" pointing to the new Out of scope section.

## Claim-Type Certificate (Pattern C)

```yaml
target_claim_type: positive_theorem  # unchanged
proposed_load_bearing_step_class: A  # unchanged (algebraic identity on local M_3(C))
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
adds_new_load_bearing_observed_or_fitted_imports: false
removes_author_side_retained_label: true  # corrects "proposed_retained" -> "audit pending"
```

## 7-criteria check (adapted for Pattern C)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern C source-note scope tightening) |
| 2 | No new claim rows or new source notes introduced | YES (edits an existing source note only) |
| 3 | No new load-bearing observed/fitted/admitted introduced | YES (no new imports; pre-existing semantic-bridge items moved to "out of scope" admitted-context) |
| 4 | Algebraic content preserved | YES (primary runner PASS=47/0 unchanged; items (1)-(4) preserved; items (5)-(6) relocated but text content preserved verbatim under "out of scope" labels) |
| 5 | Tightening responds to audit verdict | YES (directly mirrors the verdict's identification of `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` and `PHYSICAL_LATTICE_NECESSITY_NOTE.md` as unratified upstream deps) |
| 6 | Review-loop disposition | proposed pass as scope-tightening edit; audit-lane decides whether the row's verdict tightens on the next pass |
| 7 | PR body says audit-lane to ratify | YES (block proposes structural tightening only; explicitly removes the conflicting `proposed_retained` author-side tier) |

## Forbidden imports check

- No PDG observed values added.
- No literature numerical comparators added.
- No fitted selectors added.
- No admitted unit conventions made load-bearing on retention.
- No same-surface family arguments added.

## Audit-graph effect

This tightening is a structural source-note edit that:

1. Removes the conflicting `proposed_retained` author-side label that did not
   match the audit-lane `audited_conditional` verdict.
2. Explicitly separates the in-scope local algebraic content from the
   out-of-scope semantic-bridge items the audit verdict identifies as
   depending on unratified upstreams.

It does not by itself move any ledger row. The role is to give the audit
lane a cleaner source-note surface where the in-scope local algebra is
visibly separated from the audit-pending semantic-bridge claims. If the
audit lane revisits the row with this tightening in scope, the conditional
verdict may tighten on the local-algebra portion — but that decision belongs
to the audit lane.

## What this proposes

A structural rewrite of the `Three-Generation Matter Structure Note` header,
safe statement (now scoped), out-of-scope section (new), and boundary
section. Algebraic content unchanged; primary runner unchanged.
