# Staggered Two-Body Momentum-Flux Note

**Date:** 2026-04-11  
**Status:** bounded frontier hold  
**Script:** `scripts/frontier_staggered_two_body_momentum_flux.py`

## Question

Can a packet-local momentum-flux observable close the staggered two-body lane
after centroid variants, detector-side transfer, and the mid-plane link-current
readout all failed?

This probe keeps the same audited open-cubic staggered surface used by the
previous staggered two-body notes:

- open 3D staggered cubic lattice
- two orbitals `psi_A`, `psi_B`
- shared self-consistent field
- self-only controls
- parity-correct scalar coupling

The only change is the observable.

## Observable

Instead of a packet centroid or a global mid-plane cut, this probe measures a
packet-local transport flux:

- build a fixed control volume around each packet center
- read the bond current across the packet-facing outer face of that volume
- sign-adjust so positive always means flow toward the partner packet
- integrate the early-time flux into an impulse proxy

This is local to each packet edge, not a mid-plane surrogate.

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
- packet window radius: `2`

Total rows:

- `45`

## Result

The exact partner-force channel stays clean:

- partner-force attractive: `45/45`

But the packet-local momentum-flux observable does not improve closure:

- partner-facing flux inward: `0/45`
- flux fit on inward rows only: `N/A`
- impulse fit on inward rows only: `N/A`

Placement breakdown:

- `centered`: `0/15` inward
- `face_offset`: `0/15` inward
- `corner_offset`: `0/15` inward

Representative values are tiny and mostly negative:

- `flux_sym_mean` is typically in the `10^-6` to `10^-5` range with the
  wrong sign
- `impulse_sym` tracks the same sign

## Interpretation

This is a more local transport test than the mid-plane link-current probe
because the cut sits on the packet-facing edge of a control volume around each
orbital.

Even so, it does **not** close the staggered two-body lane:

- the force channel remains real
- the packet-local transport channel does not turn inward
- no retained distance law follows from the flux signal

## Honest Verdict

> On the audited open-cubic staggered surface (`sides = 12, 14, 16`,
> `G = 50`, `mu2 = 0.001`), the packet-local momentum-flux readout remains a
> hold. The force channel survives, but the transport channel stays
> `0/45` inward, so the staggered two-body lane still lacks closure.

## Next Step

If this lane is revisited, the next credible move is **not** another centroid
variant or another mid-plane cut. It would have to be a genuinely different
conserved-current formulation on the same surface, or a different graph
geometry entirely.

