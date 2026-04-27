# Source-Resolved Transverse Propagating Green

**Date:** 2026-04-05  
**Status:** exact-lattice transverse-transport pocket, frozen on the proposed_retained compact family

## Artifact chain

- [`scripts/source_resolved_transverse_propagating_green.py`](/Users/jonreilly/Projects/Physics/scripts/source_resolved_transverse_propagating_green.py)

## Question

Does the exact-lattice Green pocket change in a meaningful way if the field
gets one minimal transverse-transport step, instead of only same-site memory?

This probe stays narrow:

- one compact exact lattice family at `h = 0.25`
- one source-resolved Green control
- one same-site-memory baseline
- one transverse-smoothing candidate
- one reduction check: zero source must recover free propagation exactly
- one observable: detector support localization relative to same-site memory

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- interior source placement `source_z = 2.0`
- fixed cross5 source cluster with `5` in-bounds nodes
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`, `eps = 0.5`
- same-site memory `mix = 0.9`
- transverse smoothing `mix = 0.25`

Reduction check:

- zero-source same-site shift: `+0.000000e+00`
- zero-source transverse shift: `+0.000000e+00`

Frozen readout:

| `s` | instantaneous deflection | same-site deflection | transverse deflection | transverse/same | transverse - same |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.0010` | `+1.438000e-03` | `+1.873000e-03` | `+1.904000e-03` | `1.017` | `+3.100000e-05` |
| `0.0020` | `+2.878000e-03` | `+3.746000e-03` | `+3.808000e-03` | `1.017` | `+6.200000e-05` |
| `0.0040` | `+5.756000e-03` | `+7.492000e-03` | `+7.616000e-03` | `1.017` | `+1.240000e-04` |
| `0.0080` | `+1.151000e-02` | `+1.498000e-02` | `+1.523000e-02` | `1.017` | `+2.500000e-04` |

Fitted exponents:

- instantaneous `F~M`: `1.00`
- same-site memory `F~M`: `1.00`
- transverse `F~M`: `1.00`

## Safe read

The strongest bounded statement is:

- exact zero-source reduction survives
- the transverse-smoothed field keeps the weak-field `TOWARD` sign on the
  compact exact lattice
- the mass-scaling class stays essentially linear
- the transverse transport only nudges the detector centroid relative to the
  same-site memory control at the few-per-mille level

## Honest limitation

This is still a minimal pocket, not a full propagating field theory.

- the transverse step is one local smoothing update, not a full dynamical wave
  equation
- the source cluster is now interior, so this is a cleaner exact-lattice test
  than the boundary-clipped pocket
- the observable difference between same-site and transverse transport is
  small, so the result is best read as a controlled perturbation rather than a
  dramatic architectural shift

## Branch verdict

Treat this as a real bounded positive:

- exact zero-source reduction survives
- weak-field sign survives
- `F~M` stays at `1.00`
- transverse transport is detectable, but only as a small correction to the
  same-site-memory control
- the generated-family bottleneck is therefore not fixed by this minimal step
