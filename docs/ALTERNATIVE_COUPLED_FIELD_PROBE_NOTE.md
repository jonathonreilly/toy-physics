# Alternative Coupled-Field Probe

**Date:** 2026-04-05  
**Status:** bounded positive for an edge-carried minimal coupled-field architecture on the exact 3D lattice

## Artifact chain

- [`scripts/alternative_coupled_field_probe.py`](/Users/jonreilly/Projects/Physics/scripts/alternative_coupled_field_probe.py)
- [`logs/2026-04-05-alternative-coupled-field-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-alternative-coupled-field-probe.txt)

## Question

Can an alternative minimal coupled-field architecture, distinct from the
telegraph-style source-driven field, preserve exact zero-source reduction while
still keeping the weak-field TOWARD sign and near-linear mass scaling?

This note is intentionally narrow:

- one family: exact 3D lattice
- one field rule: edge-carried forward transport
- one comparison: edge-carried field vs instantaneous `1/r` field
- one reduction check: zero-source field should recover free propagation

## Frozen result

The frozen probe uses:

- exact 3D lattice with `h = 0.5`, `W = 6`, `L = 30`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- edge-transport calibration gain `1.427390e-46`
- transport decay `0.72`
- transport exponent `0.85`

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | edge-carried deflection | ratio | max `|f_edge|` |
| --- | ---: | ---: | ---: | ---: |
| `0.0010` | `+2.702607e-03` | `+3.021738e-05` | `0.011` | `1.0e-02` |
| `0.0020` | `+5.393344e-03` | `+5.996921e-05` | `0.011` | `2.0e-02` |
| `0.0040` | `+1.073461e-02` | `+1.182387e-04` | `0.011` | `4.0e-02` |
| `0.0080` | `+2.122358e-02` | `+2.311300e-04` | `0.011` | `8.0e-02` |

Fitted exponents:

- instantaneous `F~M`: `0.99`
- edge-carried `F~M`: `0.98`

## Safe read

The strongest bounded statement is:

- the alternative edge-carried architecture preserves exact zero-source
  recovery
- it keeps the weak-field TOWARD sign on the retained family
- it stays essentially linear in source strength

## Honest limitation

The edge-carried field is much weaker than the instantaneous comparator on this
exact lattice replay.

- the retained ratio is only about `1.1%` of the instantaneous deflection
- this does not yet give a stronger self-consistent field sector
- it is still useful because it shows a distinct architecture can preserve the
  weak-field lane without using the telegraph-style recurrence

## Branch verdict

Treat this as a real bounded positive:

- it is not the full moonshot field theory
- but it is a distinct coupled-field architecture that survives the strict
  reduction check and preserves the weak-field sign / mass-scaling readout
