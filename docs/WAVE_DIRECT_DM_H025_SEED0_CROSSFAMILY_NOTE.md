# Wave Direct-dM H=0.25 Seed0 Cross-Family Compression Note

**Date:** 2026-04-08  
**Status:** proposed_retained same-seed cross-family compression on the controlled seed-`0` fine-`H` surface  
**Primary runner:** [`scripts/wave_direct_dm_h025_seed0_crossfamily_audit.py`](../scripts/wave_direct_dm_h025_seed0_crossfamily_audit.py)  
**Runner cache:** [`logs/runner-cache/wave_direct_dm_h025_seed0_crossfamily_audit.txt`](../logs/runner-cache/wave_direct_dm_h025_seed0_crossfamily_audit.txt)

This note compresses the registered `H = 0.25` seed-`0` direct-`dM`
runner surface across the two families that currently have matching control
logs:

> Keep the `Fam1`, seed `0`, `H = 0.25` control ladder together with the
> `Fam2`, seed `0`, `H = 0.25` control ladder, and ask
> what survives if we hold the seed fixed but compare the same fine-`H`
> row across families.

## Evidence surface

The seed-`0` source rows computed by the primary runner at `S = 0.004` are:

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

## Derivation closure

The load-bearing artifact is the primary runner above.  It fixes
`seed = 0`, `H = 0.25`, strengths `S = 0, 0.002, 0.004, 0.008`, and
families `Fam1`/`Fam2` from the matched-history harness.  For each
family/strength pair it calls `measure_dm`, which builds the grown lattice,
computes the free beam, solves the early/late retarded wave histories, and
propagates the beam through those histories before reporting `dM(early)`,
`dM(late)`, `delta_hist`, and `R_hist`.

The note uses only the checks printed by that runner:

- both families have exact `S = 0` nulls
- every nonzero weak-field row has negative `delta_hist`
- each family has bounded within-ladder `|delta_hist / s|` spread below `8%`
- at `S = 0.004`, `Fam1` is the shallower row and `Fam2` is the deeper row
  by both `|R_hist|` and `|delta_hist|`

The runner also checks that the `S = 0.004` `|R_hist|` gap stays above two
percentage points, so the two rows do not collapse to a common amplitude
inside this finite surface.

## What the seed-0 surface does not say

- not a stable amplitude law
- not a family-independent `H = 0.25` portability result
- not a third-family extrapolation

The common sign stays negative, but the normalized magnitudes remain
family-dependent.
`Fam1` is the shallower weak row; `Fam2` is the deeper weak row.

## What actually survives

The cleanest retained-grade statement proposed for audit is:

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

- load-bearing runner: [`scripts/wave_direct_dm_h025_seed0_crossfamily_audit.py`](../scripts/wave_direct_dm_h025_seed0_crossfamily_audit.py)
- runner cache: [`logs/runner-cache/wave_direct_dm_h025_seed0_crossfamily_audit.txt`](../logs/runner-cache/wave_direct_dm_h025_seed0_crossfamily_audit.txt)
- source runner used by the per-family control logs:
  [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- frozen per-family logs:
  [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt),
  [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt)
- contextual control notes, not load-bearing graph dependencies for this
  cross-family compression:
  `docs/WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`,
  `docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`
