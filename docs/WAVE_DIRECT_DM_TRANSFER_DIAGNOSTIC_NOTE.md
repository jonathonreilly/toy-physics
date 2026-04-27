# Wave Direct-dM Transfer Diagnostic Note

**Date:** 2026-04-09
**Status:** proposed_retained narrow transfer diagnostic on the controlled `Fam1`/`Fam2` fine-`H` surface

This note freezes the retained runtime read that was still missing as a
repo-facing artifact:

> On the already-controlled `Fam1`/`Fam2`, `seed = 0/1`, `H = 0.25` surface,
> what single concrete diagnostic best explains the two-band direct-`dM` split
> without reopening wider family or seed searches?

The cleanest answer is a **coarse-to-fine late-gain transfer map**, not a new
geometry label and not a family law.

## Diagnostic

Use the direct matched-schedule late gain

`G = dM(late) - dM(early)`

and compare the fine row to the retained coarse pair:

`T(F, s) = G(H = 0.25) / mean(G(H = 0.5), G(H = 0.35))`

This stays narrow on purpose:

- same matched-schedule geometry as the retained direct-`dM` lane
- reference strength fixed at `s = 0.004`
- families limited to the two already-controlled fine-`H` families
- seeds limited to the two already-controlled fine-`H` seeds

## Transfer Table

| family | seed | `G(H=0.5)` | `G(H=0.35)` | mean coarse `G` | `G(H=0.25)` | `T(F,s)` | `R_hist(H=0.25)` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `Fam1` | `0` | `+0.004162` | `+0.003535` | `+0.003848` | `+0.001257` | `0.3266` | `-20.12%` |
| `Fam1` | `1` | `+0.001897` | `+0.001625` | `+0.001761` | `+0.001844` | `1.0471` | `-29.47%` |
| `Fam2` | `0` | `+0.004085` | `+0.002874` | `+0.003480` | `+0.001576` | `0.4529` | `-22.61%` |
| `Fam2` | `1` | `+0.001937` | `+0.002061` | `+0.001999` | `+0.002037` | `1.0190` | `-35.03%` |

## What Survives

The split is now materially sharper than the earlier seed-band wording alone:

- seed `0` rows **compress sharply** at fine `H`
  - `T = 0.3266`, `0.4529`
- seed `1` rows **retain coarse late-gain scale**
  - `T = 1.0471`, `1.0190`

So the narrow retained claim is:

> On the controlled `Fam1`/`Fam2`, `H = 0.25`, `s = 0.004` surface, the
> two-band direct-`dM` split is best tracked by coarse-to-fine late-gain
> retention/compression. Seed-`0` rows compress into the weaker branch, while
> seed-`1` rows retain their coarse late-gain scale.

That is stronger than “the seed bands differ” and weaker than an `H = 0.25`
portability law.

## Boundary

This note does **not** claim:

- a third-family law
- a third-seed law
- a full fine-`H` portability package
- that raw `R_hist` alone is the stable diagnostic

It only freezes one concrete split diagnostic on the existing controlled
surface.

The next honest widening control, if the direct-`dM` lane continues, remains a
single `Fam3`, seed `1`, `H = 0.25` control ladder rather than another
one-strength replay.

## Artifact Chain

- [`scripts/wave_direct_dm_transfer_diagnostic.py`](../scripts/wave_direct_dm_transfer_diagnostic.py)
- [`logs/2026-04-09-wave-direct-dm-transfer-diagnostic.txt`](../logs/2026-04-09-wave-direct-dm-transfer-diagnostic.txt)
- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAMILY_PAIR_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_FAMILY_PAIR_SYNTHESIS_NOTE.md)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-portability-batch.txt`](../logs/2026-04-08-wave-direct-dm-portability-batch.txt)
