# YT FH/LSZ Common-Window Response Provenance

Date: 2026-05-04

PR: #230

Status: bounded support / response-window provenance; no closure proposal is
authorized.

## Purpose

The FH/LSZ production chunks expose stable target-observable time series, but
the fitted `dE/ds` source-response surface is unstable.  This note records a
provenance audit of that instability.

## Result

The instability is controlled by the production fitter's per-source-shift fit
window selection.

At the 46-ready-chunk checkpoint:

- original fitted slopes are unstable: relative stdev `0.9039685737574564`
- original fit-window signatures split into multiple tau-min classes
- high original slopes (`dE/ds > 3`) occur only in mixed-window chunks
- recomputing every source shift with the same late window `tau=10..12`
  gives a stable common-window slope surface:
  - mean `1.4256769178257236`
  - relative stdev `0.005504460391515086`
  - spread ratio `1.0237482352916702`

Verification:

```bash
python3 scripts/frontier_yt_fh_lsz_common_window_response_provenance.py
# SUMMARY: PASS=11 FAIL=0
```

## Claim Boundary

This is not a physical readout switch.  The common-window recomputation is a
provenance/support result only.

It does not derive scalar LSZ normalization, finite-source-linearity,
FV/IR/model-class control, `O_sp = O_H`, source-Higgs overlap, or physical
`y_t`.  The common-window fit uncertainty is still not production grade, and
the canonical-Higgs/source-overlap gates remain open.

Forbidden shortcuts remain unused: `H_unit`, `yt_ward_identity`, observed top
mass or observed `y_t`, `alpha_LM`, plaquette/u0, `kappa_s=1`, `c2=1`,
`Z_match=1`, and `cos(theta)=1`.

Exact next action: promote this provenance finding into a predeclared
common-window response gate or postprocessor, then require finite-source-
linearity, scalar-pole model/FV/IR control, and canonical-Higgs identity before
any physical top-Yukawa readout.
