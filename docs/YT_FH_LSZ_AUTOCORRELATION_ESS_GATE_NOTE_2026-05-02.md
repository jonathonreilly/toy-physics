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

After the chunk001 through chunk010 target-series replacements and existing
chunk011/chunk012 target-series chunks, the ready set is
`[1,2,3,4,5,6,7,8,9,10,11,12]`, so it remains above the eight-chunk count
threshold used by this gate.  The earlier partial target-series coverage
blocker is repaired for the ready set: all twelve ready chunks expose
per-configuration target time series for same-source `dE/ds` and
`C_ss(q)/Gamma_ss(q)`.

The gate still does not pass because no predeclared target-observable
blocking/bootstrap or integrated-autocorrelation certificate has been emitted.
Plaquette ESS remains diagnostic only and is not a substitute for
target-observable ESS.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not treat current chunks as production evidence, does not set
`kappa_s = 1`, and does not use `H_unit`, `yt_ward_identity`, observed top
mass, observed `y_t`, `alpha_LM`, plaquette, or `u0` as proof authority.

## Next Action

Emit a predeclared blocking/bootstrap ESS certificate for the same-source
`dE/ds` and `C_ss(q)/Gamma_ss(q)` target observables, then rerun this gate
before using chunked FH/LSZ output as production evidence.
