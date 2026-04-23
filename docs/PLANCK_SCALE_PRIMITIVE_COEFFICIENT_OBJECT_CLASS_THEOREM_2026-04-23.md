# Planck-Scale Primitive-Coefficient Object-Class Theorem

**Date:** 2026-04-23  
**Status:** branch-local theorem on the last reduced-vacuum reclassification hatch  
**Audit runner:** `scripts/frontier_planck_primitive_coefficient_object_class_theorem.py`

## Question

After the primitive cell, packet, and kinematic count operator are fixed, can a
hostile reviewer still rescue the old objection by saying:

> the elementary Planck coefficient is really a dynamical reduced-vacuum
> observable?

The issue is no longer numerical. The issue is whether this reclassification is
even the same kind of object as the direct primitive-cell coefficient.

## Bottom line

Not as a fundamental identification.

Once the direct lane has fixed:

- the primitive physical object `H_cell`,
- the exact count operator `N_cell = P_A`,
- and the requirement that the elementary coefficient be universal and attached
  to that primitive cell,

a reduced-vacuum expectation value is not the same object. It belongs to an
enlarged datum class:

`(H_cell, iota, Omega)`

where:

- `iota` is the embedding of the local cell algebra into a chosen global
  system,
- `Omega` is the chosen global vacuum or source-free global state.

So a reduced-vacuum expectation is not a function of the primitive cell alone.
It is a function of a larger triple.

Therefore:

> reclassifying the elementary Planck coefficient as a reduced-vacuum
> expectation does not explain the primitive-cell coefficient. It changes the
> object under discussion.

The only coherent surviving vacuum-language use is representational:

> a separately justified distinguished global state may reproduce the intrinsic
> primitive-cell coefficient.

But in that case the coefficient itself is still primitive-cell data, and the
real burden remains the distinguished state law.

## Inputs

- [PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md](./PLANCK_SCALE_TIMELOCKED_FACTOR_CELL_OBJECT_DERIVATION_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_UNIVERSAL_CELL_COEFFICIENT_NOT_VACUUM_EXPECTATION_THEOREM_2026-04-23.md](./PLANCK_SCALE_UNIVERSAL_CELL_COEFFICIENT_NOT_VACUUM_EXPECTATION_THEOREM_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_FROM_ONE_AXIOM_THEOREM_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

## Setup

The direct lane has already fixed the primitive local object

`H_cell = C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16`

and the exact one-cell count operator

`N_cell = P_A`.

So the direct elementary coefficient is a function of the primitive cell and,
if state data is needed at all, of the state attached to that same primitive
cell.

Call this direct object class:

`Obj_dir = (H_cell, N_cell)`.

A reduced-vacuum expectation requires more data. One needs:

1. a global system containing the cell,
2. an embedding `iota` of the cell algebra into that global system,
3. a chosen global vacuum or source-free global state `Omega`,
4. reduction back to the cell.

Call that object class:

`Obj_vac = (H_cell, N_cell, iota, Omega)`.

The question is whether `Obj_vac` can be identified with `Obj_dir` without
changing the scientific content of the coefficient.

## Theorem 1: reduced-vacuum expectation is extra-datum object class

For fixed `H_cell` and `N_cell`, the map

`(iota, Omega) -> Tr(rho^red_(iota,Omega) N_cell)`

is, in general, a function of the additional pair `(iota, Omega)`.

So a reduced-vacuum expectation value is not primitive-cell data alone.

### Proof

The current branch already has explicit admissible local witness states on the
same `H_cell` and `N_cell = P_A` with distinct values:

- `Tr((I_16/16) P_A) = 1/4`,
- `Tr(((1/32) P_A + (7/96)(I_16 - P_A)) P_A) = 1/8`.

Those are enough to show that the value of `Tr(rho N_cell)` is not determined
by `(H_cell, N_cell)` alone.

Any reduced-vacuum expectation therefore depends on the extra datum selecting
which reduced state appears, whether that datum is packaged as a global vacuum,
embedding, Hamiltonian, environment, or some combination.

So reduced-vacuum expectation belongs to the larger object class `Obj_vac`.

## Theorem 2: reclassification changes the coefficient's object

Assume the elementary Planck coefficient is supposed to be:

1. universal,
2. local on the primitive physical cell,
3. attached to that primitive cell as its elementary coefficient.

Then identifying it fundamentally with a reduced-vacuum expectation changes the
object under discussion from `Obj_dir` to `Obj_vac`.

### Proof

By Theorem 1, the reduced-vacuum value is not fixed by `(H_cell, N_cell)`
alone.

So if one says

`c_cell = Tr(rho^red_(iota,Omega) N_cell)`,

the right-hand side is no longer a function of `Obj_dir` alone. It is a
function of `Obj_vac`.

But the direct lane's elementary coefficient is supposed to be attached to the
primitive cell itself. Therefore a fundamental identification with a
reduced-vacuum expectation introduces new datum and changes the object.

That is not a derivation of the primitive-cell coefficient. It is a
redefinition into a different object class.

## Corollary 1: the only coherent vacuum-language use is representational

Vacuum language can still be used in one narrower way.

If a separate theorem proves a distinguished source-free state law on the
primitive cell, or proves a distinguished global state whose reduction is that
same local state, then one may write

`c_cell = Tr(rho_* N_cell)`.

But in that case the real load-bearing theorem is the distinguished state law.
The coefficient remains primitive-cell data; the vacuum formula is only a
representation of it.

## Corollary 2: the last hatch is now narrow

After this note and the universal-vs-vacuum note, the hostile-review escape
hatch is no longer:

> maybe the coefficient is just some vacuum observable.

It is only:

> maybe there is a separately justified distinguished state law whose local
> reduction gives the intrinsic primitive-cell coefficient.

That is exactly the source-free default-datum route.

## Honest status

This note does not by itself prove the source-free default datum.

What it does prove is the sharper classification result:

- the direct Planck coefficient is attached to the primitive physical cell;
- a reduced-vacuum expectation belongs to a larger datum class;
- so a fundamental reclassification as reduced-vacuum observable is a category
  change, not an explanation of the same coefficient;
- at most, vacuum language can represent the intrinsic coefficient after a
  separate distinguished state theorem is earned.

So the remaining burden is no longer whether the coefficient is kinematic or
vacuum. That classification fight is effectively over.

The remaining burden is only:

> which distinguished source-free state law belongs to the primitive cell?
