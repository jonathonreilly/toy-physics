# Wave Direct-dM H=0.25 Fam2 Two-Point Synthesis Note

**Date:** 2026-04-08
**Status:** proposed_retained narrow synthesis on the second fine-`H` `Fam2` pair

This note freezes the second-family fine-`H` claim surface for the
direct-`dM` matched-schedule lane:

> Start from the retained direct-`dM` portability batch plus the `Fam2`
> seed-`0` boundary and seed-`1` follow-up, then compare the fully
> controlled `H = 0.25` `Fam2` pair before widening into `Fam3`, extra
> seeds, or a broader fine-`H` batch.

## Fine-`H` pair

Reference strength `S = 0.004`:

| seed | `dM(early)` | `dM(late)` | `delta_hist` | `R_hist` | late gain |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `0` | `+0.005393` | `+0.006969` | `-0.001576` | `-22.61%` | `+0.001576` |
| `1` | `+0.003777` | `+0.005814` | `-0.002037` | `-35.03%` | `+0.002037` |

Control-ladder summaries:

| seed | null max `|delta_hist|` | sign pattern | `|delta_hist / s|` spread |
| ---: | ---: | --- | ---: |
| `0` | `0.000e+00` | `- - -` | `6.67%` |
| `1` | `0.000e+00` | `- - -` | `4.25%` |

## Coarse-to-fine comparison

| seed | coarse-`H` `R_hist` band (`0.5`, `0.35`) | `H = 0.25` `R_hist` | coarse-`H` late-gain band | `H = 0.25` late gain | read |
| ---: | ---: | ---: | ---: | ---: | --- |
| `0` | `-42.33%`, `-37.73%` | `-22.61%` | `+0.004085`, `+0.002874` | `+0.001576` | old high band closes |
| `1` | `-26.31%`, `-22.32%` | `-35.03%` | `+0.001937`, `+0.002061` | `+0.002037` | seed-1 late gain retains |

## Headline read

- Both seeds keep exact null, common negative sign, and bounded
  weak-field linearity at `H = 0.25`, so the second-family fine-`H` pair
  is now controlled rather than one-strength.
- The same cross-seed asymmetry seen on `Fam1` survives on `Fam2`, but the
  stable feature is again the late-gain ordering, not a frozen amplitude
  package.
- Seed `0` collapses out of the old coarse high band into the lower
  `-22%` to `-24%` regime.
- Seed `1` keeps its late-gain scale and stays materially stronger, around
  `-35%`, but that still does not restore a refinement-stable amplitude law.

So the narrow promotion rule is:

> On the current `Fam2` fine-`H` pair, the direct-`dM` matched-history
> effect survives with controls on both seeds, and the seed-conditioned
> late-gain asymmetry survives too. But the old coarse amplitude bands do
> not survive refinement, so this is a controlled family-pair asymmetry
> result, not an `H = 0.25` portability extension.

## What this changes

- The fine-`H` story is no longer bounded to one-strength replays on the
  second family.
- `Fam1` and `Fam2` now each have a retained fine-`H` pair read.
- That is enough to justify a narrow cross-family compression pass next.
- It is still not enough to justify `Fam3`, broader seed widening, or a
  lab-facing magnitude claim.

## Artifact chain

- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_BOUNDARY_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED0_CONTROL_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_FOLLOWUP_NOTE.md`
- `docs/WAVE_DIRECT_DM_H025_FAM2_SEED1_CONTROL_NOTE.md`
- [`logs/2026-04-08-wave-direct-dm-h025-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-fam2-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed0.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-fam2-seed1.txt)
- [`logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt`](../logs/2026-04-08-wave-direct-dm-h025-control-fam2-seed1.txt)
