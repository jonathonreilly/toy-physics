# Minimal Absorbing-Horizon Probe Note

**Date:** 2026-04-05  
**Status:** moonshot strong-field absorbing-proxy probe on the retained 3D
ordered-lattice family

## Artifact chain

- [`scripts/minimal_absorbing_horizon_probe.py`](/Users/jonreilly/Projects/Physics/scripts/minimal_absorbing_horizon_probe.py)
- [`logs/2026-04-05-minimal-absorbing-horizon-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-minimal-absorbing-horizon-probe.txt)

## Question

Can a minimal absorptive extension of the retained valley-linear propagation
produce a real trapping / horizon-like threshold, measured as a drop in escape
fraction, while still reducing back to the weak-field lane at `alpha = 0`?

This note is intentionally narrow:

- one retained 3D ordered-lattice family
- one absorptive coupling parameter `alpha`
- one main observable: escape fraction to the far detector
- one weak-field reduction check at `alpha = 0`

## Frozen result

The frozen log records a sweep over:

- `h = 0.5`
- `W = 8`
- `L = 12`
- `mass_z = 3.0`
- `strength = 0.1`
- `alpha = 0.0, 0.1, 0.3, 0.5, 1.0, 2.0, 5.0, 10.0`

Frozen readout:

| alpha | escape fraction | absorbed fraction |
| ---: | ---: | ---: |
| 0.0 | `1.0000` | `0.0000` |
| 0.1 | `0.8957` | `0.1043` |
| 0.3 | `0.7205` | `0.2795` |
| 0.5 | `0.5814` | `0.4186` |
| 1.0 | `0.3447` | `0.6553` |
| 2.0 | `0.1277` | `0.8723` |
| 5.0 | `0.0088` | `0.9912` |
| 10.0 | `0.0002` | `0.9998` |

## Safe read

The honest bounded statement is:

- the `alpha = 0` row survives the weak-field reduction check and stays on the
  retained weak-field TOWARD lane
- the absorptive sweep then measures how much far-detector probability is lost
  as `alpha` increases
- the sweep does show a real threshold-like drop: the 50% escape threshold is
  reached by `alpha ≈ 1.0` on this retained family
- the strong-field branch therefore gives a real bounded trapping / absorption
  proxy, not just a smooth no-op decay

## Relation to the retained weak-field lane

Read this together with:

- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)
- [`docs/GATE_B_H025_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_H025_FARFIELD_NOTE.md)
- [`docs/PHYSICS_FIRST_ATTACK_PLAN.md`](/Users/jonreilly/Projects/Physics/docs/PHYSICS_FIRST_ATTACK_PLAN.md)

The reduction check is the key guardrail:

- if `alpha = 0` does not recover the retained weak-field lane, this branch is
  not a continuation of the current physics story
- if it does recover, then the absorption sweep can be interpreted as a
  legitimate strong-field deformation of the retained weak-field model

The branch should be judged on two things only:

- whether the escape fraction shows a real threshold / no-return regime
- whether the weak-field limit survives cleanly

On this frozen replay, both checks pass in the bounded sense:

- there is a clear threshold-like absorption regime
- the alpha=0 weak-field reduction survives and stays TOWARD

No other claim should be promoted from this note.
