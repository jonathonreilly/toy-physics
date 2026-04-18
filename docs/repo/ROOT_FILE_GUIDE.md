# Root File Guide

**Purpose:** explain the remaining top-level files that are not under `docs/`
or `scripts/`.

## Root Files

- `README.md`
  - current repo entrypoint
- `LICENSE`
  - license
- `requirements.txt`
  - minimal environment dependency pin
- `toy_event_physics.py`
  - large legacy implementation artifact; not the primary navigation entrypoint
- `ARCHITECTURE_OPTIONS.md`
  - historical architecture planning note
- `SCALING_BENCHMARK_TABLE.md`
  - historical scaling reference
- `SCALING_FAILURE_MECHANISMS.md`
  - historical scaling failure note
- `SCALING_TARGETS.md`
  - historical scaling/planning note
- `AUTOPILOT_PROTOCOL.md`
- `AUTOPILOT_JANITOR_PROTOCOL.md`
- `AUTOPILOT_SUMMARY_PROTOCOL.md`
- `AUTOPILOT_WORKLOG.md`
  - operational/project-maintenance files, not science entrypoints

## Reading Rule

If you are looking for physics state, do **not** start from the root files
above other than `README.md`. Start from:

- [`docs/START_HERE.md`](../START_HERE.md)
- [`docs/work_history/repo/LANE_STATUS_BOARD.md`](../work_history/repo/LANE_STATUS_BOARD.md)
- [`docs/repo/ACTIVE_REVIEW_QUEUE.md`](./ACTIVE_REVIEW_QUEUE.md) if you are
  checking live review feedback
