# Staggered Two-Body Link-Current Note

**Date:** 2026-04-11  
**Status:** bounded frontier hold  
**Script:** `scripts/frontier_staggered_two_body_link_current.py`

## Question

Can a true mid-plane link-current observable close the staggered two-body
lane after detector-side transfer and centroid variants failed?

This probe keeps the same audited open-cubic staggered surface used by the
previous staggered two-body notes:

- open 3D staggered cubic lattice
- two orbitals `psi_A`, `psi_B`
- shared self-consistent field
- self-only controls
- parity-correct scalar coupling

The only change is the observable.

## Observable

Instead of packet centroids or half-space transfer, this probe measures the
bond current across the mid-plane between the packets.

For each orbital, the readout sums the x-oriented link current across the
central cut. Positive sign means left-to-right flow across the packet bisector.
For the right packet, the sign is flipped so that positive always means
inward flow toward the other packet.

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

But the true link-current observable does not improve closure:

- inward mid-plane current: `0/45`
- current fit on inward rows only: `N/A`

Placement breakdown:

- `centered`: `0/15` inward
- `face_offset`: `0/15` inward
- `corner_offset`: `0/15` inward

The current is not just weak. It is consistently on the wrong side for a
transport-closure claim on this surface.

## Interpretation

This is a cleaner transport test than the detector-side transfer surrogate
because it uses a true bond current across the plane between the packets.

Even so, it does **not** close the staggered two-body lane:

- the force channel remains real
- the link-current readout does not become inward
- no retained distance law follows from the current signal

## Honest Verdict

> On the audited open-cubic staggered surface (`sides = 12, 14, 16`,
> `G = 50`, `mu2 = 0.001`), the true link-current readout remains a hold.
> The force channel survives, but the transport channel stays `0/45` inward,
> so the staggered two-body lane still lacks closure.

## Next Step

If this lane is revisited, the next credible move is a momentum-flux or
impulse readout on the same surface, not another centroid or half-space
surrogate.

