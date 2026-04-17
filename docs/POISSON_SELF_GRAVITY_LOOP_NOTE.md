# Poisson Self-Gravity Loop Note

**Date:** 2026-04-05  
**Status:** bounded self-consistent control on a small exact-lattice family, not a backreaction breakthrough

## Artifact chain

- [`scripts/poisson_self_gravity_loop.py`](/Users/jonreilly/Projects/Physics/scripts/poisson_self_gravity_loop.py)
- [`logs/2026-04-05-poisson-self-gravity-loop.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-poisson-self-gravity-loop.txt)

## Question

Can a narrow exact-lattice loop, where amplitude density sources a screened
Poisson-like field between propagation steps, preserve the weak-field gravity
lane while staying Born-linear on the frozen field snapshot?

This harness is intentionally narrow:

- one exact 3D lattice family at `h = 0.25`
- one fixed interior source patch
- one screened Poisson-like kernel
- one fixed-point loop over the field only
- one exact `epsilon = 0` reduction check
- one Born check on the final frozen field snapshot
- one weak-field sign / mass-law read across small source strengths

## What Born means here

The outer loop is nonlinear because the field is sourced from the propagated
amplitude density.

Born is therefore checked on the **frozen field snapshot at the terminal
iterate**, not on the outer fixed-point map itself.

That is the strict meaning used in the log and in this note.

## Frozen result

The frozen run uses:

- exact lattice with `h = 0.25`, `W = 3`, `L = 6`
- a 5-node interior source patch centered at `z = 2.5`
- screened kernel `exp(-mu r) / (r + eps)` with `mu = 0.08`
- backreaction couplings `epsilon = 0.0, 0.01, 0.05, 0.10, 0.20, 0.50`
- source strengths `s = 0.001, 0.002, 0.004, 0.008`
- one calibrated field gain for the whole sweep

Reduction check:

- zero-`epsilon` centroid shift: `+0.000000e+00`
- zero-`epsilon` escape ratio: `1.000000`
- zero-`epsilon` loop converged exactly

Frozen sweep summary:

| `epsilon` | weak-field sign | mean loop/inst | mean escape | Born mean/max | converged |
| --- | --- | ---: | ---: | ---: | ---: |
| `0.00` | `TOWARD` | `n/a` | `1.000` | `1.28e-15 / 1.28e-15` | `4/4` |
| `0.01` | `TOWARD` | `1.010` | `1.002` | `8.18e-16 / 1.70e-15` | `0/4` |
| `0.05` | `TOWARD` | `1.010` | `1.008` | `7.51e-16 / 1.07e-15` | `0/4` |
| `0.10` | `TOWARD` | `1.010` | `1.016` | `1.04e-15 / 2.11e-15` | `0/4` |
| `0.20` | `TOWARD` | `1.010` | `1.033` | `1.21e-15 / 2.11e-15` | `0/4` |
| `0.50` | `TOWARD` | `1.010` | `1.087` | `4.82e-16 / 1.07e-15` | `0/4` |

Weak-field mass-law read:

- instantaneous field exponent: about `1.00`
- self-consistent loop exponent: about `1.00`

## Safe read

The strongest bounded statement is:

- the exact `epsilon = 0` reduction survives exactly
- the frozen field snapshot stays Born-linear to machine precision
- the weak-field sign survives on all tested nonzero couplings
- the weak-field mass-law read stays essentially linear on the terminal iterate

## Honest limitation

This is **not** a self-gravity breakthrough.

- the outer loop does not converge under the strict `1e-10` tolerance for
  nonzero `epsilon`
- the loop effect is tiny, with `loop/inst ≈ 1.010`
- escape rises slightly rather than producing a qualitatively new trapping
  regime
- the retained observable is therefore a weak control, not a new Poisson-like
  backreaction phase

## Branch verdict

Treat this as a bounded positive control, not a new backreaction lane.

- exact zero-`epsilon` reduction survives
- the terminal frozen field remains Born-linear
- weak-field sign survives
- weak-field mass law remains essentially Newtonian
- but the self-consistent outer loop is too small and too nonconvergent to
  claim a new Poisson-like gravitational mechanism

## Fastest Falsifier

If a future version of this harness shows either:

- loss of the exact `epsilon = 0` reduction
- Born drift on the frozen terminal field snapshot
- weak-field sign flip
- or a non-Newtonian mass-law exponent emerging without a stable converged
  fixed point

then the present loop should remain only a control, not a new physics lane.
