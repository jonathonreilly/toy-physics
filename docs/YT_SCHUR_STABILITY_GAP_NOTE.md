# Schur Stability Gap Note

**Date:** 2026-04-15
**Status:** bounded support theorem
**Primary runner:** `scripts/frontier_yt_schur_stability_gap.py`

## Role

This note answers a different remaining objection:

> perhaps the current exact Schur normal-form class is true, but only as a
> knife-edge condition with no real robustness margin.

The current package now shows that this is not the case.

## Result

The admissible exact Schur coarse-operator class sits inside an open stability
basin. The first normal-form escape occurs only after pushing beyond the unit
package budget radius.

So the class is not merely nonempty; it is robust.

## Meaning

This closes another layer of ambiguity:

- not only is the coarse normal-form class unique on the current tested scale
- it is also separated from the first escape by a positive stability gap

So the remaining YT gap is not fragility of the Schur class. It is only the
microscopic admissibility theorem that the true bridge belongs to this stable,
already-unique class.
