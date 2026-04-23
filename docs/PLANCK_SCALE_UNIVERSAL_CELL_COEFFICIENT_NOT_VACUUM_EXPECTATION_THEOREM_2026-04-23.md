# Planck-Scale Universal Cell-Coefficient Not-Vacuum-Expectation Theorem

**Date:** 2026-04-23  
**Status:** branch-local theorem / reduction on the universal-vs-vacuum classification step  
**Audit runner:** `scripts/frontier_planck_universal_cell_coefficient_not_vacuum_expectation_theorem.py`

## Question

Can the elementary Planck cell coefficient be coherently read as a **generic
dynamical reduced-vacuum expectation value**, or does universality force it
into the kinematic primitive-cell counting class instead?

The target quantity is the elementary local coefficient attached to the
primitive physical cell on the direct Planck lane.

## Bottom line

The sharpest honest result is:

> if the elementary Planck cell coefficient is required to be
>
> - **universal** across admissible vacua of the same theory,
> - **local** on the primitive physical cell,
> - and **attached to that primitive cell itself** rather than to a chosen
>   global state,
>
> then it cannot coherently be a **generic dynamical reduced-vacuum
> expectation value**.

More precisely:

1. the direct counting route already fixes the elementary local count operator

   `N_cell = P_A`;

2. any value of the form

   `Tr(rho N_cell)`

   is state-dependent in general;
3. the current branch already exhibits admissible local witness states with
   distinct values on `P_A`, including `1/4` and `1/8`;
4. therefore a reading of the coefficient as a **generic** reduced-vacuum
   expectation does not produce a universal primitive-cell constant;
5. the only coherent surviving interpretations are:

   - a genuinely **kinematic** primitive-cell counting coefficient, or
   - a non-generic expectation value evaluated on a separately justified
     distinguished state law.

So the vacuum-expectation reading cannot be load-bearing by itself. If one
wants the direct Planck route to close, the remaining burden is not "pick a
vacuum" but "justify the distinguished source-free state law."

## Inputs

- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_KINEMATIC_CELL_COEFFICIENT_THEOREM_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_KINEMATIC_CELL_COEFFICIENT_THEOREM_CANDIDATE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_THEOREM_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_DEFAULT_DATUM_THEOREM_CANDIDATE_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_OBSERVABLE_PRINCIPLE_PRESSURE_IDENTIFICATION_LANE_2026-04-23.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

## Assumptions

Work with the direct Planck lane and assume:

1. **physical lattice**: the primitive local cell is a real physical object,
   not a disposable regulator artifact;
2. **local primitive attachment**: the coefficient is attached to the exact
   primitive cell rather than to a later coarse-grained global state label;
3. **universality**: the elementary coefficient is the same for all admissible
   vacua / source-free global realizations of the same theory;
4. **direct counting grammar**: the coefficient belongs to the same local
   grammar as the direct one-cell worldtube counting theorem;
5. **generic reduced-vacuum expectation reading** means:

   `c_cell = Tr(rho_vac^red N_cell)`

   where `rho_vac^red` is the local reduced state induced by a chosen vacuum,
   with no prior theorem forcing a unique value of `Tr(rho_vac^red N_cell)`.

Assumption 5 matters. If a separate theorem already proves a unique reduced
state law, then the coefficient is no longer "generic vacuum expectation"; the
distinguished state theorem is doing the real work.

## Theorem 1: the elementary operator is already fixed kinematically

The direct worldtube-to-boundary counting theorem already proves that the
elementary local count operator is

`N_cell = P_A`.

Its derivation uses one-cell locality, minimal-shell support, additive
incidence counting, residual exact `S_3`, and time-lock. It does **not** use:

- a vacuum state,
- a thermal state,
- an effective-action minimizer,
- or a Hamiltonian-selected local expectation value.

So `N_cell` is fixed before any dynamical state selection.

## Theorem 2: generic reduced-vacuum expectations are state-dependent

For a fixed local operator `N_cell = P_A`, the value

`Tr(rho N_cell)`

depends on the state `rho`.

The current branch already gives explicit admissible local witness states:

- tracial witness

  `rho_tr = I_16 / 16`,

  giving

  `Tr(rho_tr P_A) = 1/4`;

- packet-light witness

  `rho_lt = (1/32) P_A + (7/96)(I_16 - P_A)`,

  giving

  `Tr(rho_lt P_A) = 1/8`.

So a value of the form `Tr(rho P_A)` is not universal unless a further theorem
forces the allowed state class down to one distinguished state law.

## Theorem 3: universality is incompatible with the generic vacuum reading

Assume the elementary coefficient is universal in the sense of Assumption 3.

Assume also that it is identified with a **generic** reduced-vacuum
expectation:

`c_cell = Tr(rho_vac^red P_A)`.

Then one of two things must happen:

1. different admissible reduced vacua give different values on `P_A`, in which
   case `c_cell` is not universal; or
2. all admissible reduced vacua give the same value on `P_A`, in which case a
   separate state-selection theorem is already forcing that equality.

Therefore the coefficient cannot coherently be **generic reduced-vacuum
expectation data** if it is universal.

### Proof

By Theorem 2, state dependence is real on the current branch: distinct
admissible local witnesses produce distinct values on the same local operator.

So if the vacuum-expectation reading is truly generic, the value varies with
the chosen reduced vacuum and fails universality.

The only escape is that the state class is not truly generic after all, but
already restricted by an additional theorem selecting a distinguished reduced
state or at least a distinguished value on `P_A`.

That means the vacuum-expectation reading is not load-bearing. The real
load-bearing content would then be that additional state theorem.

So universality rules out the generic vacuum-expectation reading as the
primitive explanation of the coefficient.

## Corollary 1: scalar/vacuum free-energy observables are the wrong class

The older scalar boundary observable already gives an exact control:

`p_vac(L_Sigma) = (1/4) log(5/3)`,

which is not `1/4`.

So the scalar/vacuum observable class is both:

- conceptually misaligned with the direct one-cell counting grammar, and
- numerically wrong for the Planck coefficient on the exact witness.

This reinforces that the Planck coefficient is not naturally a generic vacuum
observable.

## Corollary 2: the surviving options

After Theorem 3, only two coherent interpretations remain:

1. **kinematic primitive-cell coefficient**  
   The coefficient is primitive local counting data attached to the physical
   cell itself.

2. **distinguished-state evaluation**  
   The coefficient is evaluated on a separately justified distinguished local
   state law, such as the source-free default datum of the primitive cell.

Option 2 may still be correct. But if so, the real burden is the
distinguished-state theorem, not a generic vacuum reading.

## Honest status

This note does **not** by itself prove the direct Planck route fully closed.

What it does prove is the strongest clean classification result now available:

- the universal elementary coefficient is not coherently explained as a
  **generic reduced-vacuum expectation**;
- the operator side is already kinematic;
- the remaining open content is entirely in the distinguished source-free
  state law.

So the primitive classification issue is now reduced to:

> either the coefficient is kinematic primitive-cell counting data, or it is a
> non-generic expectation value whose state law must be justified separately.

That is much sharper than the earlier vacuum-vs-pressure ambiguity.
