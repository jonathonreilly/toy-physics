# Gate B Grown Propagating Field Note

**Date:** 2026-04-05  
**Status:** retained-grown-family causal-field probe, frozen as a bounded no-go on the moderate-drift row

## Artifact chain

- [`scripts/gate_b_grown_propagating_field_probe.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_propagating_field_probe.py)
- [`logs/2026-04-05-gate-b-grown-propagating-field-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-propagating-field-probe.txt)

## Question

Can the retained Gate B grown row carry a minimal retarded-like / causal-memory
field state that still reduces exactly back to the frozen grown baseline at
`gamma = 0`, while producing a causal observable stronger than static deflection
alone?

This probe stays narrow:

- retained grown row only: `drift = 0.2`, `restore = 0.7`
- one far-field source position on that row
- one static baseline field
- one retarded-like field with a `gamma` sweep
- exact `gamma = 0` reduction check
- one causal observable beyond static deflection:
  detector-line phase ramp and escape ratio relative to `gamma = 0`

## Frozen result

The frozen probe is built so that `gamma = 0` reproduces the static retained
grown baseline exactly.

Frozen output from the retained three-seed row comparison:

| `gamma` | escape | `delta_z` | vs static | phase slope | `R^2` | phase span |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.00` | `1.000` | `1.300964e-04` | `0.000000e+00` | `0.0000` | `0.000` | `0.000` |
| `0.05` | `1.000` | `1.291910e-04` | `-9.053854e-07` | `0.0000` | `0.051` | `0.000` |
| `0.10` | `1.000` | `1.291018e-04` | `-9.945774e-07` | `0.0000` | `0.050` | `0.000` |
| `0.20` | `1.000` | `1.282304e-04` | `-1.866032e-06` | `0.0000` | `0.069` | `0.000` |
| `0.50` | `1.000` | `1.276327e-04` | `-2.463691e-06` | `0.0000` | `0.099` | `0.000` |

## Safe read

The narrow, honest statement is:

- `gamma = 0` recovers the retained grown baseline exactly
- finite `gamma` does **not** produce a coherent detector-line phase ramp on
  this retained grown row
- the escape ratio stays at `1.000` to three decimals
- only a tiny centroid shift survives, which is too weak to count as the
  desired causal observable
- the retarded-like update therefore fails the intended causal-observable bar
  even though it passes the exact reduction check

## Guardrail note

This probe is intentionally tiny.

- it does **not** claim a full self-consistent field theory
- it does **not** claim a generated-family transfer result
- it does **not** claim a horizon or trapping result

The exact reduction does pass, but the causal observable does not clear the
bar, so the right branch verdict is a clean no-go for this minimal
retarded-like field state on the retained grown family.

## Branch verdict

Treat this as a bounded no-go on the retained grown geometry row.

The exact reduction is real, but the minimal causal-memory / retarded-like
extension does not produce a stronger causal observable than static
deflection alone.
