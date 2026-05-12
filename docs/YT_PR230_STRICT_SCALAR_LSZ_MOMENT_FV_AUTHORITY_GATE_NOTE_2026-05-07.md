# PR #230 Strict Scalar-LSZ Moment/FV Authority Gate

**Status:** exact negative boundary / current two-source taste-radial raw `C_ss` rows do not supply strict scalar-LSZ moment/FV authority
**Runner:** `scripts/frontier_yt_pr230_strict_scalar_lsz_moment_fv_authority_gate.py`
**Certificate:** `outputs/yt_pr230_strict_scalar_lsz_moment_fv_authority_gate_2026-05-07.json`

## Claim

The completed two-source taste-radial chunks001-063 contain real selected-mass
scalar-source rows, but the raw `C_ss(q^2)` proxy is not the strict
scalar-LSZ Stieltjes object needed for a moment/threshold/FV authority row.

For an unsubtracted positive Stieltjes two-point object,

```text
C(x) = int dmu(s) / (x + s),        dmu(s) >= 0,        x = q_hat^2,
```

one has

```text
C(x2) - C(x1) <= 0        whenever x2 > x1.
```

The runner reads the current completed two-source taste-radial chunks through
the manifest and combiner, then compares the zero mode to the first momentum
shell.  The raw rows are positive, but the first-shell mean is larger than the
zero-mode mean across every ready chunk.

## Current Result

The certificate records:

- `ready_chunks = 63`, `expected_chunks = 63`;
- `volumes = ["12x24"]`, so no multivolume FV/IR authority is present;
- `raw_c_ss_rows_positive = true`;
- `current_raw_c_ss_proxy_fails_stieltjes_monotonicity = true`;
- `strict_scalar_lsz_moment_fv_authority_present = false`;
- `proposal_allowed = false`.

The chunk-scatter comparison gives a strong diagnostic separation:

```text
zero-mode mean C_ss  = 0.12238486128795699
first-shell mean     = 0.12533524692598016
shell - zero         = 0.002950385638023171
z-score              = 195.191222800661
```

## Boundary

This is not a global theorem against scalar LSZ.  It blocks only the shortcut
that would treat the current raw `C_ss` proxy as the strict scalar-LSZ
moment/FV authority object.

The positive route remains:

1. derive or measure a contact-subtracted or denominator-derived scalar
   two-point object whose Stieltjes/moment checks are load-bearing;
2. supply threshold-gap and multivolume FV/IR authority;
3. connect that scalar object to canonical `O_H/C_sH/C_HH` pole rows, or
   bypass it through genuine same-source W/Z response rows.

No retained or proposed-retained top-Yukawa closure is authorized.  The gate
does not set `kappa_s`, `c2`, or `Z_match` to one and does not use `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette/`u0`, or observed top/y_t inputs.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_strict_scalar_lsz_moment_fv_authority_gate.py
python3 scripts/frontier_yt_pr230_strict_scalar_lsz_moment_fv_authority_gate.py
# SUMMARY: PASS=13 FAIL=0
```
