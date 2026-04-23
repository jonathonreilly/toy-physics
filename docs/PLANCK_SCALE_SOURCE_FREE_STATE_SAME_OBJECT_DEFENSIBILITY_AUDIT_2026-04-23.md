# Planck-Scale Source-Free State Same-Object Defensibility Audit

**Date:** 2026-04-23  
**Status:** branch-local hostile-review defensibility memo  
**Audit runner:** `scripts/frontier_planck_source_free_state_same_object_defensibility_audit.py`

## Question

The package already uses same-object / different-presentation semantics on
operators and projected Green's-function coefficients.

Is it actually defensible to extend that semantics to the **source-free local
state** on the exact primitive cell?

## Short verdict

**Yes, conditionally and in a narrow sense.**

It is defensible **for source-free local states**, because a source-free state
is supposed to carry **no extra local datum beyond the primitive cell object
itself**.

It is **not** defensible as a blanket rule for **all** states. Arbitrary
prepared states can and do carry extra physical preparation data, so they are
not forced to be tracial by same-object semantics alone.

That distinction is the key point.

## Core argument

### 1. What same-object semantics already means in the package

The package already uses a theorem-grade norm of the form:

> if two descriptions are only different presentations of the same physical
> object, they cannot give different physical data.

That is explicit on the `g_bare` lane:

- [G_BARE_RIGIDITY_THEOREM_NOTE.md](./G_BARE_RIGIDITY_THEOREM_NOTE.md)
- [G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md](./G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md)

So this is not a foreign norm being imported only for Planck.

### 2. Why source-free local states are special

The crucial distinction is:

- an arbitrary prepared state includes extra preparation data;
- a **source-free** local state, by definition, is the state assigned when no
  additional local datum has been supplied.

So for a prepared state, the physical object is really something like

`(primitive cell, preparation datum)`.

For a source-free state, the physical object is just

`(primitive cell)`.

That is why the same-object extension is much more defensible for source-free
states than for arbitrary states.

### 3. Why presentation dependence would violate “source-free”

On the exact direct route, the primitive local object is the labeled factorized
cell

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z`.

Factor-preserving basis changes

`U = U_t ⊗ U_x ⊗ U_y ⊗ U_z`

do not change the labeled cell object. They only change its presentation.

If the source-free state assignment changed under such a presentation change,
then the choice of local factor frames would itself become hidden state data.
That is exactly the opposite of “source-free / no extra local datum.”

So the extension is defensible because it is not adding new content so much as
enforcing internal consistency of the phrase “source-free.”

### 4. Why this does not overreach to prepared states

Take a pure prepared state `rho = |0000><0000|`.

That state is obviously not invariant under arbitrary factor-preserving basis
changes. But that does **not** make it unphysical, because the prepared object
is not just the bare cell. It is the pair

`(cell, prepared projector/event datum)`.

Under a presentation change, both pieces transform together, and all physical
readouts stay the same.

So:

- **prepared state:** same-object semantics acts on the larger pair
  `(cell, preparation datum)`;
- **source-free state:** there is no larger pair, so the state must be
  attached to the bare cell object alone.

That is the clean reason the tracial conclusion can be specific to the
source-free case.

## Theorem-style defensibility statement

Assume:

1. the package's same-object semantics is legitimate;
2. the source-free primitive-cell state is physical data of the primitive cell
   object itself;
3. factor-preserving basis changes are presentation changes of that same
   labeled cell object;
4. “source-free” means no extra local preparation datum is being carried.

Then it is defensible to require

`U rho_sf U^dagger = rho_sf`

for every factor-preserving automorphism `U`.

And because these automorphisms generate the full local matrix algebra on
`M_16(C)`, one gets

`rho_sf = I_16 / 16`.

## What this does settle

This memo does settle that the same-object extension is **not arbitrary**.

It is supported by three points:

- the package already uses same-object semantics elsewhere;
- the direct Planck lane now has an exact primitive local object;
- source-free states are categorically different from prepared states because
  they carry no additional datum.

So the extension is scientifically defensible.

## What this still does not settle

This still does **not** prove that the extension is already part of the
accepted front-door minimal stack in
[MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md).

So the strongest honest status remains:

- **defensible branch-local extension**
- stronger than an ad hoc state-selection postulate
- still not automatically a front-door retained theorem unless the package
  explicitly accepts that same-object semantics applies to source-free local
  states on the primitive cell

## Bottom line

If hostile review asks:

> is this extension defensible?

the answer is:

**yes, because source-free local states are not arbitrary prepared states, and
letting them vary with presentation would smuggle hidden local datum into an
object that is supposed to have none.**

If hostile review asks:

> is it already unquestionably part of the accepted minimal stack?

the answer is still:

**not yet automatically; that final semantic extension still needs to be
accepted explicitly.**
