# Source-Driven Field Recovery Sweep

**Date:** 2026-04-05  
**Status:** bounded weak-field recovery companion for the minimal source-driven field branch

## Artifact chain

- [`scripts/source_driven_field_recovery_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/source_driven_field_recovery_sweep.py)
- [`logs/2026-04-05-source-driven-field-recovery-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-driven-field-recovery-sweep.txt)
- [`scripts/source_driven_field_recovery_pocket.py`](/Users/jonreilly/Projects/Physics/scripts/source_driven_field_recovery_pocket.py)
- [`logs/2026-04-05-source-driven-field-recovery-pocket.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-driven-field-recovery-pocket.txt)

## Question

Does the same minimal source-driven local-field architecture recover the weak-field
mass-scaling lane when the generated field is kept genuinely small, rather than
calibrated to the stronger `max |f_dyn| = 0.08` row used in the first probe?

## Frozen result

Broad sweep on the exact 3D lattice (`h = 0.5`, `W = 6`, `L = 30`):

| target `max |f_dyn|` | `TOWARD` | dynamic `F~M` | largest dynamic shift |
| ---: | ---: | ---: | ---: |
| `0.001` | `4/4` | `0.997` | `+3.180396e-03` |
| `0.002` | `4/4` | `0.994` | `+6.314115e-03` |
| `0.005` | `4/4` | `0.985` | `+1.543423e-02` |
| `0.010` | `4/4` | `0.968` | `+2.969381e-02` |
| `0.020` | `4/4` | `0.934` | `+5.468048e-02` |
| `0.040` | `4/4` | `0.855` | `+9.073752e-02` |
| `0.080` | `4/4` | `0.642` | `+1.105259e-01` |

Conservative pocket replay:

- `c_field = 0.40`, `damp = 0.35`, `target = 0.010`
- zero-source dynamic shift: `+0.000000e+00`
- dynamic `F~M = 0.96`
- `4/4` dynamic rows stay `TOWARD`
- mean `|dyn/inst|` ratio: `1.304`

Dynamic pocket shifts:

- `+3.601586e-03`
- `+7.129776e-03`
- `+1.396546e-02`
- `+2.675231e-02`

## Safe read

The retained statement is now:

- the minimal source-driven field architecture has a real weak-field recovery pocket
- in that pocket, `TOWARD` survives and the dynamic mass exponent stays near linear
- the same architecture drifts away from linear mass scaling as the generated field grows

## Branch verdict

This is not a full positive for self-consistent field dynamics, but it is no longer
a flat no-go either.

- weak-field recovery exists on the exact 3D lattice
- stronger-calibration rows still fail the linear weak-field class
- the architecture is therefore calibration-sensitive, not dead
