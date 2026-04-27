# Gate B Grown Trapping Frontier V3 Note

**Date:** 2026-04-05
**Status:** proposed_retained-grown-family frontier probe, frozen as a bounded positive on the moderate-drift row

## Artifact chain

- [`scripts/gate_b_grown_trapping_frontier_v3.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_trapping_frontier_v3.py)
- local log artifact: [`logs/2026-04-05-gate-b-grown-trapping-frontier-v3.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-trapping-frontier-v3.txt)

## Question

Can the retained Gate B grown row carry one more structural frontier
observable than the v2 radius shift, while still reducing exactly back to the
frozen grown baseline at `eta = 0`?

This v3 probe stays narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- one static source field on the same row
- one narrow trap slab near the middle of the transport path
- three observables:
  - `escape(eta) = P_det(eta) / P_det(0)`
  - `frontier_radius_shift(eta) = <|z|>_det(eta) - <|z|>_det(0)`
  - `frontier_shell_contrast_shift(eta) = C(eta) - C(0)`
    where `C = P_outer - P_inner` on detector-layer quartiles ordered by
    `|z|`
- exact `eta = 0` reduction check

The promoted frontier observable is the detector-layer shell-contrast shift.
The escape ratio and radius moment remain transport comparators.

## Why this is stronger than v2

v2 already showed that the trap pushes the detector-layer radial moment
outward.

V3 asks for a more structural redistribution:

- split the detector layer into an inner quartile and an outer quartile in
  `|z|`
- compare the detected probability in those two structural shells
- ask whether the trap increases the outer-minus-inner contrast even after
  exact zero-coupling reduction is enforced

That is a more structural observable than a first moment alone.

## Exact Reduction

`eta = 0` must reproduce the retained grown baseline exactly.

The specific reduction check is:

- the baseline detector distribution is used for the shell partition and the
  reference contrast
- the `eta = 0` run must return the same detector escape, radius moment, and
  shell contrast by construction

## Safe Read

The safe read stays narrow:

- `eta = 0` reproduces the retained grown baseline exactly
- escape falls steadily as trap coupling grows
- frontier radius shift remains positive as a legacy comparator
- the new structural target is the shell-contrast shift, and it also rises
  steadily with trap coupling

That means the trap is doing more than attenuating transport: it is
redistributing surviving detector mass across the frontier shell structure.

Frozen result from the retained moderate-drift row:

| `eta` | mean `escape(eta)` | mean `frontier_radius_shift` | mean `frontier_shell_contrast_shift` |
| --- | ---: | ---: | ---: |
| `0.05` | `0.799` | `+0.1236` | `+0.0337` |
| `0.10` | `0.642` | `+0.2650` | `+0.0722` |
| `0.20` | `0.428` | `+0.5915` | `+0.1608` |
| `0.35` | `0.268` | `+1.0815` | `+0.2931` |
| `0.50` | `0.205` | `+1.3795` | `+0.3735` |

## Guardrail Note

This probe does **not** claim a horizon theory.
It does **not** claim a general bidirectional field equation.
It does **not** claim generated-family transfer.
It does **not** turn the shell contrast into a new force law.

The only claim surface to keep is the exact reduction plus the structural
shell-contrast shift.

## Branch Verdict

Treat this as a bounded frontier probe on the retained grown geometry row.

The frontier should now be judged by a shell-structure observable rather than
just a first moment, while still respecting the exact `eta = 0` reduction
check.
