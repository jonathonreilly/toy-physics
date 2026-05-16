# Universal GR Isotropic Schur Localization on `PL S^3 x R`

**Claim type:** bounded_theorem
**Status:** bounded exact isotropic Schur-localization step; not a standalone full-GR closure theorem
**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Role:** direct universal route / isotropic background theorem step
**Primary runner:** [`scripts/frontier_universal_gr_isotropic_schur_localization.py`](../scripts/frontier_universal_gr_isotropic_schur_localization.py) (PASS=6/0)
**Runner cache:** [`logs/runner-cache/frontier_universal_gr_isotropic_schur_localization.txt`](../logs/runner-cache/frontier_universal_gr_isotropic_schur_localization.txt) (SHA-pinned to the runner)

## Bridge inputs (self-contained restricted packet)

This section makes the audit packet stand alone. Everything used in the
verdict, the localization, and the closed-form coefficient block below is
defined explicitly here and is also verified numerically in the runner's
T1-T6 checks. No claim depends on an unregistered upstream object.

### B1. Scalar generator and its second derivative

The exact observable-principle generator on a positive symmetric source
`D` (cf. [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md))
is

`W[D + J] - W[D] = log|det(D + J)| - log|det D|`.

For symmetric perturbations `h, k`, the unique algebraic Hessian is

`B(h, k) := D^2 W[D](h, k) = - tr(D^{-1} h D^{-1} k)`.

This is a straightforward chain-rule consequence of
`d log|det X| / dX_{ij} = (X^{-1})_{ji}` and
`d (X^{-1})_{ki} / dX_{ab} = - (X^{-1})_{ka} (X^{-1})_{bi}`. The runner
realizes this exact bilinear in `bilinear(a, b, d)`.

### B2. Symmetric 3+1 basis (10 canonical polarizations)

The canonical orthonormal basis of `Sym^2(R^{3+1})` on which the rest of
the note works, ordered `[lapse, shift_1, shift_2, shift_3, trace,
shear^{(0)}_1, shear^{(0)}_2, shear^{off}_1, shear^{off}_2, shear^{off}_3]`:

```
e_0  = E_{00}                                            # lapse
e_1  = (E_{01} + E_{10}) / sqrt(2)                       # shift_1
e_2  = (E_{02} + E_{20}) / sqrt(2)                       # shift_2
e_3  = (E_{03} + E_{30}) / sqrt(2)                       # shift_3
e_4  = diag(0, 1, 1, 1) / sqrt(3)                        # spatial trace
e_5  = diag(0, 1, -1, 0) / sqrt(2)                       # diagonal shear A
e_6  = diag(0, 1, 1, -2) / sqrt(6)                       # diagonal shear B
e_7  = (E_{12} + E_{21}) / sqrt(2)                       # off-diagonal shear xy
e_8  = (E_{13} + E_{31}) / sqrt(2)                       # off-diagonal shear xz
e_9  = (E_{23} + E_{32}) / sqrt(2)                       # off-diagonal shear yz
```

where `E_{ij}` is the standard 4x4 matrix unit. The basis is orthonormal
under the Frobenius inner product. The runner constructs this in
`canonical_polarization_frame()`.

### B3. Block projectors (explicit 10x10 matrices)

In the basis above, the four canonical block projectors are the diagonal
indicator matrices:

`P_lapse  = diag(1, 0, 0, 0, 0, 0, 0, 0, 0, 0)`  (rank 1)

`P_shift  = diag(0, 1, 1, 1, 0, 0, 0, 0, 0, 0)`  (rank 3)

`P_trace  = diag(0, 0, 0, 0, 1, 0, 0, 0, 0, 0)`  (rank 1)

`P_shear  = diag(0, 0, 0, 0, 0, 1, 1, 1, 1, 1)`  (rank 5)

They are orthogonal idempotents and sum to `I_{10}`. The invariant `A1`
projector is `Pi_A1 = P_lapse + P_trace = diag(1,0,0,0,1,0,0,0,0,0)`,
as recorded in [`UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md`](UNIVERSAL_GR_A1_INVARIANT_SECTION_NOTE.md).

The shift block (rank 3) and shear block (rank 5) are the unique
irreducible isotypic components of `Sym^2(R^4)` under the natural `SO(3)`
action on the spatial subspace `{e_1, e_2, e_3}`, as enforced by the
Casimir spectral split implemented in `block_projectors()` (eigenvalue
`-2` for shift, `-6` for shear).

### B4. Hessian matrix entries on `D = diag(a, b, b, b)`

Substituting `D^{-1} = diag(a^{-1}, b^{-1}, b^{-1}, b^{-1})` into
`B(h, k) = - tr(D^{-1} h D^{-1} k)` and evaluating on the basis above
gives the closed-form `10x10` matrix `H`. The non-zero entries are exactly:

- `H_{00} = -a^{-2}`                       (lapse <-> lapse)
- `H_{11} = H_{22} = H_{33} = -(ab)^{-1}` (shift <-> shift, each axis)
- `H_{44} = -b^{-2}`                       (trace <-> trace)
- `H_{55} = H_{66} = -b^{-2}`              (diagonal shear <-> diagonal shear)
- `H_{77} = H_{88} = H_{99} = -b^{-2}`     (off-diagonal shear <-> off-diagonal shear)

