# Universal GR Block-Constraint Interpretation on `PL S^3 x R`

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / constraint interpretation test  
**Ownership:** universal constraint interpretation only

## Verdict

The canonical block-localization theorem is strong enough to give a
canonical Hamiltonian/momentum-constraint interpretation at the block
level.

The exact universal block structure is:

- lapse block;
- shift block;
- spatial trace block;
- traceless shear block.

In the canonical symmetric `3+1` basis, the invariant core is the exact
rank-2 `A1` projector

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

The remaining complement then splits canonically by the universal `SO(3)`
Casimir into:

- shift (`j=1`, rank 3);
- traceless shear (`j=2`, rank 5).

So the lapse and shift blocks now admit a canonical constraint interpretation
on the direct universal route:

- the Hamiltonian-constraint sector is the exact `A1` core
  (`lapse + spatial trace`);
- the momentum-constraint sector is the exact `j=1` shift block.

This is the strongest exact statement currently supported by the universal
route.

## What is exact already

The universal stack already gives:

1. the scalar observable generator `W[J] = log|det(D+J)| - log|det D|`;
2. the exact `PL S^3 x R` lift;
3. the exact tensor-valued variational candidate
   `S_GR^cand[h] := 1/2 * D^2 W[g_*](h, h)`;
4. the exact symmetric `3+1` quotient-kernel uniqueness;
5. the exact invariant section `Pi_A1`;
6. the exact canonical block-localization into lapse, shift, trace, and
   traceless shear.

That means the universal route no longer lacks a canonical block split.

## Constraint interpretation

The direct universal route now supports the following block-constraint
reading:

- the `A1` core is the Hamiltonian block;
- the `j=1` complement block is the momentum block;
- the trace/shear split is canonical and orthogonal inside the remaining
  spatial sector.

So, if the question is only whether lapse/shift blocks admit a canonical
Hamiltonian/momentum-constraint interpretation, the answer is yes.

## Exact remaining gap

The canonical block split is not yet the same thing as a full Einstein/Regge
derivation.

The remaining gap is:

> the atlas still does not canonically identify the block-localized
> universal Hessian with the Einstein/Regge constraint operator, including
> the exact normalization/sign convention on the `E \oplus T1` complement.

Equivalently:

- block localization is exact;
- constraint-sector interpretation is exact;
- operator-level Einstein/Regge identification is still open.

## Honest status

The direct universal route is now:

- exact at the scalar observable level;
- exact at the `3+1` kinematic lift level;
- exact at the symmetric quotient-kernel level;
- exact at the invariant `A1` projector level;
- exact at the canonical block-localization level;
- still missing the final operator-identification theorem for full GR.

