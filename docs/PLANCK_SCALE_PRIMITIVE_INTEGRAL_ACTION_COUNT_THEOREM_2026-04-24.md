# Planck-Scale Primitive Integral Action-Count Theorem

**Date:** 2026-04-24
**Status:** positive reduced-action closure on the primitive integral-history surface
**Verifier:** `scripts/frontier_planck_primitive_integral_action_count_theorem_2026_04_24.py`

## Question

The non-homogeneous hbar/action-unit reduction left one exact target:

`Phi(I_16) = 1`.

Can that target be derived without using another homogeneous trace/naturality
argument, without using phase periodicity alone, and without predicting the SI
decimal value of `hbar`?

## Result

Yes, on the primitive integral-history surface.

The source-free primitive event history is not a rank-one prepared atom. The
full automorphism-invariant one-cell object is the complete `C^16` event cell

`A_cell = I_16`.

Closed source-free primitive histories form the free integral gluing monoid

`M_cell = N [A_cell]`.

The reduced primitive action coordinate on this integral object is the
generator-count coordinate

`ell(n [A_cell]) = n`.

Therefore

`Phi(I_16) = ell([A_cell]) = 1`,

so the trace-reduced primitive phase law gives

`gamma = 1`,

`Phi(P_eta) = 1/16`,

`kappa_info = 1/32 per bit`,

and on the minimal cubical defect

`a^2 / l_P^2 = 1`.

This is a structural reduced-action-unit closure. It is not a prediction of
the SI value of `hbar`, and it does not close the separate B3 gravity-sector
derivation.

## Theorem 1: the source-free primitive object is the full cell

Let the primitive event algebra be the diagonal event algebra of the `16`
one-cell labels. Before a preparation is supplied, the retained source-free
cell does not distinguish one label from another.

The event-frame automorphism action is transitive on the `16` labels. The only
subsets invariant under a transitive action are the empty subset and the full
set. Therefore the only nonzero source-free primitive idempotent is the full
cell:

`A_cell = I_16`.

Rank-one projectors `P_eta` are valid event atoms after a selector or source is
named. They are not the default source-free closed cell. Treating an atom as the
unit action history would add hidden preparation data.

## Theorem 2: source-free cell histories form a free integral monoid

Gluing source-free primitive cells is disjoint concatenation. With no prepared
label, no external meter, and no additional boundary character, a closed
history is determined only by the number of complete primitive cells it
contains.

Thus the source-free closed-history monoid is

`M_cell = N [A_cell]`.

The generator `[A_cell]` is indecomposable: it is one complete primitive cell,
not a sum of two nonempty source-free closed cells.

## Theorem 3: the primitive action coordinate is generator count

On a free integral monoid with one indecomposable generator, the primitive
count coordinate is uniquely determined by

`ell([A_cell]) = 1`

and additivity:

`ell(H_1 (+) H_2) = ell(H_1) + ell(H_2)`.

A rescaled real functional

`lambda ell`

is a homogeneous real measure on the same set, but it is not the primitive
integral action coordinate unless `lambda = 1`. For `lambda = 2`, the one-cell
generator is assigned the count of a two-cell history; for `0 < lambda < 1`, it
does not land in the integral history count at all.

Therefore the scale ambiguity in the real-valued trace theorem is removed only
when the reduced action coordinate is the integral primitive-history count.

## Theorem 4: gamma-one follows

The primitive phase trace theorem already proves the shape

`Phi(P) = gamma Tr(P) / 16`

and defines

`gamma = Phi(I_16)`.

The integral action-count theorem supplies the missing non-homogeneous unit:

`Phi(I_16) = ell([A_cell]) = 1`.

Therefore

`gamma = 1`.

For any rank-one event atom `P_eta`,

`Phi(P_eta) = 1/16`.

On the time-locked elementary two-bit carrier,

`kappa_info = (1/16) / 2 = 1/32 per bit`.

With the already established minimal cubical defect

`eps_* = pi/2`,

the action-phase conversion gives

`a^2 / l_P^2 = 8 pi (1/16) / (pi/2) = 1`.

## What This Closes

This closes the previous hbar/action-unit scalar on the primitive
integral-history surface:

`Phi(I_16) = 1`.

The branch may now say:

> The reduced primitive action unit is the integral count of complete
> source-free primitive cells, so the full `C^16` cell has unit reduced action
> and `gamma = 1`.

## What This Does Not Close

This theorem does not derive:

1. the SI decimal value of `hbar`;
2. a dimensionful joule-second conversion without a physical unit map;
3. the B3 dynamical metric/coframe response;
4. the gravitational parent-source object class from a bare gravity sector.

If a reviewer refuses the integral primitive-history reading and instead
allows arbitrary positive real action measures on the same source-free cells,
then the old scale countermodel returns:

`Phi_lambda(P) = lambda Tr(P) / 16`.

So the theorem is a closure of the reduced action unit as primitive cell count,
not a closure of every possible real-valued action-measure convention.

## Safe Claim

Use:

> On the primitive integral-history surface, the source-free complete `C^16`
> cell is the indecomposable generator of the closed-history monoid. The
> reduced action coordinate is its generator count, so `Phi(I_16)=1` and
> `gamma=1`.

Do not use:

> The SI numerical value of `hbar` is predicted.

Do not use:

> Bare `Cl(3)` / `Z^3` has therefore derived the dynamical gravitational
> metric/coframe sector.
