# Main-Branch Derivation Atlas Pointer

**Date:** 2026-04-15  
**Purpose:** local front-door pointer to the canonical derivation toolkit on
`main`

## Canonical atlas

The canonical derivation atlas lives on `main` at:

`docs/publication/ci3_z3/DERIVATION_ATLAS.md`

On this branch, use that object as the reusable-toolbox front door. The atlas
is not a manuscript claim surface. It is the index of:

- what has already been derived
- what the safe statement is
- what the import class is
- which note and runner are canonical

## Use rule

When a lane reuses an atlas row, carry forward:

1. the row's safe statement
2. the row's status / import class
3. the row's authority note
4. the row's primary runner

If a row is not marked `zero-input structural` or `axiom-dependent support`,
do not silently promote it into a pure internal theorem.

## Current neutrino-operator lane reuse

The exact one-generation Majorana-operator classification on this branch uses
the following atlas rows from `main`:

- `Framework axiom`
- `Anomaly-forced time`
- `Native weak algebra`
- `Structural SU(3) closure`
- `One-generation matter closure`

It does **not** yet require the `Three-generation matter structure` row,
because the exact result currently stops at the one-generation quadratic
operator-classification level.

## Local workflow

Use the atlas first, then the lane note, then the runner:

1. inspect the canonical atlas row on `main`
2. confirm the row's safe claim boundary and import class
3. open the cited authority note / runner
4. only then extend the lane

For the current neutrino lane:

- lane note: [NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md](./NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md)
- runner: [frontier_neutrino_majorana_operator.py](../scripts/frontier_neutrino_majorana_operator.py)

## Command

```bash
git show main:docs/publication/ci3_z3/DERIVATION_ATLAS.md
```
