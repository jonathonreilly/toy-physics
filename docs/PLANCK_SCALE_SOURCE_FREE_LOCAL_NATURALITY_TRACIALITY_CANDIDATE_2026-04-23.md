# Planck-Scale Source-Free Local Naturality Traciality Candidate

**Date:** 2026-04-23  
**Status:** science-only new-theory candidate on the last Planck blocker  
**Audit runner:** `scripts/frontier_planck_source_free_local_naturality_traciality_candidate.py`

## Question

Can the last Planck blocker be phrased directly on the primitive local Hilbert
surface, without starting from boundary-pressure language, packet-specific
combinatorics, or even a chosen event-frame subgroup?

The remaining blocker is purely local:

`rho_cell = I_16 / 16`.

The direct counting law is already closed:

`c_cell(rho) = Tr(rho P_A)`.

So the real question is:

> what should "source-free local state" mean on the bare finite Hilbert cell?

## Bottom line

The cleanest candidate is:

> **Source-Free Local Naturality Traciality Theorem.**
> On a bare finite local Hilbert factor with no extra local datum, the
> source-free local state assignment is natural under local unitary
> isomorphisms. Therefore it must commute with every local unitary, so on
> `H_cell = C^16` the unique normalized source-free state is
>
> `rho_cell = I_16 / 16`.

Then the already-closed direct counting theorem gives

`c_cell = Tr((I_16 / 16) P_A) = 1/4`,

so the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

This is stronger conceptually than the older flip witness and cleaner than the
boundary-pressure grammar because it states the missing content directly at the
primitive local Hilbert surface:

> if no local datum has been added, the local state cannot depend on a chosen
> local frame.

## Why this route is distinct

The automorphism/event-frame route says:

`no preferred primitive projector`
`->`
`event-frame transitivity / relabeling invariance`
`->`
`rho_cell = I_16 / 16`.

The present route starts even further upstream:

`bare finite local Hilbert factor + no extra datum`
`->`
`unitary naturality of the source-free state assignment`
`->`
`rho_cell commutes with every local unitary`
`->`
`rho_cell = I_16 / 16`.

So the load-bearing object is the bare local factor itself, not a later packet
or a chosen subgroup of primitive relabelings.

## Inputs

This note uses only already-opened branch-local surfaces:

- [PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md](./PLANCK_SCALE_DIRECT_WORLDTUBE_PACKET_COEFFICIENT_CHAIN_2026-04-23.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)

What those already fix:

1. the local carrier is a real finite Hilbert factor;
2. the direct counting law already reduces the Planck coefficient to a local
   state problem;
3. the currently retained direct stack does not select that state;
4. if the missing theorem is to be axiom-native, the best remaining place to
   seek it is the primitive local factor itself.

## Setup

Let `H_cell = C^16`.

Call a rule `H -> rho_H` a **source-free local state assignment** if it assigns
to each finite local Hilbert factor a normalized positive state operator.

Call the assignment **natural under local unitaries** if for every unitary
isomorphism `U : H -> H`,

`rho_H = U rho_H U^dagger`.

This is the finite-cell meaning of:

> with no extra local datum inserted, the source-free state cannot change under
> a mere change of local unitary frame.

## Theorem 1: unitary naturality forces the tracial state

Let `rho` be a normalized positive operator on `H = C^d`.

If

`U rho U^dagger = rho`

for every unitary `U in U(d)`,

then

`rho = I_d / d`.

### Proof

The invariance condition implies

`U rho = rho U`

for every unitary `U`.

Since the unitaries span the full matrix algebra `M_d(C)`, `rho` commutes with
all of `M_d(C)`.

Therefore `rho` lies in the center of `M_d(C)`, so

`rho = lambda I_d`.

Normalization gives

`Tr(rho) = d lambda = 1`,

so

`lambda = 1/d`.

Hence

`rho = I_d / d`.

## Corollary 1: the primitive time-locked cell is tracial

Apply Theorem 1 at `d = 16`.

If the source-free local state on the primitive cell is natural under local
unitary frame changes, then

`rho_cell = I_16 / 16`.

## Corollary 2: quarter follows immediately

The direct counting law already gives

`c_cell(rho) = Tr(rho P_A)`.

Because `rank(P_A) = 4`,

`c_cell = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4`.

So the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

## Why this may be the most axiom-native candidate

If Planck is really native, the last theorem should plausibly live on the most
primitive accepted object still available.

On this branch, that object is no longer a Schur scalar or even the packet
`P_A`. It is the bare finite local Hilbert cell itself.

The candidate claim is then simple:

- the cell is physical;
- no extra local datum has been inserted;
- so the source-free local state must be natural under unitary changes of
  local frame;
- that forces the trace state.

This is the cleanest direct reformulation I currently see.

## Honest status

This is **not** yet retained.

It is a new theorem candidate.

The honest claim is only:

- the direct counting law is already closed;
- the currently retained stack still leaves the source-free state open;
- the cleanest remaining upstream candidate may be unitary naturality of the
  source-free local state on the bare primitive Hilbert cell.

So the route is now reduced to one sharp question:

> on a physical bare finite local Hilbert factor, does "source-free local
> state" mean "unitarily natural local state"?

If yes, the Planck route closes immediately.