All other entries are zero. The proof is direct evaluation: for the
shift entry `e_1 = (E_{01} + E_{10})/sqrt(2)`, the trace
`tr(D^{-1} e_1 D^{-1} e_1) = 2 * (1/sqrt(2))^2 * (D^{-1})_{00}(D^{-1})_{11}
= a^{-1} b^{-1}`; the off-diagonal and diagonal shear cases reduce to
the spatial entries `b^{-1}` only, giving `b^{-2}`. The runner verifies
this with `max closed-form coefficient error = 3.33e-16`.

### B5. Schur localization and vanishing-leakage corollary

Because `H` is diagonal in the basis of B2 with the block-constant
spectrum of B4, it commutes with every diagonal projector that respects
the spectral split. In particular:

- `[P_lapse, H] = [P_shift, H] = [P_trace, H] = [P_shear, H] = 0`.

The off-block leakages are then immediate:

- `P_lapse H P_shift = 0` because columns of `P_shift` are zero on row 0;
- `P_trace H P_shear = 0` because column 4 of `P_shear` is zero and
  rows `5..9` of `H` are zero in column 4 (`H` is diagonal);
- `P_shift H P_shear = 0` by the same diagonal argument.

The runner certifies all three leakage norms at `0.000e+00` and the four
commutators at `0.000e+00`, so the algebraic Schur localization is exact
(not only numerically zero but provably zero by inspection of the
diagonal form derived in B4).

## Verdict

The direct universal branch is stronger than the recent anisotropic
prototype audit suggested.

On the exact `PL S^3 x R` route, the lifted background is spatially
`SO(3)`-invariant. That forces the background source to lie entirely in the
exact `A1` core:

- lapse
- spatial trace

Equivalently, any invariant lifted background has the form

`diag(a,b,b,b)`.

On that exact invariant background, the universal Hessian candidate

`B(h,k) = D^2 W[g_*](h,k)`

Schur-localizes exactly under the canonical block projectors

- `P_lapse`
- `P_shift`
- `P_trace`
- `P_shear`

and the old `trace <-> shear` mixer disappears identically.

So the previous rank-1 trace-shear obstruction was a feature of the
anisotropic toy prototype `diag(2,3,5,7)`, not the invariant direct
universal background.

## Exact invariant-background theorem

The direct universal route already had:

- exact scalar generator `W[J] = log|det(D+J)| - log|det D|`
- exact `3+1` lift `PL S^3 x R`
- exact invariant `A1` projector
- exact Casimir block split into lapse / shift / trace / shear

The missing step was to apply the route's own spatial symmetry to the
background point.

Under valid spatial rotations, the fixed subspace on the symmetric `3+1`
source representation is exactly the 2D `A1` core. Therefore any
`SO(3)`-invariant lifted background must be of the form

`diag(a,b,b,b)`.

That is the only spatially isotropic background family compatible with the
direct universal route.

## Exact Schur localization

For `D = diag(a,b,b,b)`, the universal Hessian candidate on the canonical
symmetric `3+1` basis satisfies:

- `P_lapse H = H P_lapse`
- `P_shift H = H P_shift`
- `P_trace H = H P_trace`
- `P_shear H = H P_shear`

and all cross-block leakages vanish:

- lapse `↔` shift = `0`
- shift `↔` shear = `0`
- trace `↔` shear = `0`

So the canonical block split is exact on the invariant background.

The shift and shear blocks are also exact scalar Schur blocks.

## Closed-form block coefficients

On `D = diag(a,b,b,b)`, the block coefficients are exactly:

- `alpha_lapse = -a^-2`
- `alpha_shift = -(ab)^-1`
- `alpha_trace = -b^-2`
- `alpha_shear = -b^-2`

So the entire direct-universal Hessian takes the exact block form

`H = alpha_lapse P_lapse + alpha_shift P_shift + alpha_trace P_trace + alpha_shear P_shear`.

In particular:

- the shift block is exact and isotropic
- the traceless-shear block is exact and isotropic
- the trace and shear coefficients already agree exactly on the invariant
  background

## What this changes

This removes the strongest recent direct-universal blocker.

Before:

> the universal branch still had a rank-1 `trace <-> shear` mixer.

Now:

> on the correct `SO(3)`-invariant lifted background, the universal Hessian
> already Schur-localizes exactly into lapse / shift / trace / shear.

So the direct universal route is no longer blocked by complement
canonicalization or by trace-shear leakage on the invariant background.

## Remaining open issue

This still does **not** finish full GR.

What remains is smaller:

> identify the already-localized isotropic universal Hessian with the
> Einstein/Regge operator, including the final normalization/sign
> interpretation on the invariant `PL S^3 x R` background.

That is now an operator-identification problem, not a localization problem.

## Honest status

The current direct universal route is now:

- exact at the scalar observable level
- exact at the `3+1` lift level
- exact at the quotient-kernel level
- exact at the canonical block-localization level
- exact at the invariant-background Schur-localization level
- still open only at the final Einstein/Regge operator identification level
