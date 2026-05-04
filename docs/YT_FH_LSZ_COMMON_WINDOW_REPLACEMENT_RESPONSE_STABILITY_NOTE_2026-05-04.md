# YT FH/LSZ Common-Window Replacement Response Stability

Date: 2026-05-04

PR: #230

Status: bounded support / replacement response-stability passed; no readout
switch and no retained closure proposal is authorized.

## Purpose

The original response-window acceptance gate required full ready-set v2
per-configuration covariance.  Legacy chunks001-016 cannot be honestly
backfilled to that schema.  This note records a replacement response-stability
contract that uses the fixed `tau=10..12` common-window response over the full
ready chunk set instead of fabricating legacy v2 rows.

## Result

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_common_window_replacement_response_stability.py
# SUMMARY: PASS=14 FAIL=0
```

The replacement support path passes because:

- the common-window response covers all 46 ready chunks;
- target-observable ESS and autocorrelation ESS are passed;
- legacy v2 backfill is honestly blocked;
- fixed-window central stability is passed;
- pooled common-window uncertainty is production-grade;
- finite-source-linearity is available as bounded response support.

## Claim Boundary

This is a response-stability support path only.  It does not authorize a
physical readout switch, does not supply scalar-LSZ normalization, does not
identify `O_sp = O_H`, and does not derive physical `y_t`.

Forbidden shortcuts remain unused: `H_unit`, `yt_ward_identity`, observed top
mass or observed `y_t`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`,
`Z_match=1`, and `cos(theta)=1`.

Exact next action: use this as the replacement response-stability parent for
the common-window response gate.  Remaining blockers are scalar-LSZ pole
control, FV/IR/model-class control, and canonical-Higgs/source-overlap
closure.
