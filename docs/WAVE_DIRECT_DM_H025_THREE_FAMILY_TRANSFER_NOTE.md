# Wave Direct-dM H=0.25 Three-Family Transfer Note

**Date:** 2026-04-12
**Status:** retained narrow transfer/compression freeze on the controlled
`Fam1`/`Fam2`/`Fam3` fine-`H` surface

This note freezes the next direct-`dM` widening step after the retained
two-family transfer diagnostic and the new Fam3 control rows:

> Hold the controlled `Fam1`, `Fam2`, and `Fam3` rows fixed at `H = 0.25`
> with `S = 0.004`, then ask whether the same-seed two-band read survives as
> a narrow transfer/compression statement across all three families.

## Evidence surface

The controlled rows are:

| family | seed | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | late gain |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Fam1` | `0` | `+0.004989` | `+0.006246` | `-0.001256` | `-20.12%` | `+0.001257` |
| `Fam1` | `1` | `+0.004411` | `+0.006255` | `-0.001843` | `-29.47%` | `+0.001844` |
| `Fam2` | `0` | `+0.005393` | `+0.006969` | `-0.001576` | `-22.61%` | `+0.001576` |
| `Fam2` | `1` | `+0.003777` | `+0.005814` | `-0.002037` | `-35.03%` | `+0.002037` |
| `Fam3` | `0` | `+0.005082` | `+0.006377` | `-0.001295` | `-20.31%` | `+0.001295` |
| `Fam3` | `1` | `+0.004772` | `+0.006552` | `-0.001780` | `-27.16%` | `+0.001780` |

Control-ladder summaries:

| family | seed | null max `|delta_hist|` | sign pattern | `|delta_hist / s|` spread |
| --- | ---: | ---: | --- | ---: |
| `Fam1` | `0` | `0.000e+00` | `- - -` | `7.77%` |
| `Fam1` | `1` | `0.000e+00` | `- - -` | `5.22%` |
| `Fam2` | `0` | `0.000e+00` | `- - -` | `6.67%` |
| `Fam2` | `1` | `0.000e+00` | `- - -` | `4.25%` |
| `Fam3` | `0` | `0.000e+00` | `- - -` | `7.64%` |
| `Fam3` | `1` | `0.000e+00` | `- - -` | `5.93%` |

## What Survives

The narrow retained read is now:

- every controlled row keeps the exact `S = 0` null
- every nonzero row keeps the same negative sign
- the seed split remains the primary coarse separator
- family acts mainly as a depth modulator inside each seed band

The same-seed transfer/compression pattern is therefore stable across the
three-family surface:

- seed `0` stays in the lower-magnitude band
- seed `1` stays in the higher-magnitude band
- `Fam3` fits the existing two-band read instead of forcing a new band

That is a genuine three-family transfer/compression freeze on the controlled
`H = 0.25` surface.

## Honest Read

The most conservative retained statement is:

> On the controlled `Fam1`/`Fam2`/`Fam3`, seed `0/1`, `H = 0.25`,
> `S = 0.004` surface, the direct-`dM` effect retains exact nulls, common
> negative sign, and the existing seed-conditioned transfer/compression
> split. Fam3 does not open a new band; it compresses into the existing
> same-seed structure.

That is stronger than a two-family compression note and still weaker than a
portability law.

## Boundary

This note does **not** claim:

- a family-independent `H = 0.25` portability law
- a third-seed law
- a frozen amplitude package
- a monotone family-depth law

The three-family surface is still family-dependent in absolute depth, so the
claim stays at transfer/compression only.

## Artifact Chain

- [`docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`](./WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md)
- [`logs/2026-04-09-wave-direct-dm-transfer-diagnostic.txt`](../logs/2026-04-09-wave-direct-dm-transfer-diagnostic.txt)
- [`logs/2026-04-12-wave-direct-dm-h025-control-fam3-seed0.txt`](../logs/2026-04-12-wave-direct-dm-h025-control-fam3-seed0.txt)
- [`logs/2026-04-09-wave-direct-dm-h025-control-fam3-seed1.txt`](../logs/2026-04-09-wave-direct-dm-h025-control-fam3-seed1.txt)
