# Planck-Scale `Cl(3)` Spinor-Phase Quantum No-Go Theorem

**Date:** 2026-04-23  
**Status:** science-only no-go on the most naive spinorial coefficient route  
**Audit runner:** `scripts/frontier_planck_cl3_spinor_phase_quantum_nogo.py`

## Question

Can exact `a = l_P` be forced by the most obvious purely-`Cl(3)` mechanism:

> take the elementary action quantum `q_*` to be the spinorial phase quantum
> of a finite-order cubic rotation / holonomy coming from `Cl(3)` bivectors,
> then match that directly to the Einstein/Regge hinge formula?

## Bottom line

No.

If `q_*` is taken from a nontrivial finite-order cubic spinorial holonomy, the
smallest possible nonzero phase quantum is

`q_* >= pi / 4`.

But a local positive Regge hinge defect satisfies

`0 < eps_* < 2 pi`.

The exact Planck condition from the action-phase reduction is

`a^2 / l_P^2 = 8 pi q_* / eps_*`,

so exact `a = l_P` would require

`q_* = eps_* / (8 pi) < 1/4`.

That is impossible for any nonzero finite-order cubic spinorial holonomy,
because

`pi / 4 > 1 / 4`.

So the naive "spinorial sign / finite cubic holonomy by itself fixes Planck"
route is dead.

## Inputs

This theorem uses:

- [PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md](./PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md)
- [NATIVE_GAUGE_CLOSURE_NOTE.md](./NATIVE_GAUGE_CLOSURE_NOTE.md)

Only two structural facts are needed:

1. `Cl(3)` bivectors generate the spinorial rotation algebra `spin(3) ~ su(2)`;
2. the proper rotational symmetries of the cubic lattice have finite orders
   `2`, `3`, and `4`, corresponding to SO(3) angles `pi`, `2pi/3`, and
   `pi/2`.

Their spinorial half-angles are therefore:

- `pi/2`,
- `pi/3`,
- `pi/4`.

So the smallest nonzero cubic spinorial phase quantum is `pi/4`.

## Exact reduction

### 1. Finite-order cubic spinorial phases are quantized in half-angles

For a spatial rotation by angle `theta`, the `Cl(3)` rotor is

`R(theta) = exp(-(B theta)/2)`,

so the associated spinorial phase quantum is governed by the half-angle
`theta / 2`.

On the cubic lattice, the nontrivial proper rotation orders are:

- order `2`: `theta = pi`
- order `3`: `theta = 2pi/3`
- order `4`: `theta = pi/2`

Therefore the corresponding nonzero spinorial phase quanta are:

- `pi/2`
- `pi/3`
- `pi/4`

and the smallest is

`q_min = pi/4`.

### 2. Exact Planck requires a much smaller phase quantum

From the elementary action-phase reduction,

`a^2 / l_P^2 = 8 pi q_* / eps_*`.

If we demand exact `a = l_P`, then

`q_* = eps_* / (8 pi)`.

For a local positive hinge defect,

`0 < eps_* < 2 pi`,

so exact Planck would require

`0 < q_* < 1/4`.

### 3. Contradiction

The finite-order cubic spinorial route gives

`q_* >= pi/4 ~ 0.785`,

while exact Planck would require

`q_* < 1/4 = 0.25`.

These are incompatible.

So no nonzero finite-order cubic spinorial holonomy can serve as the exact
elementary action quantum that forces `a = l_P`.

## The theorem-level statement

**Theorem (finite-order cubic spinor-phase no-go).**
Assume:

1. the elementary action quantum `q_*` is identified with a nonzero finite-
   order cubic spinorial holonomy quantum coming from `Cl(3)` bivectors;
2. the elementary curvature defect `eps_*` is a local positive Regge hinge
   defect with `0 < eps_* < 2 pi`;
3. exact Planck would mean `a = l_P` in the elementary reduction
   `a^2 / l_P^2 = 8 pi q_* / eps_*`.

Then exact `a = l_P` is impossible.

Proof:

- the smallest nonzero finite-order cubic spinorial quantum is `q_* = pi/4`;
- exact Planck would require `q_* = eps_* / (8 pi) < 1/4`;
- but `pi/4 > 1/4`.

Therefore the naive finite-order cubic spinorial-holonomy route cannot close
the Planck coefficient. □

## What this closes

This closes the most obvious pure-`Cl(3)` coefficient guess:

- "maybe the lattice is Planck because spinors pick up a minus sign under
  `2 pi`, or because a cubic rotor gives the elementary action phase."

Not enough.

The phase quantum from finite cubic rotations is too large to satisfy the
exact coefficient condition.

## What survives

This does **not** kill the whole action-quantum route.

What survives is narrower:

- a non-finite-order or non-cubic elementary phase law;
- an action quantum not tied directly to the smallest finite cubic spinorial
  holonomy;
- or a route in which the elementary coefficient is fixed by both phase and
  defect data simultaneously, not by the phase alone.

## Safe wording

**Can claim**

- finite-order cubic spinorial holonomy alone cannot force exact Planck;
- the smallest nonzero `Cl(3)` cubic spinorial phase quantum is already too
  large for the exact coefficient condition.

**Cannot claim**

- that all spinorial/action-quantum routes are dead;
- that `Cl(3)` contributes nothing to the coefficient theorem.
