# PR #230 FH/LSZ v2 Target-Response Stability Gate

**Status:** bounded-support / v2 target-response stability passed

## Purpose

The fitted `dE/ds` response-stability diagnostic remains open.  This gate asks
a narrower production-support question: among chunks that actually carry the
v2 multi-tau target-timeseries schema, are the serialized per-configuration
target slopes stable across chunks and tau windows?

## Result

The honest v2 population passes the support gate for the positive branch
`tau=0..9`.  This narrows the response-window issue to the fitted response
surface and the still-open physics gates.

This does not authorize a readout switch.  Stable v2 target slopes are not
scalar LSZ pole derivatives, not FV/IR/model-class closure, and not a
canonical-Higgs/source-overlap identity.

## Non-Claim

This does not claim retained or `proposed_retained` top-Yukawa closure.  It
does not backfill legacy chunks001-016, does not set `kappa_s = 1`,
`cos(theta)=1`, `c2=1`, or `Z_match=1`, and does not use `H_unit`,
`yt_ward_identity`, observed targets, `alpha_LM`, plaquette, or `u0`.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_v2_target_response_stability.py
# SUMMARY: PASS=10 FAIL=0
```
