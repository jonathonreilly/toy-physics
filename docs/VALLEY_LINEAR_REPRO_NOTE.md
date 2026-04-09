# Valley-Linear Reproduction Note

**Date:** 2026-04-04  
**Status:** bounded reproduction entry point for the valley-linear action fork

This note exists so a skeptical reader can replay the valley-linear lane
without mistaking it for a flagship theorem or for the broader 3D kernel
story.

## Recommended entry point

Run:

[`scripts/reproduction_audit_harness.py`](/Users/jonreilly/Projects/Physics/scripts/reproduction_audit_harness.py)

Use:

- `--valley-linear` for the bounded same-family valley-linear replay
- `--include-gate` if you also want the retained canonical gate

## What the valley-linear replay checks

The replay keeps fixed:

- the 3D ordered dense lattice family
- the `1/L^2` kernel with `h^2` measure
- the slit geometry
- the detector readout
- the field shape

It changes only the action law:

- spent-delay
- valley-linear `S = L(1-f)`

The bounded comparison is intentionally small:

- Born
- `k=0`
- `F~M` exponent
- gravity sign at `z=3`
- post-peak distance tail

## What it does not certify

This replay does **not** prove:

- the valley-linear action is derived from the axioms
- convergence under refinement is closed
- the valley-linear branch replaces the spent-delay flagship
- the broader action-power story is finished

Those questions still need separate same-family companion artifacts.

## Why this note matters

The valley-linear fork now has three layers a skeptical reader can inspect:

1. the bounded comparison harness
2. the frozen log
3. the action note

That is enough to harden the branch without overselling it.
