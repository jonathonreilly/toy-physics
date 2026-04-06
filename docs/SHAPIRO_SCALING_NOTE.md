# Shapiro Scaling Note

**Date:** 2026-04-06  
**Status:** reconstruction from retained Shapiro artifacts anchored in commit `1730b52`

## Replay Kind

This is a reconstruction, not a fresh simulation. The retained delay rows and
bridge notes already exist on `main`; this note freezes the scaling laws they
support.

## Artifact Chain

- [`scripts/shapiro_scaling_probe.py`](/Users/jonreilly/Projects/Physics/scripts/shapiro_scaling_probe.py)
- [`logs/2026-04-06-shapiro-scaling-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-shapiro-scaling-probe.txt)
- [`docs/SHAPIRO_DELAY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DELAY_NOTE.md)
- [`docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_FAMILY_PORTABILITY_NOTE.md)
- [`docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DIAMOND_BRIDGE_NOTE.md)
- [`docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md)
- [`docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md)
- retained scaling anchor: commit `1730b52` (`feat(shapiro): phase scales as s^1.000 (linear in mass), proportional to k`)

## Question

What is the canonical in-repo scaling card for the retained Shapiro delay,
keeping the exact controls explicit?

## Exact Controls

- `s = 0` maps to phase `0.000 rad` in the scaling interpretation
- `c = inst` stays exactly `0.000 rad` in the retained delay table
- exact zero control survives; this is the first gate for the scaling chain

## Retained Scaling Laws

| law | exact control | retained readout | support |
| --- | --- | --- | --- |
| `phase ~ s^1.000` | `s = 0 -> phase = 0` | linear in source strength / mass proxy | commit `1730b52` + `SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md` |
| phase decreases with `b` | large-`b` tail is the low-delay side of the sweep | `b = 3 -> +0.062 rad`; `b = 7 -> +0.040 rad` | commit `1730b52` + retained Shapiro bridge card |
| `phase ~ k` | `k -> 0` removes the phase accumulation in the action convention | chromatic / frequency-sensitive response | `SHAPIRO_DIAMOND_FREQUENCY_BRIDGE_NOTE.md` |

## Retained Delay Table

| c | phase lag mean | family spread | fam1 | fam2 | fam3 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `2.00` | `+0.0401 rad` | `0.0001 rad` | `+0.0401` | `+0.0401` | `+0.0400` |
| `1.00` | `+0.0500 rad` | `0.0002 rad` | `+0.0499` | `+0.0501` | `+0.0499` |
| `0.50` | `+0.0621 rad` | `0.0002 rad` | `+0.0621` | `+0.0622` | `+0.0620` |
| `0.25` | `+0.0679 rad` | `0.0000 rad` | `+0.0679` | `+0.0679` | `+0.0679` |

## Narrow Read

- the source/mass scaling law is the retained `phase ~ s^1.000` anchor
- the impact-parameter trend is the retained `b`-decreasing tail
- the frequency law is the retained `phase ~ k` bridge
- family spread on the portable delay table stays at or below `2e-4 rad`
- this is a portability/scaling reconstruction, not a uniqueness proof

## Final Verdict

**the retained Shapiro scaling card is a reconstruction from already-retained
artifacts: phase is linear in source strength / mass proxy, decreases with
impact parameter `b`, and is proportional to `k`, with exact zero control
explicit**
