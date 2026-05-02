# Source-Higgs Cross-Correlator Production Manifest

**Status:** bounded-support / source-Higgs cross-correlator production manifest  
**Runner:** `scripts/frontier_yt_source_higgs_cross_correlator_manifest.py`  
**Certificate:** `outputs/yt_source_higgs_cross_correlator_manifest_2026-05-02.json`

## Purpose

The source-Higgs purity route needs a concrete production schema before it can
be attempted honestly.  This manifest records the minimum same-ensemble
measurements required to evaluate `Res(C_sH)^2 = Res(C_ss) Res(C_HH)` at an
isolated scalar pole.

## Result

The manifest is support only.  The current production harness emits
same-source `C_ss` support, but it does not emit a same-surface canonical
Higgs operator `O_H`, `C_sH`, or `C_HH` rows.  No future `C_sH` production
certificate exists.

Required future evidence includes:

- `C_ss(q)`, `C_sH(q)`, and `C_HH(q)` on the same ensemble and momentum shells;
- a certified same-surface canonical-Higgs radial operator `O_H`;
- covariance across `C_ss`, `C_sH`, `C_HH`, and `dE_top/ds`;
- isolated-pole fit or accepted model-class/pole-saturation certificate;
- finite-volume, IR, zero-mode, and retained-route claim gates.

## Claim Boundary

This is not retained or proposed-retained closure.  It does not use `H_unit`
as `O_H`, static EW algebra, observed targets, `yt_ward_identity`,
`alpha_LM`, plaquette, or `u0`, and it does not set `kappa_s = 1`,
`cos(theta)=1`, `c2 = 1`, or `Z_match = 1`.

## Verification

```bash
python3 scripts/frontier_yt_source_higgs_cross_correlator_manifest.py
# SUMMARY: PASS=13 FAIL=0
```

Next action: implement `O_H` / `C_sH` / `C_HH` measurement rows using this
schema, or continue W/Z response, rank-one purity theorem, or seed-controlled
FH/LSZ chunk processing.
