# Irregular Endogenous Sign Reinforcement Note

**Date:** 2026-04-11  
**Script:** `scripts/frontier_irregular_endogenous_sign_reinforcement.py`  
**Status:** reinforcement run, hold unless both packet families close cleanly

This note is the minimal promotion-pressure follow-up to the original
irregular sign closure result.

It tests exactly the two missing checks called out in the next-steps note:

1. low-screening replay on the same observable
2. one second packet family on the same same-surface sign readout

## What Was Rechecked

The runner keeps the original graph-native matter-response observable:

- `ball1_margin`
- `ball2_margin`
- `depth_margin`

and replays it on the same irregular families:

- random geometric
- growing
- layered cycle

The packet families are:

- `shell_phase`
- `core_gaussian`

The low-screening surface is:

- `mu2 = 0.001`

The verdict rule is strict:

- if both packet families keep `ball2_margin > 0` and `depth_margin > 0` on all
  audited family/seed/G rows, the lane can move toward bounded retention
- otherwise the lane remains frontier-only

## Result

The reinforcement run does **not** close the lane.

Key output:

- `shell_phase`: `ball2_margin` only `13/30` positive overall and `depth_margin`
  only `10/30` positive overall
- `core_gaussian`: `ball2_margin` `30/30` positive and `depth_margin` `28/30`
  positive, but `ball1_margin` and `depth_margin` still miss exact closure on a
  few rows

The shell-packet sign result remains the strongest same-surface separator in the
repo, but the low-screening replay and the second packet family are not enough to
upgrade the lane to bounded main retention.

So the correct status is:

- `retain`: no
- `hold`: yes

## Why It Stays Frontier-Only

- the original shell packet was strong on the screened surface
- the low-screening replay is the right stress test, and it is not enough by
  itself
- the second packet family does not yet show portable closure at the same level
  as the original shell packet

## Promotion Pressure Outcome

This is still a real irregular-sign result, but it remains a **bounded frontier
win**, not a `main` retention candidate.

Required next work if this lane is revisited:

- add a third packet family only if it is genuinely independent
- or add a size-portability sweep on the current shell packet
- or add an unscreened control with a stronger portability argument
