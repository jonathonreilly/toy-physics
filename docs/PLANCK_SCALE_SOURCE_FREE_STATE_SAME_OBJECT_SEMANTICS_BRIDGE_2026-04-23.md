# Planck-Scale Source-Free State Same-Object Semantics Bridge

**Date:** 2026-04-23  
**Status:** branch-local bridge theorem candidate for hostile review  
**Audit runner:** `scripts/frontier_planck_source_free_state_same_object_semantics_bridge.py`

## Question

Is the remaining source-free state law really a fresh imported physics axiom, or
is it better understood as the package's already-used **same-object /
different-presentation** semantics applied to local state data on the exact
primitive cell?

## Bottom line

This is the strongest bridge currently available.

The package already uses the following theorem-grade norm elsewhere:

> different presentations of the **same physical object** cannot produce
> different physical data.

That norm is explicit in the `g_bare` closure surface:

- [G_BARE_RIGIDITY_THEOREM_NOTE.md](./G_BARE_RIGIDITY_THEOREM_NOTE.md)
- [G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md](./G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md)

On the accepted one-axiom Hilbert/locality/information surface, the graph,
locality, and state-space structure are one physical object:

- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

The exact direct Planck cell is now tied to that object surface by
[PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md):

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z ~= C^16`.

So the clean bridge claim is:

> a source-free local state is physical data attached to the exact primitive
> cell object itself, not to an arbitrary choice of factor frames.

If that same-object semantics is applied to the primitive cell state, then
factor-preserving presentation changes cannot alter the assigned source-free
state. That gives

`U rho_cell U^dagger = rho_cell`

for every

`U = U_t ⊗ U_x ⊗ U_y ⊗ U_z`,

and therefore

`rho_cell = I_16 / 16`.

With the already-closed counting theorem
[PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md),
this gives

`c_cell = Tr((I_16/16) P_A) = 1/4`,

hence the direct Planck route closes.

## Why this is better than the older phrasing

Older formulations made the last step sound like a new special law:

- max entropy,
- no preferred primitive projector,
- local automorphism invariance,
- center-only datum,
- or branch-local traciality.

This bridge reframes all of them as one more basic statement:

> the package already forbids different physics from different presentations of
> the same object; the source-free primitive-cell state should obey that same
> norm.

That is closer in spirit to the existing `g_bare` rigidity logic than to a
fresh thermodynamic or information-theoretic postulate.

## Inputs

- [MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [G_BARE_RIGIDITY_THEOREM_NOTE.md](./G_BARE_RIGIDITY_THEOREM_NOTE.md)
- [G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md](./G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md)
- [PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_OBJECT_WELL_DEFINEDNESS_THEOREM_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_OBJECT_WELL_DEFINEDNESS_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)

## Theorem 1: same-object semantics for the primitive cell state

Let the exact primitive local object be the labeled factorized cell

`H_cell = H_t ⊗ H_x ⊗ H_y ⊗ H_z`,

with each factor isomorphic to `C^2`.

Assume:

1. the accepted package semantics already treats physical data as attached to
   the physical object, not to arbitrary presentations of that object;
2. the source-free local state on the primitive cell is physical data of that
   cell object;
3. factor-preserving basis changes

   `U_t ⊗ U_x ⊗ U_y ⊗ U_z`

   are only presentation changes of the same labeled cell object.

Then the source-free local state assignment must satisfy

`U rho_cell U^dagger = rho_cell`

for every factor-preserving automorphism `U`.

### Proof

Item 1 is the theorem-grade norm already used on the `g_bare` lane: same
object, different presentation, same physical datum. Item 2 says the local
source-free state is itself physical data attached to the primitive cell.
Item 3 identifies the relevant presentation changes.

If the assigned state changed under such a presentation change, then the same
primitive cell object would carry two different physical state data depending
only on presentation, violating Item 1.

So the source-free state must be presentation-independent in the operator sense:

`U rho_cell U^dagger = rho_cell`.

## Corollary 1: traciality

The factor-preserving automorphism group

`U(2)_t × U(2)_x × U(2)_y × U(2)_z`

generates the full local matrix algebra `M_16(C)` on `H_cell`.

Therefore any operator commuting with every such automorphism lies in the
center of `M_16(C)`, hence is scalar:

`rho_cell = lambda I_16`.

Normalization gives `lambda = 1/16`, so

`rho_cell = I_16 / 16`.

## Corollary 2: quarter and Planck

Using the already-closed counting law

`c_cell(rho) = Tr(rho P_A)`,

one gets

`c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4`.

So on this direct route:

`a^2 = l_P^2`,

hence

`a = l_P`.

## Honest status

This note does **not** magically remove every hostile-review objection.

What it does do is make the remaining issue much more precise:

- no longer a special Planck-only state axiom,
- no longer a thermodynamic choice,
- no longer a packet-specific symmetry trick,
- but the extension of already-used package **same-object semantics** to local
  state data on the exact primitive cell.

The strongest remaining objection is now:

> does the package's same-object semantics, already used for operators and
> projected Green's functions, legitimately extend to source-free local states
> on the exact primitive cell object?

That is a much narrower and cleaner objection than the earlier charge that the
Planck lane was importing an unrelated state-selection law.
