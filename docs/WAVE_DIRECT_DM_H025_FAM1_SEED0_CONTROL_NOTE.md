# Wave Direct-dM H=0.25 Fam1 Seed0 Control Note

**Date:** 2026-04-08
**Status:** retained control-ladder hardening on the Fam1/seed0 fine-H boundary replay

This note freezes the missing first-family fine-`H` control artifact using the
logging-safe wrapper:

> Keep the previously retained `Fam1`, seed `0`, `H = 0.25` boundary replay
> fixed, then add the exact `S = 0` null and the weak-field ladder
> `S = 0.002, 0.004, 0.008` to test whether the fine-`H` boundary replay is
> still well-posed once the same-resolution controls are applied through the
> wrapper-backed freeze path.

## Result

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.002504` | `+0.003116` | `-0.000612` | `-19.63%` | `-0.305878` |
| `0.004` | `+0.004989` | `+0.006246` | `-0.001256` | `-20.12%` | `-0.314085` |
| `0.008` | `+0.009899` | `+0.012543` | `-0.002644` | `-21.08%` | `-0.330504` |

Summary:

- exact null: `max |delta_hist| = 0.000e+00`
- nonzero sign pattern: `- - -`
- `|delta_hist / s|` spread: `7.77%`

## Honest read

This is a real hardening of the fine-`H` branch for this specific pair.

What now survives on `Fam1`, seed `0`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- low linearity spread on `|delta_hist / s|`
- stable normalized magnitude around `-19%` to `-21%`

So the earlier one-strength boundary replay is no longer just a narrow point.
For this specific family/seed pair, it is now a properly controlled fine-`H`
point.

## What this changes

- The first-family `H = 0.25` boundary replay is now controlled with the same
  ladder pattern used on the second family.
- The `Fam1` seed-`0` row stays in the lower-magnitude boundary regime, not the
  old coarse higher band.
- The wrapper-backed freeze path is cheaper than the earlier manual direct
  capture approach because it writes the retained log atomically and avoids the
  failed retry/pipeline path.
- The broader fine-`H` story is still bounded to `Fam1` and `Fam2`, but both
  families now have controlled `H = 0.25` pairs.

## Boundary

This does **not** claim:

- a third-family law
- a third-seed law
- an `H = 0.25` portability law
- a refinement-stable amplitude package

The exact retained claim is:

> `Fam1`, seed `0`, `H = 0.25` is now a controlled fine-`H` replay with exact
> null, stable sign, and approximately linear weak-field scaling at
> `R_hist ~ -20%`.

## Artifact chain

- [`scripts/wave_direct_dm_h025_control_freeze.py`](../scripts/wave_direct_dm_h025_control_freeze.py)
- [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
