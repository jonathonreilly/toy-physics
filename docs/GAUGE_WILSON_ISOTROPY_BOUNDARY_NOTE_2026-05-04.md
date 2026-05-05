# Gauge Wilson Isotropy Boundary Note

**Date:** 2026-05-04
**Type:** open_gate
**Claim scope:** boundary record for the accepted Wilson gauge-action
isotropy surface: two proposed derivation routes do not produce a new
spatial/temporal gauge-coupling split, and the accepted isotropic Wilson
surface remains a scoped framework surface rather than a new repo-wide axiom.
**Status authority:** independent audit lane only. This note records an open
gate and narrow negative checks; it does not supply an audit verdict.
**Primary runner:** `scripts/frontier_gauge_wilson_isotropy_boundary_2026_05_04.py`

## Question

PR #528 asked whether the accepted Wilson gauge action should be changed or
re-described by a derived anisotropy. The repo governance constraint is that
review-loop must not add new axioms, new foundational premises, or new theory
language without explicit user approval.

Within that constraint, what can be salvaged from the isotropy discussion?

## Answer

Two narrow boundary checks are worth keeping:

1. The `Cl(3)` pseudoscalar squares to `-I` in the Pauli irrep, but it is
   central in odd-dimensional `Cl(3)` and therefore does not anticommute with
   the three spatial generators. It cannot by itself be used as a fourth
   Clifford generator forcing a new `Cl(3,1)` gauge-coupling ratio.
2. The standard staggered-eta product around all six plaquette orientations
   has the same sign. This check does not generate a spatial/temporal
   plaquette-weight split from an isotropic input lattice.

These checks support a conservative boundary statement:

> the accepted isotropic Wilson surface remains the scoped Wilson surface
> already used by the repo; PR #528 does not derive a new anisotropic gauge
> action and does not justify adding an anisotropy axiom.

## Relation To Existing Authority

[`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
states the accepted Wilson nearest-neighbor plaquette grammar with one common
coefficient across the six plaquette orientations. This note does not promote
that statement or re-axiomatize it. It records that two candidate mechanisms
from PR #528 do not force a different action surface.

[`GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md`](GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
also remains in force: response-ratio or scalar-bridge factors cannot be
reused as an exact constant action-coupling lift.

## Runner Result

Command:

```bash
python3 scripts/frontier_gauge_wilson_isotropy_boundary_2026_05_04.py
```

Expected summary:

```text
SUMMARY: PASS=19 FAIL=0
```

The runner verifies:

- the Pauli-irrep `Cl(3)` anticommutation relations;
- the `Cl(3)` pseudoscalar has square `-I`;
- the pseudoscalar commutes with each `Cl(3)` generator and so is not a
  standalone fourth anticommuting generator;
- all staggered eta-products around `xy`, `xz`, `xt`, `yz`, `yt`, and `zt`
  plaquettes equal `-1` on the tested parity cube.

## What This Does Not Close

This note does not prove a global no-go for every possible spacetime-emergence
route. A future retained-grade theorem could still derive a metric ratio or a
specific anisotropic Wilson action from an explicitly approved and
repo-conventional primitive.

Until such a theorem is reviewed and audited, the live boundary is:

- no repo-wide anisotropy axiom has been added;
- no new gauge-action language has been introduced;
- isotropic Wilson remains the scoped accepted surface already present in the
  plaquette stack;
- the analytic plaquette value at `beta = 6` remains open.
