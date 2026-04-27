# 4D Distance Width Probe Note

**Date:** 2026-04-04  
**Status:** bounded support chain for the proposed_retained 4D valley-linear family; not an asymptotic closure claim

## Purpose

This note freezes the current width-limited 4D distance-law status on the
retained ordered-lattice family:

- action: `S = L(1-f)`
- kernel: `1/L^3`
- field: `f = s / r^2`
- measure: `h^3`

The goal was intentionally narrow:

- compare a small width ladder at fixed `h = 0.5`
- count how often the retained family stays `TOWARD`
- measure the early-tail and far-tail behavior
- state plainly whether the width ladder closes an asymptotic law

The answer is: it does **not** close asymptotic behavior here.

## Frozen artifact chain

- [`scripts/four_d_distance_width_probe.py`](/Users/jonreilly/Projects/Physics/scripts/four_d_distance_width_probe.py)
- [`logs/2026-04-04-four-d-distance-width-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-four-d-distance-width-probe.txt)
- heavier same-family companion log:
  - [`logs/2026-04-04-4d-wide-distance-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-4d-wide-distance-law.txt)

## Probe setup

- `h = 0.5`
- `L = 15`
- `strength = 5e-5`
- `max_d_phys = 2`
- width ladder: `W = 5, 6, 7`
- mass offsets: `z = 2..7`

This is the retained 4D family from the dimensional table, probed first at a
small width ladder and then once more at a heavier `W = 8` companion to see
how much distance-law support survives as width increases.

## Frozen results

| Width | TOWARD support | Peak | Early tail | Far tail | Read |
|---|---:|---|---|---|---|
| `W=5` | `4/4` | `z=4` | not fit | only 1 point beyond peak | width-limited |
| `W=6` | `5/5` | `z=4` | `b^(-0.43)`, `R²=0.713` | only 2 points beyond peak | width-limited |
| `W=7` | `6/6` | `z=4` | `b^(-0.60)`, `R²=0.800` | `b^(-0.96)`, `R²=0.915` | strongest row, still bounded |
| `W=8` | `6/6` | `z=4` | `b^(-0.54)` | far tail still too short to close | stronger support, still bounded |

## Safe interpretation

The retained 4D family is still genuinely `TOWARD` across the tested width
ladder and the heavier `W = 8` companion, and the support becomes cleaner as
width increases.

What this probe does **not** establish:

- a stable asymptotic 4D distance law
- convergence of the tail exponent to a single width-independent value
- a promoted Newtonian `1/b^2` closure in 4D

What it **does** establish:

- the 4D valley-linear family remains attractive in this tested window
- the tail behavior is width-sensitive
- the current 4D distance-law status is still bounded by width, not settled
- the heavier `W=8` companion is supportive, but it does not close the
  asymptotic law or promote a Newtonian `1/b^2` read

## Relation to the current dimensional table

This probe is consistent with the broader 4D row in
[DIMENSIONAL_GRAVITY_TABLE.md](/Users/jonreilly/Projects/Physics/docs/DIMENSIONAL_GRAVITY_TABLE.md):

- 4D remains on the retained `1/L^3` / `f = s / r^2` family
- the mass response stays near-linear
- the distance law remains width-limited
- the new width ladder gives a cleaner frozen support chain, but not a closure
  theorem

## Bottom line

The current 4D ordered-lattice family is still a **bounded support story**, not
a finished asymptotic distance-law result.

The strongest honest summary is:

- `TOWARD` survives across the tested widths
- the far tail strengthens as width increases, but the measured exponent still
  moves enough that the law is not yet width-stable
- the width ladder is still too small to close the asymptotic law
