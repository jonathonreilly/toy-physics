# Distance Law Breakpoint Note

**Date:** 2026-04-06  
**Status:** retained narrow breakpoint diagnosis

## Artifact Chain

- [`scripts/DISTANCE_LAW_BREAKPOINT_COMPARE.py`](/Users/jonreilly/Projects/Physics/scripts/DISTANCE_LAW_BREAKPOINT_COMPARE.py)
- [`logs/DISTANCE_LAW_BREAKPOINT_COMPARE.txt`](/Users/jonreilly/Projects/Physics/logs/DISTANCE_LAW_BREAKPOINT_COMPARE.txt)
- baseline portability result: [`docs/DISTANCE_LAW_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/DISTANCE_LAW_PORTABILITY_NOTE.md)
- sign invariant context: [`docs/SIGN_PORTABILITY_INVARIANT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SIGN_PORTABILITY_INVARIANT_NOTE.md)

## Question

Which architecture features preserve the near-Newtonian distance tail, and which
features break it, across the retained families?

## Retained Baseline

The two grown-family baselines are the preservation anchor:

- grown family 1: `alpha = -0.962`, `5/5 TOWARD`
- grown family 2: `alpha = -0.947`, `5/5 TOWARD`

These are the only rows in the breakpoint set that keep both the direction and
the near-Newtonian tail together.

## Breakpoints

- alt-connectivity family:
  - parity-tapered shell routing plus dense fallback
  - near-grown magnitude survives, but the direction flips
- third family:
  - deeper branch structure / cross-quadrant load balancing
  - the tail steepens hard and the retained sign orientation is lost
- fourth family:
  - quadrant-reflection symmetry
  - long-tail bias cancels under the reflection geometry
- fifth family radial:
  - radial-shell confinement / over-locked transport
  - direction survives, but the exponent collapses far below the retained tail

## Safe Diagnosis

The distance tail is not geometry-independent across the retained families.
The preserving feature is not the family label itself. It is the open,
directed transport regime that keeps the source-response chain from being
locked by symmetry or shell routing.

The break features are:

- parity-tapered shell routing
- dense fallback edges that rotate the response
- deeper branch structure
- quadrant-reflection symmetry
- radial confinement / shell locking

## Final Verdict

**retained narrow breakpoint diagnosis: the near-Newtonian distance tail
survives only in open directed transport families; shell-locking, reflection
closure, and deep branch routing break or flatten it**
