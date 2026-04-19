# DM Leptogenesis PMNS Real-Slice Intrinsic-Class Certificate

**Date:** 2026-04-16  
**Status:** real-slice intrinsic-class / interval-box certificate on the exact
reduced `N_e` chart  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_real_slice_intrinsic_class_certificate.py`

## Question

After the exact phase reduction to the real chart `delta = 0`, can the reduced
`N_e` selector story be upgraded beyond a generic branch scan into a tighter
intrinsic-class / interval-box certificate?

## Bottom line

Yes, as far as the current branch honestly supports.

The current exact reduced-domain story can now be read in three layers:

1. the phase competition is exactly reduced to the real slice
2. the anchor-free compact-chart search on that real slice recovers exactly
   three stationary branches
3. on the strict real slice, only the low and high local interval-box classes
   are stable; the nearby middle chart collapses back into the low class under
   local real-slice probing

The exact packet selector then chooses the low class uniquely.

## What is certified

The certificate uses the exact reduced `N_e` chart coordinates

`(u1, u2, v1, v2)`

with `delta = 0` held fixed on the physical real slice.

The anchor-free real-slice support pass already recovers:

- low branch
- nearby middle branch
- high branch

This note adds a stronger local class statement:

- build strict real-slice local interval boxes around the recovered low,
  nearby-middle, and high chart representatives
- probe each box locally with `delta = 0` held fixed
- verify that the low and high boxes each refine back to their own branch
  class
- verify that the nearby middle box is not locally stable on the strict real
  slice and instead falls back into the low class

So the current reduced chart does not look like a diffuse sea of comparable
physical branches. On the strict real slice it reduces to:

- a low class
- a high class
- a nearby off-real competitor that is not locally stable as its own real-slice
  class

## Why this matters

This is the natural analogue of the atlas-style "intrinsic class" certificates:

- the remaining issue is no longer "maybe the reduced chart hides a broad family
  of equally live physical branches"
- the strict real slice now carries two locally stable classes
- the nearby middle branch is no longer an equally live strict-real competitor
- the exact packet dominance-gap law picks the low class among them

So the branch science is closed more tightly than before.

## Honest boundary

This is still not full interval arithmetic over every point of the closure
manifold.

What it does give is:

- exact real-slice reduction
- anchor-free global reduced-chart branch recovery
- two locally stable strict-real-slice interval classes
- exact packet-level choice of the physical low class

So the live residual issue is certification style, not unresolved PMNS branch
physics.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_real_slice_intrinsic_class_certificate.py
```
