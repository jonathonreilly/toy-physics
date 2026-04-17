# Minimal Source-Driven Field Probe

**Date:** 2026-04-05  
**Status:** bounded local-field-dynamics probe with exact reduction, preserved sign, and failed linear mass scaling at stronger calibration

## Artifact chain

- [`scripts/minimal_source_driven_field_probe.py`](/Users/jonreilly/Projects/Physics/scripts/minimal_source_driven_field_probe.py)
- [`logs/2026-04-05-minimal-source-driven-field-probe.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-minimal-source-driven-field-probe.txt)
- [`docs/SOURCE_DRIVEN_FIELD_RECOVERY_SWEEP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SOURCE_DRIVEN_FIELD_RECOVERY_SWEEP_NOTE.md)

## Question

Can the smallest stable local field-evolution rule, driven by a static source on
the 3D lattice, recover the weak-field gravity lane without relying on imposed
retarded scheduling?

This note is intentionally narrow:

- one family: exact 3D lattice
- one source: static source at fixed position
- one field rule: damped local telegraph-style field evolution
- one comparison: source-driven field vs instantaneous `1/r` field
- one reduction check: zero-source field returns to free propagation exactly

## Frozen result

The frozen probe uses:

- exact 3D lattice with `h = 0.5`, `W = 6`, `L = 30`
- fixed source position `z = 3`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | source-driven deflection | ratio | max `|f_dyn|` |
| --- | ---: | ---: | ---: | ---: |
| `0.0010` | `+2.702607e-03` | `+2.969381e-02` | `10.987` | `1.0e-02` |
| `0.0020` | `+5.393344e-03` | `+5.468048e-02` | `10.139` | `2.0e-02` |
| `0.0040` | `+1.073461e-02` | `+9.073752e-02` | `8.453` | `4.0e-02` |
| `0.0080` | `+2.122358e-02` | `+1.105259e-01` | `5.208` | `8.0e-02` |

Fitted exponents:

- instantaneous `F~M`: `0.99`
- source-driven `F~M`: `0.64`

## Safe read

The strongest bounded statement from this first probe alone is:

- the smallest source-driven local field rule does preserve the sign of
  attraction on this retained lattice replay
- the zero-source reduction check passes exactly
- but the source-driven field does **not** recover the linear weak-field mass
  scaling class

## Honest limitation

This first probe is therefore not a clean positive for self-consistent field dynamics.

- it is a partial survival:
  - `TOWARD` survives
  - exact zero-source reduction survives
- but it is also a clear failure of full weak-field recovery:
  - the mass exponent drops to `0.64`

## Branch verdict

Treat this note together with the recovery companion:

- at stronger calibration, the smallest stable source-driven field extension
  does not recover the retained weak-field lane in full
- the companion recovery sweep now shows a genuine weak-field pocket where the
  same architecture returns to near-linear `F~M`
- the right safe read is therefore calibration hierarchy, not blanket failure
