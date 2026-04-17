# Gate B Grown Trapping Frontier Note

**Date:** 2026-04-05  
**Status:** retained-grown-family trapping/frontier probe, frozen as a bounded positive on the moderate-drift row

## Artifact chain

- [`scripts/gate_b_grown_trapping_frontier_probe.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_trapping_frontier_probe.py)
- [`logs/2026-04-05-gate-b-grown-trapping-frontier-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-trapping-frontier-probe.txt)

## Question

Can the retained Gate B grown row carry one stronger frontier observable than
plain detector escape, while still reducing exactly back to the frozen grown
baseline at `eta = 0`?

This probe stays narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- one static source field on the same row
- one narrow trap slab near the middle of the transport path
- two observables:
  - `escape(eta) = P_det(eta) / P_det(0)`
  - `frontier_bias(eta) = (P_frontier - P_core) / P_det`
- exact `eta = 0` reduction check

The promoted frontier observable is the detector-layer core/frontier contrast.
The escape ratio remains as the transport control.

## Frozen result

The frozen log uses four seeds and the retained moderate-drift grown row.
The trap slab is narrow and lives in the middle of the transport path.

Aggregated escape ratio and frontier response:

| `eta` | mean `escape(eta)` | mean `trapped = 1 - escape` | mean `frontier_share` | mean `frontier_bias` |
| --- | ---: | ---: | ---: | ---: |
| `0.05` | `0.919` | `0.081` | `0.317` | `+0.0227` |
| `0.10` | `0.849` | `0.151` | `0.331` | `+0.0440` |
| `0.20` | `0.740` | `0.260` | `0.356` | `+0.0811` |
| `0.35` | `0.628` | `0.372` | `0.386` | `+0.1230` |
| `0.50` | `0.557` | `0.443` | `0.407` | `+0.1509` |

## Safe read

The narrow, honest statement is:

- `eta = 0` reproduces the retained grown baseline exactly by construction
- the transport escape ratio still falls steadily as the trap coupling grows
- more importantly, the detector-layer frontier bias also rises steadily
- that means the trap is doing more than attenuation: it shifts the surviving
  detector mass outward toward the frontier shell
- this is still a bounded transport observable, not a horizon theory

## Guardrail note

This probe does **not** claim a horizon theory.
It does **not** claim a general bidirectional field equation.
It does **not** claim generated-family transfer.

The exact zero-coupling reduction passes, and the frontier observable is
bounded and monotone in the tested sweep. That is the claim surface to keep.

## Branch verdict

Treat this as a bounded positive on the retained grown geometry row.

The trap window is strong enough to survive skeptical reduction checks, and
the new frontier bias observable gives a cleaner shape-sensitive read than
escape alone.
