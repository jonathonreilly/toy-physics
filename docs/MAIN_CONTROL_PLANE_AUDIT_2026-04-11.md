# Main Control-Plane Audit

**Date:** 2026-04-11  
**Scope:** coherence check of `main` after the latest staggered open-cubic promotion

Audited against `origin/main`:

- [`docs/repo/LANE_STATUS_BOARD.md`](work_history/repo/LANE_STATUS_BOARD.md)
- [`docs/CANONICAL_HARNESS_INDEX.md`](CANONICAL_HARNESS_INDEX.md)
- [`docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`](work_history/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md)
- [`docs/PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md`](PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md)
- [`docs/CLAUDE_FRONTIER_RETAIN_AUDIT_2026-04-11.md`](CLAUDE_FRONTIER_RETAIN_AUDIT_2026-04-11.md)

## Verdict

The promoted control plane is broadly coherent after the latest bounded
Wilson/staggered promotions, but it is not fully cleaned down to a portable,
repo-local rerun surface everywhere.

What is aligned across the audited docs:

- the promoted staggered open-cubic companions are consistently treated as **bounded companions**, not as full Newton closure
- staggered both-masses and trajectory-level staggered two-body closure remain open
- the Wilson lane remains bounded rather than a retained full Newton claim
- the Ollivier lane remains bounded as a proxy, not an Einstein-equation derivation

## Findings

### 1. One dangling reference remained in the publication ledger

[`docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`](work_history/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md) entry `D30` previously pointed to a note that was not present on `main`.

This integration pass fixes the ledger so `D30` now cites only the retained
Anderson/eigenvalue note actually present on `main`.

### 2. Main-facing portability cleanup is now resolved on the audited surface

The earlier high-impact portability problem was that a broad historical slice
of docs still linked runners through one local `.claude/worktrees/...` layout.
That normalization is now fixed on the main-facing notes and lane readmes that
the control plane relies on.

What remains historical:

- branch/worktree names may still appear as provenance in older notes
- broader historical doc cleanup debt still exists outside the control-plane
  surface and is tracked in:
  [`docs/MAIN_REVISIT_SWEEP_2026-04-11.md`](MAIN_REVISIT_SWEEP_2026-04-11.md)

The repo baseline should therefore now be read as:

- corrected on the bounded-companion control-plane surface
- repo-local for the audited runner links
- still carrying some broader historical prose cleanup debt outside that
  surface

## Follow-Up Boundary

This audit no longer blocks `main`, but it does not imply the whole repo is
fully normalized. For reruns, prefer:

- [`docs/repo/LANE_STATUS_BOARD.md`](work_history/repo/LANE_STATUS_BOARD.md)
- [`docs/CANONICAL_HARNESS_INDEX.md`](CANONICAL_HARNESS_INDEX.md)
- [`docs/MAIN_REVISIT_SWEEP_2026-04-11.md`](MAIN_REVISIT_SWEEP_2026-04-11.md)
