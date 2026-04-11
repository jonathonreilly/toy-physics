# Scripts Guide

**Purpose:** explain how to navigate the code side of the repo without reading
hundreds of filenames.

## Naming Conventions

- `frontier_*`
  - active frontier or later-stage retained runners
  - this is the current default namespace
- `mirror_*`, `lattice_*`, `gate_b_*`, `source_resolved_*`, `wave_*`
  - older major programs that are still important on `main`
- everything else
  - usually lane-specific historical or exploratory runners

## Current Default Runners

Start here for the current mainline:

- `frontier_staggered_17card.py`
- `frontier_staggered_full_suite.py`
- `frontier_staggered_cycle_battery.py`
- `frontier_staggered_cycle_battery_scaled.py`
- `frontier_staggered_self_gravity.py`
- `frontier_two_field_wave.py`
- `frontier_two_field_retarded_family_closure.py`
- `frontier_staggered_dag.py`
- `frontier_irregular_directional_observable.py`

## Whole-Repo Lane Index

Use the lane manifests in:

- [`docs/lanes/README.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/lanes/README.md)

That is the fastest way to know:

- which script family you are in
- whether it is current, historical, or blocked
- which note interprets the runner

## Runner Rules

- Do not assume a top-level script is canonical just because it exists.
- Check:
  - [`docs/CANONICAL_HARNESS_INDEX.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/CANONICAL_HARNESS_INDEX.md)
  - [`docs/repo/LANE_STATUS_BOARD.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/repo/LANE_STATUS_BOARD.md)
- If a bug affects semantics, use:
  - [`docs/repo/RETEST_PLAYBOOK.md`](/Users/jonreilly/Projects/Physics/.claude/worktrees/sleepy-cerf/docs/repo/RETEST_PLAYBOOK.md)
