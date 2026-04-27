# Wave Direct-dM Next Widening Recommendation

**Date:** 2026-04-08  
**Status:** updated recommendation note after closing both proposed_retained family pairs

This note records the honest next move after the current `Fam1`/`Fam2`
fine-`H` control ladders.

The existing fine-`H` evidence already shows:

- exact `S = 0` null on the controlled ladders
- common negative sign across the weak-field sweep
- low within-ladder linearity spread on `|delta_hist / s|`
- a bounded seed split in the normalized magnitude on the fully controlled
  `Fam2` pair and the controlled seed-`0` cross-family surface

The remaining question is not whether the direct-`dM` lane works at all.
It is whether more widening is the best next use of time now that both retained
families have fully controlled `H = 0.25` pairs.

## Cost Model

From the current fine-`H` point logs, one four-strength control ladder at
`H = 0.25` costs about:

- `108` to `121` seconds wall time
- `691` to `700` MB peak RSS

That cost is effectively the same for `Fam1` and `Fam2`, and roughly the
same for seed `0` and seed `1`.

So the cheapest widening step is not a faster family. It is the smallest
missing control that closes the current fine-`H` symmetry gap.

## Recommendation

The next best move is:

> **pause widening and compress the two controlled family pairs first.**

Why this one:

- both retained families now have fully controlled `H = 0.25` pairs
- the cheapest high-value update is to compress those two pair syntheses into
  one controlled cross-family read
- widening to `Fam3` before that compression would increase runtime and
  branch count without first exploiting the information already on the table

Why not the other candidates:

- `Fam3` is still the natural next widening target, but it is more expensive
  than the now-available compression pass
- another seed/family batch would widen the tree before the controlled
  `Fam1`/`Fam2` structure has been summarized cleanly

## Honest read

This recommendation is based on the retained fine-`H` surface after closing
both retained family pairs, not on a new portability promotion.

What is available now:

- controlled `Fam1` pair
- controlled `Fam2` pair
- controlled seed-`0` cross-family surface
- a bounded family-pair synthesis already pointing to seed-conditioned
  late-gain ordering rather than a stable amplitude law

That is enough to justify a controlled `Fam1`/`Fam2` compression before any
`Fam3` batch.

## Artifact Chain

- [`docs/WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM1_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md`](./WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md)
- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt)
