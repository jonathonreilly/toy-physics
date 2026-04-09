# Gate B Grown Trapping Frontier V2 Note

**Date:** 2026-04-05  
**Status:** retained-grown-family frontier probe, frozen as a bounded positive on the moderate-drift row

## Artifact chain

- [`scripts/gate_b_grown_trapping_frontier_v2.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_trapping_frontier_v2.py)
- [`logs/2026-04-05-gate-b-grown-trapping-frontier-v2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-trapping-frontier-v2.txt)

## Question

Can the retained Gate B grown row carry one stronger structural frontier
observable than plain detector escape, while still reducing exactly back to
the frozen grown baseline at `eta = 0`?

This probe stays narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- one static source field on the same row
- one narrow trap slab near the middle of the transport path
- two observables:
  - `escape(eta) = P_det(eta) / P_det(0)`
  - `frontier_radius_shift(eta) = <|z|>_det(eta) - <|z|>_det(0)`
- exact `eta = 0` reduction check

The promoted frontier observable is the detector-layer radial moment shift.
The escape ratio remains as the transport control.

## Frozen result

The frozen log uses four seeds on the retained moderate-drift grown row. The
trap slab is narrow and lives in the middle of the transport path.

Aggregated escape ratio and frontier radius response:

| `eta` | mean `escape(eta)` | mean `trapped = 1 - escape` | mean `frontier_radius_shift` |
| --- | ---: | ---: | ---: |
| `0.05` | `0.919` | `0.081` | `+0.0684` |
| `0.10` | `0.849` | `0.151` | `+0.1320` |
| `0.20` | `0.740` | `0.260` | `+0.2427` |
| `0.35` | `0.628` | `0.372` | `+0.3666` |
| `0.50` | `0.557` | `0.443` | `+0.4480` |

## Safe read

The safe read stays narrow:

- `eta = 0` reproduces the retained grown baseline exactly
- the escape ratio falls steadily as the trap coupling grows
- the frontier radius shift rises steadily too, so surviving detector mass is
  being pushed outward on the detector shell
- this is stronger than plain escape alone, but it is still only a bounded
  transport/frontier probe

## Guardrail note

This probe does **not** claim a horizon theory.
It does **not** claim a general bidirectional field equation.
It does **not** claim generated-family transfer.

The only claim surface to keep is the exact reduction plus the promoted
frontier moment shift.

## Branch verdict

Treat this as a bounded positive on the retained grown geometry row.

The trap window now has two reviewable signals:

- escape falls steadily with the trap coupling
- the detector frontier radius shifts outward steadily as well

That is still not a horizon theory, but it is stronger than the previous
escape-only transport probe.
