# Higher-Symmetry Gravity Probe Note

**Date:** 2026-04-03  
**Status:** bounded gravity response, no review-safe law window

This note freezes the gravity-side follow-up for the retained higher-symmetry
lane, using the dedicated probe in:

[`scripts/higher_symmetry_gravity_probe.py`](/Users/jonreilly/Projects/Physics/scripts/higher_symmetry_gravity_probe.py)

Log:

[`logs/2026-04-03-higher-symmetry-gravity-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-higher-symmetry-gravity-probe.txt)

## Question

The joint validation already showed that `Z2 x Z2` is Born-clean, gravity-
positive, and decohering. The remaining question was whether that gravity
signal has an actual mass or distance law, or whether it is only a positive
joint pocket.

This probe used the same `Z2 x Z2` geometry family as the joint validator and
ran two narrow checks:

- fixed-anchor mass prefixes on the gravity layer
- fixed-mass distance sweeps on the same retained geometry

## Setup

- family: `Z2 x Z2`
- `16` seeds
- `N = 25, 40, 60, 80, 100`
- `z2z2_quarter = 12` (`48` total nodes per layer)
- `connect_radius = 5.0`
- `anchor_b = 5.0`
- fixed mass count for distance sweep: `4`
- `k` band: `3, 5, 7`

## Fixed-Anchor Mass Window

The mass window is positive, but it is not clean enough to freeze as a hardened
law.

Representative fits:

### `N = 25`

- window fit `M in {2,3,5,8}`
- `delta ~= 0.2146 * M^0.404`
- `R^2 = 0.218`

### `N = 40`

- window fit `M in {2,3,5,8}`
- `delta ~= 0.3220 * M^0.490`
- `R^2 = 0.752`

### `N = 60`

- window fit `M in {2,3,5,8}`
- `delta ~= 0.0343 * M^1.828`
- `R^2 = 0.798`

### `N = 100`

- window fit `M in {2,3,5,8}`
- `delta ~= 0.3712 * M^0.500`
- `R^2 = 0.135`

## Fixed-Distance Sweep

The distance sweep does not produce a review-safe falling tail.

Observed pattern:

- the mean response is often positive
- the curve peaks inside the tested window
- there are not enough falling-tail points for a robust power-law fit

Representative peak rows:

### `N = 25`

- peak mean deflection near `b = 8.0`
- no review-safe tail fit

### `N = 40`

- peak mean deflection near `b = 8.0`
- no review-safe tail fit

### `N = 60`

- peak mean deflection near `b = 12.0`
- no review-safe tail fit

### `N = 80`

- no positive falling tail

### `N = 100`

- peak mean deflection near `b = 8.0`
- no review-safe tail fit

## Retained Conclusion

The gravity-side picture for `Z2 x Z2` is:

- **positive response:** yes
- **usable mass law window:** not yet
- **usable distance law:** no
- **gravity contender:** not yet

The strongest supported statement is therefore:

- `Z2 x Z2` is a real **decoherence lead** that stays Born-clean and keeps a
  positive gravity signal
- but it does **not** yet have a review-safe gravity law window comparable to
  the retained mirror boundary probe

So the current safe ranking is:

1. Mirror chokepoint remains the stronger gravity-side pocket
2. `Z2 x Z2` remains the strongest higher-symmetry decoherence lead
3. The gravity-law question for `Z2 x Z2` is still open

