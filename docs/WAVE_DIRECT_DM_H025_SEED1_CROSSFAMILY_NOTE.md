# Wave Direct-dM H=0.25 Seed1 Cross-Family Compression Note

**Date:** 2026-04-08
**Status:** retained same-seed cross-family compression on the controlled seed-`1` fine-`H` surface

This note compresses the retained `H = 0.25` seed-`1` evidence across the
two retained families:

> Keep the retained `Fam1`, seed `1`, `H = 0.25` control ladder together
> with the retained `Fam2`, seed `1`, `H = 0.25` control ladder, and ask
> what survives if we hold the seed fixed but compare the same fine-`H`
> row across families.

## Evidence surface

The seed-`1` retained rows are:

| family | `H` | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | late gain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Fam1` | `0.25` | `+0.004411` | `+0.006255` | `-0.001843` | `-29.47%` | `+0.001844` |
| `Fam2` | `0.25` | `+0.003777` | `+0.005814` | `-0.002037` | `-35.03%` | `+0.002037` |

Both rows are now controlled at the same resolution:

- exact `S = 0` null
- sign pattern `- - -`
- bounded `|delta_hist / s|` spread

Per-family summaries:

| family | null max `|delta_hist|` | sign pattern | `|delta_hist / s|` spread |
| --- | ---: | --- | ---: |
| `Fam1` | `0.000e+00` | `- - -` | `5.22%` |
| `Fam2` | `0.000e+00` | `- - -` | `4.25%` |

## What the seed-1 surface does not say

- not a stable amplitude law
- not a family-independent `H = 0.25` portability result
- not a third-family extrapolation

The common sign stays negative, but the normalized magnitudes remain
family-dependent.
`Fam1` is the shallower strong branch; `Fam2` is the deeper strong branch.

## What actually survives

The cleanest retained statement is:

> seed `1` occupies the higher-magnitude side of the fine-`H` direct-`dM`
> story in both retained families, and the two families sit at different
> depths inside that stronger branch: `Fam1` is controlled near
> `R_hist ~ -30%`, while `Fam2` is controlled near `R_hist ~ -35%`.

That is a same-seed cross-family compression result, not a portability law.

## Boundary

This note does **not** claim:

- that the seed-`1` rows define a stable amplitude band
- that the direct-`dM` lane has a family-wide fine-`H` law
- that the fine-`H` evidence extends to `Fam3`

The honest boundary is:

> the seed-`1` fine-`H` surface is consistent across families in sign,
> ordering, and weak-field control, but it still does not define a stable
> amplitude law or a portability claim beyond `Fam1`/`Fam2`.

## Artifact chain

- [`docs/WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md)
