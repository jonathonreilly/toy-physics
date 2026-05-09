# DM Neutrino Source-Surface Split-2 Upper-Face Local Neighborhoods Candidate

**Date:** 2026-04-18  
**Status:** bounded - bounded or caveated result note
**Primary runner:** `scripts/frontier_dm_neutrino_source_surface_split2_upper_face_local_neighborhoods_candidate.py`

## Inputs

This note depends on:

- [DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_BOUNDARY_BAND_TRANSITION_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_BOUNDARY_BAND_TRANSITION_CANDIDATE_NOTE_2026-04-18.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_PROFILE_TRANSITION_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_EDGE_PROFILE_TRANSITION_CANDIDATE_NOTE_2026-04-18.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_LOWER_REPAIR_UPPER_FACE_EXTREMALS_CANDIDATE_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_SPLIT2_LOWER_REPAIR_UPPER_FACE_EXTREMALS_CANDIDATE_NOTE_2026-04-18.md)

The carrier and bundle theorems supply the active slack chart, the preferred
quotient, and the repair threshold; the split-2 reduction chain (boundary
band, edge profile, upper-face extremals) supplies the prior compression to
the two extremals around which these local 3D neighborhoods are scanned.

## Question

After the split-2 broad lower-repair pressure is compressed to the two explicit
upper-face extremals, do tested local 3D neighborhoods around those extremals
already produce a transport-compatible lower-repair rival?

## Bottom line

No on the tested local boxes.

The carrier-side pressure is exhausted to the two explicit local upper-face
neighborhoods:

- the best-eta cap neighborhood around
  `(m,delta,s) = (-0.14, 1.188513342509166, 0.0195041737783)`,
- the closest-lane endpoint neighborhood around
  `(m,delta,s) = (-0.14, 1.188955544069478, 0)`.

On the tested cap box

- `m in [-0.145,-0.14]`,
- `delta in [1.1835,1.1935]`,
- `s in [0.0145,0.0245]`,

the local lower-repair eta maximum stays pinned at the exact cap point with

- `eta/eta_obs = 0.884523189582`,
- `Lambda_+ = Lambda_+(x_*)`,

and even there the closest lower-repair packet lane on the box still stays at
distance

- `0.242283527374`

from the preferred quotient.

On the tested endpoint box

- `m in [-0.145,-0.14]`,
- `delta in [1.1839,1.1890]`,
- `s in [0,0.005]`,

the local lower-repair closest-lane point stays pinned at the exact endpoint
with

- packet distance `0.233274467128`,
- `eta/eta_obs = 0.883631424817`,
- `Lambda_+ = Lambda_+(x_*)`,

while the best lower-repair transport value anywhere on that box still stays
below closure:

- `max eta/eta_obs = 0.883977578548`.

So the remaining carrier-side geometric issue is no longer a diffuse split-2
low-slack region and no longer even a vague upper-face ridge. On the present
branch it is exhausted to the two explicit local upper-face neighborhoods
above, and both tested neighborhoods are still transport-incompatible.

## Practical consequence

The next carrier-side theorem target is now minimal:

1. interval-certified exclusion or dominance on the exact carrier inside those
   two local neighborhoods, or
2. a no-go theorem that current exact methods cannot certify them.

Anything broader is below the current reduction surface.
