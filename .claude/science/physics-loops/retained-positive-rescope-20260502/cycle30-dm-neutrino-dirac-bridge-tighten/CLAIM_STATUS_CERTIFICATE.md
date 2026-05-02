# Cycle 30 Claim Status Certificate — DM Neutrino Dirac Bridge source-note tightening (Pattern C)

**Block:** physics-loop/dm-neutrino-dirac-bridge-tighten-block30-20260502
**Edited file:** docs/DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md
**Primary runner:** scripts/frontier_dm_neutrino_dirac_bridge_theorem.py (PASS=28/0, unchanged)
**Audit-acceleration companion:** scripts/audit_companion_dm_neutrino_dirac_bridge_exact.py (PASS=29/0, from cycle 26)
**Target row:** dm_neutrino_dirac_bridge_theorem_note_2026-04-15 (claim_type=positive_theorem, audit_status=audited_conditional, td=115, load_bearing_step_class=C)

## Block type

**Pattern C — source-note scope tightening.** This block does NOT introduce a
new claim row, a new positive theorem, or a new runner. It edits the existing
source note for `dm_neutrino_dirac_bridge_theorem_note_2026-04-15` to:

1. Replace the conflicting author-side
   `Status: EXACT WITHIN THE RETAINED LOCAL HIGGS FAMILY` paragraph
   with explicit `Type: positive_theorem`, `Claim scope` (in-scope
   algebraic Cl(4) content; out-of-scope upstream framework items),
   and `Status: audit pending` recording the `audited_conditional`
   ledger verdict.

2. Restructure the original `## Status` heading content to "Status
   (in-scope)" and explicitly enumerate which items are algebraic /
   in-scope (1, 2, 4, 6) versus admitted-context inputs (3 = `V_sel`,
   5 = weak-axis branch convention).

3. Add a new "Out of scope (admitted-context to this note)" section
   explicitly naming the four upstream items the audit verdict
   identifies as load-bearing gaps:
   - local post-EWSB Higgs family upstream;
   - `V_sel` selector minima claim;
   - 3+1 chirality operator framework derivation;
   - weak-axis branch convention.

4. Cite the audit-acceleration companion from cycle 26 as the
   exact-precision verification of the in-scope algebraic content
   (PASS=29/0 on the 4x4 Euclidean Cl(4) realization).

The edit is purely structural; no algebraic claim is added or removed. The
primary runner's PASS count is unchanged (28/28).

## Audit verdict that motivates this tightening

The audit-lane verdict on this row reads:

> Issue: the proof starts from the retained local post-EWSB Higgs family
> M(phi), the exact selector V_sel, the 3+1 completed chirality surface,
> and a weak-axis branch convention, but these inputs are not present as
> one-hop retained dependencies in the ledger. Why this blocks: the
> runner proves the algebra after those structures are chosen, not that
> the framework forces those structures from retained primitives. Repair
> target: add retained dependencies or an integrated derivation for the
> Higgs family, selector, 3+1 chirality operator, and weak-axis
> convention before the Gamma_1 selection step.

The tightening directly mirrors that separation: the in-scope algebraic
content of the chiral off-diagonal property is verified at exact
precision (cycle-26 companion), while the four verdict-identified
upstream items are explicitly relocated to "Out of scope".

## Specific edits

1. **Header reformatted.** Replaced
   `Status: EXACT WITHIN THE RETAINED LOCAL HIGGS FAMILY. OPEN ON
   NORMALIZATION.` with explicit Type / Claim scope / Status: audit pending
   headers.

2. **§"Status" retitled to "Status (in-scope)"** and reframed to
   explicitly mark items 3 and 5 as admitted-context (selector minima
   claim and weak-axis branch convention respectively); clarified that
   the chiral off-diagonal property (items 1-2) and its consequences
   (items 4, 6) are the algebraic in-scope content; cited the cycle-26
   audit-acceleration companion.

3. **New §"Out of scope (admitted-context to this note)" section** placed
   at the end, naming the four verdict-identified upstream items.

The remainder of the source note (Theorem statement, "Why Xi_5 Is
Excluded", "Why The Second-Order Cascade Still Matters", "What This
Changes", "New Sharp Blocker") is left structurally unchanged.

## Claim-Type Certificate (Pattern C)

```yaml
target_claim_type: positive_theorem  # unchanged
proposed_load_bearing_step_class: C  # unchanged (first-principles compute)
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
adds_new_load_bearing_observed_or_fitted_imports: false
removes_author_side_exact_label: true  # corrects "EXACT WITHIN ... " -> "audit pending"
```

## 7-criteria check (adapted for Pattern C)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern C source-note scope tightening) |
| 2 | No new claim rows or new source notes introduced | YES (edits an existing source note only) |
| 3 | No new load-bearing observed/fitted/admitted introduced | YES (no new imports; pre-existing four upstream items relocated to "out of scope" admitted-context with explicit role labels) |
| 4 | Algebraic content preserved | YES (primary runner PASS=28/0 unchanged; audit-acceleration companion PASS=29/0 unchanged; chiral off-diagonal algebra preserved verbatim in source note) |
| 5 | Tightening responds to audit verdict | YES (directly mirrors the verdict's identification of the four upstream items as the load-bearing gaps) |
| 6 | Review-loop disposition | proposed pass as scope-tightening edit; audit-lane decides whether the row's verdict tightens on the next pass |
| 7 | PR body says audit-lane to ratify | YES (block proposes structural tightening only; explicitly removes the conflicting `EXACT WITHIN ...` author-side label) |

## Forbidden imports check

- No PDG observed values added.
- No literature numerical comparators added.
- No fitted selectors added.
- No admitted unit conventions made load-bearing on retention.
- No same-surface family arguments added.

## Audit-graph effect

This tightening is a structural source-note edit. It does not by itself
move any ledger row. The role is to give the audit lane a cleaner
source-note surface where the in-scope algebraic content (chiral
off-diagonal property) is visibly separated from the four
verdict-identified upstream gaps. If the audit lane revisits the row
with this tightening in scope, the conditional verdict may tighten on
the in-scope algebraic portion — but that decision belongs to the
audit lane.

## What this proposes

A structural rewrite of the `DM Neutrino Dirac Bridge Theorem Note`
header, status section, and new out-of-scope section, with cross-
reference to the cycle-26 audit-acceleration companion. Algebraic
content unchanged; primary runner unchanged.
