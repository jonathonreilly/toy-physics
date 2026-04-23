# Planck-Scale Source-Free Central Cell-State Theorem Candidate

**Date:** 2026-04-23  
**Status:** science-only new-theory candidate on the last Planck blocker  
**Audit runner:** `scripts/frontier_planck_source_free_central_cell_state_theorem_candidate.py`

## Question

Can the last open Planck blocker be stated more natively than either
boundary-pressure language or packet-specific symmetry tricks?

The remaining blocker is now purely local:

`rho_cell = I_16 / 16`.

The direct counting law is already closed:

`c_cell(rho) = Tr(rho P_A)`.

So the only question is which source-free local state lives on the primitive
time-locked cell algebra.

## Bottom line

Yes.

The cleanest direct candidate is:

> **Source-Free Central Cell-State Theorem.**
> On the primitive one-cell algebra `A_cell = M_16(C)`, a source-free local
> state may depend only on exact central local datum. Since the center of
> `M_16(C)` is one-dimensional, the unique normalized source-free local state
> is
>
> `rho_cell = I_16 / 16`.

Then the direct counting theorem immediately gives

`c_cell = Tr((I_16 / 16) P_A) = 1/4`,

so the direct Planck chain closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

This is cleaner than the older scalar Schur route because it does not talk
about free energies at all, and cleaner than the older flip witness because it
states the real missing content directly:

> source-free local data cannot contain any noncentral one-cell structure.

## Why this is a distinct route

The automorphism/traciality candidate says:

> no preferred primitive projector
> `->`
> automorphism invariance
> `->`
> traciality.

The present route is one step more algebraic:

> no local datum
> `->`
> dependence only on exact central cell structure
> `->`
> scalar density matrix
> `->`
> traciality.

This uses the primitive matrix algebra itself as the load-bearing object.

## Inputs

This note builds only on already-opened branch-local surfaces:

- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)

What those already fix:

1. the primitive local carrier is a real physical finite cell;
2. the direct counting law already reduces the Planck coefficient to a local
   state problem on that cell;
3. the current retained stack does **not** itself choose the source-free state;
4. the remaining freedom is therefore exactly a question about what
   source-free local datum is admissible on `M_16(C)`.

## Setup

Work on the primitive one-cell algebra

`A_cell = End(H_cell) = M_16(C)`.

Let `Z(A_cell)` denote its center.

Define a **source-free central state candidate** to mean a normalized positive
operator `rho` on `H_cell` such that the local state law depends only on exact
central one-cell datum, i.e. on `Z(A_cell)` rather than on any chosen
noncentral projector, basis, packet, or local Hamiltonian insertion.

This is the mathematical form of the physical statement:

> without any added local source datum, the primitive cell cannot carry a
> preferred internal direction.

## Theorem 1: the center of `M_16(C)` is scalar

`Z(M_16(C)) = C I_16`.

### Proof

Let `X` commute with every matrix unit `E_ij`.

Write `X = (x_ab)`.

From `X E_ii = E_ii X` one gets

- `x_ab = 0` whenever `a != b`,

so `X` is diagonal.

From `X E_ij = E_ij X` with `i != j` one gets

- the `i`th and `j`th diagonal entries are equal.

Since this holds for every pair `i,j`, all diagonal entries are equal. Thus

`X = lambda I_16`.

So the center is exactly the scalar line.

## Corollary 1: central source-free state is tracial

Assume the source-free local state may depend only on exact central cell
datum.

Then `rho_cell` must lie on the scalar line:

`rho_cell = lambda I_16`.

Positivity requires `lambda >= 0`, and normalization gives

`Tr(rho_cell) = 16 lambda = 1`.

Therefore

`lambda = 1/16`,

hence

`rho_cell = I_16 / 16`.

This is exactly the tracial state on the primitive cell.

## Corollary 2: quarter follows immediately

The direct counting theorem already gives

`c_cell(rho) = Tr(rho P_A)`.

Since `rank(P_A) = 4`,

`c_cell = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4`.

So the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

## Why this may be the most native formulation

This route does not need to start from:

- Schur boundary free energy,
- packet-specific combinatorics,
- or even a chosen transitive subgroup of primitive relabelings.

It starts from the primitive local algebra itself.

If the cell is physical and source-free means "no extra local datum", then the
state law should be central before it is anything else. On a full matrix
algebra, "central" is already strong enough to force the trace state.

That makes this route a serious candidate for the cleanest axiom-native close:

- primitive physical cell,
- no extra local datum,
- center-only state law,
- normalized trace,
- quarter,
- Planck.

## Honest status

This is **not** yet retained.

It is a new direct theorem candidate.

The honest claim is only:

- the direct counting law is already closed;
- the accepted retained stack underdetermines the source-free state;
- the cleanest remaining algebraic candidate is now the center-only source-free
  state theorem on `M_16(C)`.

So the Planck lane is now reduced to a very sharp question:

> on a physical primitive finite cell, does "source-free local datum" mean
> "central datum only"?

If yes, Planck closes immediately.
