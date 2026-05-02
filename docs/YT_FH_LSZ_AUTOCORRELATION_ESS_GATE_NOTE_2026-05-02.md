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

After chunks007-008 completed, the ready set reaches the eight-chunk count
threshold used by this gate.  The blocker is now sharper: the current chunks
expose plaquette histories, so a diagnostic plaquette autocorrelation can be
estimated, but they still do not expose the target time series needed for
load-bearing FH/LSZ ESS.  Plaquette ESS is not a substitute for
target-observable ESS.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not treat current chunks as production evidence, does not set
`kappa_s = 1`, and does not use `H_unit`, `yt_ward_identity`, observed top
mass, observed `y_t`, `alpha_LM`, plaquette, or `u0` as proof authority.

## Next Action

Extend the production harness or postprocessor to retain per-configuration
same-source `dE/ds` and `C_ss(q)` target time series, or emit a predeclared
blocking/bootstrap ESS certificate.  Rerun this gate before using chunked
FH/LSZ output as production evidence.
