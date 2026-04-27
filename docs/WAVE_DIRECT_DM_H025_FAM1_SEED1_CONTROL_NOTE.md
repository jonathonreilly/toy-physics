# Wave Direct-dM H=0.25 Fam1 Seed1 Control Note

**Date:** 2026-04-08
**Status:** proposed_retained control-ladder hardening on the Fam1/seed1 fine-H continuation

This note upgrades the earlier one-strength `Fam1`, seed `1`,
`H = 0.25` continuation by adding the same-resolution control stack:

> Keep the previously retained `Fam1`, seed `1`, `H = 0.25` point fixed,
> then add the exact `S = 0` null and the weak-field ladder
> `S = 0.002, 0.004, 0.008` to test whether the fine-`H` stronger branch
> is still well-posed once the coarse-lane controls are applied at the same
> resolution.

## Result

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.002215` | `+0.003121` | `-0.000905` | `-29.02%` | `-0.452743` |
| `0.004` | `+0.004411` | `+0.006255` | `-0.001843` | `-29.47%` | `-0.460793` |
| `0.008` | `+0.008748` | `+0.012563` | `-0.003816` | `-30.37%` | `-0.476948` |

Summary:

- exact null: `max |delta_hist| = 0.000e+00`
- nonzero sign pattern: `- - -`
- `|delta_hist / s|` spread: `5.22%`

## Honest read

This is a real hardening of the fine-`H` branch for this specific pair.

What now survives on `Fam1`, seed `1`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- low linearity spread on `|delta_hist / s|`
- stable normalized magnitude around `-29%` to `-30%`

So the earlier one-strength continuation is no longer just a narrow replay.
For this specific family/seed pair, it is now a properly controlled fine-`H`
point.

## What this changes

- The first-family `H = 0.25` pair is now fully controlled:
  `Fam1`, seed `0` sits near `R_hist = -20%`, while `Fam1`, seed `1` sits near
  `R_hist = -30%`.
- The stronger seed-`1` branch survives the full control ladder.
  It does not collapse into the weaker seed-`0` regime.
- That means both retained families now have a fully controlled fine-`H` pair,
  and both pairs show the same qualitative split:
  seed `0` weaker, seed `1` stronger.

## Boundary

This does **not** yet establish a full portability law.

What remains open:

- the current claim is still bounded to `Fam1` and `Fam2`, not `Fam3`
- the effect still does not define a refinement-stable amplitude package
- cross-family compression of the now-controlled pairs is the next honest
  synthesis step before further widening

So the exact retained claim is:

> `Fam1`, seed `1`, `H = 0.25` is now a controlled fine-`H` replay with exact
> null, stable sign, and approximately linear weak-field scaling at
> `R_hist ~ -30%`. Together with the existing `Fam1`, seed `0` control ladder,
> that closes the first-family fine-`H` pair without promoting a portability
> law.

## Artifact chain

- [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- [`scripts/wave_direct_dm_h025_control_freeze.py`](../scripts/wave_direct_dm_h025_control_freeze.py)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed1.txt)
- [`docs/WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md`](./WAVE_DIRECT_DM_H025_LOW_BAND_RETENTION_NOTE.md)
- [`docs/WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md`](./WAVE_DIRECT_DM_H025_TWO_POINT_SYNTHESIS_NOTE.md)
