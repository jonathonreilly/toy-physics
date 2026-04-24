# Planck-Scale Hbar Strong Routes Status Theorem

**Date:** 2026-04-24
**Status:** hbar/gamma route audit; primitive action route now closed in reduced count units
**Verifier:** `scripts/frontier_planck_hbar_strong_routes_status_theorem.py`

## Question

After the phase trace theorem

`Phi(P) = gamma Tr(P)/16`,

can any stronger first-principles route now close

`gamma = 1`

without using homogeneous trace/naturality or bare U(1)/finite-root
periodicity?

## Result

The current branch has reduced the hbar/action-unit target to one
non-homogeneous real unit statement:

`Phi(I_16) = 1`.

The original strong-route audit showed that homogeneous trace/naturality,
periodicity, finite roots, noncompact central lines, spectral flow without an
action-index unit map, and ordinary Ward balance do not close that statement.
The primitive action-generator route is now closed on the primitive
integral-history surface by
[PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md](./PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md).
The structural action-phase representation is then closed by
[PLANCK_SCALE_ACTION_PHASE_REPRESENTATION_HBAR_THEOREM_2026-04-24.md](./PLANCK_SCALE_ACTION_PHASE_REPRESENTATION_HBAR_THEOREM_2026-04-24.md).

The exact theorem supplied there is:

> derive a primitive real action generator whose complete `C^16` event cell has
> unit reduced action before exponentiation.

It is closed as reduced action count and as structural `S/hbar=Phi`, not as an
SI-value derivation of `hbar`. The other strong routes remain useful
independent attacks, but they are not needed for `gamma=1` once the integral
primitive-history surface is accepted.

## Route 1: noncompact central extension

A noncompact central extension can lift phase from `U(1)` to an additive real
line:

`0 -> R -> G_hat -> G -> 1`.

That avoids the `2 pi` periodicity obstruction. But it does not by itself fix
the scale of the central generator. If `Z` is central, then `lambda Z` is also
central for any positive real `lambda`.

Thus a noncompact central extension changes the target from

`phase class modulo 2 pi`

to

`real action generator up to scale`.

It still needs a primitive unit theorem selecting the generator for which

`Phi(I_16) = 1`.

On the retained finite event symmetry, a real central extension also has no
automatic nontrivial continuous level. On a translation group such as `Z^d`,
real Heisenberg-type cocycles require an antisymmetric/symplectic two-form.
The retained cubic symmetry in three spatial directions supplies no invariant
spatial two-form. Thus the central-extension route must first derive the
needed action-valued cocycle or symplectic datum; it is not already present in
bare `Cl(3)` / `Z^3`.

## Route 2: spectral flow / index

An index theorem could close the target if it proves that one complete
primitive event cell carries index one:

`Index(D_cell) = 1`.

Then one could set the real action unit by the index normalization. But the
current finite `C^16` event cell has not supplied:

1. a canonical Fredholm/Dirac pair `D_cell`;
2. a boundary path whose spectral flow is invariantly one;
3. a theorem that the index is the action generator rather than just a count.

Without those objects, the phrase "index one" is an import. The viable target
is therefore:

> construct the canonical primitive event Dirac/Fredholm pair and prove its
> one-cell spectral flow is one.

## Route 3: primitive action generator

The most direct closure would be a theorem:

`A_cell := I_16`

is the primitive generator of the reduced action monoid, and the action monoid
is normalized by generator count:

`Phi(A_cell) = 1`.

This closes `gamma = 1` once the source-free closed histories are treated as
the free integral monoid `N[A_cell]`. The integral action-count theorem proves
that `A_cell = I_16` is the minimal invariant complete-cell generator and that
the reduced action coordinate is generator count.

The hostile-review caveat is narrow: if a reviewer refuses the integral
primitive-history reading and instead allows arbitrary positive real action
measures on the same cell histories, the old scale ray returns.

## Route 4: microscopic Ward/action normalization

A microscopic Ward theorem could close `gamma = 1` if it derives a source
parameter `s` whose identity derivative is already dimensionless reduced
action with unit primitive cell charge.

The present boundary Ward stack does this for the Planck boundary coefficient
inside the retained parent-source boundary-action object class. It does not
derive the universal quantum of action. Reusing it for hbar would be circular
unless the action unit is derived before importing standard gravitational
area/action normalization.

## Consequence

The hbar lane is now split:

1. reduced action-count `gamma=1` is closed on the primitive integral-history
   surface;
2. SI `hbar`, central-extension, spectral-flow, and microscopic Ward
   derivations remain unclaimed.

The exact survivor for any non-count route is still not a vague conversion
constant. It is the same specific non-homogeneous theorem:

> the complete primitive `C^16` event cell is the unit generator of reduced
> real action.

This may still be attacked independently through a noncompact central
extension, spectral-flow/index theorem, or microscopic action Ward identity.
Those routes are not closed in the current branch.

## Safe Claim

Use:

> The branch derives the trace shape `q_atom = gamma/16` and proves that
> homogeneous, periodic, and finite-root arguments do not select `gamma = 1`.
> The primitive integral-history theorem supplies `gamma=1` in reduced
> action-count units, and the action-phase representation theorem gives
> `S/hbar=Phi`. This is not an SI-value derivation of `hbar`.

Do not use:

> The branch predicts the SI numerical value of `hbar`.

Do not use:

> A noncompact central extension alone fixes `gamma = 1`.

Do not use:

> An index route is closed before a canonical primitive event Dirac/Fredholm
> pair and index-one theorem are derived.
