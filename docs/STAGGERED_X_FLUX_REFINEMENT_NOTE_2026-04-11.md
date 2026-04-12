# Staggered Two-Body X-Directed Flux Refinement Note

**Date:** 2026-04-11  
**Status:** bounded frontier hold  
**Source:** historical x-flux refinement commit `9ad140f`

## Question

Can the staggered two-body transport lane be upgraded by restricting shell flux
to the force axis only and removing the known `side=12` boundary artifact?

This refinement starts from the earlier staged two-body transport probes and
changes only the readout:

- keep the same open 3D staggered cubic surface
- keep the same shared self-consistent field and self-only controls
- restrict the shell flux to x-directed edges only
- drop `side=12`
- add `side=18` as a convergence check
- add a time-integrated impulse observable on the same x-directed shell flux

## Audited Surface

- sides: `14, 16, 18`
- placements:
  - `centered`
  - `face_offset`
  - `corner_offset`
- separations: `d = 3, 4, 5, 6, 7`
- `mass = 0.30`
- `G = 50.0`
- `mu2 = 0.001`
- `dt = 0.08`
- `N_steps = 10`
- packet width: `sigma = 0.80`

Total rows:

- `45`

## Result

The exact partner-force channel remains clean:

- partner-force attractive: `45/45`

The x-directed flux gate is also clean:

- x-directed shell flux both inward: `45/45`
- by side=14: `15/15`
- by side=16: `15/15`
- by side=18: `15/15`
- power-law `R^2` for flux magnitude vs separation: `~0.007`

But the time-integrated impulse does **not** converge:

- impulse both inward: `30/45`
- by side=14: `15/15`
- by side=16: `15/15`
- by side=18: `0/15`
- power-law `R^2` for impulse magnitude vs separation: `~0.016`

## Interpretation

The x-direction restriction removes the earlier dilution from `y/z` edges and
the `side=12` boundary artifact. That is a real improvement for the sign gate.

It still does **not** produce a retained staggered two-body trajectory law:

- the x-flux observable is qualitative only, not a quantitative force proxy
- the impulse observable is non-convergent and flips at `side=18`
- no portable distance law follows from either readout

## Honest Verdict

> On the audited open-cubic staggered surface (`sides = 14, 16, 18`,
> `G = 50`, `mu2 = 0.001`), the x-directed shell-flux gate is a strong
> qualitative sign check, but the impulse remains non-convergent and the lane
> still lacks trajectory closure. This remains a hold.

## Next Step

If this family is revisited, the next credible move is not another shell-flux
or impulse variant. It would have to be a genuinely new conserved-current
observable or a different graph geometry.
