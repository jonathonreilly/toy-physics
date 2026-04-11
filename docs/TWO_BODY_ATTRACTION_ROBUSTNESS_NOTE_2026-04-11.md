# Two-Body Attraction Robustness Note

**Date:** 2026-04-11  
**Status:** bounded positive on the open-Wilson side lane; not a repo-wide Newton closure  
**Script:** `frontier_two_body_attraction_robustness.py`

## Question

Does the low-screening open-Wilson two-body attraction result survive a real
robustness surface beyond one fixed placement on one fixed lattice?

This follow-up keeps the same audited mutual-channel observable:

- `shared` evolution under one field sourced by both packets
- `self_only` evolution under each packet's own field
- retained signal:
  `a_mutual = a_sep(shared) - a_sep(self_only)`

But it broadens the surface in two concrete ways:

- **side**: `18, 20, 22`
- **placement family**:
  - `centered`
  - `face_offset`
  - `corner_offset`

The placement families remain on the same open cubic Wilson geometry. They are
not graph-family changes. They test whether the result is robust to moving the
same x-axis pair away from the exact center line and closer to open boundaries.

## Audited Surface

Common convention throughout:

- open 3D Wilson lattice
- `MASS = 0.3`
- `WILSON_R = 1.0`
- `DT = 0.08`
- `N_STEPS = 15`
- `sigma = 1.0`
- `G = 5`
- `mu^2 = 0.001`
- `REG = 1e-3`
- separations `d = 4, 6, 8, 10, 12`

Total rows:

- `3` sides
- `3` placement families
- `5` separations
- `45` deterministic configurations

This is a real side/placement robustness sweep. It is **not** a cross-graph or
cross-architecture robustness claim.

## Main Result

The signal stays strong on the full audited surface.

Counts:

- attractive: `45/45`
- clean (`SNR > 2`): `45/45`
- both packets move inward relative to `self_only`: `45/45`

So the fixed-surface Wilson result does **not** collapse when side and
placement family are varied within the same low-screening open-Wilson setup.

## Representative Rows

- `side=18, centered, d=4`
  - `a_mut = -0.497777 +/- 0.079205`
  - `SNR = 6.28`
  - `dsep_shared = -0.3428`
  - `dsep_self = +0.0272`
- `side=20, centered, d=8`
  - `a_mut = -0.126948 +/- 0.023067`
  - `SNR = 5.50`
  - `dsep_shared = -0.0497`
  - `dsep_self = +0.0453`
- `side=22, corner_offset, d=12`
  - `a_mut = -0.059236 +/- 0.010855`
  - `SNR = 5.46`
  - `dsep_shared = +0.0245`
  - `dsep_self = +0.0690`

The qualitative pattern is stable everywhere:

- `shared` always closes more strongly than `self_only`
- `self_only` is typically weakly outward on this surface
- `free` stays essentially flat

## Robustness Table

By side:

- `side=18`: attract `15/15`, clean `15/15`, inward `15/15`
- `side=20`: attract `15/15`, clean `15/15`, inward `15/15`
- `side=22`: attract `15/15`, clean `15/15`, inward `15/15`

By placement family:

- `centered`: attract `15/15`, clean `15/15`, inward `15/15`
- `face_offset`: attract `15/15`, clean `15/15`, inward `15/15`
- `corner_offset`: attract `15/15`, clean `15/15`, inward `15/15`

## Distance-Law Fit

Across all `45` strong rows:

- `|a_mut| ~ d^-1.952`
- `R^2 = 0.9986`

Placement-family fits:

- `centered`: `-1.977`, `R^2 = 0.9994`
- `face_offset`: `-1.952`, `R^2 = 0.9992`
- `corner_offset`: `-1.927`, `R^2 = 0.9989`

So the bounded open-Wilson robustness surface remains very close to
inverse-square scaling.

## Honest Read

This is materially stronger than the earlier fixed-surface statement.

What now survives:

- the low-screening open-Wilson two-body attraction is robust across:
  - three sides
  - three placement families
  - five separations
- the mutual-channel readout remains attractive and clean on every audited row
- the distance law remains near inverse-square on the whole bounded surface

What this still does **not** establish:

- cross-graph robustness
- cross-architecture robustness
- full both-masses Newton closure
- action-reaction closure
- a retained claim that the whole repo has solved emergent Newtonian gravity

So the correct bounded statement is:

> On the low-screening open-Wilson side lane, the shared-vs-self-only
> mutual-channel attraction survives a real side-and-placement robustness
> surface (`45/45` attractive, `45/45` clean) and retains a near-inverse-square
> falloff (`|a_mut| ~ d^-1.952`, `R^2=0.9986`).

That is strong enough to matter, but it is still a bounded Wilson result, not a
global retained Newton closure for the project.
