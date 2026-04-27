# Gate B Grown Trapping Transport Note

**Date:** 2026-04-05  
**Status:** proposed_retained-grown-family trapping-capable transport probe, frozen as a bounded positive on the moderate-drift row

## Artifact chain

- [`scripts/gate_b_grown_trapping_transport_probe.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_trapping_transport_probe.py)
- [`logs/2026-04-05-gate-b-grown-trapping-transport-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-trapping-transport-probe.txt)

## Question

Can the retained Gate B grown row carry a minimal trap-capable transport
extension that still reduces exactly back to the frozen grown baseline at
`eta = 0`, while producing one bounded escape observable?

This probe stays narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- one static source field on that row
- one narrow trap slab near the middle of the path
- one observable: `escape(eta) = P_det(eta) / P_det(0)`
- exact `eta = 0` reduction check

## Frozen result

The frozen log uses four seeds and the retained moderate-drift grown row.
The trap slab is narrow and lives in the middle of the transport path.

Aggregated escape ratio:

| `eta` | mean `escape(eta)` | mean `trapped = 1 - escape` |
| --- | ---: | ---: |
| `0.05` | `0.799` | `0.201` |
| `0.10` | `0.642` | `0.358` |
| `0.20` | `0.428` | `0.572` |
| `0.35` | `0.268` | `0.732` |
| `0.50` | `0.205` | `0.795` |

## Safe read

The narrow, honest statement is:

- `eta = 0` reproduces the retained grown baseline exactly by construction
- the only promoted observable is the detector escape ratio
- escape falls steadily as the trap coupling increases
- by `eta = 0.50`, the mean detector escape is down to `0.205`
- this is a real trap-sensitive transport channel on the retained grown row,
  but it is still only a bounded transport probe

## Guardrail note

This probe does **not** claim a horizon theory.
It does **not** claim a general bidirectional field equation.
It does **not** claim generated-family transfer.

The exact zero-coupling reduction passes, and the escape observable is
bounded and monotone in the tested sweep. That is the claim surface to keep.

## Branch verdict

Treat this as a bounded positive on the retained grown geometry row.

The trap window is strong enough to survive skeptical reduction checks, and
the grown family now has a clean escape/trapping knob that can be carried
forward without over-reading it.
