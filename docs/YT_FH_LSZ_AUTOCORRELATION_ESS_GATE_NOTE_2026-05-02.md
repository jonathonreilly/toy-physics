# PR #230 FH/LSZ Autocorrelation ESS Gate

**Status:** open / FH-LSZ autocorrelation ESS gate not passed  
**Runner:** `scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py`  
**Certificate:** `outputs/yt_fh_lsz_autocorrelation_ess_gate_2026-05-02.json`

## Purpose

Chunked FH/LSZ output cannot become production evidence merely because chunks
finish.  The load-bearing observables need autocorrelation and effective
sample-size certification.

## Gate

The gate requires:

- enough ready chunks for a production ESS diagnostic;
- per-configuration target time series for same-source `dE/ds`;
- per-configuration target time series for same-source `C_ss(q)` or
  `Gamma_ss(q)`;
- a blocking/bootstrap or integrated-autocorrelation certificate for those
  target observables;
- scalar LSZ, FV/IR/model-class, finite-source-linearity, and
  canonical-Higgs identity gates after target ESS is accepted.

After chunk012 and the chunk001 target-series replacement, the ready set is
`[1,2,3,4,5,6,7,8,9,10,11,12]`, so it remains above the eight-chunk count
threshold used by this gate.  The blocker is partial target-series coverage:
chunks001, 011, and 012 expose per-configuration target time series for
same-source `dE/ds` and `C_ss(q)/Gamma_ss(q)`, but chunks002-010 still do not.
The whole ready set therefore still lacks a target-observable ESS certificate.
Plaquette ESS is not a substitute for target-observable ESS.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not treat current chunks as production evidence, does not set
`kappa_s = 1`, and does not use `H_unit`, `yt_ward_identity`, observed top
mass, observed `y_t`, `alpha_LM`, plaquette, or `u0` as proof authority.

## Next Action

Continue future chunks with target time-series serialization, replace older
chunks002-010 if a same-ready-set target ESS certificate is required, or emit a
predeclared blocking/bootstrap ESS certificate.  Rerun this gate before using
chunked FH/LSZ output as production evidence.
