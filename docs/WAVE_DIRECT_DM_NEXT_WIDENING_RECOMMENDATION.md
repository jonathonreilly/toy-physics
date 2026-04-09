# Wave Direct-dM Next Widening Recommendation

**Date:** 2026-04-08  
**Status:** updated recommendation note after closing the seed-`0` cross-family surface

This note records the cheapest useful next widening step after the
current seed-`0` `H = 0.25` cross-family controls.

The existing fine-`H` evidence already shows:

- exact `S = 0` null on the controlled ladders
- common negative sign across the weak-field sweep
- low within-ladder linearity spread on `|delta_hist / s|`
- a bounded seed split in the normalized magnitude on the fully controlled
  `Fam2` pair and the controlled seed-`0` cross-family surface

The remaining question is not whether the direct-`dM` lane works at all.
It is which missing first-family `H = 0.25` control point buys the most
information per unit runtime now that seed `0` is closed across families.

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

The next best batch is:

> `Fam1`, seed `1`, `H = 0.25` control ladder.

Why this one:

- it is now the oldest remaining uncontrolled fine-`H` point
- it closes the first-family pair under the same control stack
- it pairs directly with the existing `Fam2`, seed `1` control ladder,
  giving the cleanest same-seed cross-family comparison on the stronger branch
  before widening to `Fam3`

Why not the other candidates:

- a widened seed/family batch is strictly more expensive and is not the
  cheapest next discriminator until the first-family pair is fully controlled
- `Fam3` is premature while the first-family pair still lacks any full
  same-resolution control ladder

## Honest read

This recommendation is based on the retained fine-`H` surface after closing the
second-family pair, not on a new portability promotion.

If `Fam1`, seed `1`, `H = 0.25` comes back with exact null, common negative
sign, and low within-ladder spread, both retained families will have a fully
controlled fine-`H` pair.

If it does not, the lane will have identified the first control failure inside
the stronger branch before spending a broader batch on `Fam3` or extra seeds.

## Artifact Chain

- [`docs/WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM1_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md`](./WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md)
- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-fam2-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt)
