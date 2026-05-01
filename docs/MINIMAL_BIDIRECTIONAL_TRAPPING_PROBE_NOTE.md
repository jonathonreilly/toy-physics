# Minimal Bidirectional Trapping Probe

**Date:** 2026-04-05  
**Status:** bounded moonshot trapping probe on the generated-geometry family
**Last verified:** 2026-05-01 — runner exits 0 with branch verdict "viable"; the previously-absent frozen log was regenerated as `logs/2026-04-05-minimal-bidirectional-trapping-probe.txt`

## Artifact chain

- [`scripts/minimal_bidirectional_trapping_probe.py`](../scripts/minimal_bidirectional_trapping_probe.py)
- [`logs/2026-04-05-minimal-bidirectional-trapping-probe.txt`](../logs/2026-04-05-minimal-bidirectional-trapping-probe.txt)

## Question

Can a minimal trapping extension create a genuine no-return threshold on the
retained generated-geometry family while still reducing back to the weak-field
lane at `alpha = 0`?

This note is intentionally narrow:

- one trapping parameter `alpha`
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

- the trapping extension does produce a real no-return threshold on this
  retained family
- the escape fraction falls below `50%` already by `alpha ≈ 0.10`
- the weak-field recovery check still holds at `alpha = 0`

The honest limitation is equally important:

- this is still a proxy trapping observable, not a full black-hole theory
- the branch is viable as a moonshot because it finds a sharp new threshold
  while still reducing cleanly back to the weak-field lane

## Relation to the retained lane

Read this together with:

- [`GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_NOTE.md)
- [`GATE_B_NONLABEL_CONNECTIVITY_V1_DISTANCE_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_DISTANCE_NOTE.md)
- [`GATE_B_NONLABEL_CONNECTIVITY_V1_JOINT_NOTE.md`](GATE_B_NONLABEL_CONNECTIVITY_V1_JOINT_NOTE.md)
- [`GATE_B_FARFIELD_NOTE.md`](GATE_B_FARFIELD_NOTE.md)

The retained weak-field story remains intact, and the new trapping branch adds
a qualitatively new strong-field observable: a no-return threshold.

## Branch verdict

This branch is **viable** as a moonshot direction.
It is not a full black-hole theory, but it is no longer just a narrative idea:
it produces a bounded threshold and reduces back to the weak-field lane.
