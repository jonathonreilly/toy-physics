# Start Here

**Date:** 2026-04-11  
**Purpose:** current navigation entrypoint for the repo

This repo is now too large to navigate by filename browsing alone. The right
way in is:

1. Read the lane map:
   [`docs/repo/LANE_STATUS_BOARD.md`](repo/LANE_STATUS_BOARD.md)
2. Read the repo organization layer:
   [`docs/repo/REPO_ORGANIZATION.md`](repo/REPO_ORGANIZATION.md)
3. Read the lane manifests:
   [`docs/lanes/README.md`](lanes/README.md)
4. Read the publication-discovery ledger:
   [`docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`](POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md)
5. Read the publication-discovery audit:
   [`docs/PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md`](PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md)
6. Read the retained runner map:
   [`docs/CANONICAL_HARNESS_INDEX.md`](CANONICAL_HARNESS_INDEX.md)
7. Read the bug / rerun workflow:
   [`docs/repo/RETEST_PLAYBOOK.md`](repo/RETEST_PLAYBOOK.md)
8. Read the rerun-required bug audit:
   [`docs/RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md`](RERUN_REQUIRED_BUG_AUDIT_2026-04-11.md)
9. Read the recent frontier retain audit:
   [`docs/CLAUDE_FRONTIER_RETAIN_AUDIT_2026-04-11.md`](CLAUDE_FRONTIER_RETAIN_AUDIT_2026-04-11.md)
10. Then read the current retained science state:
   [`docs/FULL_TEST_MATRIX_2026-04-10.md`](FULL_TEST_MATRIX_2026-04-10.md)

## Current Program Reality

The repo has one clear primary lane, but `main` also contains several major
historical retained programs.

- **Primary retained lane:** staggered fermion with corrected parity coupling
- **Cleanest directional result:** exact lattice-force canonical card
- **Strongest graph-native companion results:** cycle battery, scaled cycle
  battery, self-gravity, two-field wave, retarded family closure, and DAG
  compatibility
- **Main open blocker:** broader irregular off-lattice transport / portability
  closure beyond the bounded core-packet sign surface
- **Exploratory reopen:** emergent geometry growth, but only as a bounded,
  high-coupling partial positive

The older mirror / ordered-lattice / action / coin-walk programs are still in
the repo and still scientifically useful, but they are no longer the current
navigation baseline. Use the lane board to see exactly where each one sits.

## Whole-Repo Families

The lane board covers the whole repo, not just the current frontier. The main
families on `main` are:

- current mainline: staggered fermion + parity coupling
- current blocker: irregular off-lattice transport / portability beyond the
  bounded core-packet sign surface
- exploratory reopen: emergent geometry growth
- historical retained: mirror / exact geometry / `Z2 x Z2`
- historical retained: ordered lattice / dense spent-delay
- historical retained: nearest-neighbor refinement
- historical retained: structured chokepoint / generated-symmetry bridge
- historical bounded: action-power / valley-linear / dimension-dependent kernel
- historical bounded: generated geometry / Gate B / source-resolved
- historical blocked: coin / chiral / Dirac-walk line
- historical control: scalar / KG controls and moonshot horizon probes

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

1. [`scripts/frontier_staggered_cycle_battery.py`](../scripts/frontier_staggered_cycle_battery.py)
2. [`scripts/frontier_staggered_cycle_battery_scaled.py`](../scripts/frontier_staggered_cycle_battery_scaled.py)
3. [`scripts/frontier_staggered_self_gravity.py`](../scripts/frontier_staggered_self_gravity.py)
4. [`scripts/frontier_two_field_wave.py`](../scripts/frontier_two_field_wave.py)
5. [`scripts/frontier_two_field_retarded_family_closure.py`](../scripts/frontier_two_field_retarded_family_closure.py)
6. [`scripts/frontier_staggered_dag.py`](../scripts/frontier_staggered_dag.py)

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
