# Wave Direct-dM H=0.25 Seed0 Cross-Family Compression Note

**Date:** 2026-04-08  
**Status:** bounded-support same-seed cross-family compression on the controlled seed-`0` fine-`H` surface
**Type:** bounded_theorem
**Runner:** `scripts/wave_direct_dm_h025_seed0_crossfamily_assertions.py`

This note compresses the controlled `H = 0.25` seed-`0` evidence across the
two families that currently have it:

> Keep the controlled `Fam1`, seed `0`, `H = 0.25` control ladder together
> with the controlled `Fam2`, seed `0`, `H = 0.25` control ladder, and ask
> what survives if we hold the seed fixed but compare the same fine-`H`
> row across families.

## Evidence surface

The seed-`0` source rows are:

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

The runner is log-backed: it reads the frozen control logs listed in the
artifact chain and asserts the two-row compression table, the exact nulls,
the nonzero negative sign pattern, the weak-field spread bounds, and the
selected-row ordering.  It deliberately does not rerun the expensive fine-`H`
controls and does not certify any family-wide law.

## What the seed-0 surface does not say

- not a stable amplitude law
- not a family-independent `H = 0.25` portability result
- not a third-family extrapolation
The common sign stays negative, but the normalized magnitudes remain
family-dependent.
`Fam1` is the shallower weak branch; `Fam2` is the deeper weak branch.

## What actually survives

The cleanest bounded statement is:

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

## Assertion closeout

Primary runner:

- `scripts/wave_direct_dm_h025_seed0_crossfamily_assertions.py`

Transcript:

- `outputs/wave_direct_dm_h025_seed0_crossfamily_assertions_2026-05-06.txt`

The runner prints:

- `WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_ASSERTIONS=TRUE`
- `WAVE_DIRECT_DM_H025_SEED0_SHARED_SIGN=negative`
- `WAVE_DIRECT_DM_H025_SEED0_COMMON_ORDERING=Fam2_deeper_than_Fam1_at_strength_0.004`
- `WAVE_DIRECT_DM_H025_SEED0_WEAK_FIELD_CONTROL=TRUE`
- `WAVE_DIRECT_DM_H025_SEED0_PORTABILITY_LAW=FALSE`
- `WAVE_DIRECT_DM_H025_STABLE_AMPLITUDE_LAW=FALSE`
- `RESIDUAL_SCOPE=fam3_and_family_wide_portability_not_claimed`

## Artifact chain

- Source log: `logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`
- Source log: `logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`
- Primary assertion runner: `scripts/wave_direct_dm_h025_seed0_crossfamily_assertions.py`
- Assertion transcript: `outputs/wave_direct_dm_h025_seed0_crossfamily_assertions_2026-05-06.txt`
- Context note: `docs/WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`
- Context note: `docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`
- Context note: `docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`
- Context note: `docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`
- Context note: `docs/WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`
- Context note: `docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`
