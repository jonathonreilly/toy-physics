# Repo Organization

**Date:** 2026-04-11  
**Purpose:** stable navigation layer over a large, active research repo

## Why This Exists

The repo has accumulated:

- many historical architecture lanes
- many similarly named runner scripts
- notes that mix retained, bounded, and exploratory claims
- repeated semantic bugs in observables and runner assumptions

The correct fix is **not** a risky physical file move while science work is
still landing. The fix is a stable control plane:

- one lane board
- one canonical harness index
- one retest playbook
- one machine-readable lane registry

## Actual Layout

- `scripts/`
  - all runners and probes
  - `frontier_*` is the current frontier namespace
  - older non-`frontier_` scripts are often historical or lane-specific
- `docs/`
  - retained notes, synthesis notes, audits, backlogs, and historical writeups
- `docs/repo/`
  - navigation/control-plane docs added specifically to keep the repo usable
- `outputs/`, `logs/`
  - run artifacts and transient output

## Status Meanings

- `primary-retained`
  - current best-supported lane
  - this is where new readers should start
- `retained-companion`
  - real, replayable, and worth citing
  - but not the single top-level entrypoint
- `open-blocker`
  - a real missing piece that currently limits the main claim surface
- `exploratory-reopen`
  - partially positive but not yet promoted
- `historical-control`
  - useful for comparison, methodology, or negative controls
- `historical-bounded`
  - scientifically useful but no longer current flagship
- `historical-blocked`
  - a lane with a diagnosed mechanism-level blocker

## Navigation Files

- [`docs/repo/LANE_STATUS_BOARD.md`](LANE_STATUS_BOARD.md)
  - where each lane sits now
- [`docs/CANONICAL_HARNESS_INDEX.md`](../CANONICAL_HARNESS_INDEX.md)
  - which scripts to rerun first
- [`docs/repo/RETEST_PLAYBOOK.md`](RETEST_PLAYBOOK.md)
  - how to handle runner bugs or claim changes
- [`docs/repo/LANE_REGISTRY.yaml`](LANE_REGISTRY.yaml)
  - machine-readable registry for automation and future tooling

## File-Naming Rules Going Forward

- New current-program runners should stay in `scripts/` and use a clear,
  lane-specific prefix:
  - `frontier_staggered_*`
  - `frontier_two_field_*`
  - `frontier_emergent_geometry_*`
- New retained notes should be explicit about the runner they interpret.
- New strategy or synthesis notes should not silently replace retained notes.
- If a lane is historical, mark that in the lane board and registry instead of
  renaming dozens of files.

## How To Add New Work

When a new runner lands:

1. Decide which lane it belongs to.
2. Add or update its retained note if the result is promotable.
3. Update the relevant lane entry in:
   - [`docs/repo/LANE_STATUS_BOARD.md`](LANE_STATUS_BOARD.md)
   - [`docs/repo/LANE_REGISTRY.yaml`](LANE_REGISTRY.yaml)
4. If the result changes the retained program surface, also update:
   - [`docs/FULL_TEST_MATRIX_2026-04-10.md`](../FULL_TEST_MATRIX_2026-04-10.md)
   - [`docs/SESSION_SYNTHESIS_2026-04-10_FINAL.md`](../SESSION_SYNTHESIS_2026-04-10_FINAL.md)

## What This Organization Deliberately Does Not Do

- It does **not** move old scripts around while the frontier branch is active.
- It does **not** pretend every note in `docs/` is equally current.
- It does **not** merge exact-lattice force claims with irregular-graph proxy
  claims.
- It does **not** let a runner become “canonical” just because it exists.

This is a navigation and governance layer first. Physical file moves can come
later, after the active frontier stabilizes.
