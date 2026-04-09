# Minimal Absorbing Horizon Probe

**Date:** 2026-04-05  
**Status:** bounded moonshot trapping probe on the retained generated-geometry family

## Artifact chain

- [`scripts/minimal_absorbing_horizon_probe.py`](/Users/jonreilly/Projects/Physics/scripts/minimal_absorbing_horizon_probe.py)
- [`logs/2026-04-05-minimal-absorbing-horizon-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-minimal-absorbing-horizon-probe.txt)

## Question

Can a minimal absorptive extension of the retained generated-geometry family
produce a genuine trapping / no-return threshold while still reducing back to
the weak-field lane at `alpha = 0`?

This note is intentionally narrow:

- one absorptive parameter `alpha`
- one observable: escape fraction versus `alpha`
- one weak-field recovery check at `alpha = 0`

## Frozen result

The frozen log is on the retained no-restore grown geometry family with the
geometry-sector stencil connectivity, `h = 0.5`, `W = 10`, `NL = 25`,
`seeds = 4`, and `z = [3, 4, 5]`.

Weak-field recovery check:

- exact grid: `3/3` TOWARD, `F~M = 1.00`
- sector stencil: `3/3` TOWARD, `F~M = 1.00`

Escape fraction versus absorption:

| alpha | escape | no-return |
| --- | ---: | ---: |
| `0.00` | `1.0002` | `-0.0002` |
| `0.10` | `0.4353` | `0.5647` |
| `0.30` | `0.0903` | `0.9097` |
| `0.50` | `0.0202` | `0.9798` |
| `2.00` | `0.0000` | `1.0000` |
| `10.00` | `0.0000` | `1.0000` |

## Safe read

The strongest bounded statement is:

- the absorptive extension does produce a real trapping threshold on this
  retained family
- the escape fraction falls below `50%` already by `alpha ≈ 0.10`
- the weak-field recovery check still holds at `alpha = 0`

The honest limitation is equally important:

- this is still a proxy horizon / trapping observable, not a full black-hole
  theory
- the branch is viable as a moonshot because it finds a sharp new threshold
  while still reducing cleanly back to the weak-field lane

## Relation to the retained lane

Read this together with:

- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_DISTANCE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_DISTANCE_NOTE.md)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V1_JOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V1_JOINT_NOTE.md)
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)

The retained weak-field story remains intact, and the new absorptive branch
adds a qualitatively new strong-field observable: a trapping threshold.

## Branch verdict

This branch is **viable** as a moonshot direction.
It is not a full black-hole theory, but it is no longer just a narrative idea:
it produces a retained threshold and reduces back to the weak-field lane.
