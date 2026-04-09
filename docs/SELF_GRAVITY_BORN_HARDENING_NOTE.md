# Self-Gravity Born Hardening Note

**Date:** 2026-04-06  
**Status:** bounded no-go on the exact-lattice Poisson-like backreaction lane under strict reduction/Born controls

## Artifact Chain

- [`scripts/poisson_self_gravity_loop_v3.py`](/Users/jonreilly/Projects/Physics/scripts/poisson_self_gravity_loop_v3.py)
- [`logs/2026-04-06-self-gravity-born-hardening.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-06-self-gravity-born-hardening.txt)

## What Was Checked

This hardening pass stayed narrow and review-safe:

- exact `epsilon = 0` reduction on the same loop machinery
- matched-null comparison against the same update pipeline
- snapshot Born on the frozen field snapshot
- end-to-end Born through the full nonlinear loop

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
- zero-epsilon phase R^2: `0.000`
- zero-epsilon converged: `True`
- zero-epsilon iters/resid: `0 / 0.000e+00`

That is the strongest retained identity result. It is a null-control check, not
evidence for a retained backreaction law.

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

The lane does not support a review-safe retained backreaction claim.

- exact `epsilon = 0` identity survives cleanly
- the snapshot Born check is machine-clean only on the frozen field snapshot
- the full-loop Born audit is not machine-clean
- the nonlinear rows do not converge under the strict tolerance
- nonzero coupling remains a tiny control surface, not a retained mechanism

## Conclusion

This stays a **hardened bounded no-go**. The exact zero-coupling reduction is
explicit, the snapshot Born check is explicit, and the end-to-end Born check is
explicit, but together they still do not justify promoting the lane to a
retained self-gravity/backreaction mechanism.
