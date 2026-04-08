# Wave Direct-dM Next Widening Recommendation

**Date:** 2026-04-08  
**Status:** recommendation note for the next fine-`H` widening step

This note records the cheapest useful next widening step after the
current `H = 0.25` control ladders.

The existing fine-`H` evidence already shows:

- exact `S = 0` null on the controlled ladders
- common negative sign across the weak-field sweep
- low within-ladder linearity spread on `|delta_hist / s|`
- a bounded seed split in the normalized magnitude

The remaining question is not whether the direct-`dM` lane works at all.
It is which missing `H = 0.25` control point buys the most information
per unit runtime.

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

> `Fam2`, seed `0`, `H = 0.25` control ladder.

Why this one:

- it is the missing same-resolution partner to the already retained
  `Fam2`, seed `1` control ladder
- it directly tests whether the seed-dependent late-gain split survives
  when the second family is given the same control stack on both seeds
- it is cheaper in information terms than widening to a new family or a
  wider seed/family batch

Why not the other candidates:

- `Fam1`, seed `0` is already diagnosed as a boundary point, so a second
  control ladder there would mostly duplicate what the current synthesis
  already knows
- `Fam1`, seed `1` is already retained as a controlled fine-`H` point
- a widened seed/family batch is strictly more expensive and is not the
  cheapest next discriminator until the `Fam2` pair is closed

## Honest read

This recommendation is based on existing retained evidence, not on a new
promoted control result.

If `Fam2`, seed `0`, `H = 0.25` comes back aligned with the current
`Fam2`, seed `1` control ladder, the fine-`H` story gets a stronger
family-pair surface.

If it does not, the next widening step should be a broader seed/family
batch only after the `Fam2` pair has been fully characterized.

## Artifact Chain

- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md)
- [`docs/WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md`](./WAVE_DIRECT_DM_SEED_BAND_DIAGNOSIS_NOTE.md)
- [`logs/2026-04-08-wave-direct-dm-h025-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-fam2-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-fam2-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt)
