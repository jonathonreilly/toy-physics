# Wave Direct-dM H=0.25 Fam3 Seed0 Control Note

**Date:** 2026-04-09
**Status:** retained control-ladder hardening on the Fam3/seed0 fine-H control

This note freezes the complementary third-family direct-`dM` widening point:

> After the controlled `Fam3`, seed `1`, `H = 0.25` replay, add the exact
> `S = 0` null and the weak-field ladder `S = 0.002, 0.004, 0.008` on the
> matching `Fam3`, seed `0` row and ask whether the weaker branch also survives
> as a properly controlled fine-`H` point.

## Result

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.002552` | `+0.003183` | `-0.000631` | `-19.82%` | `-0.315420` |
| `0.004` | `+0.005082` | `+0.006377` | `-0.001295` | `-20.31%` | `-0.323729` |
| `0.008` | `+0.010075` | `+0.012798` | `-0.002723` | `-21.28%` | `-0.340377` |

Summary:

- exact null: `max |delta_hist| = 0.000e+00`
- nonzero sign pattern: `- - -`
- `|delta_hist / s|` spread: `7.64%`

## Honest Read

This is a real hardening of the fine-`H` branch for this specific pair.

What now survives on `Fam3`, seed `0`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- bounded weak-field linearity on `|delta_hist / s|`
- stable normalized magnitude around `-20%` to `-21%`

So the third-family weaker branch is no longer just a one-strength widening
point. For this specific family/seed pair, it is now a properly controlled
fine-`H` point.

## What This Changes

- The third-family `H = 0.25` pair now has both seed-local control ladders:
  seed `0` sits near `R_hist = -20%`, while seed `1` sits near `R_hist = -27%`.
- The same cross-seed ordering seen on the controlled `Fam1` and `Fam2` pairs
  survives on `Fam3`: seed `0` stays weaker, seed `1` stays stronger.
- That is enough for a narrow Fam3 pair synthesis against the existing
  `Fam1`/`Fam2` transfer map, without reopening one-strength seed-band work.

## Boundary

This does **not** yet establish a third-family portability law.

What remains bounded:

- the current claim is still restricted to the matched-schedule `H = 0.25`
  surface
- the stable feature is the controlled cross-seed asymmetry, not a
  refinement-stable amplitude package
- any broader statement should compare the now-controlled Fam3 pair against the
  retained `Fam1`/`Fam2` transfer diagnostic rather than widen to more seeds or
  families immediately

So the exact retained claim is:

> `Fam3`, seed `0`, `H = 0.25` is now a controlled fine-`H` replay with exact
> null, stable sign, and approximately linear weak-field scaling at
> `R_hist ~ -20%`. Together with the existing controlled `Fam3`, seed `1` row,
> that closes the third-family fine-`H` pair as a narrow cross-seed asymmetry
> result, not a portability law.

## Artifact Chain

- [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- [`scripts/wave_direct_dm_h025_control_freeze.py`](../scripts/wave_direct_dm_h025_control_freeze.py)
- [`logs/2026-04-09-wave-direct-dm-h025-control-fam3-seed0.txt`](../logs/2026-04-09-wave-direct-dm-h025-control-fam3-seed0.txt)
- [`docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`](./WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md)
