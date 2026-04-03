# Higher Symmetry Comparison Note

**Date:** 2026-04-03  
**Status:** retained decoherence-side lead, but not the best gravity lane

This note freezes the current review-safe joint validation of the higher-
symmetry families:

[`scripts/higher_symmetry_joint_validation.py`](/Users/jonreilly/Projects/Physics/scripts/higher_symmetry_joint_validation.py)

Captured log:

[`logs/2026-04-03-higher-symmetry-joint-validation.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-higher-symmetry-joint-validation.txt)

## Setup

- `k = 5.0`
- `16` seeds
- `r = 5.0`
- families compared:
  - random (none)
  - `Z₂` mirror
  - `Z₂×Z₂` mirror
  - ring-like approximate rotational symmetry

## Joint Result

On this harness, `Z₂×Z₂` is the clear decoherence-side standout while
remaining Born-clean and gravity-positive.

| N | random (none) | Z₂ mirror | Z₂×Z₂ | ring |
|---|---:|---:|---:|---:|
| 25 | `0.731±0.046` | `1.000±0.000` | `0.616±0.032` | `0.684±0.025` |
| 40 | `0.864±0.037` | `1.000±0.000` | `0.661±0.035` | `0.783±0.037` |
| 60 | `0.901±0.026` | `1.000±0.000` | `0.682±0.036` | `0.837±0.032` |
| 80 | `0.880±0.026` | `1.000±0.000` | `0.782±0.028` | `0.921±0.034` |

The strongest supported row is:

- `Z₂×Z₂`, `N=25`
- `pur_cl = 0.616±0.032`
- `d_TV = 0.8927`
- `band+ = 21/30`
- `ok = 30` successful rows in the joint validation pass

The rough mean-curve fit on `Z₂×Z₂` in the joint validation gives:

- `(1 - pur_cl) ≈ 1.61 × N^-0.43`
- `R² ≈ 0.80`

That is a real decoherence-side improvement over the random and ring baselines
in this file, and it is also stronger than the current mirror chokepoint note
on the same purity proxy at matched `N`:

- mirror chokepoint at `N=25`: `pur_cl = 0.733±0.05`
- mirror chokepoint at `N=80`: `pur_cl = 0.818±0.03`
- `Z₂×Z₂` at `N=25`: `pur_cl = 0.616±0.032`
- `Z₂×Z₂` at `N=80`: `pur_cl = 0.782±0.028`

So on the review-safe decoherence-side metric, `Z₂×Z₂` is a real retained
improvement over the current mirror lane.

## Narrow Read

- `Z₂×Z₂` is the best decoherence-side family in this comparison.
- The plain `Z₂` lane in this script is not useful as a successor here; it
  saturates at `pur_cl = 1.0`.
- The joint validation keeps Born near machine precision and gravity positive,
  so this is not decoherence-only noise.
- The mirror chokepoint lane on `main` remains the stronger gravity-heavy
  bounded pocket, but `Z₂×Z₂` wins on the review-safe decoherence proxy.

## Verdict

**Retained lead.**

`Z₂×Z₂` is the best higher-symmetry family on the review-safe decoherence-side
metric, while staying Born-clean and gravity-positive in the joint validation.
It does not replace the mirror chokepoint as the strongest gravity-heavy lane,
but it is a real retained improvement on decoherence.
