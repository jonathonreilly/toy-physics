# Wave Direct-dM H=0.25 Low-Band Retention Note

**Date:** 2026-04-08
**Status:** retained narrow validation on the Fam1/seed1 low-band continuation

This note records the complementary direct `H = 0.25` replay for the
direct-`dM` amplitude-band story:

> Start from the retained lower-magnitude reference point
> (`Fam1`, seed `1`, `S = 0.004`) and ask whether the same configuration
> stays in the lower-magnitude band when the matched-history lane is
> refined from `H = 0.5` / `0.35` down to `H = 0.25`.

## Reference comparison

All three rows use the same family, seed, and source strength.

| H | dM(early) | dM(late) | delta_hist | R_hist | late gain |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.50 | +0.005594 | +0.007491 | -0.001897 | -25.33% | +0.001897 |
| 0.35 | +0.006509 | +0.008134 | -0.001625 | -19.98% | +0.001625 |
| 0.25 | +0.004411 | +0.006255 | -0.001843 | -29.47% | +0.001844 |

Runtime / memory for the `H = 0.25` replay:

- elapsed = `108.16 s`
- peak RSS = `697.8 MB`

## Narrow read

- The matched-history effect survives cleanly at `H = 0.25` on the seed-`1`
  continuation:
  `delta_hist` stays negative and materially nonzero.
- The lower-magnitude branch is also the more refinement-stable one on the
  current single-family read:
  the `H = 0.25` late gain `+0.001844` sits almost exactly on the retained
  `H = 0.5` / `0.35` seed-`1` values.
- The normalized magnitude does not collapse toward zero or drift up toward
  the old seed-`0` band.
  Instead it lands at `R_hist = -29.47%`, still inside the old lower band and
  slightly stronger than the `H = 0.5` seed-`1` reference.

So the honest conclusion is:

> The direct `H = 0.25` low-band replay is a **retained** continuation of the
> seed-`1` branch at the level of sign plus late-gain difference. The
> matched-history sign survives and the seed-`1` late-gain scale stays close
> to the coarse rows, but the absolute branch responses still drift downward
> at the finer refinement.

## What this changes

- The two planned `H = 0.25` validation points have now both landed.
- The old seed ordering from `H = 0.5` / `0.35` does **not** survive the
  first fine-`H` check:
  the former high-band seed-`0` point dropped to `R_hist = -20.12%`, while
  this seed-`1` point stays at `R_hist = -29.47%`.
- On the current two-point, single-family evidence, the refinement issue is
  no longer “does the low band survive?” but “how should the cross-seed
  ordering be described once seed `0` loses most of its extra late gain?”
- The narrow two-point synthesis is now frozen in
  [`WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md).
- That synthesis keeps the fine-`H` claim at the single-family
  cross-seed-reordering / uneven-late-gain-compression level, not a wider
  portability extension.
- Extra-family, third-seed, and weaker-strength reserve points remain demoted
  until one post-synthesis reserve point is chosen deliberately.

## Artifact chain

- [`scripts/wave_direct_dm_h025_point_runner.py`](../scripts/wave_direct_dm_h025_point_runner.py)
- [`logs/2026-04-08-wave-direct-dm-h025-low-band.txt`](../logs/2026-04-08-wave-direct-dm-h025-low-band.txt)
- [`docs/WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
