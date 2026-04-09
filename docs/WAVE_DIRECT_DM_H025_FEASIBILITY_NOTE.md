# Wave Direct-dM H=0.25 Feasibility Note

**Date:** 2026-04-08
**Status:** minimal single-family feasibility probe, now reclassified as the Fam1/seed0 high-band boundary point

This note records the smallest practical question on the direct-dM lane:

> Can the existing matched-history direct-dM harness run at `H = 0.25`
> on this workstation for one family and one strength without destabilizing
> the claim surface?

The probe is intentionally narrow:

- one family / one geometry setup
- one strength, defaulting to `S_PHYS`
- one `H` point: `0.25`

If this probe completes in a reasonable wall time and memory footprint,
the main lane can add `H = 0.25` as one more retained point.
If not, the current matched-history lane should stay at `H = 0.5` and
`H = 0.35` and the flagship claim surface should not be widened yet.

## Result

The smallest `H = 0.25` run completed on this workstation for one
family and one strength, but it was not cheap.
The exact same `Fam1`, seed `0`, `S = 0.004`, `H = 0.25` point now has two
runtime references in the artifact chain:

- original feasibility probe:
  - `family = Fam1`
  - `strength = 0.004`
  - `H = 0.25`
  - `elapsed = 147.05 s`
  - `peak RSS = 710192 KB` `~ 693 MB`
- current reusable point-runner replay of that same point:
  - `elapsed = 110.41 s`
  - `peak RSS = 699.7 MB`
- `delta_hist = -0.001256`
- `R_hist = -20.12%`

That makes `H = 0.25` **feasible in principle** for a single-family
matched-history check, but too slow to treat as a routine addition to the
main lane without a stronger reason or a more optimized runner.

The safest current interpretation is now:

- the run is still the proof-of-feasibility point for the `H = 0.25` harness
- but it is no longer a neutral staging result:
  this exact replay is now the diagnosed `Fam1`, seed `0` high-band boundary
- the sign survives, yet the normalized magnitude lands at `-20.12%`, so the
  old high-magnitude band does not carry straight through to `H = 0.25`
- the complementary seed-`1` replay has now also landed and stays at
  `R_hist = -29.47%`; the fine-`H` two-point interpretation is now frozen in
  the synthesis note linked below
- the main lane should still be considered anchored by `H = 0.5` and
  `H = 0.35` until one post-synthesis reserve point is chosen and widened only
  if it stays coherent

The boundary interpretation is recorded in
[`WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md).
The frozen two-point interpretation is now recorded in
[`WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md).

## Artifact chain

- [`scripts/wave_direct_dm_h025_feasibility_probe.py`](../scripts/wave_direct_dm_h025_feasibility_probe.py)
- [`scripts/wave_direct_dm_h025_point_runner.py`](../scripts/wave_direct_dm_h025_point_runner.py)
- [`docs/WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md`](./WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
