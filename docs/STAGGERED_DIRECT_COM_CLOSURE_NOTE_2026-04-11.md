# Staggered Direct-CoM Closure Probe

**Date:** 2026-04-11  
**Status:** frontier-only bounded negative  
**Script:** `scripts/frontier_staggered_direct_com_closure.py`

## Question

Can the primary open-cubic staggered two-body lane be upgraded from a
force-led positive to a **direct-CoM closure** using a stronger parity-aware
readout?

The earlier portability probe already showed that a simple local pair-block
centroid was not enough. This follow-up kept the same staggered physics and
replaced only the readout.

## Readout

For each packet:

1. coarse-grain the density into `2x2x2` staggered taste cells
2. build a packet-local `x` profile in a fixed local cell window
3. estimate the **direct mutual shift** by aligning the `SHARED` profile
   directly against the `SELF_ONLY` profile on the same time slice

This is a better small-signal observable than the previous centroid attempt,
because it measures the relative translation between two nearly identical local
envelopes instead of subtracting two separately unstable centroids.

Positive inward convention:

- left packet A: `shared` shifted right relative to `self_only`
- right packet B: `shared` shifted left relative to `self_only`

## Audited surface

- open 3D staggered cubic lattice
- sides: `12, 14, 16`
- placements:
  - `centered`
  - `face_offset`
  - `corner_offset`
- separations: `d = 3, 4, 5, 6, 7`
- `mass = 0.30`
- `G = 50.0`
- `mu2 = 0.001`
- `dt = 0.08`
- `N_steps = 8`
- packet width: `sigma = 0.80`
- local readout window: `WINDOW_BLOCKS = 3`

Total rows:

- `45`

## Exact result

- partner-force attractive: `45/45`
- template-shift inward: `18/45`
- template-shift law on inward rows only:
  - `<dx_mut> ~ d^-0.623`
  - `R^2 = 0.0591`

Placement breakdown:

- `centered`: `6/15` inward, fit `-0.644`, `R^2 = 0.0621`
- `face_offset`: `6/15` inward, fit `-0.641`, `R^2 = 0.0601`
- `corner_offset`: `6/15` inward, fit `-0.583`, `R^2 = 0.0553`

Representative rows:

- `centered, side=12, d=3`
  - force `+4.9556e-01`
  - template shifts `(+3.333e-03, +3.833e-03)`
  - inward
- `centered, side=12, d=5`
  - force `+1.8543e-01`
  - template shifts `(-3.667e-03, -3.167e-03)`
  - outward
- `centered, side=12, d=6`
  - force `+1.3118e-01`
  - template shifts `(+5.000e-04, +5.000e-04)`
  - nearly zero / ambiguous

## What improved

Relative to the earlier local pair-block centroid probe:

- old local direct-CoM inward count: `5/45`
- new template-shift inward count: `18/45`

So the parity-aware template shift is a **better** direct-CoM readout than the
simple local centroid.

## Why it still fails

The improved readout still does not define a retained trajectory law.

Failure mode:

- exact partner-force stays clean on every row
- direct-CoM signs alternate with separation instead of staying uniformly inward
- the fitted distance law on the surviving inward rows is weak and not Newtonian

The most visible pattern is:

- `d = 3, 7` often inward
- `d = 5` often outward
- `d = 4, 6` frequently collapse to near-zero relative shift

That is a parity / blocking aliasing pattern, not a stable trajectory law.

## Interpretation

This is the strongest honest direct-CoM attempt on the current bounded
staggered self-consistent surface, and it still does **not** close the lane.

What is now established:

- the staggered self-consistent two-body channel is real in exact partner-force
  observables
- a stronger parity-aware direct-CoM readout improves over naive local
  centroids
- but direct trajectory-level closure still fails on the primary architecture

## Bottom line

The correct bounded frontier statement is:

> On the primary open-cubic staggered architecture, a parity-aware `2x2x2`
> cell-envelope template-shift readout improves the direct-CoM signal relative
> to naive local centroids, but it still fails to produce a portable inward
> trajectory law. The staggered two-body lane remains force-led rather than
> direct-CoM closed.
