# Planck-Scale Source-Free Local State Law Theorem

**Date:** 2026-04-23  
**Status:** branch-local conditional theorem candidate for the last Planck blocker  
**Audit runner:** `scripts/frontier_planck_source_free_local_state_law_theorem.py`

## Question

Can the last blocker

`rho_cell = I_16 / 16`

be derived directly from the primitive local tensor-product structure, instead
of being left as a free full-cell state-selection principle?

The direct counting law is already closed:

`c_cell(rho) = Tr(rho P_A)`.

So the only issue is the source-free state on the primitive time-locked cell.

## Bottom line

Conditionally yes.

The source-free local state law is:

> **On a bare local `C^2` factor with no added local datum, the unique
> source-free state is the normalized trace `I_2 / 2`.**

The primitive time-locked cell is the exact tensor product

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z`.

Because source-free local composition carries no cross-factor datum, the
source-free cell state factorizes across the exact local tensor factors:

`rho_cell = (I_2 / 2)⊗4 = I_16 / 16`.

Then the already-closed counting theorem gives

`c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4`,

so the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

This is stronger than the older full-cell candidate notes because the law is
reduced to two sharp state-law principles:

- primitive local Hilbert factors,
- no-datum local frame invariance on each factor,
- no cross-factor source datum in the source-free local state.

## Hostile-review correction

This note does **not** show that the source-free state law follows from the
currently accepted minimal package by itself.

The derivation depends on two additional state-law premises:

1. **bare-factor unitary no-datum invariance** on `C^2`;
2. **no-cross-factor-datum tensor composition** on the exact local tensor
   product.

Those premises are clean and physically motivated, but they are still fresh
branch-local promotions. They are **not** yet part of the accepted minimal
input stack recorded in [MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md).

So this note should be read as:

- a clean **conditional close candidate**;
- not an already-earned retained axiom-native close.

## Why this is cleaner

The older full-cell candidates all said, in different language, that the
source-free state on `M_16(C)` should be tracial.

This note moves one level deeper:

1. derive the source-free state on the primitive `C^2` factor;
2. lift it to the time-locked cell by the exact tensor-product structure.

That makes the state law more native to the one-axiom Hilbert/locality surface
than a direct ad hoc full-`M_16(C)` postulate.

## Inputs

This theorem uses the already-open branch-local surfaces:

- [SINGLE_AXIOM_HILBERT_NOTE.md](./SINGLE_AXIOM_HILBERT_NOTE.md)
- [SINGLE_AXIOM_INFORMATION_NOTE.md](./SINGLE_AXIOM_INFORMATION_NOTE.md)
- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)

What those already fix:

1. the primitive local structure is tensor-product Hilbert locality;
2. the lattice/local carrier is physical, not regulator bookkeeping;
3. the direct counting law is already closed;
4. the old retained stack underdetermines the full-cell state if no new
   source-free state law is added.

## Definition: source-free local state law

Call a local state law **source-free** if:

1. it assigns a normalized positive state to a bare local Hilbert factor;
2. it depends on no extra local datum beyond the factor itself;
3. it is invariant under exact local unitary frame changes on that bare factor;
4. on an exact tensor product of independent bare local factors, it introduces
   no cross-factor datum and therefore composes by tensor product.

This is the finite-cell form of:

> no local source, no preferred local frame, no added cross-factor correlator
> datum.

## Theorem 1: the source-free state on a bare `C^2` factor is `I_2 / 2`

Let `rho` be the source-free state on a bare local factor `H = C^2`.

By local unitary frame invariance,

`U rho U^dagger = rho`

for every `U in U(2)`.

So `rho` commutes with every `2 x 2` matrix and therefore lies in the center
of `M_2(C)`.

Hence

`rho = lambda I_2`.

Normalization gives

`Tr(rho) = 2 lambda = 1`,

so

`lambda = 1/2`.

Therefore

`rho_sf(C^2) = I_2 / 2`.

## Theorem 2: exact tensor-product locality lifts the state law to the cell

The primitive time-locked cell has the exact factorization

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z`.

By the source-free composition law, the source-free state on the full cell is
the tensor product of the source-free states on the four bare factors:

`rho_cell = rho_sf(C^2_t) ⊗ rho_sf(C^2_x) ⊗ rho_sf(C^2_y) ⊗ rho_sf(C^2_z)`.

Using Theorem 1 on each factor,

`rho_cell = (I_2 / 2) ⊗ (I_2 / 2) ⊗ (I_2 / 2) ⊗ (I_2 / 2) = I_16 / 16`.

So the source-free primitive time-locked cell state is exactly tracial.

## Why the composition law is the right no-datum rule

If one allowed the source-free state on the exact tensor product of bare local
factors to include extra non-product correlator structure, that correlator
structure would itself be additional local datum beyond the individual factors.

So on the source-free local surface:

- the local factor law is fixed by bare-factor invariance;
- the full-cell law is the tensor product of those factor laws.

This is precisely the point where the current retained-direct underdetermination
note stopped: it did not yet add a source-free composition law.

## Corollary 1: quarter follows immediately

The direct counting theorem already gives

`c_cell(rho) = Tr(rho P_A)`.

With

`rho_cell = I_16 / 16`

and `rank(P_A)=4`,

`c_cell = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4`.

So the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

## Relation to the other direct routes

This theorem subsumes the older direct candidates.

- **Automorphism/event-frame route:** the factor law already forbids any
  preferred primitive projector.
- **Center-only route:** `I_2/2` and therefore `I_16/16` are exactly the
  central states on the corresponding matrix algebras.
- **Naturality route:** Theorem 1 is the 2D naturality argument, and Theorem 2
  extends it by tensor-product locality.
- **Max-entropy route:** the resulting state is also the entropy maximizer, but
  entropy is no longer the primary load-bearing principle here.
- **Spectral-datum exclusion:** any nontracial alternative would inject local
  spectral/correlator datum beyond the bare factors.

So the branch no longer needs five rival last-step stories. This theorem is the
cleanest synthesis.

## Honest status

This theorem is branch-local science. It is not woven through `main`.

The honest claim is:

- the direct counting law is already closed;
- the older retained-direct stack still underdetermines the source-free state;
- once source-free bare-factor invariance and no-cross-factor-datum
  composition are admitted as the correct local state law, the primitive cell
  state is derived exactly:
  `rho_cell = I_16 / 16`.

So on this branch-local Planck lane, the source-free state law is no longer an
open coefficient guess. But it is still conditional on those two promoted
state-law premises, not yet a retained consequence of the accepted package by
itself.
