# Main Control-Plane Audit

**Date:** 2026-04-11  
**Scope:** coherence check of `main` after the latest staggered open-cubic promotion

Audited against `origin/main`:

- [`docs/repo/LANE_STATUS_BOARD.md`](/Users/jonreilly/Projects/Physics/docs/repo/LANE_STATUS_BOARD.md)
- [`docs/CANONICAL_HARNESS_INDEX.md`](/Users/jonreilly/Projects/Physics/docs/CANONICAL_HARNESS_INDEX.md)
- [`docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`](/Users/jonreilly/Projects/Physics/docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md)
- [`docs/PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md`](/Users/jonreilly/Projects/Physics/docs/PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md)
- [`docs/CLAUDE_FRONTIER_RETAIN_AUDIT_2026-04-11.md`](/Users/jonreilly/Projects/Physics/docs/CLAUDE_FRONTIER_RETAIN_AUDIT_2026-04-11.md)

## Verdict

The promoted control plane is broadly coherent.

What is aligned across the audited docs:

- the promoted staggered open-cubic companions are consistently treated as **bounded retained companions**, not as full Newton closure
- staggered both-masses and trajectory-level staggered two-body closure remain open
- the Wilson lane remains bounded rather than a retained full Newton claim
- the Ollivier lane remains bounded as a proxy, not an Einstein-equation derivation

## Finding

### 1. One dangling reference remained in the publication ledger

[`docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md`](/Users/jonreilly/Projects/Physics/docs/POTENTIAL_PUBLICATION_DISCOVERIES_LOG.md) entry `D30` previously pointed to a note that was not present on `main`.

This integration pass fixes the ledger so `D30` now cites only the retained
Anderson/eigenvalue note actually present on `main`.

## No Further Mainline Fixes Needed From This Audit

Outside the repaired `D30` reference, I did **not** find a new contradiction
requiring immediate edits.
