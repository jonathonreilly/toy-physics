# Wave Direct-dM H=0.25 Fam3 Seed1 Control Note

**Date:** 2026-04-09
**Status:** proposed_retained control-ladder hardening on the Fam3/seed1 fine-H control

This note freezes the next predeclared direct-`dM` widening point after the
two-family transfer diagnostic:

> Keep the controlled `Fam3`, seed `1`, `H = 0.25` point fixed, then add the
> exact `S = 0` null and the weak-field ladder `S = 0.002, 0.004, 0.008` to
> check whether the first third-family row survives as a properly controlled
> fine-`H` replay.

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

This is a real hardening of one third-family fine-`H` row.

What now survives on `Fam3`, seed `1`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- low linearity spread on `|delta_hist / s|`
- stable normalized magnitude around `-27%`

So the earlier one-strength widening point is no longer just a narrow replay.
For this specific family/seed pair, it is now a properly controlled fine-`H`
point.

## What This Changes

- The direct-`dM` note stack now includes one controlled `Fam3`, seed `1`,
  `H = 0.25` row with exact null and a full weak-field ladder.
- The retained claim remains one-row only.

## Boundary

This note does **not** yet establish:

- a wider family conclusion
- a replacement for the retained transfer diagnostic

So the exact retained claim of this note is:

> `Fam3`, seed `1`, `H = 0.25` is now a controlled fine-`H` replay with exact
> null, stable sign, and approximately linear weak-field scaling at
> `R_hist ~ -27%`. That is enough to count as the first honest third-family
> control row, but not enough for a family law.

## Artifact Chain

- [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- [`scripts/wave_direct_dm_h025_control_freeze.py`](../scripts/wave_direct_dm_h025_control_freeze.py)
- [`logs/2026-04-09-wave-direct-dm-h025-control-fam3-seed1.txt`](../logs/2026-04-09-wave-direct-dm-h025-control-fam3-seed1.txt)
- [`docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`](./WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md)
