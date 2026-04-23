# Planck-Scale Source-Free Local Frame Well-Definedness Theorem

**Date:** 2026-04-23  
**Status:** branch-local direct theorem candidate on the last Planck blocker  
**Audit runner:** `scripts/frontier_planck_source_free_local_frame_well_definedness_theorem.py`

## Question

Can the last source-free-state blocker be derived without importing a separate
tensor-composition law, and without retreating to scalar boundary language?

The direct counting law is already closed:

`c_cell(rho) = Tr(rho P_A)`.

So the only remaining issue is the local state on the exact time-locked cell.

## Bottom line

Yes, conditionally, in a cleaner form than the earlier state-law theorem.

Let the primitive time-locked cell be the exact labeled tensor product

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z`.

If the source-free local state is required to be **well-defined on this bare
factorized object**, meaning it cannot depend on a chosen basis on any of the
four labeled `C^2` factors, then it must be invariant under the independent
local frame group

`U(2)_t × U(2)_x × U(2)_y × U(2)_z`.

That invariance alone forces

`rho_cell = I_16 / 16`.

Then the direct counting theorem gives

`c_cell = Tr((I_16/16) P_A) = 1/4`,

so the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

This is cleaner than the earlier tensor-composition packaging because the only
remaining promoted content is now:

> source-free local state assignment on the exact labeled factorized cell must
> be well-defined under independent basis changes on the four bare local
> factors.

## Why this is sharper

The previous theorem candidate used two promoted ingredients:

1. bare-factor unitary invariance on `C^2`;
2. no-cross-factor-datum tensor composition.

This note removes the second one.

It works directly on the full exact cell and uses only:

- the exact labeled factorization already present on the branch-local time-lock
  route;
- well-definedness under independent local frame changes on those factors.

So the whole issue is reduced to one question:

> on the exact time-locked factorized cell, is source-free local state
> assignment allowed to depend on a chosen local basis?

If no, traciality follows immediately.

## Inputs

This note uses the already-open branch-local surfaces:

- [PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md](./PLANCK_SCALE_WORLDTUBE_TO_BOUNDARY_CELL_COUNTING_THEOREM_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_CELL_STATE_RETAINED_DERIVATION_LANE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_LOCAL_NATURALITY_TRACIALITY_CANDIDATE_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_LOCAL_NATURALITY_TRACIALITY_CANDIDATE_2026-04-23.md)
- [PLANCK_SCALE_SOURCE_FREE_LOCAL_STATE_LAW_THEOREM_2026-04-23.md](./PLANCK_SCALE_SOURCE_FREE_LOCAL_STATE_LAW_THEOREM_2026-04-23.md)

What those already fix:

1. the branch-local direct route uses the exact four-bit time-locked cell;
2. the direct counting law is already closed;
3. the currently accepted retained-direct stack still underdetermines the
   source-free state;
4. the naturality route already suggested that basis-free local state
   assignment is the right upstream issue.

## Setup

Work on the exact labeled factorization

`H_cell = H_t ⊗ H_x ⊗ H_y ⊗ H_z`,

with each `H_mu ≅ C^2`.

Call a source-free local state assignment **frame-well-defined** if the
assigned density operator on `H_cell` is unchanged under independent basis
changes on the four labeled factors:

`rho_cell = (U_t ⊗ U_x ⊗ U_y ⊗ U_z) rho_cell (U_t ⊗ U_x ⊗ U_y ⊗ U_z)^dagger`

for every

`U_mu in U(2)`.

This is not yet a retained theorem of the accepted stack. It is the cleanest
single promoted content left after the reduction work.

## Theorem 1: independent local frame invariance forces the tracial cell state

Assume `rho_cell` is a normalized positive operator on

`H_cell = C^2_t ⊗ C^2_x ⊗ C^2_y ⊗ C^2_z`

and is invariant under the full local frame group

`U(2)_t × U(2)_x × U(2)_y × U(2)_z`.

Then

`rho_cell = I_16 / 16`.

### Proof

Let

`A = End(H_cell) = M_2(C) ⊗ M_2(C) ⊗ M_2(C) ⊗ M_2(C) = M_16(C)`.

The representation of the local frame group contains the full unitary group on
each factor separately.

If `rho_cell` is invariant under the group, then it commutes with:

- `M_2(C) ⊗ I ⊗ I ⊗ I`,
- `I ⊗ M_2(C) ⊗ I ⊗ I`,
- `I ⊗ I ⊗ M_2(C) ⊗ I`,
- `I ⊗ I ⊗ I ⊗ M_2(C)`.

These four commuting subalgebras generate the full matrix algebra `M_16(C)`.

Therefore `rho_cell` commutes with all of `M_16(C)`, so it lies in its center.

Hence

`rho_cell = lambda I_16`.

Normalization gives

`Tr(rho_cell) = 16 lambda = 1`,

so

`lambda = 1/16`.

Therefore

`rho_cell = I_16 / 16`.

## Corollary 1: quarter follows immediately

The direct counting theorem already gives

`c_cell(rho) = Tr(rho P_A)`.

So with `rho_cell = I_16 / 16` and `rank(P_A)=4`,

`c_cell = Tr((I_16 / 16) P_A) = 4/16 = 1/4`.

Hence the direct Planck route closes:

`a^2 = l_P^2`,
hence
`a = l_P`.

## Why this is the best current hostile-review target

This route is stronger than the older candidates because:

- it no longer needs a separate tensor-composition axiom;
- it works directly on the exact branch-local factorized cell;
- it reduces the open content to one well-definedness question about source-free
  local state assignment.

So the branch is now down to a single sharp challenge:

> can source-free local state on the exact labeled factorized cell depend on a
> chosen basis on any of the four bare `C^2` factors?

If hostile review agrees the answer is no, the route closes.

## Honest status

This is still branch-local science.

It is not woven through `main`, and it is not yet enough to claim a retained
axiom-native close on its own. But it is a cleaner and stronger theorem
candidate than the earlier two-premise state-law note.
