# Composite-Source Additivity Note

**Date:** 2026-04-04  
**Status:** bounded test-particle additivity probe on the proposed_retained 3D ordered-lattice family

## Artifact chain

- Script: [`scripts/composite_source_additivity_harness.py`](/Users/jonreilly/Projects/Physics/scripts/composite_source_additivity_harness.py)
- Log: [`logs/2026-04-04-composite-source-additivity-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-composite-source-additivity-harness.txt)

This is a narrow probe on one fixed family:

- 3D ordered dense lattice
- `h = 0.5`, `W = 8`, `L = 12`
- point-packet test particle
- source positions on the same retained geometry
- action compared on the same family: `valley-linear` and `spent-delay`

## What was tested

The harness separates two bounded statements:

1. **Same-site source-strength additivity**
   - compare `delta(s1 + s2)` against `delta(s1) + delta(s2)` for one source location

2. **Disjoint-source field additivity**
   - compare `delta(field_A + field_B)` against `delta(field_A) + delta(field_B)` for two separated sources

These are test-particle response statements only. They do **not** by themselves
define or derive a persistent-pattern inertial mass.

## Frozen replay

### Valley-linear

Valley-linear is additive to machine precision on this weak-field test-particle family.

Same-site relative error:

- `0.00%` for `(s1, s2) = (1e-5, 2e-5)`
- `0.00%` for `(1e-5, 5e-5)`
- `0.00%` for `(2e-5, 5e-5)`

Disjoint-source relative error:

- `0.00%` for `z = (4, 6)`
- `0.00%` for `z = (3, 6)`

### Spent-delay

Spent-delay deviates strongly from additivity on the same family.

Same-site relative error:

- `28.25%` for `(1e-5, 2e-5)`
- `24.29%` for `(1e-5, 5e-5)`
- `27.50%` for `(2e-5, 5e-5)`

Disjoint-source relative error:

- `28.79%` for `z = (4, 6)`
- `28.57%` for `z = (3, 6)`

## Safe read

The strongest retained statement is:

- on the fixed weak-field 3D ordered-lattice family, valley-linear behaves as a
  genuinely additive source-response law for a test particle
- on that same family, spent-delay does not

This strengthens the Newton-selection lane, but only in a bounded way:

- it supports the idea that source strength and response belong to the same
  additive linear law on the valley-linear test-particle family
- it does **not** yet derive persistent-pattern inertial mass
- it does **not** close the one-parameter-mass step beyond the tested family

## Relation to the Newton derivation

This note sharpens Principle 3 in
[NEWTON_DERIVATION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/NEWTON_DERIVATION_NOTE.md):

- stronger than before:
  - valley-linear now has a frozen additivity replay, not just a verbal
    composition argument
  - a second retained-family cross-check now exists:
    `docs/COMPOSITE_SOURCE_ADDITIVITY_2D_NOTE.md` (downstream consumer in same lane; cross-reference only — not a one-hop dep of this note)
- still open:
  - whether a persistent localized pattern has an effective inertial response
  - whether that inertial response is governed by the same parameter that
    sources the field

## Best next move

The next step should not be another same-family test-particle replay.

It should be one of:

- the smallest viable persistent-pattern / inertial-response experiment
- a beyond-fixed-family additivity cross-check
- a bounded note saying clearly whether the additivity lane survives outside
  this retained family
