# Universal GR Casimir Block Localization on `PL S^3 x R`

**Claim type:** positive_theorem
**Status:** exact support theorem; audit status is set only by the independent audit lane
**Date:** 2026-04-14
**Updated:** 2026-05-06
**Role:** direct universal route / canonical block-localization theorem step
**Script:** `scripts/frontier_universal_gr_casimir_block_localization.py` (PASS=8 FAIL=0 on current worktree)

## Verdict

The direct universal route has a canonical lapse / shift / trace / shear
block split at the representation level.

Equivalently, the route has a canonical block-localization operator onto the
lapse / shift / trace / shear channels.

The previous packet only asserted the Casimir spectrum. This note now fixes
the actual symmetric `3+1` representation, the invariant `Pi_A1` projector,
the complement generators, the Casimir, and the four projectors used by the
claim.

This is a block-localization theorem, not a full GR theorem. It does not choose
a basis inside the shift or shear irreps, and it does not identify the
block-localized universal Hessian with the Einstein/Regge operator.

## Representation Fixed in the Packet

Use coordinate order `(t, x, y, z)` and the Frobenius inner product on real
symmetric `4 x 4` perturbations. The runner constructs the following
orthonormal polarization basis:

1. `e_0 = h_tt` (lapse)
2. `e_1,e_2,e_3 = h_tx,h_ty,h_tz` (shift)
3. `e_4 = (h_xx + h_yy + h_zz) / sqrt(3)` (spatial trace)
4. `e_5 = (h_xx - h_yy) / sqrt(2)`
5. `e_6 = (h_xx + h_yy - 2 h_zz) / sqrt(6)`
6. `e_7,e_8,e_9 = h_xy,h_xz,h_yz`

Here the off-diagonal symmetric tensors are normalized as
`(E_ab + E_ba) / sqrt(2)`.

Spatial rotations act by

`rho(R) h = R^T h R`,

with `R = diag(1, R_3)` and `R_3 in SO(3)`. The infinitesimal generators are

`(G_a)_{ij} = <e_i, A_a^T e_j + e_j A_a>`,

where `A_a` is the embedded skew generator for rotations around spatial axis
`a`.

## A1 Projector

In this basis,

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

So `Pi_A1` fixes exactly the lapse and spatial-trace channels. The runner
checks that `Pi_A1` has no generator mixing with its complement:

`A1_complement_mixing_zero = True`.

Thus the 8D complement is an invariant `SO(3)` subrepresentation, not an
extra chosen definition.

## Complement Casimir

Order the complement as

`(h_tx,h_ty,h_tz, q_1,q_2,h_xy,h_xz,h_yz)`,

where `q_1 = (h_xx-h_yy)/sqrt(2)` and
`q_2 = (h_xx+h_yy-2h_zz)/sqrt(6)`.

The runner constructs

`C = G_x^2 + G_y^2 + G_z^2`

on this complement. The computed matrix is diagonal in the displayed
complement order:

`diag(C) = (-2,-2,-2,-6,-6,-6,-6,-6)`,

with off-diagonal entries exactly zero. Therefore the exact spectrum is:

- `-2` with multiplicity `3`;
- `-6` with multiplicity `5`.

With the real anti-Hermitian convention used here, these are `-j(j+1)` for:

- `j=1`: the shift-vector block;
- `j=2`: the traceless spatial-shear block.

## Canonical Block Projectors

The spectral projectors of the complement Casimir give:

- `P_lapse = diag(1,0,0,0,0,0,0,0,0,0)`;
- `P_shift = diag(0,1,1,1,0,0,0,0,0,0)`;
- `P_trace = diag(0,0,0,0,1,0,0,0,0,0)`;
- `P_shear = diag(0,0,0,0,0,1,1,1,1,1)`.

The runner checks:

- ranks: `1,3,1,5`;
- completeness: `True`;
- orthogonality: `True`;
- idempotence: `True`;
- commutation with `G_x,G_y,G_z`: `True`.

So the four projectors are exact, orthogonal, complete, and canonical under
the displayed universal `SO(3)` action.

## What This Does and Does Not Close

Closed here:

- the invariant `A1` core is lapse plus spatial trace;
- the complement is an actual `SO(3)` representation;
- its Casimir splits the complement into the `j=1` shift block and `j=2`
  traceless-shear block;
- the resulting four block projectors are explicit and checkable.

Not closed here:

- no preferred basis is chosen inside the degenerate `j=1` or `j=2` blocks;
- no full complement-frame bundle or distinguished connection is claimed;
- no Einstein/Regge dynamics identification is claimed.

The old blocker asking for a full canonical complement frame was too strong
for block localization. The remaining GR route question is whether the
canonical block-localized universal Hessian matches the Einstein/Regge law
blockwise, or whether an additional theorem is needed inside the shift/shear
channels.

## Source Dependencies

This section records the source authorities and runner needed for a
restricted-packet re-audit. It does not promote this note by itself.

- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [S3_ANOMALY_SPACETIME_LIFT_NOTE.md](S3_ANOMALY_SPACETIME_LIFT_NOTE.md)
- [UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md](UNIVERSAL_GR_TENSOR_VARIATIONAL_CANDIDATE_NOTE.md)
- [UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md](UNIVERSAL_GR_TENSOR_QUOTIENT_UNIQUENESS_NOTE.md)
- [UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md](UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md)
- `scripts/frontier_universal_gr_casimir_block_localization.py`
