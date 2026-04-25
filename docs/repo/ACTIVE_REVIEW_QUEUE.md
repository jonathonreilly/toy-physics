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

As of `2026-04-25`, there are **no live repo-governance or claim-surface
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
- memory lane: protocol- and geometry-stable observable remains open
- emergent-geometry growth: multi-size, multi-seed stability remains open

### New as of 2026-04-25

- **Lorentz boost-covariance lane** (review-ready, full positive closure):
  five-phase landing on `lorentz-boost-covariance` branch off main:
  1. [LORENTZ_BOOST_COVARIANCE_GAP_NOTE](../LORENTZ_BOOST_COVARIANCE_GAP_NOTE.md)
     -- scope clarification.
  2. [LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE](../LORENTZ_BOOST_COVARIANCE_2D_THEOREM_NOTE.md)
     -- 1+1D SO(1,1) full boost covariance of the path-sum 2-point function;
     `frontier_lorentz_boost_2d.py` PASS=39.
  3. [ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE](../ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md)
     -- bounded no-go on the directional-measure kernel + decoupling theorem
     for Phase 4; `frontier_angular_kernel_underdetermination_nogo.py` PASS=64.
  4. [LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE](../LORENTZ_BOOST_COVARIANCE_3PLUS1D_THEOREM_NOTE.md)
     -- 3+1D SO(3,1) boost covariance of the continuum 2-point function with
     closed form `m K_1(m sqrt(-s²))/(4π² sqrt(-s²))` and dim-6 cubic-harmonic
     LV at finite `a`; `frontier_lorentz_boost_3plus1d.py` PASS=55.
  5. [LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE](../LORENTZ_KERNEL_POSITIVE_CLOSURE_NOTE.md)
     -- new primitives (P5a Causal Locality, P5b Per-Step Unitarity,
     P5c Reflection Symmetry, P5d Klein-Gordon Continuum Limit) jointly
     determine the kernel uniquely as the canonical Hamiltonian heat-kernel.
     Directional measure with `w = exp(-beta theta^2)` is explicitly excluded
     by (P5b) for any (beta, k); minimum unitarity defect 0.067 vs canonical
     machine-precision 7e-16. `frontier_lorentz_kernel_positive_closure.py`
     PASS=33.

  Lane status: full positive closure. Strict extension of
  EMERGENT_LORENTZ_INVARIANCE_NOTE from on-shell dispersion isotropy to
  off-shell SO(3,1) boost covariance, with the angular-kernel question
  uniquely closed under explicit primitives. Total tally: 191 PASS / 0 FAIL
  across 5 runners. Disposition: ready for review on the feature branch.

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
