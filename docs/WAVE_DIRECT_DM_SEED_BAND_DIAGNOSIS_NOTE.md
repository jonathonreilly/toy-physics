# Wave Direct-dM Seed-Band Diagnosis

**Date:** 2026-04-08
**Status:** proposed_retained narrow diagnostic on the bounded portability batch

This note explains the main unresolved nuance from the retained
direct-`dM` portability batch:

> Why do the two seeds split into a larger `R_hist` band
> (`~ -37% .. -45%`) and a smaller one (`~ -20% .. -30%`) even though the
> sign, exact null, and weak-field linearity all survive?

The diagnosis stays narrow on purpose. It does **not** widen the family or
`H = 0.25` surface. It only decomposes the already-retained
reference-strength rows from the batch.

## Setup

- source artifact: [`docs/WAVE_DIRECT_DM_PORTABILITY_BATCH_NOTE.md`](./WAVE_DIRECT_DM_PORTABILITY_BATCH_NOTE.md)
- retained controls inherited from that batch:
  - exact `S = 0` null on all `12` family/seed/`H` buckets
  - common negative sign on every nonzero run
  - low within-seed linearity spread over `s = 0.002, 0.004, 0.008`
- rows diagnosed here:
  - families: `Fam1`, `Fam2`, `Fam3`
  - seeds: `0`, `1`
  - `H = 0.5`, `0.35`
  - reference strength: `s = 0.004`

## Headline read

The split is **not** an early-branch failure and **not** a family-sign
effect.

It is a **late-branch amplification split**:

- both seeds keep the same negative `delta_hist` sign on all `6` checked
  family/`H` rows
- seed `1` does not lose the early response:
  - mean `dE = +0.006026`
  - seed `0` mean `dE = +0.005094`
- the large difference is in how much extra response the late schedule
  acquires:
  - seed `0` mean late gain `dL - dE = +0.003712`
  - seed `1` mean late gain `dL - dE = +0.001949`
- the same point shows up in the amplification ratio:
  - seed `0` mean `dL / dE = 1.727`
  - seed `1` mean `dL / dE = 1.328`

So the safer interpretation is:

> the two-band split comes from seed-dependent **late-branch amplification**
> on the matched-schedule replay, not from loss of the early branch and not
> from a family-dependent sign flip.

## Seed summary

| seed | mean `dE` | mean `dL` | mean `dL - dE` | `dL / dE` band | mean `R_hist` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0` | `+0.005094` | `+0.008806` | `+0.003712` | `1.606 .. 1.795` | `-42.02%` |
| `1` | `+0.006026` | `+0.007976` | `+0.001949` | `1.250 .. 1.414` | `-24.57%` |

## `H`-resolved summary

| seed | `H` | mean `dE` | mean `dL` | mean `dL - dE` | mean `dL / dE` | mean `R_hist` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `0` | `0.5` | `+0.005329` | `+0.009413` | `+0.004084` | `1.767` | `-43.40%` |
| `0` | `0.35` | `+0.004859` | `+0.008198` | `+0.003340` | `1.687` | `-40.63%` |
| `1` | `0.5` | `+0.005495` | `+0.007526` | `+0.002032` | `1.370` | `-26.97%` |
| `1` | `0.35` | `+0.006558` | `+0.008425` | `+0.001867` | `1.286` | `-22.18%` |

## Honest boundary

This note explains the **amplitude decomposition** of the two bands on the
current observables only.

It does **not** yet say:

- what deeper geometry feature causes the seed dependence
- whether the same split persists at `H = 0.25`
- whether later seed/family widening will preserve the same two-band picture

Those were the next questions.
The narrow two-point `H = 0.25` synthesis is now frozen in
[`WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md):
the old seed ordering is not refinement-stable on the current single-family
read, and the promoted fine-`H` claim stays at the cross-seed reordering /
uneven late-gain-compression level.

The next honest move after that is at most one reserve point, with a clear
order:

- first one extra-family replay
- only then consider one extra-seed or weaker-strength replay

## Artifact chain

- [`scripts/wave_direct_dm_seed_band_diagnosis.py`](../scripts/wave_direct_dm_seed_band_diagnosis.py)
- [`logs/2026-04-08-wave-direct-dm-seed-band-diagnosis.txt`](../logs/2026-04-08-wave-direct-dm-seed-band-diagnosis.txt)
- `docs/WAVE_DIRECT_DM_PORTABILITY_BATCH_NOTE.md`
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
