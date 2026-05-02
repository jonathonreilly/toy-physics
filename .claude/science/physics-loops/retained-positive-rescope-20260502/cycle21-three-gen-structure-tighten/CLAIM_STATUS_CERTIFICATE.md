# Cycle 21 Claim Status Certificate — Three-Generation Structure source-note tightening (Pattern C)

**Block:** physics-loop/three-gen-structure-tighten-block21-20260502
**Edited file:** docs/THREE_GENERATION_STRUCTURE_NOTE.md
**Primary runner:** scripts/frontier_three_generation_observable_theorem.py (PASS=47/0, unchanged)
**Target row:** three_generation_structure_note (claim_type=positive_theorem)

## Block type

**Pattern C — source-note scope tightening.** This block does NOT introduce a
new claim row, a new positive theorem, or a new runner. It edits the existing
source note for `three_generation_structure_note` to add explicit Type, Claim
scope, and Status authority headers, and to introduce an "Out of scope (admitted-context
to this note)" section that explicitly separates the in-scope local
algebraic/spectral content (items 1-4) from the two semantic-bridge
conclusions (items 5-6) that depend on separate authority rows.

The edit is purely structural; no algebraic claim is added or removed. The
primary runner's PASS count is unchanged (47/47).

## Review motivation

The tightening separates:

- The **in-scope** local algebraic/spectral content (items 1-4: corner/orbit
  algebra `8 = 1 + 1 + 3 + 3`; `hw=1` triplet as lightest nonzero; no-rooting
  on `Cl(3)/Z^3`; no-proper-quotient on `M_3(C)`).
- The **out-of-scope** semantic-bridge claims (items 5-6: physical species
  bridge via observable separation + Hilbert semantics; substrate-level
  physical-lattice reading on accepted one-axiom surface). These depend on
  separate upstream rows and are admitted-context to this note.

## Specific edits

1. **Header block reformatted.** Removed `Status: proposed_retained`
   author-side tier. Added explicit `Type: positive_theorem`, `Claim scope:`
   identifying in-scope items (1)-(4) and flagging items (5)-(6) as
   out-of-scope, and `Status authority:` noting that source does not set or
   predict an audit outcome.

2. **§"Safe statement" retitled to "Safe statement (in-scope)"** and
   reframed to list only the four local algebraic/spectral items (1)-(4).
   The two semantic-bridge items (5)-(6) are removed from this section
   and relocated to the new "Out of scope" section below.

3. **New §"Out of scope (admitted-context to this note)" section** explicitly
   naming the two semantic-bridge claims that depend on separate authorities:
   - **Physical species bridge** (depends on
     `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`).
   - **Substrate-level physical-lattice reading** (depends on
     `PHYSICAL_LATTICE_NECESSITY_NOTE.md`).

4. **§"Boundary" retitled to "Boundary (in-scope only)"** and reformatted to:
   - rephrase author-side status bullets as "in-scope:";
   - explicitly list the two semantic-bridge items as "not in-scope; see
     above" pointing to the new Out of scope section.

## Claim-Type Certificate (Pattern C)

```yaml
proposed_claim_type: positive_theorem  # unchanged
proposed_load_bearing_step_class: A  # unchanged (algebraic identity on local M_3(C))
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_status: false
status_authority: independent_audit_lane
adds_new_load_bearing_observed_or_fitted_imports: false
removes_author_side_status_label: true
```

## 7-criteria check (adapted for Pattern C)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern C source-note scope tightening) |
| 2 | No new claim rows or new source notes introduced | YES (edits an existing source note only) |
| 3 | No new load-bearing observed/fitted/admitted introduced | YES (no new imports; pre-existing semantic-bridge items moved to "out of scope" admitted-context) |
| 4 | Algebraic content preserved | YES (primary runner PASS=47/0 unchanged; items (1)-(4) preserved; items (5)-(6) relocated but text content preserved verbatim under "out of scope" labels) |
| 5 | Tightening responds to review concern | YES (separates `three_generation_observable_theorem_note` and `physical_lattice_necessity_note` into admitted-context authority rows) |
| 6 | Review-loop disposition | proposed pass as scope-tightening edit; audit-lane decides any later row disposition |
| 7 | PR body says audit-lane to ratify | YES (block proposes structural tightening only; explicitly removes the conflicting `proposed_retained` author-side tier) |

## Forbidden imports check

- No PDG observed values added.
- No literature numerical comparators added.
- No fitted selectors added.
- No admitted unit conventions made load-bearing on the claim.
- No same-surface family arguments added.

## Audit-graph effect

This tightening is a structural source-note edit that:

1. Removes the conflicting `proposed_retained` author-side label.
2. Explicitly separates the in-scope local algebraic content from the
   out-of-scope semantic-bridge items that depend on separate upstream rows.

It does not by itself move any ledger row. The role is to give the audit
lane a cleaner source-note surface where the in-scope local algebra is
visibly separated from the semantic-bridge claims. Independent audit owns any
later row disposition.

## What this proposes

A structural rewrite of the `Three-Generation Matter Structure Note` header,
safe statement (now scoped), out-of-scope section (new), and boundary
section. Algebraic content unchanged; primary runner unchanged.
