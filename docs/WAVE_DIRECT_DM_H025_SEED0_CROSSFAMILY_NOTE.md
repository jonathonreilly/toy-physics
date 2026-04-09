# Wave Direct-dM H=0.25 Seed0 Cross-Family Compression Note

**Date:** 2026-04-08  
**Status:** retained same-seed cross-family compression on the controlled seed-`0` fine-`H` surface

This note compresses the retained `H = 0.25` seed-`0` evidence across the
two families that currently have it:

> Keep the retained `Fam1`, seed `0`, `H = 0.25` control ladder together
> with the retained `Fam2`, seed `0`, `H = 0.25` control ladder, and ask
> what survives if we hold the seed fixed but compare the same fine-`H`
> row across families.

## Evidence surface

The seed-`0` retained rows are:

| family | `H` | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | late gain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Fam1` | `0.25` | `+0.004989` | `+0.006246` | `-0.001256` | `-20.12%` | `+0.001257` |
| `Fam2` | `0.25` | `+0.005393` | `+0.006969` | `-0.001576` | `-22.61%` | `+0.001576` |

Both rows are now controlled at the same resolution:

- exact `S = 0` null
- sign pattern `- - -`
- bounded `|delta_hist / s|` spread

Per-family summaries:

| family | null max `|delta_hist|` | sign pattern | `|delta_hist / s|` spread |
| --- | ---: | --- | ---: |
| `Fam1` | `0.000e+00` | `- - -` | `7.77%` |
| `Fam2` | `0.000e+00` | `- - -` | `6.67%` |

## What the seed-0 surface does not say

- not a stable amplitude law
- not a family-independent `H = 0.25` portability result
- not a third-family extrapolation
The common sign stays negative, but the normalized magnitudes remain
family-dependent.
`Fam1` is the shallower weak branch; `Fam2` is the deeper weak branch.

## What actually survives

The cleanest retained statement is:

> seed `0` occupies the lower-magnitude side of the fine-`H` direct-`dM`
> story in both families, and the two families sit at different depths
> inside that weak branch: `Fam1` is controlled near `R_hist ~ -20%`,
> while `Fam2` is controlled near `R_hist ~ -23%`.

That is a same-seed cross-family compression result, not a portability law.

## Boundary

This note does **not** claim:

- that the seed-`0` rows define a stable amplitude band
- that the direct-`dM` lane has a family-wide fine-`H` law
- that the fine-`H` evidence extends to `Fam3`

The honest boundary is:

> the seed-`0` fine-`H` surface is consistent across families in sign,
> ordering, and weak-field control, but it still does not define a stable
> amplitude law or a portability claim beyond `Fam1`/`Fam2`.

## Artifact chain

- [`docs/WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md)
