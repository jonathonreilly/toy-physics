# Source-Driven Field Recovery Sweep

**Date:** 2026-04-05  
**Status:** bounded partial recovery on the exact 3D lattice

## Artifact chain

- [`scripts/source_driven_field_recovery_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/source_driven_field_recovery_sweep.py)
- [`logs/2026-04-05-source-driven-field-recovery-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-source-driven-field-recovery-sweep.txt)

## Question

Can the minimal source-driven local field architecture recover both `TOWARD`
and the near-Newtonian mass-scaling exponent by weakening the field
normalization or nudging the telegraph parameters?

This note is intentionally narrow:

- one exact 3D lattice family
- one source-driven field architecture
- one local scan over `c_field`, `damp`, and field normalization
- one score: preserve `TOWARD` and move `F~M` toward `1.00`

## Frozen result

The retained sweep scanned:

- `c_field = 0.40, 0.45, 0.50`
- `damp = 0.20, 0.35, 0.50`
- `target_field_max = 0.01, 0.02, 0.04`

The best row found was:

- `c_field = 0.50`
- `damp = 0.20`
- `target_field_max = 0.010`

Frozen readout for that best row:

- `TOWARD rows: 4/4`
- `dynamic F~M exponent: 0.98`
- `mean |dyn/inst| ratio: 1.804`

The dynamic centroid shifts were:

- `+4.932711e-03`
- `+9.799604e-03`
- `+1.933482e-02`
- `+3.760381e-02`

## Safe read

The strongest bounded statement is:

- weaker normalization and nearby telegraph parameters can recover the
  `TOWARD` sign on all tested source strengths
- the source-driven field can get very close to the linear mass-scaling class
  on this exact-lattice replay
- but the sweep does **not** yet produce a clean retained `F~M = 1.00`
  recovery

## Honest limitation

This is a partial recovery, not a full rescue.

- the source-driven architecture can be tuned into the near-Newtonian regime
- but the best retained exponent is `0.98`, not `1.00`
- that means the minimal self-generated field rule still falls just short of a
  full weak-field closure

## Branch verdict

Treat this as the strongest result so far for the minimal source-driven field
architecture:

- `TOWARD` survives
- near-linear scaling almost returns
- exact closure is still missing

That is useful progress, but not yet a complete source-generated field theory.
