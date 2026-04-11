# Irregular Endogenous Sign Size Portability Note

**Date:** 2026-04-11  
**Script:** `scripts/frontier_irregular_endogenous_sign_size_portability.py`  
**Status:** frontier-only, hold for `main`

This note is the size-portability discriminator for the irregular sign lane.
It keeps the original shell-packet observable and changes only graph size on
the same low-screening surface (`mu2 = 0.001`).

## Question

Does the same graph-native shell-packet sign separator survive graph growth on
the retained irregular families?

## Design

- same observable as the original shell-packet lane
- same low-screening surface
- same early-time window
- only graph size changes

Size grid:

- `6`
- `8`
- `10`
- `12`

Each size is replayed on the three irregular families:

- random geometric
- growing
- layered cycle

## Result

The sweep does **not** close the lane.

Key summary:

- `max_norm_drift = 1.332e-15`
- random geometric keeps `ball2_margin > 0` across all sizes
- layered cycle keeps `ball2_margin > 0` across all sizes
- growing does not: `ball2_margin` is negative or near-zero on most size rows
- `depth_margin` also fails to stay positive across the full size grid,
  especially on growing and on the larger layered-cycle rows

Representative failures:

- `size=6`, growing: `ball2_margin 0/10`, `depth_margin 4/10`
- `size=8`, layered_cycle: `ball2_margin 0/10`, `depth_margin 0/10`
- `size=10`, growing: `ball2_margin 2/10`, `depth_margin 8/10`
- `size=12`, layered_cycle: `ball2_margin 0/10`, `depth_margin 0/10`

## Honest Verdict

This is a real size-sensitivity check, but it does not upgrade the irregular
sign lane to bounded retention.

What it shows:

- the original shell-packet separator is not a one-size artifact
- it is still not portable enough across graph growth to close the lane

What it does not show:

- a graph-growth invariant irregular sign law
- a second portable packet family
- a third-family closure strong enough to override the hold

So the correct status is:

- `retain`: no
- `hold`: yes

## Next Step

If this lane is revisited, the next credible discriminator is no longer another
packet variant. It would need either:

- a genuinely independent packet family with the same sign readout, or
- a different observable altogether on the same irregular surface
