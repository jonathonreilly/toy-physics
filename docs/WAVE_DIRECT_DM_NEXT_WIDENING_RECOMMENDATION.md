# Wave Direct-dM Next Widening Recommendation

**Date:** 2026-04-08  
**Status:** updated recommendation note after closing the `Fam2` fine-`H` pair

This note records the cheapest useful next widening step after the
current `Fam2` `H = 0.25` control ladders.

The existing fine-`H` evidence already shows:

- exact `S = 0` null on the controlled ladders
- common negative sign across the weak-field sweep
- low within-ladder linearity spread on `|delta_hist / s|`
- a bounded seed split in the normalized magnitude on the fully controlled
  `Fam2` pair

The remaining question is not whether the direct-`dM` lane works at all.
It is which missing first-family `H = 0.25` control point buys the most
information per unit runtime.

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

> `Fam1`, seed `0`, `H = 0.25` control ladder.

Why this one:

- it is the oldest remaining uncontrolled fine-`H` point
- it is the original high-band-collapse boundary case, so a control ladder
  there is the cheapest way to test whether the weak branch is genuinely
  stable on the first family
- it pairs directly with the newly controlled `Fam2`, seed `0` row, giving the
  cleanest same-seed cross-family comparison before widening to `Fam3`

Why not the other candidates:

- `Fam1`, seed `1` is still useful, but it is less decisive than hardening the
  original boundary row on the first family
- a widened seed/family batch is strictly more expensive and is not the
  cheapest next discriminator until at least one `Fam1` point is controlled
- `Fam3` is premature while the first-family pair still lacks any full
  same-resolution control ladder

## Honest read

This recommendation is based on the retained fine-`H` surface after closing the
second-family pair, not on a new portability promotion.

If `Fam1`, seed `0`, `H = 0.25` comes back with exact null, common negative
sign, and low within-ladder spread, the weak branch will be controlled on both
families.

If it does not, the lane will have identified the first cross-family weakness
inside the same seed before spending a broader batch on `Fam3` or extra seeds.

## Artifact Chain

- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md)
- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-fam2-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt)
