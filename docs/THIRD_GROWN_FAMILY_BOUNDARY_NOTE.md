# Third Grown Family Boundary Note

**Date:** 2026-04-06  
**Status:** support - structural or confirmatory support note

## Artifact chain

- [`scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py`](/Users/jonreilly/Projects/Physics/scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py)
- [`logs/2026-04-06-third-grown-family-sign.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-third-grown-family-sign.txt)
- `docs/THIRD_GROWN_FAMILY_SIGN_NOTE.md` (sibling artifact in same lane;
  cross-reference only — not a one-hop dep of this note)

## Boundary read

The third grown family is not uniformly positive across the full tested window.

The failure mode is not control leakage:

- exact zero-source baselines stay zero
- exact neutral `+1/-1` cancellation stays zero

The boundary is sign-orientation reversal at the edges of the tested drift
window:

- `drift = 0.0` rows are sign-reversed
- `drift = 0.5` rows are sign-reversed
- the signed basin lives in the interior drift window

This is useful because it tells us the family is genuinely structured. It is
not a generic failure of the harness, and it is not a family-wide closure.

## Diagnosed boundary

The third family has a small signed-source basin centered in the tested drift
window, but the edge drifts fall into a clean opposite-sign regime.

That means the right interpretation is:

- a retained bounded basin exists
- the basin is narrow and drift-sensitive
- the boundary is structural, not a control artifact
