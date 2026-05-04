# YT FH/LSZ Common-Window Pooled Response Estimator

Date: 2026-05-04

PR: #230

Status: bounded support / pooled fixed-window response estimator; no readout
switch and no retained closure proposal is authorized.

## Purpose

The common-window provenance audit showed that a fixed `tau=10..12` window
stabilizes the central `dE/ds` slope across ready chunks, but its initial
uncertainty field used typical per-fit covariance and remained
non-production-grade.  This note records a stricter support estimator using
independent chunk-to-chunk scatter.

## Result

At 46 ready chunks:

- fixed-window mean response: `1.4256769178257236`
- empirical standard error from chunk scatter: `0.001157062859635867`
- relative standard error: `0.0008115884077021353`

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_common_window_pooled_response_estimator.py
# SUMMARY: PASS=9 FAIL=0
```

The pooled fixed-window estimator is production-grade as an uncertainty
estimate for the fixed-window central response.  It retires only the
estimator-uncertainty sub-blocker inside the common-window gate.

## Claim Boundary

This is not physical `y_t` evidence by itself.  It does not authorize a
response readout switch, does not supply scalar-LSZ normalization, does not
establish finite-source-linearity, and does not prove `O_sp = O_H`.

Forbidden shortcuts remain unused: `H_unit`, `yt_ward_identity`, observed top
mass or observed `y_t`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`,
`Z_match=1`, and `cos(theta)=1`.

Exact next action: rerun the common-window gate with this estimator as a
parent.  Remaining blockers are finite-source-linearity, response-window
acceptance, fitted/replacement response stability, scalar-LSZ, and
canonical-Higgs/source-overlap closure.
