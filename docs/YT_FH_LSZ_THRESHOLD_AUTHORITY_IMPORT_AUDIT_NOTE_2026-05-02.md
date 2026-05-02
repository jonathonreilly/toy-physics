# PR #230 FH/LSZ Threshold-Authority Import Audit

**Status:** exact negative boundary / FH-LSZ threshold-authority import audit
**Runner:** `scripts/frontier_yt_fh_lsz_threshold_authority_import_audit.py`
**Certificate:** `outputs/yt_fh_lsz_threshold_authority_import_audit_2026-05-02.json`

## Claim

The pole-saturation threshold gate names a possible repair, but the current PR
#230 surface does not supply that authority.

The audit checks for a pole-saturation/continuum-threshold certificate,
microscopic scalar-denominator certificate, and combined L12 production output.
All are absent.  The model-class gate and retained-route certificate remain
blocking.

## Boundary

This is not closure.  It prevents silently importing the missing threshold or
pole-saturation premise as if it were already derived.

## Verification

```bash
python3 scripts/frontier_yt_fh_lsz_threshold_authority_import_audit.py
# SUMMARY: PASS=8 FAIL=0
```
