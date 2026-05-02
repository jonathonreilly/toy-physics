# PR #230 FH/LSZ Target Time-Series Higgs-Identity No-Go

**Status:** exact negative boundary / FH-LSZ target time series not canonical-Higgs identity  
**Runner:** `scripts/frontier_yt_fh_lsz_target_timeseries_higgs_identity_no_go.py`  
**Certificate:** `outputs/yt_fh_lsz_target_timeseries_higgs_identity_no_go_2026-05-02.json`

## Purpose

The target time-series harness removes an instrumentation blocker for future
autocorrelation/ESS checks.  This note tests whether perfect same-source target
time series would also identify the source pole with the canonical Higgs radial
mode used by `v`.

## Result

They do not.  The runner constructs two neutral-scalar response models with
the same source-coordinate observables:

- same source response limit `dE/ds`;
- same source inverse-propagator derivative `dGamma_ss/dp^2`;
- same source-rescaling-invariant FH/LSZ readout;
- different canonical-Higgs Yukawa coupling.

The mixed model rotates the measured source pole into
`O_s = cos(theta) h + sin(theta) chi` and lets the orthogonal scalar `chi`
also couple to the top.  Since the current authority surface does not provide a
no-orthogonal-top-coupling theorem, source-pole purity theorem, sector-overlap
identity, or independent canonical-Higgs response observable, same-source
target time series remain source-coordinate data.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not treat target time series as physical `dE/dh`, does not set
`kappa_s = 1`, and does not use `H_unit`, `yt_ward_identity`, observed top
mass, observed `y_t`, `alpha_LM`, plaquette, or `u0` as proof authority.

## Next Action

Close one identity premise: source-pole purity, no orthogonal top coupling,
same-source sector-overlap equality, or an independent canonical-Higgs response
observable such as same-source W/Z mass slopes.
