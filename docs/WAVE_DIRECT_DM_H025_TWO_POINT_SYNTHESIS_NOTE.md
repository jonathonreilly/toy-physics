# Wave Direct-dM H=0.25 Two-Point Synthesis Note

**Date:** 2026-04-08
**Status:** proposed_retained narrow synthesis on the controlled first fine-`H` `Fam1` pair

This note freezes the first honest fine-`H` claim surface for the
direct-`dM` matched-schedule lane:

> Start from the retained direct-`dM` portability batch plus the seed-band
> diagnosis, then compare exactly the two planned `H = 0.25` `Fam1`,
> `S = 0.004` replays (`seed = 0`, `1`) before widening into any broader
> family, seed, or strength batch.

## Fine-`H` pair

| seed | dM(early) | dM(late) | delta_hist | R_hist | late gain |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0` | `+0.004989` | `+0.006246` | `-0.001256` | `-20.12%` | `+0.001257` |
| `1` | `+0.004411` | `+0.006255` | `-0.001843` | `-29.47%` | `+0.001844` |

Control-ladder summaries:

| seed | null max `|delta_hist|` | sign pattern | `|delta_hist / s|` spread |
| ---: | ---: | --- | ---: |
| `0` | `0.000e+00` | `- - -` | `7.77%` |
| `1` | `0.000e+00` | `- - -` | `5.22%` |

## Coarse-to-fine comparison

| seed | coarse-`H` `R_hist` band (`0.5`, `0.35`) | `H = 0.25` `R_hist` | coarse-`H` late-gain band | `H = 0.25` late gain | read |
| ---: | ---: | ---: | ---: | ---: | --- |
| `0` | `-43.59%`, `-42.36%` | `-20.12%` | `+0.004162`, `+0.003535` | `+0.001257` | old high band closes |
| `1` | `-25.33%`, `-19.98%` | `-29.47%` | `+0.001897`, `+0.001625` | `+0.001844` | low band retains |

## Headline read

- Both seeds keep exact null, common negative sign, and bounded
  weak-field linearity at `H = 0.25`, so the first-family fine-`H` pair is
  now controlled rather than one-strength.
- The old coarse-`H` seed ordering is **not** refinement-stable:
  at `H = 0.25`, the seed-`1` row is now the stronger of the two.
- The flip is driven by uneven late-gain compression:
  seed `0` loses most of its extra late-branch gain, while seed `1` stays
  close to its old lower-band late-gain level.
- This is not an absolute-response continuation:
  both fine-`H` rows shift downward in raw `dM(early)` / `dM(late)` compared
  with the larger coarse-`H` values, so the stable feature is the sign plus
  the late-minus-early separation, not a frozen amplitude package.

So the narrow promotion rule is:

> On the current controlled `Fam1` fine-`H` pair, the
> direct-`dM` matched-history effect survives in sign on both seeds, but the
> old coarse-`H` seed ordering is not refinement-stable. Seed `1` retains the
> lower-magnitude branch at `R_hist = -29.47%`, while seed `0` collapses to a
> boundary at `R_hist = -20.12%` because its extra late-branch gain compresses
> sharply. This is a controlled single-family cross-seed reordering / uneven
> late-gain-compression result, not an `H = 0.25` portability extension.

## What this does not support

- not an `H = 0.25` portability batch
- not a family-wide fine-`H` seed law
- not a refinement-stable amplitude package
- not a weaker-strength or third-seed rule yet

## Next honest move

- Keep the existing direct-`dM` base fixed:
  matched-history note, bounded family scout, `H = 0.25` feasibility note,
  and bounded portability batch.
- The second-family pair is already controlled in
  `WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`.
- If the lane continues next, the honest move is now a narrow controlled
  `Fam1`/`Fam2` family-pair synthesis before any `Fam3`, third-seed, or
  weaker-strength reserve point.
- Keep comparator work demoted unless a materially different exact
  `c = infinity` construction appears.

## Artifact chain

- `docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FEASIBILITY_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`
- `docs/WAVE_DIRECT_DM_PORTABILITY_BATCH_NOTE.md`
- [`scripts/wave_direct_dm_h025_point_runner.py`](../scripts/wave_direct_dm_h025_point_runner.py)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-high-band.txt`](../logs/2026-04-08-wave-direct-dm-h025-high-band.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-low-band.txt`](../logs/2026-04-08-wave-direct-dm-h025-low-band.txt)
