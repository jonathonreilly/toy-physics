# Gate B Grown Propagating Field Radical Note

**Date:** 2026-04-05  
**Status:** bounded no-go for a beam-sourced self-consistent propagating-field
architecture on the retained grown row

**Audit-lane runner update (2026-05-09):** The primary runner `scripts/gate_b_grown_propagating_field_radical.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 added; runs in 87s under the new budget. The runner's pass/fail semantics are unchanged; this update only ensures the audit-lane sees a complete cache instead of a TIMEOUT row.

## Artifact chain

- [`scripts/gate_b_grown_propagating_field_radical.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_propagating_field_radical.py)
- [`logs/2026-04-05-gate-b-grown-propagating-field-radical.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-propagating-field-radical.txt)

## Question

Can a materially different grown-row architecture, where the field is
re-sourced from the propagated beam density/current and iterated to a
self-consistent fixed point, produce a causal observable while still reducing
exactly to the retained grown baseline when the feedback coupling is zero?

This probe is intentionally narrow:

- retained grown geometry row only: `drift = 0.2`, `restore = 0.7`
- one static source-resolved baseline field
- one beam-sourced complex feedback field
- one iterative fixed-point update of the field itself
- exact `alpha = 0` reduction check
- one promoted observable beyond static deflection:
  detector-line phase ramp relative to the `alpha = 0` baseline

## Architecture

This is not another gamma blend or memory tweak.

The field is updated from the beam itself:

1. propagate through the current complex field
2. extract layer densities and a layer-current proxy from the propagated beam
3. build a causal feedback field from those layer observables
4. feed that field back into the next propagation step

The feedback is iterated once per step. The zero-coupling baseline is exactly
the retained static grown field.

## Frozen result

Fast retained falsifier on the grown row:

- exact `alpha = 0` reduction survives by construction
- detector escape only shifts weakly: `1.000 -> 1.007 -> 1.015`
- detector-line phase slope stays essentially flat:
  `0.0000 -> 0.0001 -> 0.0002`
- phase span remains tiny: `0.000 -> 0.055 -> 0.111`
- feedback residual stays small: `0.000e+00 -> 1.710e-04 -> 3.420e-04`
- weak-field mass scaling collapses:
  - `F~M(alpha=0) = 0.254`
  - `F~M(alpha=0.5) = 0.256`

Single-seed sweep summary:

| `alpha` | escape | phase slope | phase span | residual |
| --- | ---: | ---: | ---: | ---: |
| `0.00` | `1.000` | `0.0000` | `0.000` | `0.000e+00` |
| `0.25` | `1.007` | `0.0001` | `0.055` | `1.710e-04` |
| `0.50` | `1.015` | `0.0002` | `0.111` | `3.420e-04` |

## Safe read

The narrow, honest statement is:

- the zero-coupling reduction is real
- the self-consistent feedback field is materially different from the earlier
  gamma-memory and transport-envelope probes
- but the causal observable remains essentially flat on the retained grown
  row
- weak-field mass scaling is nowhere near the retained `~1.0` class
- so this radical architecture does **not** open a new causal-field lane on
  the retained grown geometry row

## Guardrail note

This is a fast falsifier, not a full multi-seed closure.

That said, the signal is weak enough that the right verdict is still the
strict one: the beam-sourced self-consistent propagating-field attempt does
not yet survive the weak-field bar on the retained grown row.

## Branch verdict

Treat this as a bounded no-go.

The exact reduction passes, but the propagated feedback does not generate a
meaningful causal phase ramp or a near-linear weak-field class.
