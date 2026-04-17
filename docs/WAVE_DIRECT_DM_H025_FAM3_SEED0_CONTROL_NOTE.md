# Wave Direct-dM H=0.25 Fam3 Seed0 Control Note

**Date:** 2026-04-12
**Status:** retained control-ladder hardening on the Fam3/seed0 fine-H control

This note freezes the complementary predeclared direct-`dM` widening point
after the retained `Fam3`, seed `1` control row:

> Keep the controlled `Fam3`, seed `0`, `H = 0.25` point fixed, then add the
> exact `S = 0` null and the weak-field ladder `S = 0.002, 0.004, 0.008` to
> check whether the weaker branch also survives as a properly controlled
> fine-`H` replay.

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

This is a real hardening of the complementary third-family fine-`H` row.

What now survives on `Fam3`, seed `0`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- low linearity spread on `|delta_hist / s|`
- stable normalized magnitude around `-20%`

So the earlier one-strength widening point is no longer just a narrow replay.
For this specific family/seed pair, it is now a properly controlled fine-`H`
point on the weaker branch.

## What This Changes

- The direct-`dM` note stack now includes the complementary controlled
  `Fam3`, seed `0`, `H = 0.25` row alongside the retained `Fam3`, seed `1`
  row.
- The retained claim of this note remains row-level only.

## Boundary

This note does **not** yet establish:

- a wider family conclusion
- a portability law
- a third-seed law
- a replacement for the retained transfer diagnostic
- a separate pair-level or three-family synthesis

So the exact retained claim of this note is:

> `Fam3`, seed `0`, `H = 0.25` is now a controlled fine-`H` replay with exact
> null, stable sign, and approximately linear weak-field scaling at
> `R_hist ~ -20%`. That is enough to count as the complementary controlled
> third-family row, but not enough by itself for a wider law.

## Artifact Chain

- [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- [`scripts/wave_direct_dm_h025_control_freeze.py`](../scripts/wave_direct_dm_h025_control_freeze.py)
- [`logs/2026-04-12-wave-direct-dm-h025-control-fam3-seed0.txt`](../logs/2026-04-12-wave-direct-dm-h025-control-fam3-seed0.txt)
- [`docs/WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`](./WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md)
