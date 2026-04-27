# Gate B Grown Propagating Field v2 Note

**Date:** 2026-04-05  
**Status:** bounded no-go for a stronger proposed_retained-grown propagating-field
architecture on the moderate-drift row

## Artifact chain

- [`scripts/gate_b_grown_propagating_field_v2.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_propagating_field_v2.py)
- [`logs/2026-04-05-gate-b-grown-propagating-field-v2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-propagating-field-v2.txt)

## Question

Can a minimally stronger retained-grown architecture than simple
layer-memory / gamma blending produce a causal observable on the moderate-drift
Gate B row while still reducing exactly to the retained grown baseline at
`gamma = 0`?

This v2 probe is intentionally narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- one static source-resolved baseline field
- one complex transport-envelope field with a second-order layer recurrence
  and transverse coupling
- exact `gamma = 0` reduction check
- one promoted observable beyond static deflection:
  detector escape ratio plus detector-line phase ramp relative to the static
  baseline

## Frozen result

The frozen sweep uses four seeds and the retained moderate-drift grown row.
The transport envelope is stronger than simple layer-memory blending, because
it adds:

- a second-order layer recurrence
- transverse Laplacian coupling
- a phase-tilted source drive
- a complex field contribution that only enters when `gamma > 0`

Aggregated result:

| `gamma` | escape | `delta_z` | phase slope | `R^2` | phase span |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.00` | `1.000` | `+1.350067e-04` | `0.0000` | `0.000` | `0.000` |
| `0.05` | `1.000` | `+4.048540e-05` | `0.0000` | `0.566` | `0.001` |
| `0.10` | `1.000` | `-5.403749e-05` | `0.0001` | `0.566` | `0.001` |
| `0.20` | `1.000` | `-2.430880e-04` | `0.0001` | `0.566` | `0.003` |
| `0.50` | `0.999` | `-8.102773e-04` | `0.0003` | `0.566` | `0.007` |

Weak-field mass-scaling sanity check:

- `F~M` at `gamma = 0`: `1.000`
- `F~M` at `gamma = 0.5`: `1.000`

## Safe read

The narrow, honest statement is:

- `gamma = 0` reproduces the retained grown baseline exactly
- the stronger transport-envelope architecture does not produce a meaningful
  escape signal on the retained grown row
- the detector-line phase ramp stays effectively flat
- only a tiny centroid shift survives, and it is too small to count as a
  retained causal observable
- weak-field mass scaling stays linear, which is good, but not enough to save
  the causal-field claim

## Guardrail note

This v2 probe is not a full self-consistent field theory.
It does **not** claim generated-family transfer.
It does **not** claim a horizon theory.
It does **not** claim a trapping threshold.

The architecture is stronger than the earlier layer-memory / retarded-like
blend, but it still fails the intended causal-observable bar on the retained
grown row.

## Branch verdict

Treat this as a bounded no-go for the stronger retained-grown propagating-field
architecture tested here.

The exact zero-coupling reduction is real, but the transport envelope remains
too weak to produce a retained phase or escape observable beyond static
deflection.
