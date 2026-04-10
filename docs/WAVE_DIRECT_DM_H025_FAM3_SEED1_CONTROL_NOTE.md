# Wave Direct-dM H=0.25 Fam3 Seed1 Control Note

**Date:** 2026-04-09
**Status:** retained control-ladder hardening on the Fam3/seed1 fine-H control

This note freezes the third-family direct-`dM` widening point that was still
missing as a repo-facing artifact:

> Keep the controlled `Fam3`, seed `1`, `H = 0.25` point fixed, then add the
> exact `S = 0` null and the weak-field ladder `S = 0.002, 0.004, 0.008` to
> check whether the retained weak branch stays well-posed at the same
> resolution.

## Result

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.002397` | `+0.003269` | `-0.000872` | `-26.68%` | `-0.436079` |
| `0.004` | `+0.004772` | `+0.006552` | `-0.001780` | `-27.16%` | `-0.444901` |
| `0.008` | `+0.009457` | `+0.013158` | `-0.003701` | `-28.13%` | `-0.462626` |

Summary:

- exact null: `max |delta_hist| = 0.000e+00`
- nonzero sign pattern: `- - -`
- `|delta_hist / s|` spread: `5.93%`

## Honest Read

This is a real hardening of the fine-`H` branch for this specific pair.

What now survives on `Fam3`, seed `1`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- low linearity spread on `|delta_hist / s|`
- stable normalized magnitude around `-27%`

So the earlier one-strength widening point is no longer just a narrow replay.
For this specific family/seed pair, it is now a properly controlled fine-`H`
point.

## What This Changes

- The third-family `H = 0.25` row now sits in the same controlled ladder style
  as the existing `Fam1`/`Fam2` control points.
- `Fam3`, seed `1` stays in the weaker branch, but it does not collapse to the
  exact zero/null regime.
- The family-specific read remains narrow: this confirms one controlled row,
  not a third-family portability law.

## Boundary

This does **not** yet establish a wider family law.

What remains open:

- `Fam3`, seed `0` should stay gated behind this result
- the current claim is still bounded to one third-family control row
- any synthesis beyond this point should compare against the already retained
  `Fam1`/`Fam2` transfer map rather than reopen one-strength seed-band work

So the exact retained claim is:

> `Fam3`, seed `1`, `H = 0.25` is now a controlled fine-`H` replay with exact
> null, stable sign, and approximately linear weak-field scaling at
> `R_hist ~ -27%`. That is the honest third-family widening point, not a
> portability law.

## Artifact Chain

- [`logs/2026-04-09-direct-dm-fam3-seed1-h025-control.txt`](../logs/2026-04-09-direct-dm-fam3-seed1-h025-control.txt)
- [`docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`](./WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
