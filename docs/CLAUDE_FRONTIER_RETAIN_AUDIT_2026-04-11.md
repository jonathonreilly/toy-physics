# Claude Frontier Retain Audit — 2026-04-11

**Purpose:** classify the late 2026-04-11 Claude frontier batch into:

- safe to retain on `main`
- frontier-only until further audit
- fix/rerun or redesign before reuse

This note is about the **recent Claude frontier wave**, not the whole repo.
Use it with:

- [CODE_REVIEW_LAST_WEEK_2026-04-11.md](CODE_REVIEW_LAST_WEEK_2026-04-11.md)
- [RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md](RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md)
- [PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md](PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md)
- [repo/LANE_STATUS_BOARD.md](repo/LANE_STATUS_BOARD.md)

## Retain To `main`

These items are useful, honestly framed, and coherent enough to become part of
the repo baseline.

### 1. Review / rerun control-plane hardening

Keep:

- [CODE_REVIEW_LAST_WEEK_2026-04-11.md](CODE_REVIEW_LAST_WEEK_2026-04-11.md)
- [RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md](RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md)

Why:

- they capture the real bugs from the last-week frontier surface
- they stop stale or invalid runners from being silently promoted

### 2. Wilson `mu^2` distance calibration

Keep:

- [WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md](WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md)
- [scripts/frontier_wilson_mu2_sweep.py](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_wilson_mu2_sweep.py)

Why:

- this is the cleanest diagnosis of the steep Wilson distance exponent
- the current note is careful: it says the exponent is **screening-controlled**
  and becomes Newton-compatible as `mu^2` is reduced
- it does **not** overclaim full Newton closure

### 3. Memory `mu^2` / geometry diagnostic

Keep:

- [MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md](MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md)
- [scripts/frontier_memory_mu2_size_sweep.py](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_memory_mu2_size_sweep.py)

Why:

- it corrects an important false simplification
- the honest result is that memory fragility is **not purely** a Yukawa-range
  effect; geometry scaling and boundary placement matter at least as much

### 4. Born-rule boundary marker

Keep:

- [BORN_RULE_ANALYSIS_2026-04-11.md](BORN_RULE_ANALYSIS_2026-04-11.md)

Why:

- it is a useful boundary statement, not a positive claim
- it correctly says the old alpha sweep was probing fixed-point smoothness, not
  measurement theory

### 5. Spectral / trajectory theory memo

Keep as a memo, not a theorem:

- [SPECTRAL_TRAJECTORY_THEOREM_2026-04-11.md](SPECTRAL_TRAJECTORY_THEOREM_2026-04-11.md)

Why:

- it is a coherent organizing document for the current scientific state
- it should be read as an interpretive framework built from the repo record,
  not as a proven theorem

## Frontier-Only For Now

These are not necessarily wrong, but they are not yet `main`-grade.

### 1. Full Newton-law headline

Do not retain as a repo truth yet:

- `scripts/frontier_wilson_unscreened.py`
- `scripts/frontier_wilson_newton_law.py`
- `scripts/frontier_newton_both_masses.py`

Reason:

- the distance-law side is now much stronger
- the mass-law side is still not closed on a valid both-masses runner
- the old periodic Wilson runner only tested source-strength scaling

Current honest baseline:

> the open Wilson distance exponent is strongly controlled by `mu^2` and
> becomes Newton-compatible as screening is reduced; full Newton closure is
> still pending a valid both-masses law on the same surface

### 2. BMV / branch-entanglement extensions

Keep bounded retained notes that are already honest, but do not promote the
stronger new frontier claims yet.

Reason:

- current branch/BMV runners still do not implement a full gravity-quantumness
  witness
- the corrected bounded 2-body and W-type 3-body notes are already enough for
  `main`

### 3. Ollivier / Einstein, graph selection, topological, CDT quantitative,
Hartree N-body, mirror Z2, error correction

Leave on frontier until separately audited.

Reason:

- several sit on periodic 2D surfaces that need extra scrutiny because of the
  validated wraparound-weight bug class
- others are plausible but still only represented by a fresh frontier script
  plus a claim-heavy session narrative

### 4. Screening-fix global narrative

Do not retain [SCREENING_FIX_RECHECK_LIST_2026-04-11.md](SCREENING_FIX_RECHECK_LIST_2026-04-11.md) to `main` as written.

Reason:

- it overstates the shared diagnosis
- `mu^2 = 0.22` was a major confound for some lanes, but not the universal root
  cause of everything involving Poisson coupling

## Fix / Rerun Or Redesign Before Reuse

Use [RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md](RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md) as the detailed source. The highest-priority items are:

### 1. Periodic 2D wraparound-weight bug

Affected examples:

- `scripts/frontier_self_consistency_test.py`
- `scripts/frontier_eigenvalue_stats_and_anderson_phase.py`
- `scripts/frontier_born_rule_alpha.py`

Impact:

- periodic 2D follow-on claims from the late frontier wave should not be
  promoted again until this is fixed and rerun

### 2. Self-consistency random controls

Affected:

- `scripts/frontier_self_consistency_test.py`

Impact:

- the deterministic `self-consistent` vs `static` split is still useful
- the stronger sigma-like random-control language needs corrected nulls

### 3. Invalid or redesign-only claim surfaces

Do not rerun in current form:

- `scripts/frontier_two_body_mutual_attraction.py`
- `scripts/frontier_wilson_newton_law.py`
- `scripts/frontier_born_rule_alpha.py`
- `scripts/frontier_entanglement_area_law.py`
- `scripts/frontier_bekenstein_hawking.py`

## Practical Reading Rule

If a recent Claude result is only present in:

- a new `frontier_*` runner
- a session summary
- and no honest retained note

then treat it as **frontier-only** until this audit is updated.
