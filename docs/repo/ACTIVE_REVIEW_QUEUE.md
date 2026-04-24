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
  before reuse outside the corrected retained notes; the static-analysis
  audit in
  [`PERIODIC_TORUS_DIAGNOSTICS_CODE_AUDIT_NOTE_2026-04-24.md`](../PERIODIC_TORUS_DIAGNOSTICS_CODE_AUDIT_NOTE_2026-04-24.md)
  freezes a 9-script `NEEDS_REVIEW` list (out of 2048 scripts/*.py scanned),
  with all 9 canonical-corrected scripts validated as `CLEAN_*`. Manual
  per-script confirmation against the helper at
  `scripts/periodic_geometry.py` is the next step
- Wilson two-body lane: both-masses scaling closes at smoke-test level on the
  side=9 open-boundary cross-coupling acceleration (`a_a^cross / m_b` constant
  at `3.6%` CV across n=5 mass configs, see
  [`WILSON_TWO_BODY_ACTION_REACTION_BOTH_MASSES_NOTE_2026-04-23.md`](../WILSON_TWO_BODY_ACTION_REACTION_BOTH_MASSES_NOTE_2026-04-23.md));
  action-reaction at the per-packet centroid level remains open with the
  sharpened obstruction now identified as self-Hartree contamination of the
  heavier packet in the SHARED-SELF_ONLY differential protocol
- boundary-law / holographic lane: keep the effect bounded and do not overread
  it as a holography derivation; the area-law slope is seed-stable to ~2% CV
  and monotonically decreasing in G, but the gravity-induced suppression ratio
  `slope(G=10)/slope(G=0)` is NOT size-coherent (37% spread across
  sides 8/10/12/14, trending toward 1.0 with size — apparent finite-size
  effect, see [`BOUNDARY_LAW_COEFFICIENT_STABILITY_NOTE_2026-04-24.md`](../BOUNDARY_LAW_COEFFICIENT_STABILITY_NOTE_2026-04-24.md));
  extended to side in {16, 18, 20} in
  [`BOUNDARY_LAW_FINITE_SIZE_ASYMPTOTE_NOTE_2026-04-24.md`](../BOUNDARY_LAW_FINITE_SIZE_ASYMPTOTE_NOTE_2026-04-24.md):
  the suppression ratio fits `1 - C(G)/side` with RMS < 2%, asymptote at
  `side -> infinity` is approximately 1.0 within ~4% (consistent with no
  thermodynamic-limit gravity coefficient renormalization), and the
  finite-size constant `C(G)` grows monotonically and sub-linearly in G
  (C(5)=2.63, C(10)=4.21, C(20)=6.09)
- memory lane: protocol- and geometry-stable observable remains open
- emergent-geometry growth: multi-size, multi-seed stability remains open;
  failure pattern is now frozen with a `G=0` null control in
  [`EMERGENT_GEOMETRY_MULTISIZE_NULL_CONTROL_NOTE_2026-04-24.md`](../EMERGENT_GEOMETRY_MULTISIZE_NULL_CONTROL_NOTE_2026-04-24.md):
  the matter-coupling materially exceeds the null floor (force battery: G=100
  beats G=0 by `>= 2` ROBUST_TOWARD counts at all 5 sizes), but never reaches
  the unanimous 5/5 size-stability gate on either the force battery or the
  displacement test (max 4/5 at `n=80`)

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
