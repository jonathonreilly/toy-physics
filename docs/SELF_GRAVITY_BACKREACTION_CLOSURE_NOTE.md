# Self-Gravity Backreaction Closure Note

**Date:** 2026-04-06  
**Status:** bounded no-go on the exact-lattice Poisson-like backreaction lane under strict reduction/Born controls

## Artifact Chain

- [`scripts/poisson_self_gravity_loop_v3.py`](/Users/jonreilly/Projects/Physics/scripts/poisson_self_gravity_loop_v3.py)
- [`logs/2026-04-06-self-gravity-backreaction-closure.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-self-gravity-backreaction-closure.txt)

## What Was Checked

This rerun kept the lane narrow and review-safe:

- exact `epsilon = 0` reduction on the same loop machinery
- matched-null comparison against the same update pipeline
- detector centroid shift and detector-line phase-ramp observables
- snapshot Born and end-to-end Born on the retained audit row

## Retained Exact-Lattice Setup

- `h = 0.25`
- `W = 3`, `L = 6`
- launch node `[312]`
- source patch nodes `[5322, 5347, 5297, 5323, 5321]`
- Born triplet `[287, 312, 337]`
- kernel `exp(-mu r)/(r+eps)` with `mu = 0.08`, `eps = 0.50`
- source strengths `(0.002, 0.004, 0.008)`
- backreaction couplings `(0.0, 0.05, 0.2, 0.5)`

## Exact Reduction

The null control is exact:

- zero-epsilon centroid shift: `+0.000000e+00`
- zero-epsilon escape ratio: `1.000000`
- zero-epsilon phase slope: `+0.0000e+00`
- zero-epsilon phase span: `+0.0000e+00`
- zero-epsilon converged: `True`
- zero-epsilon iters/resid: `0 / 0.000e+00`

That is the strongest retained identity result. It certifies only the null
control, not a promoted self-gravity mechanism.

## Born Audit

Representative retained Born row:

- `epsilon = 0.05`
- `source_strength = 0.0040`

Results:

- step-local Born: `1.546e-16`
- end-to-end Born: `4.911e-06`
- coupled centroid: `+2.215286e-16`
- null centroid: `+6.441020e-17`
- coupled escape: `8.175319`
- null escape: `8.091428`
- coupled converged: `False` after `6` iterations

## Closed Read

The lane does not support a review-safe retained backreaction claim:

- the exact `epsilon = 0` identity survives cleanly
- the step-local Born check is machine-clean, but only on the frozen snapshot
- the nonlinear loop does not converge under the strict tolerance
- the full-loop Born audit is not machine-clean
- the nonzero rows only show a tiny control surface, not a retained law

The strongest defensible conclusion is therefore:

- this is a tiny control surface, not a retained self-gravity mechanism
- the review-safe endpoint is a hardened bounded no-go

## Next Step

Do not promote this lane further unless a later version can simultaneously deliver:

- exact `epsilon = 0` identity
- converged nonlinear loop at nonzero coupling
- step-local Born near machine precision
- end-to-end Born that remains review-clean
