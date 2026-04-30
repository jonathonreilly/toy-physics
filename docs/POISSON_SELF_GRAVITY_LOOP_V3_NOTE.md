# Poisson Self-Gravity Loop V3 Note

**Date:** 2026-04-05  
**Status:** bounded - bounded or caveated result note

## Artifact chain

- [`scripts/poisson_self_gravity_loop_v3.py`](/Users/jonreilly/Projects/Physics/scripts/poisson_self_gravity_loop_v3.py)
- [`logs/2026-04-05-poisson-self-gravity-loop-v3.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-poisson-self-gravity-loop-v3.txt)

## What this harness checks

This is the stricter follow-up to the earlier Poisson self-gravity controls:

- exact `epsilon = 0` identity reduction on the same loop machinery
- matched-null comparison against the same update pipeline with zero coupling
- promoted observables stronger than raw escape:
  - matched-null detector centroid shift
  - detector-line phase-ramp slope/span relative to the null baseline
- per-step Born on the frozen terminal field snapshot
- end-to-end Born through the full nonlinear loop, where feasible

## Exact-lattice setup

The retained run uses:

- exact lattice at `h = 0.25`
- `W = 3`, `L = 6`
- reduced exact causal stencil for tractability in Python
- one interior 5-node source patch
- screened Poisson-like kernel `exp(-mu r) / (r + eps)`
- source strengths `s = 0.002, 0.004, 0.008`
- backreaction couplings `epsilon = 0.0, 0.05, 0.20, 0.50`

## Reduction check

The exact null behaves exactly as required:

- zero-`epsilon` centroid shift: `+0.000000e+00`
- zero-`epsilon` escape ratio: `1.000000`
- zero-`epsilon` phase slope: `+0.0000e+00`
- zero-`epsilon` phase span: `+0.0000e+00`
- zero-`epsilon` convergence: `True`

That is the key identity-control result.

## Sweep summary

Frozen sweep behavior:

| `epsilon` | mean matched-null centroid delta | mean phase slope | mean phase span | mean escape | TOWARD rows | converged |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `0.00` | `+0.000000e+00` | `+0.0000e+00` | `+0.0000e+00` | `1.000` | `0/3` | `3/3` |
| `0.05` | `+2.186632e-03` | `-2.2198e-03` | `+1.5585e-02` | `1.010` | `3/3` | `0/3` |
| `0.20` | `+8.767442e-03` | `-8.8945e-03` | `+6.2503e-02` | `1.039` | `3/3` | `0/3` |
| `0.50` | `+2.203560e-02` | `-2.2310e-02` | `+1.5690e-01` | `1.102` | `3/3` | `0/3` |

## Born audit

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
- coupled convergence: `False` after `6` iterations

## Safe read

The strict retained read is:

- the exact `epsilon = 0` reduction survives exactly
- the matched-null control survives exactly
- the promoted observables do move in the expected direction at nonzero coupling
- but the effect is still small
- the loop does not converge for the nonzero-coupling rows under the strict tolerance
- step-local Born survives on the frozen field snapshot
- end-to-end Born is no longer machine-clean through the full loop

## Branch verdict

This stays a **tiny control**, not a new Poisson-like self-gravity lane.

The strongest retained statement is:

- exact null identity is solid
- a small positive centroid / phase-ramp shift appears under backreaction
- but the shift is not large enough, and the nonlinear loop is not converged enough, to promote this to a new exact-lattice self-gravity mechanism

## Limit diagnosis

The limit is informative rather than mysterious:

- exact `epsilon = 0` identity holds exactly
- the matched-null control also holds exactly
- the promoted observables move in the right direction for nonzero coupling
- the loop remains numerically unstable enough that end-to-end Born drifts away from machine precision
- source-strength retuning does not rescue the scaling into a larger effect

That points to a genuine but weak backreaction perturbation on this reduced family, not a self-gravity mechanism waiting to be uncovered. The strongest read is that this family is a control surface with a small physical signal, not a latent lane with a missed stronger effect.

## Fastest falsifier for future versions

If a later version can simultaneously achieve:

- exact `epsilon = 0` identity
- converged nonlinear loop at nonzero coupling
- step-local Born near machine precision
- and a matched-null phase-ramp or signed-moment effect that is materially larger than this tiny control

then the lane may become a real self-gravity candidate.

Until then, this remains a bounded control.
