# Planck-Scale Action-Phase Representation Hbar Theorem

**Date:** 2026-04-24
**Status:** structural `hbar` derivation as primitive action-to-phase conversion
**Verifier:** `scripts/frontier_planck_action_phase_representation_hbar_theorem_2026_04_24.py`

## Question

Can the branch extend the reduced action-count result

`Phi(I_16) = 1`

into a structural derivation of `hbar`?

## Result

Yes, in the physically meaningful structural sense.

The primitive integral action-count theorem gives the source-free closed
history monoid

`M_cell = N [A_cell]`

and the reduced action coordinate

`Phi(n[A_cell]) = n`.

A coherent quantum history representation assigns phases multiplicatively under
history gluing:

`U(H_1 (+) H_2) = U(H_1) U(H_2)`.

Lifting the phase to the universal cover gives an additive phase coordinate

`theta(H_1 (+) H_2) = theta(H_1) + theta(H_2)`.

The same-source/no-hidden-character rule identifies this phase generator with
the primitive action-count generator:

`theta(H) = Phi(H)`.

Therefore, in conventional notation

`U(H) = exp(i S(H)/hbar)`,

the branch derives

`S(H)/hbar = Phi(H)`.

For one complete primitive cell,

`S(A_cell)/hbar = Phi(A_cell) = 1`.

This is the structural `hbar` result: `hbar` is the conversion factor between
physical action `S` and the primitive integral action-count phase `Phi`. It is
not a prediction of the SI decimal value of `hbar`.

## Theorem 1: coherent gluing forces an additive phase generator

Let `M_cell = N[A_cell]` be the closed source-free primitive history monoid.
Coherent amplitudes compose multiplicatively under disjoint gluing:

`U(m+n) = U(m) U(n)`.

Thus `U` is a monoid homomorphism

`U : M_cell -> U(1)`.

Choosing the universal-cover phase coordinate gives

`theta : M_cell -> R`,

with

`U(H) = exp(i theta(H))`

and

`theta(m+n) = theta(m) + theta(n)`.

On the free one-generator monoid, every additive phase coordinate is fixed by
its value on `[A_cell]`.

## Theorem 2: same-source phase excludes an extra scale

The primitive integral action-count theorem already supplies the action source

`Phi(n[A_cell]) = n`.

A different phase lift

`theta_lambda(H) = lambda Phi(H)`

would give

`U_lambda(H) = exp(i lambda Phi(H))`.

For `lambda != 1`, the quotient

`U_lambda(H) / U_1(H) = exp(i (lambda - 1) Phi(H))`

is an extra source-free one-dimensional phase character on the same primitive
history source. It is not a new incidence, not a prepared boundary source, and
not retained multiplicity.

The same-source/no-hidden-character rule used throughout the Planck packet
forbids such extra characters. Therefore

`lambda = 1`

and

`theta = Phi`.

## Theorem 3: `hbar` is the physical action-to-count conversion

In standard action-phase notation, coherent histories are written

`U(H) = exp(i S(H)/hbar)`.

Theorem 2 gives

`U(H) = exp(i Phi(H))`.

Therefore

`S(H)/hbar = Phi(H)`

as the dimensionless physical phase.

Equivalently,

`S(H) = hbar Phi(H)`.

The primitive action quantum is the physical action assigned to one unit of the
primitive integral count. For the one-cell generator,

`Phi(A_cell) = 1`,

so

`S(A_cell) = hbar`.

That is the structural derivation of the role of `hbar`: it converts one
primitive action-count unit into physical action.

## Relation To Planck

On the minimal primitive atom,

`q_atom = 1/16`.

On the minimal cubical defect,

`eps_* = pi/2`,

so

`a^2/l_P^2 = 8 pi (1/16)/(pi/2) = 1`.

The same reduced action-count phase is therefore what appears in both:

1. the action-phase representation `exp(i S/hbar)`;
2. the dimensionless Planck relation `a^2 c_light^3/(hbar G)=1`.

## What Is Closed

Closed:

1. the primitive integral action-count unit `Phi(I_16)=1`;
2. the coherent-history phase representation `theta=Phi`;
3. the structural `hbar` statement `S/hbar = Phi`;
4. the one-cell action quantum statement `S(A_cell)=hbar`.

## What Is Not Claimed

Not claimed:

1. the SI decimal value of `hbar`;
2. an independent prediction of joule-seconds without a physical unit
   convention;
3. a derivation of every equivalent role of `hbar` such as canonical
   commutators, uncertainty relations, or angular-momentum spectra.

Those roles become downstream quantum-mechanical representations of the same
action-phase unit, but they are not proved in this theorem.

## Safe Claim

Use:

> The primitive integral action count is the universal-cover phase generator of
> coherent histories. Hence `S/hbar = Phi`, and one complete primitive cell has
> action `hbar` in physical units.

Do not use:

> The branch predicts the SI decimal value of `hbar`.

Do not use:

> The branch has derived all canonical commutator or uncertainty-relation
> appearances of `hbar`.
