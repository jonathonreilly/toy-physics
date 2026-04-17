# Wave Direct-dM H=0.25 Fam2 Seed0 Control Note

**Date:** 2026-04-08
**Status:** retained control-ladder hardening on the Fam2/seed0 fine-H boundary replay

This note upgrades the earlier one-strength `Fam2`, seed `0`,
`H = 0.25` boundary replay by adding the same-resolution control stack:

> Keep the previously retained `Fam2`, seed `0`, `H = 0.25` point fixed,
> then add the exact `S = 0` null and the weak-field ladder
> `S = 0.002, 0.004, 0.008` to test whether the fine-`H` boundary replay
> is still well-posed once the coarse-lane controls are applied at the same
> resolution.

## Result

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.002705` | `+0.003476` | `-0.000770` | `-22.16%` | `-0.385126` |
| `0.004` | `+0.005393` | `+0.006969` | `-0.001576` | `-22.61%` | `-0.393942` |
| `0.008` | `+0.010714` | `+0.014007` | `-0.003293` | `-23.51%` | `-0.411609` |

Summary:

- exact null: `max |delta_hist| = 0.000e+00`
- nonzero sign pattern: `- - -`
- `|delta_hist / s|` spread: `6.67%`

## Honest read

This is a real hardening of the fine-`H` branch for this specific pair.

What now survives on `Fam2`, seed `0`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- low linearity spread on `|delta_hist / s|`
- stable normalized magnitude around `-22%` to `-24%`

So the earlier one-strength boundary replay is no longer just a narrow point.
For this specific family/seed pair, it is now a properly controlled fine-`H`
point.

## What this changes

- The second-family `H = 0.25` pair is now fully controlled:
  both `Fam2`, seed `0` and `Fam2`, seed `1` have exact null, common negative
  sign, and low within-ladder linearity spread.
- The old `Fam2`, seed-`0` row remains in the lower-magnitude branch even after
  the full ladder is applied.
  This did not drift back toward the old coarse high band; it stayed near
  `R_hist = -23%`.
- That strengthens the current seed-split read on the second family:
  seed `1` is still the stronger branch (`-35%`), seed `0` remains the weaker
  branch (`-23%`), and both are now controlled at the same resolution.

## Boundary

This does **not** yet close the whole fine-`H` family-pair critique.

What remains open:

- the `Fam1` pair still does not have the same full control ladder at
  `H = 0.25`
- the current claim is still bounded to `Fam1` and `Fam2`, not `Fam3`
- the result still supports a bounded fine-`H` family-pair surface, not a full
  `H = 0.25` portability law

So the exact retained claim is:

> `Fam2`, seed `0`, `H = 0.25` is now a controlled fine-`H` replay with exact
> null, stable sign, and approximately linear weak-field scaling at
> `R_hist ~ -23%`. Together with the existing `Fam2`, seed `1` control ladder,
> that closes the second-family fine-`H` pair without promoting a full
> portability law.

## Artifact chain

- [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
