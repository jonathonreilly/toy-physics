# W/Z Response Harness Absence Guard

**Status:** bounded-support / WZ response harness absence guard  
**Runner:** `scripts/frontier_yt_wz_response_harness_absence_guard.py`  
**Certificate:** `outputs/yt_wz_response_harness_absence_guard_2026-05-02.json`

## Purpose

The same-source W/Z response route can cancel `kappa_s` only if the repo
measures W/Z mass response under the same scalar source and supplies the
sector-overlap / canonical-Higgs identity certificates.  This block adds an
explicit production-certificate guard so the current QCD top harness cannot be
mistaken for that evidence.

## Result

The production certificate now has a `wz_mass_response` metadata block with
`enabled: false`, `implementation_status: absent_guarded`, and required objects
for same-source W/Z mass fits, `dM_W/ds` or `dM_Z/ds`, covariance with
`dE_top/ds`, and identity certificates.

This is instrumentation support only.  It does not implement W/Z correlators,
W/Z source slopes, covariance, sector-overlap identity, canonical-Higgs
identity, or retained closure.

## Verification

```bash
python3 scripts/frontier_yt_wz_response_harness_absence_guard.py
# SUMMARY: PASS=12 FAIL=0
```

Next action: implement actual W/Z response observables with identity
certificates, implement same-surface `O_H`/`C_sH`/`C_HH` rows, derive a
source-Higgs identity theorem, or process FH/LSZ chunks.
