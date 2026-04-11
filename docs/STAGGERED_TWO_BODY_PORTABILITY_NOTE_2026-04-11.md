# Staggered Two-Body Portability / Direct-CoM Closure Probe

**Date:** 2026-04-11  
**Status:** bounded frontier negative on `claude/sleepy-cerf`  
**Script:** `scripts/frontier_staggered_two_body_portability.py`

## Question

Can the primary staggered self-consistent two-body lane be upgraded from a
force-led positive to a **direct-CoM portability closure** by using a more
local centroid readout?

The retained `main` result already showed:

- exact partner-force channel: clean and near-Newton on a calibrated open 3D
  surface
- blocked trajectory channel: noisy and not fully portable

This frontier probe held the physics fixed and changed only the readout.

## Design

Same underlying staggered two-body physics as the retained main harness:

- open 3D staggered lattice
- two orbitals `psi_A`, `psi_B`
- shared self-consistent field:
  - `Phi = Phi_A + Phi_B`
  - `(L + mu^2 I) Phi_A = G |psi_A|^2`
  - `(L + mu^2 I) Phi_B = G |psi_B|^2`
- self-only controls for each orbital
- parity-correct scalar coupling:
  - `H_diag = (m + Phi) * epsilon(x)`

Three observables were compared on the same rows:

1. **Exact partner-force channel**
   - A feels `Phi_B` only
   - B feels `Phi_A` only

2. **Retained global blocked-half centroid**
   - the existing `main` trajectory companion

3. **New local pair-block direct-CoM channel**
   - collapse density onto the `x` profile
   - pair even/odd sites into 2-site blocks
   - compute a packet-local centroid in a fixed block window around the initial
     packet center

The local window radius was checked at:

- `LOCAL_RADIUS_BLOCKS = 1`
- `LOCAL_RADIUS_BLOCKS = 2`
- `LOCAL_RADIUS_BLOCKS = 3`

## Audited surface

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

## Exact result

For the default local window (`LOCAL_RADIUS_BLOCKS = 2`):

- partner-force attractive: `45/45`
- global blocked-half inward: `8/45`
- local pair-block inward: `5/45`
- both global and local inward: `5/45`

The local readout is therefore **worse**, not better, than the retained global
blocked companion on this portability surface.

No meaningful local direct-CoM distance-law fit survives, because too few rows
remain inward and the surviving signs are not portable enough to define a
stable law.

Placement breakdown:

- `centered`: global `3/15`, local `2/15`
- `face_offset`: global `3/15`, local `2/15`
- `corner_offset`: global `2/15`, local `1/15`

## Radius sensitivity

The result is not a window-size tuning issue.

For `LOCAL_RADIUS_BLOCKS = 1, 2, 3`, the summary was identical:

- partner-force attractive: `45/45`
- global blocked-half inward: `8/45`
- local pair-block inward: `5/45`
- both inward: `5/45`

So the direct-CoM failure survives a small local-window sensitivity sweep.

## Representative failure rows

The failure mode is concrete:

- `centered, side=14, d=3`
  - force: `+4.9002e-01`
  - local deltas: `(-1.317e-03, +9.430e-04)`
  - A moves the wrong way in the local direct-CoM readout

- `centered, side=16, d=5`
  - force: `+1.7653e-01`
  - local deltas: `(-5.072e-04, -1.574e-04)`
  - both local packet shifts fail the inward sign

- `corner_offset, side=14, d=5`
  - force: `+2.5561e-01`
  - local deltas: `(-7.739e-04, +1.074e-03)`
  - one packet still moves outward despite a clean attractive partner force

These are not near-zero force rows. The force channel remains strong while the
direct-CoM channel changes sign.

## Interpretation

This probe does **not** strengthen direct-CoM closure on the primary staggered
architecture.

What it shows instead:

- the exact staggered self-consistent partner-force channel is robust on this
  bounded surface
- the direct-CoM trajectory problem is not fixed by a simple local packet
  window
- the retained `main` story was already the right one:
  - staggered self-consistent two-body is real
  - but it remains **force-led**, not direct-CoM closed

## What this falsifies

This falsifies a specific next-step hope:

> a local pair-blocked centroid is enough to turn the staggered self-consistent
> two-body lane into a portable trajectory closure

On this audited surface, that answer is no.

## Next step

If the goal is still a trajectory-level staggered closure, the next observable
should not be another centroid variant.

The likely next candidates are:

1. a packet-window momentum / impulse observable
2. a detector-side flux observable
3. a readout tied to conserved current rather than position moments

## Bottom line

The bounded frontier conclusion is:

> On the primary staggered architecture, the self-consistent two-body channel
> remains robust in an exact partner-force observable, but direct-CoM
> portability/closure fails even after local pair-block coarse-graining and
> window-radius sensitivity checks.
