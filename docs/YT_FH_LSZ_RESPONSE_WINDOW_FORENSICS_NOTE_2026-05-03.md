# PR #230 FH/LSZ Response-Window Forensics

**Status:** bounded-support / FH-LSZ response-window forensics
**Runner:** `scripts/frontier_yt_fh_lsz_response_window_forensics.py`
**Certificate:** `outputs/yt_fh_lsz_response_window_forensics_2026-05-03.json`

## Purpose

The target-observable ESS gate now passes for chunks001-026, but the ready
chunk response-stability diagnostic still fails on the fitted `dE/ds` central
values.  This runner compares that fitted response surface with the serialized
per-configuration tau=1 effective-energy response target series.

## Result

```text
python3 scripts/frontier_yt_fh_lsz_response_window_forensics.py
# SUMMARY: PASS=10 FAIL=0
```

The fitted-slope surface remains unstable:

```text
n = 26
mean = 2.4505744350486798
relative_stdev = 0.8963361077055534
spread_ratio = 5.920283844112204
median = 1.4287544738947873
```

The tau=1 target diagnostic is stable across the same chunks:

```text
n = 26
mean = 1.245795387237233
relative_stdev = 0.006279954340116946
spread_ratio = 1.0229374224682368
median = 1.245909205954382
```

This identifies a response-window/readout-selection blocker.  It does not
authorize switching the production FH response readout from the fitted slope to
the tau=1 target diagnostic.

## Claim Boundary

This is forensics only.  It does not claim retained or `proposed_retained`
closure, does not replace the production response readout by fiat, does not
set `kappa_s = 1`, and does not use `H_unit`, Ward authority, observed target
values, `alpha_LM`, plaquette, or `u0` as proof inputs.

Even a passed future response-window acceptance gate would still require
scalar-pole derivative/model-class/FV/IR control and canonical-Higgs
source-overlap identity before physical `y_t` closure.

## Next Action

Add a predeclared FH response-window acceptance gate that compares multiple
effective-mass tau windows, fit windows, and source radii with covariance, then
rerun response stability.  In parallel, keep the scalar-pole/FV/IR/model-class
and canonical-Higgs identity gates as separate blockers.

## Follow-Up

The response-window acceptance gate now exists and is not passed.  Chunk-level
tau-window central values are stable across tau windows 0-9, but
per-configuration multi-tau covariance and multiple source radii are absent, so
no production readout switch is authorized.
