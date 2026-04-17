# Wave Direct-dM H=0.25 High-Band Boundary Note

**Date:** 2026-04-08
**Status:** diagnosed closure on the Fam1/seed0 high-band continuation

This note records the first direct `H = 0.25` replay for the direct-`dM`
amplitude-band story:

> Start from the retained higher-magnitude reference point
> (`Fam1`, seed `0`, `S = 0.004`) and ask whether the same configuration
> stays in the higher-magnitude band when the matched-history lane is
> refined from `H = 0.5` / `0.35` down to `H = 0.25`.

## Reference comparison

All three rows use the same family, seed, and source strength.

| H | dM(early) | dM(late) | delta_hist | R_hist | late gain |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.50 | +0.005385 | +0.009547 | -0.004161 | -43.59% | +0.004162 |
| 0.35 | +0.004811 | +0.008346 | -0.003535 | -42.36% | +0.003535 |
| 0.25 | +0.004989 | +0.006246 | -0.001256 | -20.12% | +0.001257 |

Runtime / memory for the `H = 0.25` replay:

- elapsed = `110.41 s`
- peak RSS = `699.7 MB`

## Narrow read

- The matched-history effect still exists at `H = 0.25`:
  `delta_hist` stays negative and materially nonzero.
- But the old **high-band** label does not survive this refinement step.
  The normalized magnitude drops from roughly `-42%` to `-44%` at
  `H = 0.5` / `0.35` down to `-20.12%` at `H = 0.25`.
- The drop is driven by weaker late-branch amplification, not by sign loss
  and not by an early-branch collapse:
  `dM(early)` stays near the earlier values, while the late gain shrinks
  from `+0.004162` / `+0.003535` to `+0.001257`.

So the honest conclusion is:

> The first direct `H = 0.25` replay is a **boundary**, not a portability
> positive for the old high-magnitude band. The effect survives in sign, but
> the Fam1/seed0 amplitude falls into the lower-magnitude regime at the finer
> refinement.

## What this changes

- The existing `H = 0.25` feasibility point should now be interpreted as the
  first high-band boundary replay, not as a neutral staging result.
- The complementary lower-band replay has now landed in
  [`WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md`](./WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md):
  `Fam1`, seed `1`, `S = 0.004`, `H = 0.25` stays at `R_hist = -29.47%`.
- That means the old seed ordering does **not** survive this first fine-`H`
  check.
  The current `H = 0.25` issue is no longer whether both seeds collapse into
  one band, but how to describe the cross-seed reordering after seed `0`
  loses most of its extra late gain.
- The narrow two-point synthesis is now frozen in
  [`WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md).
- That synthesis keeps the fine-`H` claim at the single-family cross-seed
  reordering / uneven late-gain-compression level rather than promoting a
  broader portability read.
- Wider family or seed expansion remains demoted until one post-synthesis
  reserve point is chosen deliberately.

## Artifact chain

- [`scripts/wave_direct_dm_h025_point_runner.py`](../scripts/wave_direct_dm_h025_point_runner.py)
- [`logs/2026-04-08-wave-direct-dm-h025-high-band.txt`](../logs/2026-04-08-wave-direct-dm-h025-high-band.txt)
- [`docs/WAVE_DIRECT_DM_H025_FEASIBILITY_NOTE.md`](./WAVE_DIRECT_DM_H025_FEASIBILITY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md`](./WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
