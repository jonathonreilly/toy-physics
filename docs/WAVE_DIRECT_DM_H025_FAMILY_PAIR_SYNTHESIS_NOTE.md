# Wave Direct-dM H=0.25 Family-Pair Synthesis Note

**Date:** 2026-04-08
**Status:** retained narrow synthesis on the current `Fam1`/`Fam2` fine-`H` evidence

This note compresses the two existing fine-`H` threads into one answer to the
current question:

> Is the two-band split better indexed by seed, by family, or by the realized
> move trace?

The answer, on the retained evidence, is:

> seed is the best coarse label, family is secondary, and the actual separator
> is the realized late-branch amplification trace.

## Evidence surface

The synthesis uses four retained artifacts:

- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)

The relevant rows are:

| family | seed | `H` | `dM(early)` | `dM(late)` | `late gain` | `R_hist` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Fam1` | `0` | `0.25` | `+0.004989` | `+0.006246` | `+0.001257` | `-20.12%` |
| `Fam1` | `1` | `0.25` | `+0.004411` | `+0.006255` | `+0.001844` | `-29.47%` |
| `Fam2` | `0` | `0.25` | `+0.005393` | `+0.006969` | `+0.001576` | `-22.61%` |
| `Fam2` | `1` | `0.25` | `+0.003777` | `+0.005814` | `+0.002037` | `-35.03%` |

## What the split is not

- not a sign split
- not an early-branch collapse
- not a family-local quirk
- not a stable `R_hist` ordering under refinement

The sign stays negative in every retained fine-`H` row above.
The early branch stays present in every row.
The family effect is present, but it is smaller than the seed effect.

## What actually separates the bands

The most stable discriminator is the realized move trace, specifically the
late-branch amplification relative to the early response.

At `H = 0.25`:

- `Fam1` seed `1` has larger late gain than seed `0`
- `Fam2` seed `1` has larger late gain than seed `0`
- the larger late gain corresponds to the more negative `R_hist`

That makes the late-branch trace the cleanest mechanistic index on the fine-`H`
pair, while seed remains the best coarse predictor of which side of the split a
row falls on.

## Seed vs family

Seed is the stronger of the two labels:

- on the coarse retained batch, seed separates the two bands more strongly than
  family does
- on the fine-`H` family pair, the same seed ordering is still visible inside
  each family, but the exact `R_hist` ordering is not refinement-stable unless
  you look at the late-branch trace

Family matters mainly as a scale shift:

- `Fam2` pushes the negative branch deeper than `Fam1` for the same seed
- but it does not replace the seed axis as the primary split

## Honest read

The safest retained statement is:

> the two-band story is primarily a seed-conditioned late-branch
> amplification effect, modulated by family, and best tracked by the realized
> `dL / dE` or late-gain compression rather than by family label alone.

That is stronger than “seed split” and weaker than a family law.

## Boundary

This note does **not** claim:

- a third-family law
- a third-seed law
- an `H = 0.25` portability law
- a refinement-stable amplitude package

The fine-`H` evidence is still bounded to `Fam1` and `Fam2`.
The second-family pair is now controlled at `H = 0.25`, but the `Fam1` pair is
still only one-strength replay evidence.

## Artifact chain

- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
