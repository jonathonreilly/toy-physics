# Source-Driven Field Recovery h=0.25 Pocket Note

**Date:** 2026-04-05  
**Status:** smallest serious h=0.25 refinement falsifier for the source-driven field branch

## Artifact chain

- [`scripts/source_driven_field_recovery_h025_pocket.py`](/Users/jonreilly/Projects/Physics/scripts/source_driven_field_recovery_h025_pocket.py)
- [`logs/2026-04-05-source-driven-field-recovery-h025-pocket.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-driven-field-recovery-h025-pocket.txt)

## Question

Does the retained exact-lattice weak-field recovery pocket survive one refinement step to `h = 0.25` when we keep the test small enough to stay practical?

This note is intentionally narrow:

- one exact 3D lattice family
- one conservative pocket calibration
- one transfer check against the exact-lattice weak-field lane

## Frozen result

The smallest serious `h = 0.25` test uses:

- `h = 0.25`
- `W = 3`
- `L = 12`
- `c = 0.40`
- `damp = 0.35`
- `target_max = 0.010`

Reduction check:

- zero-source dynamic shift: `+0.000000e+00`

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

The exact `h = 0.25` refinement check keeps:

- exact zero-source reduction
- all-TOWARD sign
- near-linear dynamic mass scaling

But it fails the amplitude-transfer gate badly:

- mean `|dynamic / instantaneous| = 0.055`

So the transfer is not a full positive. It is a clean bounded falsifier for the claim that the exact-lattice source-driven recovery pocket transfers to this refinement family with useful amplitude.

## Branch verdict

This is the smallest serious refinement test, and it says:

- the weak-field pocket does not survive refinement in a strong enough way to count as a transfer
- sign and exponent survive
- amplitude collapses too far below the instantaneous lane
- the exact-lattice source-driven field branch remains calibration-sensitive rather than genuinely refinement-stable
