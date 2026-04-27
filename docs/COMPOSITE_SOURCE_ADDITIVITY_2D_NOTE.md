# Composite-Source Additivity Cross-Family Note

**Date:** 2026-04-04  
**Status:** bounded second-family additivity probe on the proposed_retained 2D ordered lattice

## Artifact chain

- Script: [`scripts/composite_source_additivity_2d_cross_family.py`](/Users/jonreilly/Projects/Physics/scripts/composite_source_additivity_2d_cross_family.py)
- Log: [`logs/2026-04-04-composite-source-additivity-2d-cross-family.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-composite-source-additivity-2d-cross-family.txt)

This is the smallest real cross-family check for the valley-linear additivity
story:

- family: 2D ordered lattice
- `h = 0.5`
- `W = 20`
- `L = 40`
- slit geometry and detector readout follow the retained 2D continuum lane

## What was tested

The harness compares the same two bounded statements as the 3D additivity
probe, but on a different retained family:

1. **Same-site source-strength additivity**
   - compare `delta(s1 + s2)` against `delta(s1) + delta(s2)` for one source location

2. **Disjoint-source field additivity**
   - compare `delta(field_A + field_B)` against `delta(field_A) + delta(field_B)` for two separated sources

This remains a test-particle response probe only. It does **not** derive
persistent-pattern inertial mass.

## Frozen replay

### Valley-linear

Valley-linear stays additive to printed precision on the 2D ordered-lattice
family.

Same-site relative error:

- `0.04%` for `(s1, s2) = (1e-5, 2e-5)`
- `0.04%` for `(1e-5, 5e-5)`
- `0.08%` for `(2e-5, 5e-5)`

Disjoint-source relative error:

- `0.00%` for `y = (3, 7)`
- `0.01%` for `y = (4, 9)`

### Spent-delay

Spent-delay still deviates strongly on the same second family.

Same-site relative error:

- `28.99%` for `(1e-5, 2e-5)`
- `25.26%` for `(1e-5, 5e-5)`
- `28.65%` for `(2e-5, 5e-5)`

Disjoint-source relative error:

- `27.01%` for `y = (3, 7)`
- `27.45%` for `y = (4, 9)`

## Safe read

The bounded cross-family statement is:

- on the retained 2D ordered-lattice family, valley-linear remains
  source-additive to within printed precision
- spent-delay does not

This is the right kind of second-family support for the Newton-selection lane:

- it suggests the additivity story is not a one-off artifact of the fixed 3D family
- it still only supports a test-particle response law
- it still does **not** close persistent-pattern / inertial-mass closure

## Relation to the main derivation lane

This note extends the bounded additivity story in
[COMPOSITE_SOURCE_ADDITIVITY_NOTE.md](/Users/jonreilly/Projects/Physics/docs/COMPOSITE_SOURCE_ADDITIVITY_NOTE.md):

- 3D retained family: additivity frozen
- 2D ordered family: additivity still frozen
- persistent-pattern inertia: still open

That is the cleanest current interpretation:

- the valley-linear additivity lane now has a second family behind it
- the open step is narrower, not wider
- the codebase still does not justify “Newton derived from first principles”

## Best next move

The next step should be one of:

- a smallest viable persistent-pattern or quasi-persistent inertial-response experiment
- a third-family additivity cross-check if a cheap reusable family already exists
- a bounded note saying the additivity lane is now supported on two families
  but still not a persistent-mass theorem
