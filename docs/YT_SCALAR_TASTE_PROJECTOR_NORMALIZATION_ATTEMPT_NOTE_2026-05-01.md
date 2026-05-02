# Scalar Taste-Projector Normalization Theorem Attempt

**Date:** 2026-05-01
**Status:** exact negative boundary / scalar taste-projector normalization theorem attempt blocked
**Runner:** `scripts/frontier_yt_scalar_taste_projector_normalization_attempt.py`
**Certificate:** `outputs/yt_scalar_taste_projector_normalization_attempt_2026-05-01.json`

## Purpose

After color-singlet `q=0` cancellation, finite-`q` IR regularity, and the
zero-mode-removed ladder search, the finite pole witnesses were narrowed to a
taste/projector problem.  This block asks whether the `Cl(3)/Z^3` source
surface itself supplies the scalar taste/projector normalization needed for a
retained scalar pole or LSZ claim.

## Result

```text
python3 scripts/frontier_yt_scalar_taste_projector_normalization_attempt.py
# SUMMARY: PASS=8 FAIL=0
```

The executable check separates an algebraic fact from a physical closure
claim:

| Check | Result |
|---|---|
| BZ taste corners | `16` |
| unnormalized local corner-sum norm squared | `16` |
| unit taste-singlet norm squared | `1` |
| ladder scale from local sum to unit singlet | `1/16` |
| finite crossings after unit-singlet normalization | none |
| current source-unit theorem fixes canonical Higgs metric | no |
| current taste-carrier import audit admits non-origin corners | no |

The unit-norm taste singlet is straightforward:

```text
O_singlet = (1/sqrt(16)) sum_t O_t
```

But this does not identify the physical scalar carrier or fix the
source-to-canonical-Higgs LSZ normalization.  The source term can be written as
`s O_local = (sqrt(16) s) O_singlet`, so the factor can be moved into the
source coordinate unless the canonical scalar metric or pole residue is
derived.

## Claim Boundary

This is not retained or proposed-retained `y_t` closure.  It does not set
`kappa_s = 1`, use `H_unit`, use `yt_ward_identity`, select by observed top
mass or observed `y_t`, or import alpha/plaquette/`u0`, `c2 = 1`, or
`Z_match = 1`.

The next positive route is now even narrower: derive the physical scalar
taste/carrier projection and projector normalization from the retained
`Cl(3)/Z^3` source functional together with the interacting pole derivative,
or measure that same-source pole derivative in production FH/LSZ data.
