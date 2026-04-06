# Self-Gravity Failure Diagnosis

**Date:** 2026-04-06  
**Status:** diagnosed closure of the exact-lattice Poisson-like backreaction lane

## Artifact chain

- [`docs/POISSON_SELF_GRAVITY_LOOP_V3_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/POISSON_SELF_GRAVITY_LOOP_V3_NOTE.md)
- [`docs/SELF_GRAVITY_BACKREACTION_CLOSURE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/SELF_GRAVITY_BACKREACTION_CLOSURE_NOTE.md)
- [`scripts/poisson_self_gravity_loop_v3.py`](/Users/jonreilly/Projects/Physics/scripts/poisson_self_gravity_loop_v3.py)

## Question

Why does the exact-lattice Poisson-like self-gravity / backreaction lane fail the
review bar?

The short answer is not “because nothing happens.” A small effect does happen.
The failure is that the effect stays too weak, too unstable, and too dependent
on the nonlinear loop to survive as a retained mechanism.

## What survives

The lane does retain three important pieces:

- exact `epsilon = 0` identity reduction
- matched-null control consistency
- a small nonzero-coupling centroid / phase-ramp perturbation

Those are real.

From the retained loop note:

- zero-`epsilon` centroid shift: `+0.000000e+00`
- zero-`epsilon` escape ratio: `1.000000`
- zero-`epsilon` phase slope: `+0.0000e+00`
- zero-`epsilon` phase span: `+0.0000e+00`
- zero-`epsilon` convergence: `True`

And at nonzero coupling, the promoted observables move in the expected direction.

## Why it still fails

The failure is a **three-part limit**, not a single bad measurement:

1. **The backreaction signal is small.**
   The nonzero-coupling centroid / phase-ramp shifts remain tiny even on the
   retained audit rows.

2. **The nonlinear loop is not stable enough.**
   The strict retained row from the loop audit does not converge cleanly at
   nonzero coupling, so the effect cannot be promoted as a stable retained
   mechanism.

3. **End-to-end Born stops being machine-clean.**
   Step-local Born on the frozen field snapshot is fine, but the full loop is
   no longer Born-clean at the retained tolerance.

## Mechanism-level diagnosis

The clearest retained explanation is:

- the lane behaves like a **tiny control surface** with weak backreaction
- it does **not** yet behave like a converged self-gravity mechanism
- the apparent absorption / redistribution is therefore best read as a
  numerically fragile perturbation on the control surface, not as a promoted
  physical backreaction law

So the failure is not primarily:

- “Born is violated everywhere”
- “the null control is broken”
- “nothing changes at all”

It is instead:

- the signal is too small
- the nonlinear iteration is too unstable
- the end-to-end retention is not strong enough to support a mechanism claim

## Strongest retained conclusion

This lane is now a **bounded no-go**.

The best honest summary is:

- exact null identity holds
- a tiny backreaction perturbation exists
- but the perturbation does not survive as a stable, review-safe self-gravity
  mechanism on this architecture

## What would reopen it

To reopen this lane, a later architecture would need to show all four at once:

- exact `epsilon = 0` identity
- converged nonlinear loop at nonzero coupling
- step-local Born near machine precision
- end-to-end Born that stays review-clean

Until then, the lane is closed for mechanism claims.
