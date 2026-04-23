# Planck-Scale Kinematic Cell-Coefficient Theorem Candidate

**Date:** 2026-04-23  
**Status:** branch-local theorem candidate for the last physical-classification step  
**Audit runner:** `scripts/frontier_planck_kinematic_cell_coefficient_theorem_candidate.py`

## Question

Is the elementary Planck cell coefficient

`c_cell`

best understood as:

- a **kinematic primitive-cell counting datum**, or
- a **dynamical vacuum-state observable**?

## Bottom line

The strongest direct-branch answer is:

> the elementary Planck cell coefficient is **kinematic primitive-cell
> counting data**, not a dynamical vacuum-state observable.

More precisely:

1. the exact elementary boundary count operator is already fixed by local
   primitive-cell kinematics:

   `N_cell = P_A`;

2. any numerical evaluation

   `Tr(rho N_cell)`

   is state-dependent unless one also specifies what `rho` is;
3. so a universal elementary cell coefficient cannot be identified with an
   arbitrary vacuum expectation value;
4. the only coherent universal reading is:

   - kinematic count operator fixed by the primitive cell,
   - evaluated on the **source-free default datum** of that same cell.

On that reading, the direct route closes with

`rho_cell = I_16/16`,
`c_cell = Tr((I_16/16) P_A) = 1/4`,
`a = l_P`.

## Why this is the right question

The source-free state problem became difficult because one could still try to
read the coefficient as if it were a generic vacuum expectation value of the
interacting theory.

But a universal Planck coefficient should be:

- local;
- elementary;
- attached to the primitive physical cell;
- and independent of which admissible global vacuum/state one later places on
  the theory.

That is a kinematic role, not a dynamical vacuum role.

## Inputs

- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_THEOREM_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_THEOREM_CANDIDATE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

## Theorem 1: the elementary count operator is kinematic

The direct cell-counting theorem already proves that the elementary
codimension-1 boundary count operator is

`N_cell = P_A`.

Its derivation uses only:

- one-cell locality,
- minimal-shell support,
- additive count semantics,
- integer-valued atomic incidence counts,
- residual `S_3` invariance,
- and time-lock.

No vacuum state, no thermal weighting, no interacting effective action, and no
Hamiltonian-selected local expectation value enters this derivation.

So `N_cell` is fixed at the kinematic primitive-cell level.

## Theorem 2: vacuum expectations are state-dependent and therefore not
universal elementary coefficients

For a fixed kinematic count operator `N_cell = P_A`, the value

`Tr(rho N_cell)`

depends on the state `rho`.

On the current branch there are explicit admissible witnesses:

- tracial candidate `rho_tr = I_16/16`, giving
  `Tr(rho_tr P_A) = 1/4`;
- packet-light candidate `rho_lt`, giving
  `Tr(rho_lt P_A) = 1/8`.

So if one identifies the elementary Planck coefficient with a generic
vacuum-state expectation value, the value is not fixed by the primitive-cell
kinematics alone.

That is incompatible with the intended role of a universal elementary cell
coefficient.

## Corollary 1: the scalar/vacuum observable class is the wrong class for the
Planck coefficient

The old scalar Schur/free-energy route already provides a negative control.
Its exact source-free scalar quantity is

`p_vac(L_Sigma) = (1/(2n)) log det(L_Sigma)`,

and on the witness it lands

`(1/4) log(5/3)`,

not `1/4`.

So the scalar/vacuum observable class is both:

- mathematically different from the kinematic count operator class,
- and numerically wrong for Planck on the current branch.

This is evidence that the Planck coefficient should not be read as a scalar
vacuum observable.

## Theorem 3: universal elementary cell coefficient must be read on the bare
cell datum

Because the lattice is physical, the primitive time-locked `C^16` cell is a
real local object.

An elementary Planck coefficient is supposed to describe that object at the
bare local level, before any further prepared local datum is supplied.

So the only coherent universal interpretation is:

- the operator side is the kinematic count operator `N_cell = P_A`;
- the state side is the **source-free default datum** of the same primitive
  cell.

That is exactly the content of the default-datum theorem candidate.

## Corollary 2: direct Planck close on the default-datum reading

If the source-free primitive-cell state is the default bare-cell datum, then

`rho_cell = I_16/16`.

Therefore

`c_cell = Tr((I_16/16) P_A) = 1/4`,

and the direct route gives

`a^2 = l_P^2`,

hence

`a = l_P`.

## Honest status

This note does **not** by itself promote the branch to a front-door retained
close.

What it does do is settle the classification issue much more sharply:

- the direct branch already fixed the **kinematic** object;
- vacuum/state dependence is a separate layer;
- so the only remaining semantic move is to accept the source-free
  **default-datum** reading on the physical primitive cell.

That is narrower and stronger than saying "we just choose a uniform vacuum."
