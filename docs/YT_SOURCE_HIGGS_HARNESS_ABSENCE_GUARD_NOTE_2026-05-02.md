# Source-Higgs Harness Absence Guard

**Status:** bounded-support / source-Higgs harness absence guard  
**Runner:** `scripts/frontier_yt_source_higgs_harness_absence_guard.py`  
**Certificate:** `outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json`

## Purpose

The `C_sH` / `C_HH` Gram-purity route remains one of the cleanest possible
ways to certify source-pole purity, but it requires a same-surface canonical
Higgs operator.  This block adds an explicit production-certificate guard so
future `C_ss` outputs cannot be mistaken for `O_H`, `C_sH`, or `C_HH`
evidence.

## Result

The production harness certificate now has a `source_higgs_cross_correlator`
metadata block with `enabled: false`, `implementation_status:
absent_guarded`, and a required-object list naming `O_H`, `C_sH(q)`,
`C_HH(q)`, and same-ensemble covariance.  It also records that the canonical
Higgs operator realization is absent and that the output must not be used as a
physical Yukawa readout.

This is instrumentation support only.  It does not implement `O_H`, `C_sH`,
`C_HH`, pole residues, covariance, Gram-purity data, or retained closure.

## Verification

```bash
python3 scripts/frontier_yt_source_higgs_harness_absence_guard.py
# SUMMARY: PASS=13 FAIL=0
```

Next action: implement an actual same-surface `O_H` observable and
`C_sH`/`C_HH` rows, derive a source-Higgs identity theorem, implement W/Z
response with identity certificates, or process FH/LSZ chunks.
