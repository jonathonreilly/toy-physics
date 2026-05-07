# Wave Direct-dM H=0.25 Fam2 Seed0 Boundary Note

**Date:** 2026-04-08
**Status:** diagnosed closure on the first extra-family `H = 0.25` reserve point

This note records the first family-widening replay after the frozen
`Fam1` two-point synthesis on the direct-`dM` matched-history lane:

> Hold the direct-`dM` setup fixed, keep the first extra-family reserve
> point as narrow as possible (`Fam2`, seed `0`, `S = 0.004`), and ask
> whether the old higher-magnitude band survives at `H = 0.25` on a
> second family before widening into `Fam3`, extra-seed, or
> weaker-strength work.

## Reference comparison

All three rows use the same family, seed, and source strength.

| H | dM(early) | dM(late) | delta_hist | R_hist | late gain |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.50 | +0.005565 | +0.009650 | -0.004085 | -42.33% | +0.004085 |
| 0.35 | +0.004743 | +0.007617 | -0.002874 | -37.73% | +0.002874 |
| 0.25 | +0.005393 | +0.006969 | -0.001576 | -22.61% | +0.001576 |

Runtime / memory for the `H = 0.25` replay:

- elapsed = `120.78 s`
- peak RSS = `691.0 MB`

## Narrow read

- The matched-history effect still survives on the first extra-family
  `H = 0.25` replay:
  `delta_hist` stays negative and materially nonzero.
- But the old **high-band** label does not survive this family-widening
  refinement step either.
  The normalized magnitude drops from `-42.33%` / `-37.73%` at
  `H = 0.5` / `0.35` down to `-22.61%` at `H = 0.25`.
- The change is again a late-gain compression story, not sign loss and
  not an early-branch collapse:
  `dM(early)` stays near the coarse rows, while late gain shrinks from
  `+0.004085` / `+0.002874` to `+0.001576`.

So the honest conclusion is:

> The first extra-family `H = 0.25` reserve point is another
> **boundary**, not an extra-family portability positive. On the tested
> `Fam2`, seed-`0` row, the direct-`dM` sign survives but the old
> higher-magnitude band still collapses into the lower-magnitude regime.

## What This Changes

- The `Fam1` seed-`0` boundary at `R_hist = -20.12%` is no longer an
  obviously family-local quirk: the first `Fam2` seed-`0` replay also
  closes the old higher band, here at `R_hist = -22.61%`.
- The same `Fam2`, seed `0`, `H = 0.25` replay now also has a
  same-resolution control ladder in
  [`WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md):
  exact `S = 0` null, sign pattern `- - -`, and `|delta_hist / s|` spread
  `6.67%` over `S = 0.002, 0.004, 0.008`.
- That is still **not** enough to promote a family-wide fine-`H` law.
  Even with controls, this row stays in the lower boundary regime.
- The narrow `Fam2` pair synthesis now also exists in
  `WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md` (DOWNSTREAM aggregator; backticked to avoid length-2 cycle).
- The next honest move is therefore a cross-family compression pass over the
  retained `Fam1` and `Fam2` fine-`H` pair syntheses, not a jump to `Fam3`,
  a third seed, or a weaker-strength batch.

## Artifact Chain

- [`scripts/wave_direct_dm_h025_point_runner.py`](../scripts/wave_direct_dm_h025_point_runner.py)
- [`logs/2026-04-08-wave-direct-dm-h025-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-fam2-seed0.txt)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- `docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md` (DOWNSTREAM aggregator; backticked to avoid length-2 cycle)
- `docs/WAVE_DIRECT_DM_PORTABILITY_BATCH_NOTE.md`
