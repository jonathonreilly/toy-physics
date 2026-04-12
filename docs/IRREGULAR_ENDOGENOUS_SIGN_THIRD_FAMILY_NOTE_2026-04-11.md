# Irregular Endogenous Sign Third-Family Note

**Date:** 2026-04-11  
**Script:** `scripts/frontier_irregular_endogenous_sign_third_family.py`  
**Status:** third-family discriminator, hold for `main`

This note is the last irregular-sign discriminator requested after:

- the original shell-packet sign-closure result
- the low-screening reinforcement replay
- the size-portability sweep

The goal here was deliberately narrow:

- keep the same irregular graph families
- keep the same low-screening surface (`mu2 = 0.001`)
- keep the same same-surface sign readout
- replace the packet family with a genuinely independent annulus packet

## Question

Does a third independent packet family preserve the same-surface sign separator
on the retained irregular bipartite families?

## Design

The packet is graph-native once the graph is fixed:

```text
psi_0(d) ~ exp(-(d - r0)^2 / (2 sigma_r^2))
```

with

- `r0 = 3.0`
- `sigma_r = 1.0`

The same three irregular families are tested:

- random geometric
- growing
- layered cycle

The same early-time window and same observables are used:

- `ball1_margin`
- `ball2_margin`
- `depth_margin`

Positive margins mean attraction keeps the packet closer to the source region
than repulsion on the same surface.

## Result

The annulus family does **not** close the lane.

### Global summary

- `ball1_margin`: `20/30` positive
- `ball2_margin`: `22/30` positive
- `depth_margin`: `30/30` positive
- `max_norm_drift = 5.551e-16`

### Family-level read

- `random_geometric`: `ball2_margin` is negative or nearly zero on most rows
- `growing`: positive on all audited rows
- `layered_cycle`: positive on all audited rows

The positive depth separation is real, but the stricter same-surface packet
closure is not portable enough across the full audited surface.

## Honest Verdict

This third-family run adds hold pressure, not retain pressure.

What it shows:

- the irregular sign effect is not just the original shell packet
- the annulus packet still sees attraction stay closer than repulsion on many
  rows

What it does not show:

- a third-family closure strong enough for bounded main retention
- portable same-surface sign closure across all audited irregular rows
- a different irregular observable that would supersede the current packet
  readout

So the correct status is:

- `retain`: no
- `hold`: yes

## Next Step

If this lane is revisited, the next credible move is no longer another packet
shape. It would need a different observable on the same irregular surface.
