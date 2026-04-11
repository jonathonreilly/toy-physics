# Staggered Two-Body Detector-Side Transport Note

**Date:** 2026-04-11  
**Status:** bounded frontier hold  
**Script:** `scripts/frontier_staggered_two_body_transport.py`

## Question

Can the primary open-cubic staggered self-consistent two-body lane be upgraded
from a force-led positive to a transport-led closure by using a detector-side
transfer observable instead of a centroid readout?

This probe keeps the same physics as the retained staggered two-body lane:

- open 3D staggered cubic lattice
- two orbitals `psi_A`, `psi_B`
- shared self-consistent field
- self-only controls
- parity-correct scalar coupling

The only change is the observable.

## Observable

Instead of packet centroids, this probe measures the detector-side probability
transfer across the mid-plane between the packets:

- for packet `A` on the left, the inner detector side is the right half-space
- for packet `B` on the right, the inner detector side is the left half-space
- the transport score is the shared-minus-self inner-half transfer

This is a transport observable, not a position-moment observable.

## Audited Surface

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

Total rows:

- `45`

## Result

The exact partner-force channel stays clean:

- partner-force attractive: `45/45`

But the detector-side transfer observable does not improve closure:

- detector-side transfer inward: `0/45`
- transfer fit on inward rows only: `N/A`

Placement breakdown:

- `centered`: `0/15` inward
- `face_offset`: `0/15` inward
- `corner_offset`: `0/15` inward

The sign is not just weak. It is consistently on the wrong side for a
transport-closure claim: the shared-minus-self inner-half transfer is never
positive on the audited surface.

## Interpretation

This probe is a cleaner transport test than the centroid variants because it
tracks probability transfer into the detector-side half-space directly.

Even so, it does **not** close the staggered two-body lane:

- the force channel remains real
- the transport readout does not become inward
- no retained distance law follows from the detector-side transfer signal

## What This Means

The redesign answer is narrow and honest:

> detector-side transfer is a better observable than the blocked centroids, but
> on the audited open-cubic staggered surface it still does not produce a
> transport closure.

So this is a **hold**, not a promotion candidate.

## Next Step

If this lane is reopened again, the next observable should be a true current or
flux row defined directly on the links or detector plane, not another
probability-moment surrogate.

The current probe establishes only this:

- exact partner-force survives
- transport transfer does not close
- centroid replacement alone is not enough
