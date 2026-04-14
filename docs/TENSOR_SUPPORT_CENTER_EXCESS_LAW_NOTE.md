# Exact Support-Side `A1` Center-Excess Law and the Remaining Tensor Gap

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_tensor_support_center_excess_law.py`  
**Status:** exact support-side reduction plus bounded tensor-law narrowing

## Purpose

The projective-blindness note proved that the current exact shell/junction
toolbox cannot see the remaining scalar `A1` background datum at fixed total
charge.

That still left one key axiom-first question:

> after leaving the shell side, what exact microscopic scalar on the support
> block actually survives and can carry the last tensor law?

This note answers that question.

## Exact support-side statement

Work on the exact seven-site star support with the canonical `A1` basis

- `e0 = A1(center)`
- `s = A1(shell-average)`

and normalize `s` to unit total charge by `s / sqrt(6)`.

Let `phi_support = G_S q` be the exact support potential induced by the exact
support Green matrix `G_S`.

Then:

- the arm-site support potential per unit charge is identical for the two
  unit-charge `A1` endpoint backgrounds
  - `e0`
  - `s / sqrt(6)`
- the only exact difference between those two endpoint backgrounds on the
  support is the center excess

`phi_support(center) - phi_support(arm_mean) = 1/6`

with machine-precision residual.

So after fixing total charge, the exact `A1` support block retains one scalar
microscopic datum:

`delta_A1(q) = phi_support(center)/Q - phi_support(arm_mean)/Q`.

This is the support-side datum that survives the shell-blindness theorem.

## Exact canonical formula

For the canonical `Q = 1` projective `A1` family

`q_A1(r) = (e0 + r s) / (1 + sqrt(6) r)`

the support-side scalar is exactly

`delta_A1(r) = 1 / (6 (1 + sqrt(6) r))`.

So the last microscopic scalar is no longer an abstract projective parameter.
It is an explicit exact support-side center-excess observable.

## Bounded tensor-law consequence

Using the current bright tensor coefficients

- `gamma_E`
- `gamma_T`

from the current tensor-boundary-drive pipeline, the runner fixes an affine law
from the two exact `A1` support endpoints:

- center background `e0`
- shell background `s / sqrt(6)`

and tests it on:

1. intermediate canonical `A1` projective backgrounds
2. the exact local `O_h` `A1` baseline
3. the finite-rank `A1` baseline

Result:

- on the canonical `A1` family the affine support law reproduces the bright
  tensor coefficients with errors of order `1e-8`
- on the audited exact local `O_h` and finite-rank `A1` baselines, the same
  law reproduces the coefficients at the same `few x 1e-6` level already seen
  in the earlier projective-compatibility note

So the remaining tensor law is now much tighter than

- “some unknown scalar function of `r`”

It is almost exactly:

- an affine law in one exact support-side scalar `delta_A1`

with coefficients fixed by the two exact `A1` endpoint backgrounds.

## Interpretation

This is the cleanest axiom-first gravity reduction so far.

The shell side is blind to the last scalar datum, but the microscopic support
block is not.

And on that support block, the surviving scalar datum is explicit:

- center excess at fixed total charge

So the remaining gravity theorem is no longer:

- derive an arbitrary scalar renormalization function

It is:

1. derive the exact tensor observable on the support block
2. derive the exact tensor endpoint coefficients at
   - `e0`
   - `s / sqrt(6)`
3. then recover the full affine support law in `delta_A1`

## What this closes

This closes another false level of generality.

The last tensor law is no longer a generic function on the projective `A1`
manifold. On the current restricted class it is almost entirely controlled by:

- one exact support-side scalar `delta_A1`
- two endpoint tensor coefficients

## What this still does not close

This note still does **not** close:

1. the exact tensor boundary observable itself
2. the exact tensor endpoint coefficients
3. the full restricted tensor completion theorem
4. full nonlinear GR

## Practical conclusion

The current best gravity target is now:

> derive the exact tensor observable on the microscopic `A1 x {E_x, T1x}`
> support block and its two `A1` endpoint coefficients. If that lands, the
> remaining scalar law is already organized as the affine support-side
> center-excess law.
