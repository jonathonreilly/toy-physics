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
