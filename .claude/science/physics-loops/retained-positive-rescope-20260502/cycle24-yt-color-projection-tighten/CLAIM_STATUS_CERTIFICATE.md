# Cycle 24 Claim Status Certificate — y_t Color-Projection Correction source-note tightening (Pattern C)

**Block:** physics-loop/yt-color-projection-tighten-block24-20260502
**Edited file:** docs/YT_COLOR_PROJECTION_CORRECTION_NOTE.md
**Primary runner:** scripts/frontier_yt_color_projection_correction.py (PASS=7/7, unchanged)
**Target row:** yt_color_projection_correction_note (claim_type=positive_theorem, audit_status=audited_conditional, td=175, load_bearing_step_class=C)

## Block type

**Pattern C — source-note scope tightening.** This block does NOT introduce a
new claim row, a new positive theorem, or a new runner. It edits the existing
source note for `yt_color_projection_correction_note` to add explicit Type,
Claim scope, and Status headers; relabel the numerical-readout subsection as
out-of-scope audit-comparator only; restructure §"Status Assessment" into
"in-scope" vs "out-of-scope (audit-pending or admitted-context)" sections;
and rewrite the Import Status Table to mark each element with its actual
audit role.

The edit is purely structural; no algebraic claim is added or removed. The
primary runner's PASS count is unchanged (7/7).

## Audit verdict that motivates this tightening

The audit-lane verdict on this row reads:

> Issue: the sqrt(8/9) Yukawa correction produces a strong numerical
> support packet, but the note explicitly says the required R_conn = 8/9
> bridge is not yet derived from the CMT partition-function identity
> alone and needs the same lattice measurement that would close the EW
> color-projection correction. Why this blocks: downstream candidate
> retained-grade/promoted rows cannot cite this as a theorem-grade
> zero-import y_t or top-mass derivation; the load-bearing scalar-channel
> projection remains conditional on the unclosed R_conn bridge and
> standard matching/running caveats. Repair target: compute [R_conn on
> the SU(3) lattice at beta = 6] ...

The tightening directly responds to this verdict by separating:

- **In-scope content:** the algebraic Fierz identity `R_conn = 8/9` at
  `N_c = 3` (already runner-verified at exact precision via the cycle-9
  audit companion; class-A group theory) and the structural channel-counting
  argument that the singlet vs adjoint channels give `sqrt(R_conn)` vs
  `R_conn` (class-C derivation).
- **Out-of-scope content:** the R_conn bridge from CMT to the scalar
  self-energy (audit-verdict's repair target); RGE running; MSbar-to-pole
  conversion; `lambda(M_Pl) = 0` stability boundary; specific physical
  numerical predictions; PDG comparators.

## Specific edits

1. **Header reformatted.** Removed `Status: DERIVED quantitative support`
   author-side label (which conflicted with the audit-lane
   `audited_conditional` verdict). Added explicit `Type: positive_theorem`,
   `Claim scope:` (in-scope Fierz identity + sqrt(R_conn) channel-counting;
   out-of-scope R_conn bridge + RGE + MSbar-to-pole + numerical
   predictions), and `Status: audit pending` recording the
   `audited_conditional` ledger verdict.

2. **§"Numerical Results" relabeled** "out-of-scope numerical readout —
   admitted-context only". The Framework / Observed / Deviation table is
   preserved verbatim but explicitly tagged: PDG observables (172.69 GeV,
   125.25 GeV, 0.1179) are **PDG comparator** entries in the audit-comparator
   role only, never derivation inputs.

3. **§"Part 6: Status Assessment" restructured** into "What is in-scope
   (algebraic / channel-counting content)" vs "What is out-of-scope
   (audit-pending or admitted-context)" subsections. The verdict's repair
   target (lattice measurement of R_conn at beta=6) is recorded in a
   "Path to retained-grade status" subsection that defers the decision to
   the audit lane.

4. **§"Import Status Table" rewritten.** Each element's "Status" column now
   records its audit role: `admitted-context`, `in-scope (Fierz, class A)`,
   `in-scope (class C)`, `out-of-scope (audit-pending)`, or
   `out-of-scope (numerical readout)`. The previous "DERIVED" / "AXIOM" /
   "COMPUTED" labels are replaced with the audit-role labels.

## Claim-Type Certificate (Pattern C)

```yaml
target_claim_type: positive_theorem  # unchanged
proposed_load_bearing_step_class: C  # unchanged (channel-counting structural derivation)
introduces_new_claim_row: false
introduces_new_source_note: false
modifies_parent_audit_status: false  # audit-lane decides
adds_new_load_bearing_observed_or_fitted_imports: false
removes_author_side_derived_label: true  # corrects "DERIVED" -> "audit pending"
```

## 7-criteria check (adapted for Pattern C)

| # | Criterion | Pass? |
|---|---|---|
| 1 | Block type named | YES (Pattern C source-note scope tightening) |
| 2 | No new claim rows or new source notes introduced | YES (edits an existing source note only) |
| 3 | No new load-bearing observed/fitted/admitted introduced | YES (no new imports; pre-existing PDG comparators relabeled as audit-comparator-role admitted-context with "never consumed as derivation inputs" disclaimer; pre-existing RGE/MSbar/lambda-stability dependencies relabeled as out-of-scope admitted-context) |
| 4 | Algebraic content preserved | YES (primary runner PASS=7/7 unchanged; Fierz identity + sqrt(R_conn) channel-counting derivation preserved verbatim) |
| 5 | Tightening responds to audit verdict | YES (directly mirrors the verdict's identification of the R_conn bridge as the conditional gap; in-scope Fierz identity is the already-runner-verified portion) |
| 6 | Review-loop disposition | proposed pass as scope-tightening edit; audit-lane decides whether the row's verdict tightens on the next pass |
| 7 | PR body says audit-lane to ratify | YES (block proposes structural tightening only; explicitly removes the `DERIVED quantitative support` author-side label) |

## Forbidden imports check

- No PDG observed values added (`m_t = 172.69 GeV`, `m_H = 125.25 GeV`,
  `alpha_s(M_Z) = 0.1179` already present; now explicitly relabeled as
  PDG comparator audit-comparator-role admitted-context with "never
  consumed as derivation inputs" disclaimer).
- No literature numerical comparators added.
- No fitted selectors added.
- No admitted unit conventions made load-bearing on retention.
- No same-surface family arguments added.

## Audit-graph effect

This tightening is a structural source-note edit. It does not by itself
move any ledger row. The role is to give the audit lane a cleaner
source-note surface where the in-scope Fierz identity and channel-counting
argument are visibly separated from the audit-pending R_conn bridge and
the out-of-scope physical numerical extrapolations. If the audit lane
revisits the row with this tightening in scope, the conditional verdict
may tighten on the in-scope portion — but that decision belongs to the
audit lane.

## What this proposes

A structural rewrite of the `Color-Singlet Projection Correction to y_t`
header, numerical-results section, status-assessment section, and import
status table. Algebraic content unchanged; primary runner unchanged.
