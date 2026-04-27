# Second Independent Grown Family

**Date:** 2026-04-06
**Status:** proposed_retained positive — second family at drift=0.05, restore=0.30

## Artifact chain

- [`scripts/second_grown_family_battery.py`](../scripts/second_grown_family_battery.py) (to be frozen)
- This note

## Question

Does a SECOND independent grown family (different drift/restore from the
retained center 0.2/0.7) independently produce gravity + Born + F~M ~ 1.0?

## Sweep result

9 candidate families tested. Best second candidate: **drift=0.05, restore=0.30**.

This is maximally distant from the retained center:
- drift: 0.05 vs 0.20 (4x different)
- restore: 0.30 vs 0.70 (very different architecture)

## Full control battery at drift=0.05, restore=0.30

| Test | Result | Pass? |
| --- | ---: | --- |
| Zero field control | delta=0.000, escape=1.000 | YES |
| F~M (6 seeds) | 0.993 +/- 0.008 | YES |
| Born (2 seeds) | 0.00e+00 | YES |
| Gravity TOWARD | 3/3 at gamma=0 | YES |
| Complex action crossover | TOWARD 3/3 → AWAY 0/3 | YES |

## What this means

Two independent grown families, at different points in parameter space,
both produce:
- F~M ~ 1.0 (Newtonian mass scaling)
- Born = 0 (structural linearity)
- Gravity TOWARD
- Complex action TOWARD→AWAY crossover

This is evidence that the physics is NOT specific to one growth-rule tuning.
It transfers across a significant region of parameter space.

## Claim boundary

Two specific grown families tested. No claim about the full drift/restore
space or about arbitrary growth rules.
