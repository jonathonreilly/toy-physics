# Hadron Mass Program — Handoff

**Branch:** `frontier/hadron-mass-program-20260427`
**Workstream:** `hadron-mass-program-20260427`

## Current State

Pack scaffold built; grounding complete. No science cycles executed
yet. Selected Cycle-1 route: **R2 — Lane 3 dependency audit + Lane 1
theorem plan** (the lane file's explicit "first parallel-worker
target").

`STATE.yaml` is the single-source-of-truth resume surface.

## Next Exact Action

Execute Cycle 1 on Route R2:

1. Author
   `docs/HADRON_MASS_LANE1_THEOREM_PLAN_NOTE_2026-04-27.md`
   (Lane 3 dependency audit + Lane 1 theorem plan, structured per
   `ARTIFACT_PLAN.md`).
2. Branch-local 6-criterion self-review.
3. Commit to `frontier/hadron-mass-program-20260427`.
4. Refresh `STATE.yaml` (cycles_completed, current_phase) and append
   to `REVIEW_HISTORY.md`.
5. Push branch to `origin`. No PR.

## Repo-Wide Weaving (NOT to apply on this branch)

Proposed weaves are recorded in `ARTIFACT_PLAN.md`'s
"Repo-wide weaving" section. Do not apply on
`frontier/hadron-mass-program-20260427`. Per skill delivery policy,
this branch carries science only; repo-wide weaving is for
post-workstream review.

## Stop Conditions Status

- Runtime budget: 12h declared; significant remaining at scaffold-
  complete.
- Max cycles: not configured.
- Review blocker: none.
- External worktree change: not applicable (worktree fresh from
  `origin/main`).
- Target status achieved: no.
- Required network/literature/tool access unavailable: no.

Continue to Cycle 1.

## Notes for resume

If a future session picks this up via `--mode resume`:

1. Read `STATE.yaml` first.
2. Verify `branch` matches checkout and `base` is still `origin/main`
   (re-fetch if needed).
3. Confirm `lock_status: unavailable` is still the case
   (`scripts/automation_lock.py` path still hardcoded to
   `/Users/jonreilly`); skip cooperative lock per skill.
4. Resume from `next_exact_action`. Do not re-do the grounding or
   pack-build steps.
