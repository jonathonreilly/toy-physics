# Canonical Harness Index

**Date:** 2026-04-11  
**Purpose:** current retained runner map

This file is intentionally shorter than the historical version. It lists the
current runners people should actually use first, grouped by lane.

For lane status, use:

- [`docs/repo/LANE_STATUS_BOARD.md`](repo/LANE_STATUS_BOARD.md)

For retest workflow, use:

- [`docs/repo/RETEST_PLAYBOOK.md`](repo/RETEST_PLAYBOOK.md)

## 1. Primary Retained Surface

These are the first runners to trust for the current program:

- [`scripts/frontier_staggered_17card.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_17card.py)
- [`scripts/frontier_staggered_full_suite.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_full_suite.py)
- [`scripts/frontier_two_sign_parity.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_sign_parity.py)

Primary notes:

- [`docs/STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md)
- [`docs/FULL_TEST_MATRIX_2026-04-10.md`](FULL_TEST_MATRIX_2026-04-10.md)
- [`docs/GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md)

## 2. Retained Irregular-Graph Structural Surface

- [`scripts/frontier_staggered_cycle_battery.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_cycle_battery.py)
- [`scripts/frontier_staggered_cycle_battery_scaled.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_cycle_battery_scaled.py)
- [`scripts/frontier_staggered_self_gravity.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_self_gravity.py)
- [`scripts/frontier_staggered_self_gravity_scaling.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_self_gravity_scaling.py)
- [`scripts/frontier_two_field_wave.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_field_wave.py)
- [`scripts/frontier_two_field_retarded_family_closure.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_field_retarded_family_closure.py)
- [`scripts/frontier_staggered_dag.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_dag.py)
- [`scripts/frontier_staggered_graph_portable.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_staggered_graph_portable.py)

Key notes:

- [`docs/CYCLE_BATTERY_NOTE_2026-04-10.md`](CYCLE_BATTERY_NOTE_2026-04-10.md)
- [`docs/CYCLE_BATTERY_SCALED_NOTE_2026-04-10.md`](CYCLE_BATTERY_SCALED_NOTE_2026-04-10.md)
- [`docs/SELF_GRAVITY_SCALING_NOTE_2026-04-10.md`](SELF_GRAVITY_SCALING_NOTE_2026-04-10.md)
- [`docs/TWO_FIELD_RETARDED_FAMILY_CLOSURE_NOTE_2026-04-10.md`](TWO_FIELD_RETARDED_FAMILY_CLOSURE_NOTE_2026-04-10.md)
- [`docs/STAGGERED_DAG_NOTE_2026-04-10.md`](STAGGERED_DAG_NOTE_2026-04-10.md)

## 3. Open Directional Blocker Surface

These scripts should be run before making any new off-lattice gravity-direction
claim:

- [`scripts/frontier_irregular_directional_observable.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_irregular_directional_observable.py)
- [`scripts/frontier_two_sign_comparison.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_two_sign_comparison.py)

Key notes:

- [`docs/IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md`](IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md)
- [`docs/TWO_SIGN_COMPARISON_NOTE_2026-04-10.md`](TWO_SIGN_COMPARISON_NOTE_2026-04-10.md)

## 4. Exploratory Reopen Surface

- [`scripts/frontier_emergent_geometry_v2.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_emergent_geometry_v2.py)
- [`scripts/frontier_emergent_geometry_g_sweep.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_emergent_geometry_g_sweep.py)
- [`scripts/frontier_emergent_geometry_multisize.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_emergent_geometry_multisize.py)

Key note:

- [`docs/EMERGENT_GEOMETRY_GROWTH_NOTE_2026-04-10.md`](EMERGENT_GEOMETRY_GROWTH_NOTE_2026-04-10.md)

## 5. Historical / Legacy Entrypoints

Use these only if you are intentionally revisiting older lanes:

- mirror / exact geometry:
  - [`docs/UNIFIED_PROGRAM_NOTE.md`](UNIFIED_PROGRAM_NOTE.md)
  - [`scripts/mirror_2d_validation.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/mirror_2d_validation.py)
- ordered lattice / action-power / valley-linear:
  - [`docs/ACTION_ARCHITECTURE_MATRIX_NOTE.md`](ACTION_ARCHITECTURE_MATRIX_NOTE.md)
  - [`scripts/frontier_3plus1d_closure_card.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_3plus1d_closure_card.py)
- coin / chiral lane:
  - [`docs/CHIRAL_WALK_SYNTHESIS_2026-04-09.md`](CHIRAL_WALK_SYNTHESIS_2026-04-09.md)
  - [`scripts/frontier_chiral_bottleneck_card.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_chiral_bottleneck_card.py)
- generated geometry / Gate B:
  - [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)
  - [`scripts/gate_b_grown_joint_package.py`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/scripts/gate_b_grown_joint_package.py)

## Reading Rule

If a claim is not represented in:

- a runner,
- a retained note,
- and the lane board,

then it is not yet organized enough to treat as stable repo state.
