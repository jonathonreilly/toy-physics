# Wave Direct-dM H=0.25 Fam1 Seed0 Control Note

**Date:** 2026-04-08
**Status:** proposed_retained control-ladder hardening on the Fam1/seed0 fine-H boundary replay

This note upgrades the earlier one-strength `Fam1`, seed `0`,
`H = 0.25` boundary replay by adding the same-resolution control stack:

> Keep the previously retained `Fam1`, seed `0`, `H = 0.25` point fixed,
> then add the exact `S = 0` null and the weak-field ladder
> `S = 0.002, 0.004, 0.008` to test whether the fine-`H` boundary replay
> is still well-posed once the coarse-lane controls are applied at the same
> resolution.

## Result

| strength | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | `delta_hist / s` |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.000` | `+0.000000` | `+0.000000` | `+0.000000` | `+0.00%` | `n/a` |
| `0.002` | `+0.002504` | `+0.003116` | `-0.000612` | `-19.63%` | `-0.305878` |
| `0.004` | `+0.004989` | `+0.006246` | `-0.001256` | `-20.12%` | `-0.314085` |
| `0.008` | `+0.009899` | `+0.012543` | `-0.002644` | `-21.08%` | `-0.330504` |

Summary:

- exact null: `max |delta_hist| = 0.000e+00`
- nonzero sign pattern: `- - -`
- `|delta_hist / s|` spread: `7.77%`

## Honest read

This is a real hardening of the fine-`H` branch for this specific pair.

What now survives on `Fam1`, seed `0`, `H = 0.25`:

- exact `S = 0` null
- common negative sign across the weak-field ladder
- low linearity spread on `|delta_hist / s|`
- stable normalized magnitude around `-20%` to `-21%`

So the earlier one-strength boundary replay is no longer just a narrow point.
For this specific family/seed pair, it is now a properly controlled fine-`H`
point.

## What this changes

- The seed-`0` branch is now controlled on both retained families:
  `Fam1`, seed `0` sits near `R_hist = -20%`, while `Fam2`, seed `0` sits near
  `R_hist = -23%`.
- The old high-band label does not come back once the ladder is applied.
  This row stays in the weaker fine-`H` branch.
- That strengthens the current seed-conditioned read:
  seed `0` is the weaker branch on both retained families at `H = 0.25`,
  with family acting as a smaller scale shift inside that branch.

## Boundary

This does **not** yet close the whole fine-`H` family-pair critique.

What remains open:

- `Fam1`, seed `1`, `H = 0.25` still lacks the same full control ladder
- the current claim is still bounded to `Fam1` and `Fam2`, not `Fam3`
- the result still supports a bounded fine-`H` family-pair surface, not a full
  `H = 0.25` portability law

So the exact retained claim is:

> `Fam1`, seed `0`, `H = 0.25` is now a controlled fine-`H` replay with exact
> null, stable sign, and approximately linear weak-field scaling at
> `R_hist ~ -20%`. Together with the existing `Fam2`, seed `0` control ladder,
> that closes the seed-`0` cross-family surface without promoting a full
> portability law.

## Artifact chain

- [`scripts/wave_direct_dm_h025_control_batch.py`](../scripts/wave_direct_dm_h025_control_batch.py)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam1-seed0.txt)
- `docs/WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*)

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [wave_direct_dm_h025_high_band_boundary_note](WAVE_DIRECT_DM_H025_HIGH_BAND_BOUNDARY_NOTE.md)
- [wave_direct_dm_h025_seed0_crossfamily_note](WAVE_DIRECT_DM_H025_SEED0_CROSSFAMILY_NOTE.md)
