# Branch Scrub Ledger

**Date:** 2026-04-12  
**Purpose:** record which source branches have been scrubbed into
`codex/review-active`, what was captured, and whether the source branch is safe
to archive

## Branches

### `origin/claude/youthful-neumann`

Status:

- partially scrubbed into `codex/review-active`

Captured in this pass:

- `docs/EM_GRAVITY_COEXISTENCE_2X2_NOTE.md`
- `scripts/em_gravity_coexistence_2x2.py`
- `docs/DISPERSION_RUNNING_EXPONENT_NOTE.md`
- `scripts/frontier_dispersion_running_exponent.py`
- `docs/HAWKING_BOGOLIUBOV_QUENCH_NOTE.md`
- `scripts/frontier_hawking_bogoliubov_quench.py`
- `docs/DISTANCE_LAW_64_FROZEN_CONTROL_NOTE.md`
- `scripts/frontier_distance_law_64_frozen_control.py`
- `docs/DISTANCE_LAW_DEFINITIVE_NOTE.md`
- `scripts/frontier_distance_law_definitive.py`
- `docs/ACTION_NORMALIZATION_NOTE.md`
- `scripts/frontier_action_normalization.py`
- `docs/BEYOND_LATTICE_QCD_NOTE.md`
- `scripts/frontier_beyond_lattice_qcd.py`
- `docs/DIAMOND_NV_EXPERIMENT_CARD.md`
- `docs/DIAMOND_NV_LATTICE_CORRECTION_NOTE.md`
- `scripts/frontier_diamond_nv_lattice_correction.py`
- `docs/POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md`
- `scripts/frontier_poisson_exhaustive_uniqueness.py`
- `docs/INDEPENDENT_SPATIAL_METRIC_NOTE.md`
- `scripts/frontier_independent_spatial_metric.py`

Already captured before this pass:

- the overnight audit bundle and its narrowed hold notes

Not yet archive-ready:

- yes; do not archive or delete yet

Reason:

- the branch still contains many additional docs/scripts beyond the bounded
  overnight candidates, and those need one more uniqueness pass before the
  branch can be marked fully captured

### `origin/codex/review-final-20260411`

Status:

- superseded by `origin/codex/review-active`

Archive readiness:

- archive-ready once downstream references are switched to `review-active`

### `origin/codex/resonance-controls`

Status:

- partially scrubbed into `codex/review-active`

Captured in this pass:

- `docs/LENSING_H025_EXACT_EDGE_REFERENCE_NOTE.md`
- `scripts/lensing_adjoint_kernel_reduced_model.py`
- `scripts/infinite_lattice_green_kernel.py`
- `docs/SPECTRAL_DIMENSION_CDT_AUDIT_2026-04-11.md`
- `scripts/frontier_spectral_on_lattice_fluxnorm.py`
- `scripts/frontier_geometric_baseline_control.py`
- `scripts/frontier_phase_strip_control.py`
- `docs/WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_THREE_FAMILY_TRANSFER_NOTE.md`
- `docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`
- `docs/WAVE_STATIC_MATRIXFREE_MOVING_SOURCE_FIXED_BEAM_BOUNDARY_NOTE.md`
- `scripts/wave_static_direct_probe.py`

Not yet archive-ready:

- yes; do not archive or delete yet

Reason:

- the branch still contains a large exploratory surface beyond the historical
  bounded slice above, including many older action-power, connectivity,
  generated-geometry, and causal/wave notes
- the imported slice preserves the cleanest repo-facing historical controls,
  but the branch still needs further uniqueness review before archive

### `origin/codex/irregular-sign-closure`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `docs/IRREGULAR_ENDOGENOUS_SIGN_CLOSURE_NOTE_2026-04-11.md`
- `scripts/frontier_irregular_endogenous_sign_closure.py`

Archive readiness:

- archive-ready

Reason:

- relative to `origin/frontier/spot-checks`, this branch's unique payload is the
  single shell-packet irregular sign-closure note+runner pair above, and that
  pair is now preserved on the active review branch

### `origin/codex/wilson-temporal-robustness`

Status:

- scrubbed into `codex/review-active`

Captured in this pass:

- `docs/TWO_BODY_ATTRACTION_FROZEN_SOURCE_NOTE_2026-04-11.md`
- `scripts/frontier_two_body_attraction_frozen_source.py`

Archive readiness:

- archive-ready

Reason:

- the branch-specific payload beyond the already-captured Wilson temporal and
  robustness notes is the frozen-source control pair above, and that pair is
  now preserved on the active review branch

## Codex First-Pass Triage

These statuses are mechanical only: whether the branch tip is already an
ancestor of `origin/main` or `origin/codex/review-active`. Non-ancestor status
means the branch still needs a uniqueness pass before archive.

### Already subsumed by `main`

- `origin/codex/main-distance-64`
- `origin/codex/main-newton-note`
- `origin/codex/main-open-cubic-validation`
- `origin/codex/main-post-validation`
- `origin/codex/strict-staggered-repro`

### Already subsumed by `review-active`

- `origin/codex/review-final-20260411`
- `origin/codex/main-open-cubic-validation`
- `origin/codex/main-post-validation`
- `origin/codex/strict-staggered-repro`

### Archive-ready now

These branches are already represented by `main` or `codex/review-active` and
do not need further science capture before archive:

- `origin/codex/review-final-20260411`
- `origin/codex/main-open-cubic-validation`
- `origin/codex/main-post-validation`
- `origin/codex/strict-staggered-repro`
- `origin/codex/main-distance-64`
- `origin/codex/main-newton-note`

### Likely archive-ready after one short verification pass

These appear to be promotion/integration helper branches rather than unique
science branches, but they still need a quick final diff audit before delete:

- `origin/codex/archive-main-retain-audit-20260411`
- `origin/codex/archive-main-wilson-bounded-20260411`

### Still need uniqueness review before archive

- `origin/codex/archive-automation-backup-20260411`
- `origin/codex/archive-claude-distracted-napier-20260411`
- `origin/codex/archive-main-retain-audit-20260411`
- `origin/codex/archive-main-wilson-bounded-20260411`
- `origin/codex/axiom-risk-ledger`
- `origin/codex/chiral-harness-tests`
- `origin/codex/irregular-sign-closure`
- `origin/codex/local-lorentzian-beamsplitter`
- `origin/codex/main-revisit-sweep`
- `origin/codex/next-session-tests`
- `origin/codex/resonance-controls`
- `origin/codex/source-weight-spectral`
- `origin/codex/staggered-direct-com`
- `origin/codex/wilson-temporal-robustness`
- `origin/codex/wilson-temporal-window-lane`
