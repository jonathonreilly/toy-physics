# Start Here

**Date:** 2026-04-11  
**Purpose:** current navigation entrypoint for the repo

This repo is now too large to navigate by filename browsing alone. The right
way in is:

1. Read the lane map:
   [`docs/repo/LANE_STATUS_BOARD.md`](repo/LANE_STATUS_BOARD.md)
2. Read the repo organization layer:
   [`docs/repo/REPO_ORGANIZATION.md`](repo/REPO_ORGANIZATION.md)
3. Read the retained runner map:
   [`docs/CANONICAL_HARNESS_INDEX.md`](CANONICAL_HARNESS_INDEX.md)
4. Read the bug / rerun workflow:
   [`docs/repo/RETEST_PLAYBOOK.md`](repo/RETEST_PLAYBOOK.md)
5. Then read the current retained science state:
   [`docs/FULL_TEST_MATRIX_2026-04-10.md`](FULL_TEST_MATRIX_2026-04-10.md)

## Current Program Reality

The repo has one clear primary lane:

- **Primary retained lane:** staggered fermion with corrected parity coupling
- **Cleanest directional result:** exact lattice-force canonical card
- **Strongest graph-native companion results:** cycle battery, scaled cycle
  battery, self-gravity, two-field wave, retarded family closure, and DAG
  compatibility
- **Main open blocker:** no frozen sign-selective endogenous irregular-graph
  observable yet
- **Exploratory reopen:** emergent geometry growth, but only as a bounded,
  high-coupling partial positive

The older mirror / ordered-lattice / action / coin-walk programs are still in
the repo and still scientifically useful, but they are no longer the current
navigation baseline. Use the lane board to see exactly where each one sits.

## Read In This Order

If you want the current best result:

1. [`docs/STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md)
2. [`docs/FULL_TEST_MATRIX_2026-04-10.md`](FULL_TEST_MATRIX_2026-04-10.md)
3. [`docs/GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md)

If you want the current exact-vs-irregular distinction:

1. [`docs/GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md)
2. [`docs/IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md`](IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md)
3. [`docs/TWO_SIGN_COMPARISON_NOTE_2026-04-10.md`](TWO_SIGN_COMPARISON_NOTE_2026-04-10.md)

If you need the exact retained graph-native stack:

1. [`scripts/frontier_staggered_cycle_battery.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_cycle_battery.py)
2. [`scripts/frontier_staggered_cycle_battery_scaled.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_cycle_battery_scaled.py)
3. [`scripts/frontier_staggered_self_gravity.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_self_gravity.py)
4. [`scripts/frontier_two_field_wave.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_field_wave.py)
5. [`scripts/frontier_two_field_retarded_family_closure.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_field_retarded_family_closure.py)
6. [`scripts/frontier_staggered_dag.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_dag.py)

If you want to understand where historical lanes sit:

- [`docs/repo/LANE_STATUS_BOARD.md`](repo/LANE_STATUS_BOARD.md)

## Navigation Rules

- Treat `docs/repo/` as the control plane for the repo.
- Treat `docs/FULL_TEST_MATRIX_2026-04-10.md` as the retained score/state map.
- Treat `docs/SESSION_SYNTHESIS_2026-04-10_FINAL.md` as the narrative snapshot.
- Treat `scripts/frontier_*` as the current frontier namespace.
- Do not assume an old flagship note is current just because it is prominent.
  Check the lane board first.

## Historical Note

The older `START_HERE` content that centered mirror / ordered-lattice /
action-power as the main path has been superseded by the current navigation
layer. Those lanes are still in the repo, but they are now indexed as
historical or bounded lanes instead of the default entrypoint.
