# PR #230 FH/LSZ Affine-Contact Complete-Monotonicity No-Go

**Status:** exact negative boundary / affine contact complete-monotonicity
no-go
**Runner:**
`scripts/frontier_yt_fh_lsz_affine_contact_complete_monotonicity_no_go.py`
**Certificate:**
`outputs/yt_fh_lsz_affine_contact_complete_monotonicity_no_go_2026-05-05.json`

## Claim

The current polefit8x8 rows cannot be repaired into a positive Stieltjes
scalar-LSZ object by an affine local contact subtraction.

The earlier contact-subtraction boundary showed that finite first-order
monotonicity restoration does not identify the affine contact slope.  This
block tests the stronger necessary condition.  A positive Stieltjes transform
is completely monotone, so for ordered shell points its divided differences
obey

```text
(-1)^k C[x_i, ..., x_{i+k}] >= 0 .
```

For an affine contact family

```text
C_a(x) = C_raw(x) - a x ,
```

the slope `a` changes only first divided differences.  All second and higher
divided differences are invariant under the affine subtraction.  On the
current combined polefit8x8 rows those higher finite complete-monotonicity
signs have robust violations.  Therefore no affine contact slope can provide
the missing contact-subtracted scalar two-point certificate.

## Boundary

This closes only the affine-contact repair route.  It does not rule out a
higher-polynomial contact certificate, a microscopic scalar-denominator
theorem, or a strict Stieltjes moment-threshold-FV certificate from future
same-surface data.

No retained or proposed-retained top-Yukawa closure is authorized.  The runner
does not set `kappa_s=1`, `c2=1`, or `Z_match=1`, and it does not use H-unit,
Ward authority, observed targets, `alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_affine_contact_complete_monotonicity_no_go.py
python3 scripts/frontier_yt_fh_lsz_affine_contact_complete_monotonicity_no_go.py
# SUMMARY: PASS=11 FAIL=0
```
