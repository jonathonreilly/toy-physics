# Poisson Self-Gravity Born Audit Note

**Date:** 2026-04-05  
**Status:** explicit per-step vs end-to-end Born audit for the iterated
Poisson-like backreaction loop

## Artifact chain

- [`scripts/poisson_self_gravity_born_audit.py`](/Users/jonreilly/Projects/Physics/scripts/poisson_self_gravity_born_audit.py)
- [`logs/2026-04-05-poisson-self-gravity-born-audit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-poisson-self-gravity-born-audit.txt)

## Question

Does the iterated Poisson-like self-gravity loop preserve Born only at the
level of each frozen propagation step, or also end-to-end through the full
loop?

This audit is intentionally narrow:

- one exact 3D lattice family at `h = 0.25`
- one three-slit source set on the input layer
- one screened Poisson-like backreaction loop
- one exact `epsilon = 0` reduction check
- one step-local Born check on a frozen loop snapshot
- one end-to-end Born check through the full iterated loop

## What Born means here

The audit separates two distinct questions:

1. **Step-local Born**
   - freeze the converged field snapshot
   - test the usual three-slit Sorkin `I3/P` on that fixed field

2. **End-to-end Born**
   - run the full nonlinear loop separately for `a`, `b`, `c`, `ab`, `ac`,
     `bc`, and `abc`
   - compute the final detector `I3/P` from the converged loop outputs

That distinction matters because the outer map is nonlinear even if each fixed
field propagation step is linear.

## Frozen result

Representative retained row:

- `epsilon = 0.05`
- source strength `s = 0.004`

Reduction check:

- exact `epsilon = 0` reduction survives exactly

Frozen Born audit row:

| `epsilon` | source strength | step-local Born | end-to-end Born | step converged | end converged |
| --- | ---: | ---: | ---: | ---: | ---: |
| `0.05` | `0.0040` | `8.834e-16` | `6.830e-05` | `False` | `False` |

## Safe read

The strict conclusion is:

- the frozen field snapshot remains Born-clean to machine precision
- the full iterated loop does **not** stay machine-clean end-to-end on the
  tested nonzero coupling
- the loop therefore preserves Born only at the per-step / frozen-snapshot
  level on this audit
- the nonzero backreaction map is nonlinear enough to generate a small but
  real end-to-end Born drift

## Honest limitation

This is a narrow audit, not a universal theorem.

- it uses one exact lattice family
- it uses one representative nonzero coupling row
- it demonstrates the key distinction the audit was meant to separate

## Branch verdict

Treat this as:

- **per-step Born survives**
- **end-to-end Born does not remain machine-clean on the tested loop**

So the retained control is still useful, but the iterated backreaction map is
not Born-safe as a full nonlinear evolution.
