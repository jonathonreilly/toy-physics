# Source-Driven Field Recovery H=0.25 Pocket

**Date:** 2026-04-05  
**Status:** bounded refinement-positive for the source-driven field branch

## Artifact chain

- [`scripts/source_driven_field_recovery_h025_pocket.py`](/Users/jonreilly/Projects/Physics/scripts/source_driven_field_recovery_h025_pocket.py)
- [`logs/2026-04-05-source-driven-field-recovery-h025-pocket.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-driven-field-recovery-h025-pocket.txt)

## Question

Does the weak-field recovery pocket survive one refinement step to `h = 0.25`
while keeping exact zero-source reduction and near-linear mass scaling?

This note is intentionally narrow:

- one exact lattice family
- one source-driven local-field rule
- one refinement step to `h = 0.25`
- one comparison against the instantaneous `1/r` field
- one reduction check: zero source should recover free propagation exactly

## Frozen result

The frozen pocket uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 12`
- `c = 0.40`, `damp = 0.35`, `target_max = 0.010`

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`
- calibration gain: `1.451422e-02`

Frozen readout:

| `s` | instantaneous deflection | dynamic deflection | ratio | max `|f_dyn|` |
| --- | ---: | ---: | ---: | ---: |
| `0.0010` | `+2.052833e-03` | `+1.110107e-04` | `0.054` | `1.250000e-03` |
| `0.0020` | `+4.090292e-03` | `+2.218763e-04` | `0.054` | `2.500000e-03` |
| `0.0040` | `+8.119464e-03` | `+4.431713e-04` | `0.055` | `5.000000e-03` |
| `0.0080` | `+1.599854e-02` | `+8.840129e-04` | `0.055` | `1.000000e-02` |

Fitted exponents:

- instantaneous `F~M`: `0.99`
- dynamic `F~M`: `1.00`

## Safe read

The strongest bounded statement is:

- the refinement step preserves exact zero-source reduction
- the dynamic pocket keeps all rows `TOWARD`
- the dynamic mass exponent stays essentially linear

## Honest limitation

The pocket is very weak in amplitude.

- mean `|dynamic / instantaneous| = 0.055`
- so this is a refinement-positive survival, not a self-consistent field upgrade

## Branch verdict

Treat this as a bounded refinement-positive:

- exact reduction survives
- sign survives
- linear mass scaling survives
- amplitude is too small for a strong-field rescue
