# Distance Law Breakpoint Note

**Date:** 2026-04-06 (status line rephrased 2026-04-28 per audit-lane verdict)
**Status:** bounded narrow breakpoint table — the runner reprints hard-coded `alpha` / direction rows; the architecture-feature diagnosis (open directed vs shell vs reflection vs deep-branch routing) is not closed by matched ablation computations. Cited distance-law portability note is unknown; sign-invariant context is conditional. Not a tier-ratifiable architecture-feature theorem.

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

## Audit boundary (2026-04-28)

Audit verdict (`audited_conditional`, leaf criticality):

> Issue: the note turns a static breakpoint table into a causal
> architecture-feature diagnosis, but the runner only reprints
> hard-coded alpha/direction rows and labels. Why this blocks: the
> conclusion that open directed transport preserves the tail while
> shell routing, reflection closure, or deep branch routing break
> it requires either clean upstream rows or matched ablation
> computations; the cited distance-law portability note is unknown
> and the sign-invariant context is already conditional.

## What this note does NOT claim

- A tier-ratifiable architecture-feature theorem.
- That the runner re-derives the alpha/direction labels; it
  reprints them as hard-coded rows.
- That the cited distance-law portability note is audit-clean.

## What would close this lane (Path A future work)

A retained architecture-feature theorem would require:

1. A runner that performs matched ablation computations for shell
   routing, reflection closure, and deep-branch routing.
2. Audit-clean upstream rows for the distance-law portability note.
3. A sign-invariant authority registered as a one-hop dependency.
