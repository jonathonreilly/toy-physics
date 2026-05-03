# Active Review Queue

**Status:** canonical live queue for current-main review feedback  
**Purpose:** single place to record reviewer findings that still need a decision,
fix, or explicit rejection on `main`

## Rule

Use this file for **active** review feedback only.

- add new reviewer findings here first
- keep each item short and decision-oriented
- link any long-form packet in
  [`docs/work_history/repo/review_feedback/`](../work_history/repo/review_feedback/README.md)
- when an item is resolved, remove it from the open list and record it in the
  queue history section or the linked detailed packet

Do not use scattered backlog notes or branch-local memos as the live review
truth surface.

## Current State

As of `2026-04-18`, there are **no live repo-governance or claim-surface
blockers** waiting in the review queue. The remaining items are science-facing
open lanes rather than review-hygiene debt.

Current science/open-lane follow-ups:

- irregular off-lattice sign lane: portability beyond the bounded centered
  core-packet surface remains open
- periodic 2D torus diagnostics: nearby torus probes still need code audit
  before reuse outside the corrected retained notes
- Wilson two-body lane: full both-masses law and action-reaction remain open
- boundary-law / holographic lane: keep the effect bounded and do not overread
  it as a holography derivation
- `2026-05-03-gbare-parent-retention-gate`
  Scope: `G_BARE_DERIVATION_NOTE.md` and downstream `g_bare = 1` status
  surfaces.
  Finding: the salvaged rescaling-freedom and constraint-vs-convention
  candidate rows must be independently audited and retained, with retained
  dependency closure, before the parent theorem or status surfaces cite them
  as closing repair targets.
  Disposition: `science-needed`.
- Planck Target 2 / area-law carrier: the simple-fiber Widom class is now
  closed negatively; any positive `1/4` entropy carrier needs a physical
  multi-pocket/multi-interval law or a gapped horizon-sector primitive-boundary
  theorem
- memory lane: protocol- and geometry-stable observable remains open
- emergent-geometry growth: multi-size, multi-seed stability remains open

## Intake Format

Record each new finding as one bullet:

- `ID`
  short label; date if needed
- `Scope`
  affected lane, note, script, or package surface
- `Finding`
  one-sentence statement of the issue
- `Disposition`
  one of: `triage`, `fix on main`, `support-only demotion`, `science-needed`,
  `reject`
- `Detail`
  optional link to a longer packet in work history

## Queue History

- `2026-04-18`
  repo-wide review/backlog cleanup completed; the old operational review
  packets and planning backlogs were moved out of the front-door `docs/`
  surface into [`docs/work_history/repo/review_feedback/`](../work_history/repo/review_feedback/README.md)
  and [`docs/work_history/repo/backlog/`](../work_history/repo/backlog/README.md)
