# DM Neutrino Source-Surface Minimal Active-Displacement Selector Theorem

**Date:** 2026-04-16  
**Status:** exact constructive point-selection theorem with one genuinely new
right-sensitive input  
**Script:** `scripts/frontier_dm_neutrino_source_surface_minimal_active_displacement_selector_theorem.py`

## Question

The current exact bank is already exhausted and does **not** pick the live
`2`-real point `(delta, q_+)` on the source-oriented sheet.

If we add one genuinely new right-sensitive input, can we derive that
point-selection law exactly?

## New input

Yes, if we add the following intrinsic variational selector:

> among all points on the exact live active chamber
> `q_+ >= sqrt(8/3) - delta`,
> choose the unique point minimizing the Frobenius size of the active
> right-sensitive displacement
> `Delta_H,act(delta,q_+) = delta T_delta + q_+ T_q`.

This is a genuinely new input. It is **not** contained in the old bank.

## Bottom line

With that input, the point-selection law closes exactly.

The active generators are

- `T_delta = [[0,-1,1],[-1,1,0],[1,0,-1]]`
- `T_q     = [[0,1,1],[1,0,1],[1,1,0]]`.

They satisfy

- `<T_delta, T_q>_F = 0`
- `||T_delta||_F^2 = ||T_q||_F^2 = 6`.

So the active action is exactly

- `S_act(delta,q_+) = ||delta T_delta + q_+ T_q||_F^2`
- `= 6(delta^2 + q_+^2)`.

Minimizing that action on the exact half-plane

- `q_+ >= sqrt(8/3) - delta`

gives the unique projection of the origin to the boundary line, hence

- `delta_* = q_+* = sqrt(6)/3 = sqrt(8/3)/2`.

Therefore

- `rho_* = sqrt(8/3) - delta_* = sqrt(6)/3`
- `r31,* = 1/2`
- `phi_+,* = pi/2`.

So the new input closes the exact `2`-real point-selection law itself.

## Why this is the right kind of new input

The old bank already fixed:

- the source package `(gamma, E1, E2)`
- the intrinsic slot pair `(a_*, b_*)`
- the intrinsic CP pair `(cp1, cp2)`
- the exact active chamber and its affine generators.

What it did **not** fix was the coefficient of the two right-sensitive active
generators `(T_delta, T_q)`.

This input acts directly and only on that remaining right-sensitive object.
So it is minimal in scope:

- it does not reopen source packaging,
- it does not reopen PMNS,
- it does not add a larger carrier.

It selects only the exact remaining `2`-real point.

## Exact theorem

### 1. The active displacement carries an intrinsic Euclidean quadratic form

On the live source-oriented sheet,

- `Delta_H,act(delta,q_+) = delta T_delta + q_+ T_q`.

Because the two active generators are Frobenius-orthogonal and have equal
norm, the induced active action is exactly

- `S_act(delta,q_+) = 6(delta^2 + q_+^2)`.

So the remaining selector problem becomes the exact Euclidean projection
problem for the active chamber.

### 2. The admissible domain is the exact active half-plane

The active-half-plane theorem already gives the exact domain

- `q_+ >= sqrt(8/3) - delta`.

So the variational selector is a strict convex quadratic minimization on a
closed half-plane. It therefore has a unique minimizer.

### 3. The unique minimizer is the boundary midpoint

The unconstrained minimum of `S_act` is the origin, but the origin is outside
the admissible half-plane. Therefore the constrained minimum lies on the
boundary line

- `q_+ = sqrt(8/3) - delta`.

Substituting that into the exact action gives

- `S_bdy(delta) = 6(delta^2 + (sqrt(8/3) - delta)^2)`
- `= 12 delta^2 - 8 sqrt(6) delta + 16`.

Differentiating gives

- `S_bdy'(delta) = 24 delta - 8 sqrt(6)`,

so the unique minimizer is

- `delta_* = sqrt(6)/3`,

and then

- `q_+* = sqrt(8/3) - delta_* = sqrt(6)/3`.

### 4. The selected point has exact carrier consequences

At that selected point

- `rho_* = sqrt(8/3) - delta_* = sqrt(6)/3`
- `q_+* - sqrt(8/3) + delta_* = 0`

so the source-surface boundary relation gives

- `r31,* = 1/2`
- `phi_+,* = pi/2`.

Thus the selector picks the unique smallest active displacement exactly on the
maximal-phase source boundary.

## The theorem-level statement

**Theorem (Minimal active-displacement selector for the live `2`-real point).**
Assume the exact active-affine source-surface theorem and the exact active
half-plane theorem. Add the new right-sensitive input that the physical point
is the unique minimizer of the Frobenius action
`S_act(delta,q_+) = ||delta T_delta + q_+ T_q||_F^2` on the admissible chamber
`q_+ >= sqrt(8/3) - delta`. Then the active action is exactly
`6(delta^2 + q_+^2)`, so the unique constrained minimizer is the orthogonal
projection of the origin to the boundary line. Therefore
`delta_* = q_+* = sqrt(6)/3`, equivalently
`rho_* = sqrt(6)/3`, `r31,* = 1/2`, and `phi_+,* = pi/2`.

## What this closes

This closes the exact `2`-real point-selection law itself, once the new input
is accepted.

The branch can now say more sharply:

- the old bank alone does **not** select `(delta, q_+)`
- but one minimal new right-sensitive variational input does
- and it selects the exact closed form
  `(delta_*, q_+*) = (sqrt(6)/3, sqrt(6)/3)`.

## What this does not close

This is **input-driven** closure, not old-bank-only closure.

So this note does **not** prove that the variational selector is already
implicit in the original bank. It proves that one genuinely new and minimal
right-sensitive input is enough to finish the law exactly.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_minimal_active_displacement_selector_theorem.py
```
