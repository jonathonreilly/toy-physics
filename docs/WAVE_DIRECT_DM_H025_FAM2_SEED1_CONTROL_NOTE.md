# Wave Direct-dM H=0.25 Fam2 Seed1 Control Note

**Date:** 2026-04-08
**Status:** proposed_retained control-ladder hardening on the Fam2/seed1 fine-H replay

This note upgrades the earlier one-strength `Fam2`, seed `1`,
`H = 0.25` follow-up by adding the missing same-resolution control stack:

> Keep the previously retained `Fam2`, seed `1`, `H = 0.25` point fixed,
> then add the exact `S = 0` null and the weak-field ladder
> `S = 0.002, 0.004, 0.008` to test whether the fine-`H` replay is still
> well-posed once the coarse-lane controls are applied at the same
> resolution.

## Result

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.001896` | `+0.002900` | `-0.001004` | `-34.62%` | `-0.501940` |
| `0.004` | `+0.003777` | `+0.005814` | `-0.002037` | `-35.03%` | `-0.509158` |
| `0.008` | `+0.007497` | `+0.011686` | `-0.004189` | `-35.85%` | `-0.523664` |

Summary:

- exact null: `max |delta_hist| = 0.000e+00`
- nonzero sign pattern: `- - -`
- `|delta_hist / s|` spread: `4.25%`

## Honest read

This is a real hardening of the fine-`H` branch for this specific pair.

What now survives on `Fam2`, seed `1`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- low linearity spread on `|delta_hist / s|`
- stable normalized magnitude around `-35%`

So the earlier one-strength follow-up is no longer just a narrow replay.
For this specific family/seed pair, it is now a properly controlled
fine-`H` point.

## Boundary

This does **not** yet close the whole fine-`H` family-pair critique.

What remains open:

- the complementary `Fam2`, seed `0`, `H = 0.25` row is now also controlled
  in
  `WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md` (sibling artifact in same lane; cross-reference only — not a one-hop dep of this note),
  but the family pair still does not support a stable amplitude law
- `Fam1`/`Fam2` together still do not have a full same-resolution control
  ladder on all four fine-`H` points
- the result still supports a bounded family-pair asymmetry surface, not a
  full `H = 0.25` portability law

So the exact retained claim is:

> `Fam2`, seed `1`, `H = 0.25` is now a controlled fine-`H` replay with
> exact null, stable sign, and approximately linear weak-field scaling.
> That materially strengthens the second-family side of the fine-`H`
> story, but it does not yet close the full family-pair control gap.

## Artifact chain

- [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt)
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`
- [`docs/WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_FAM2_TWO_POINT_SYNTHESIS_NOTE.md)
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`
