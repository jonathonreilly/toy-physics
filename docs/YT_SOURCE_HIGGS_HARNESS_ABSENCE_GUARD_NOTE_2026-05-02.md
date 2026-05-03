# Source-Higgs Harness Default-Off Guard

**Status:** bounded-support / source-Higgs harness default-off guard
**Runner:** `scripts/frontier_yt_source_higgs_harness_absence_guard.py`
**Certificate:** `outputs/yt_source_higgs_harness_absence_guard_2026-05-02.json`

## Purpose

The `C_sH` / `C_HH` Gram-purity route remains one of the cleanest possible
ways to certify source-pole purity, but it requires a same-surface canonical
Higgs operator.  This block adds an explicit production-certificate guard so
future `C_ss` outputs cannot be mistaken for `O_H`, `C_sH`, or `C_HH`
evidence.

## Result

The production harness certificate now has a default-off
`source_higgs_cross_correlator` metadata block.  The block is enabled only when
`--source-higgs-cross-modes`, `--source-higgs-cross-noises`, and
`--source-higgs-operator-certificate` are all supplied.  The required-object
list names `O_H`, `C_sH(q)`, `C_HH(q)`, and same-ensemble covariance, and the
certificate still records that finite rows must not be used as a physical
Yukawa readout.

This is instrumentation support only.  It does not supply a canonical `O_H`
identity certificate, pole residues, covariance, Gram-purity data, or retained
closure.

## Verification

```bash
python3 scripts/frontier_yt_source_higgs_harness_absence_guard.py
# SUMMARY: PASS=13 FAIL=0
```

Next action: supply or derive an audit-acceptable canonical-Higgs operator
certificate, run source-Higgs cross-correlator measurements, extract pole
residues, then pass the Gram-purity and retained-route gates.
