# Shapiro Scaling Direct Replay Note

**Date:** 2026-04-08  
**Status:** direct data-bearing replay of the retained Shapiro scaling laws

## Artifact Chain

- [`scripts/shapiro_scaling_direct_replay.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_scaling_direct_replay.py)
- [`scripts/shapiro_scaling_probe.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_scaling_probe.py)
- [`logs/2026-04-08-shapiro-scaling-direct-replay.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-08-shapiro-scaling-direct-replay.txt)
- [`docs/SHAPIRO_EXPERIMENTAL_CARD.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_EXPERIMENTAL_CARD.md)
- [`logs/2026-04-06-shapiro-delay-portable.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-delay-portable.txt)
- [`docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md)

## What Is Being Replayed

This is not a reconstruction from the anchor commit. It is a direct freeze of
the retained in-repo data:

- `s` law from the experimental card
- `b` law from the experimental card
- `k` law from the experimental card
- exact zero controls from the experimental card and portable delay log

## Exact Controls

- `s = 0 -> phase = 0.000 rad`
- `c = inst -> phase = 0.000000 rad`
- `b` is not an exact-zero law; it is a monotone tail law that approaches
  zero at large separation

## Direct Scaling Laws

| law | control | direct readout | source |
| --- | --- | --- | --- |
| `phase ~ s^1.000` | `s = 0 -> phase = 0` | verified over `s = 0.001` to `0.016` | `docs/SHAPIRO_EXPERIMENTAL_CARD.md` |
| phase decreases with `b` | large `b -> phase -> 0` | `b = 3.0 -> +0.062 rad`; `b = 5.0 -> +0.049 rad`; `b = 7.0 -> +0.040 rad` | `docs/SHAPIRO_EXPERIMENTAL_CARD.md` |
| `phase ~ k` | instantaneous field -> phase = 0 | `k = 2.0 -> +0.030 rad`; `k = 5.0 -> +0.062 rad`; `k = 10.0 -> +0.200 rad` | `docs/SHAPIRO_EXPERIMENTAL_CARD.md` |

## Portable Delay Table

| c | fam1 | fam2 | fam3 | mean |
| ---: | ---: | ---: | ---: | ---: |
| inst | -0.000000 | +0.000000 | -0.000000 | +0.000000 |
| 2.00 | +0.040233 | +0.040431 | +0.040130 | +0.040265 |
| 1.00 | +0.050011 | +0.050325 | +0.049930 | +0.050089 |
| 0.50 | +0.061643 | +0.061958 | +0.061700 | +0.061767 |
| 0.25 | +0.067893 | +0.068326 | +0.067886 | +0.068035 |

## Narrow Read

- the source-mass law stays linear over the retained 16x sweep
- the impact-parameter law stays ordered on the retained sampled rows
- the chromatic law stays direct in the retained k table
- the exact zero controls survive in both the source-off and instantaneous-field gates
- the portable delay log keeps the zero control explicit while showing the finite-c phase table

## Final Verdict

**the Shapiro scaling lane can close as a direct data-bearing replay: the retained s, b, and k laws are frozen from repo data, and the exact zero controls remain explicit**
