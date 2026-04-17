# Retest Playbook

**Date:** 2026-04-11  
**Purpose:** how to retest the repo when a runner bug or semantic bug is found

Current rerun-required bug ledger:

- [`docs/RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md`](../RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md)

## 1. Pick The Lane First

Before rerunning anything, identify the lane in:

- [`docs/work_history/repo/LANE_STATUS_BOARD.md`](../work_history/repo/LANE_STATUS_BOARD.md)

Do not start from filenames alone. The same bug class can mean different
things on:

- exact lattice-force runners
- irregular-graph proxy runners
- historical coin/action lanes

## 2. Reproduce At The Smallest Honest Surface

Use the smallest retained runner that actually carries the claim:

- exact cubic directional claim:
  - [`scripts/frontier_staggered_17card.py`](../../scripts/frontier_staggered_17card.py)
- irregular structural interaction claim:
  - [`scripts/frontier_staggered_cycle_battery.py`](../../scripts/frontier_staggered_cycle_battery.py)
- scaled irregular claim:
  - [`scripts/frontier_staggered_cycle_battery_scaled.py`](../../scripts/frontier_staggered_cycle_battery_scaled.py)
- endogenous self-gravity:
  - [`scripts/frontier_staggered_self_gravity.py`](../../scripts/frontier_staggered_self_gravity.py)
- two-field retarded sibling:
  - [`scripts/frontier_two_field_retarded_family_closure.py`](../../scripts/frontier_two_field_retarded_family_closure.py)
- causal DAG compatibility:
  - [`scripts/frontier_staggered_dag.py`](../../scripts/frontier_staggered_dag.py)
- emergent geometry:
  - [`scripts/frontier_emergent_geometry_v2.py`](../../scripts/frontier_emergent_geometry_v2.py)
  - [`scripts/frontier_emergent_geometry_g_sweep.py`](../../scripts/frontier_emergent_geometry_g_sweep.py)

## 3. If The Bug Touches Gravity Direction

You must split exact-lattice from irregular-graph immediately.

### Exact lattice / direct external-potential sign

Rerun:

- [`scripts/frontier_staggered_17card.py`](../../scripts/frontier_staggered_17card.py)
- [`scripts/frontier_two_sign_parity.py`](../../scripts/frontier_two_sign_parity.py)

Interpretation:

- this is the only retained surface that currently supports a clean
  directional-gravity claim

### Irregular graph sign / direction

Rerun:

- [`scripts/frontier_irregular_directional_observable.py`](../../scripts/frontier_irregular_directional_observable.py)
- [`scripts/frontier_two_sign_comparison.py`](../../scripts/frontier_two_sign_comparison.py)
- whichever retained irregular battery is implicated

Interpretation:

- do not promote shell/edge-radial inwardness to directional gravity without a
  sign-selective same-surface observable

## 4. If The Bug Touches Field Law / Backreaction

Rerun in this order:

1. [`scripts/frontier_staggered_self_gravity.py`](../../scripts/frontier_staggered_self_gravity.py)
2. [`scripts/frontier_two_field_wave.py`](../../scripts/frontier_two_field_wave.py)
3. [`scripts/frontier_two_field_retarded_family_closure.py`](../../scripts/frontier_two_field_retarded_family_closure.py)
4. [`scripts/frontier_staggered_backreaction_green_closure.py`](../../scripts/frontier_staggered_backreaction_green_closure.py) if the bug touches scale closure specifically

## 5. If The Bug Touches Growth / Geometry

Rerun:

- [`scripts/frontier_emergent_geometry_v2.py`](../../scripts/frontier_emergent_geometry_v2.py)
- [`scripts/frontier_emergent_geometry_g_sweep.py`](../../scripts/frontier_emergent_geometry_g_sweep.py)
- [`scripts/frontier_emergent_geometry_multisize.py`](../../scripts/frontier_emergent_geometry_multisize.py) if size dependence is implicated

## 6. Environment

Default replay environment:

```bash
source .venv/bin/activate
python scripts/frontier_staggered_17card.py
```

Use repo-root relative execution from the worktree. Avoid ad hoc copies of
scripts in scratch directories.

## 7. Required Docs To Update If Semantics Change

If a bug changes a retained claim, update all affected surfaces:

- lane note for the runner
- [`docs/FULL_TEST_MATRIX_2026-04-10.md`](../FULL_TEST_MATRIX_2026-04-10.md)
- [`docs/SESSION_SYNTHESIS_2026-04-10_FINAL.md`](../SESSION_SYNTHESIS_2026-04-10_FINAL.md)
- [`docs/work_history/repo/LANE_STATUS_BOARD.md`](../work_history/repo/LANE_STATUS_BOARD.md)
- [`docs/repo/LANE_REGISTRY.yaml`](LANE_REGISTRY.yaml)

Also update these when the bug is sign-related:

- [`docs/GRAVITY_SIGN_AUDIT_2026-04-10.md`](../GRAVITY_SIGN_AUDIT_2026-04-10.md)
- [`docs/TWO_SIGN_COMPARISON_NOTE_2026-04-10.md`](../TWO_SIGN_COMPARISON_NOTE_2026-04-10.md)

## 8. Guardrails

- Do not count `SKIP` or `N/A` as `PASS`.
- Do not merge exact-force and proxy-force semantics.
- Do not let a new script silently replace a retained runner without updating
  the lane board and matrix.
- Do not summarize a lane from memory. Read the retained note and runner first.
