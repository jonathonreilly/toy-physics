# Lattice NN High-Precision Note

**Date:** 2026-04-03  
**Status:** attempted raw high-precision continuation, but `h = 0.125` was not
completed in a practical runtime window

This note records the narrow high-precision follow-up to the raw nearest-
neighbor lattice refinement result.

## Goal

The question was intentionally narrow:

- does the raw nearest-neighbor lattice refinement trend extend one more step
  to `h = 0.125`
- without any rescaling trick
- while keeping the same raw kernel and the same observables

## Setup

The high-precision continuation re-used the raw nearest-neighbor family from:

- [`scripts/lattice_nn_continuum.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_continuum.py)

The continuation script was:

- [`scripts/lattice_nn_high_precision.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_nn_high_precision.py)

The run was executed with arbitrary-precision arithmetic in a temporary local
virtual environment.

## Outcome

The `h = 0.125` continuation did **not** complete in a practical runtime window.

What this means:

- the raw high-precision kernel is computationally expensive at this spacing
- the run did not fail because of a known physics inconsistency in the code path
- but it also did **not** produce a retained numerical result for
  `h = 0.125`

So the current evidence is:

- `h = 0.25` remains the last Born-clean raw refinement point
- the `h = 0.125` high-precision continuation is still open
- the blocking issue is runtime cost, not a promoted physics conclusion

## Safe conclusion

The correct project-level wording is:

- the raw nearest-neighbor lattice shows a Born-clean refinement trend through
  `h = 0.25`
- the first high-precision `h = 0.125` continuation was attempted, but it was
  not practical to complete in the current raw implementation
- therefore there is still no canonical `h = 0.125` Born-clean extension to
  promote

## Next step

If the project wants to pursue this further, the next move is not more broad
parameter fishing. It is one of:

- a faster exact-arithmetic implementation
- a more selective observable check at `h = 0.125`
- or a different discretization measure that preserves Born without periodic
  rescaling

Until then, treat the nearest-neighbor result as a strong finite-resolution
refinement law, not a completed continuum theorem.
