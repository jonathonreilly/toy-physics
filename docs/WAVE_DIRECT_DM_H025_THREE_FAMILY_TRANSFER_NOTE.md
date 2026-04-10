# Wave Direct-dM H=0.25 Three-Family Transfer Note

**Date:** 2026-04-10
**Status:** retained narrow three-family transfer compression on the controlled `H = 0.25` surface

This note freezes the next bounded direct-`dM` closeout after both `Fam3`
control ladders landed:

> On the controlled `Fam1`/`Fam2`/`Fam3`, seed-`0`/`1`, `H = 0.25`,
> `s = 0.004` matched-schedule surface, what survives if the existing
> coarse-to-fine late-gain transfer diagnostic is extended to the third family?

The answer is still narrow:

> seed `0` compresses sharply on all three families, seed `1` stays above
> seed `0` on all three families, and the new `Fam3` pair adds extra seed-`1`
> compression without changing the cross-seed ordering.

This is a transfer/compression result, not an `H = 0.25` portability law.

## Evidence surface

This closeout uses the already-retained direct-`dM` chain:

- [`docs/WAVE_DIRECT_DM_MATCHED_HISTORY_NOTE.md`](./WAVE_DIRECT_DM_MATCHED_HISTORY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_PORTABILITY_BATCH_NOTE.md`](./WAVE_DIRECT_DM_PORTABILITY_BATCH_NOTE.md)
- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`](./WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md)

As in the earlier two-family diagnostic, use the late gain

`G = dM(late) - dM(early)`

and compare the fine row against the retained coarse pair:

`T(F, s) = G(H = 0.25) / mean(G(H = 0.5), G(H = 0.35))`

The surface stays intentionally fixed:

- families: `Fam1`, `Fam2`, `Fam3`
- seeds: `0`, `1`
- resolution: `H = 0.25`
- strength: `s = 0.004`
- same matched-history schedule pair as the retained direct-`dM` lane

## Three-family transfer table

| family | seed | mean coarse `G` | `G(H = 0.25)` | `T(F,s)` | `R_hist(H = 0.25)` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `Fam1` | `0` | `+0.003848` | `+0.001257` | `0.3266` | `-20.12%` |
| `Fam1` | `1` | `+0.001761` | `+0.001844` | `1.0471` | `-29.47%` |
| `Fam2` | `0` | `+0.003480` | `+0.001576` | `0.4529` | `-22.61%` |
| `Fam2` | `1` | `+0.001999` | `+0.002037` | `1.0190` | `-35.03%` |
| `Fam3` | `0` | `+0.003808` | `+0.001295` | `0.3401` | `-20.31%` |
| `Fam3` | `1` | `+0.002089` | `+0.001780` | `0.8525` | `-27.16%` |

## What survives

Three features now survive on the fully controlled three-family fine-`H`
surface:

- seed-`0` rows compress sharply on every family:
  `T = 0.3266`, `0.4529`, `0.3401`
- seed-`1` rows remain above the seed-`0` branch on every family:
  `T = 1.0471`, `1.0190`, `0.8525`
- the new `Fam3` pair does not restore the old coarse high band; it only shows
  that the cross-seed ordering survives one more family even when seed `1`
  compresses somewhat relative to `Fam1`/`Fam2`

So the honest retained statement is:

> On the controlled `Fam1`/`Fam2`/`Fam3`, seed-`0`/`1`, `H = 0.25`,
> `s = 0.004` matched-schedule surface, the direct-`dM` split is still best
> tracked as late-gain transfer/compression. Seed `0` compresses into the
> weaker branch on all three families, while seed `1` stays above seed `0`
> on all three families. `Fam3` adds extra seed-`1` compression, but it does
> not change the branch ordering.

That is stronger than the earlier two-family diagnostic and weaker than a
fine-`H` portability claim.

## What this changes

- The active direct-`dM` freeze no longer needs to speak only in historical
  `Fam1`/`Fam2` language: the third-family control pair is now folded into the
  same transfer/compression frame.
- The clean cross-family feature is branch ordering, not a universal transfer
  factor and not a stable `R_hist` amplitude package.
- The next honest direct-`dM` push is now the one already queued in the
  orchestrator: explain the split with one concrete history-coupling or
  geometry/transfer diagnostic on this controlled surface, then decide whether
  any genuinely predeclared `H = 0.25` control ladder still remains.

## Boundary

This note does **not** claim:

- an `H = 0.25` portability law
- a third-seed law
- a fourth-family law
- that seed `1` always preserves its full coarse transfer factor

The retained read stays narrow:

- controlled surface only
- matched-schedule direct-`dM` observable only
- branch ordering and compression only

## Artifact chain

- [`logs/2026-04-09-wave-direct-dm-h025-three-family-transfer.txt`](../logs/2026-04-09-wave-direct-dm-h025-three-family-transfer.txt)
- [`logs/2026-04-09-wave-direct-dm-transfer-diagnostic.txt`](../logs/2026-04-09-wave-direct-dm-transfer-diagnostic.txt)
- [`logs/2026-04-09-wave-direct-dm-h025-control-fam3-seed0.txt`](../logs/2026-04-09-wave-direct-dm-h025-control-fam3-seed0.txt)
- [`logs/2026-04-09-direct-dm-fam3-seed1-h025-control.txt`](../logs/2026-04-09-direct-dm-fam3-seed1-h025-control.txt)
- [`docs/WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md`](./WAVE_DIRECT_DM_TRANSFER_DIAGNOSTIC_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM3_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM3_SEED1_CONTROL_NOTE.md)
