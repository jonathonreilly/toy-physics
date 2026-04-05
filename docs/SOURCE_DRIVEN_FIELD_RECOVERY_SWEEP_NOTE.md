# Source-Driven Field Recovery Sweep

## Setup

This note records the weak-field recovery sweep for the existing source-driven field architecture on the exact 3D lattice.

Sweep artifact:
- [scripts/source_driven_field_recovery_sweep.py](/Users/jonreilly/Projects/Physics/scripts/source_driven_field_recovery_sweep.py)
- [logs/2026-04-05-source-driven-field-recovery-sweep.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-driven-field-recovery-sweep.txt)

The sweep scanned weak calibration targets against the same source strengths used by the minimal source-driven field probe.

## Result

Best recovery pocket:
- `c_field = 0.50`
- `damp = 0.20`
- `target_field_max = 0.010`
- `TOWARD rows: 4/4`
- dynamic `F~M` exponent: `0.98`

Representative dynamic centroid shifts in that pocket:
- `+4.932711e-03`
- `+9.799604e-03`
- `+1.933482e-02`
- `+3.760381e-02`

## Safe Read

The exact-lattice source-driven field architecture has a real weak-field recovery pocket.
When the calibrated dynamic field is kept small, it preserves `TOWARD` on all tested source strengths and comes close to linear mass scaling.
As the calibration grows, the exponent drifts away from `1.00`, so this is a calibration-sensitive partial recovery, not a full source-generated field theory.
