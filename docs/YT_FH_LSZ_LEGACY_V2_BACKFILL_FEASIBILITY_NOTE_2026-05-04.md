# PR #230 FH/LSZ Legacy v2 Backfill Feasibility Audit

**Status:** exact negative boundary / chunks001-016 cannot be honestly
v2-backfilled

## Purpose

Chunks001-016 predate the v2 multi-tau target-timeseries schema.  This audit
checks whether those legacy chunks can be upgraded from saved artifacts without
rerunning the production harness.

## Result

They cannot be honestly backfilled.  The saved chunks contain aggregate
source-shift correlators and legacy tau=1 per-configuration target rows, but
they do not store the raw per-configuration source-shift correlator time
series required to reconstruct v2 multi-tau covariance rows.

An aggregate-only reconstruction would be a schema-padded surrogate, not the
same evidence consumed by the response-window gates.  The honest options are:

- use chunks017+ as the v2 multi-tau population for covariance diagnostics;
- rerun chunks001-016 with the current v2 harness if an all-configuration
  same-schema covariance table becomes required.

## Non-Claim

This does not claim retained or `proposed_retained` top-Yukawa closure.  It
does not set `kappa_s = 1`, `cos(theta)=1`, `c2=1`, or `Z_match=1`, and it does
not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`, plaquette,
or `u0`.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_legacy_v2_backfill_feasibility.py
# SUMMARY: PASS=10 FAIL=0
```
