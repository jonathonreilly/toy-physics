# PR #230 FH/LSZ Autocorrelation ESS Gate

**Status:** bounded-support / FH-LSZ autocorrelation ESS gate passed for target observables
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

After the chunk001 through chunk010 target-series replacements, existing
chunk011/chunk012 target-series chunks, and the chunk013-016 target-ESS wave,
the ready set is `[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]`.  All sixteen
ready chunks expose per-configuration target time series for same-source
`dE/ds` and `C_ss(q)/Gamma_ss(q)`.

The target-observable ESS certificate now passes:

```text
python3 scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py
# SUMMARY: PASS=8 FAIL=0
# limiting_target_ess=210.7849819291294 >= 200.0
```

The autocorrelation/ESS gate therefore passes as bounded support:

```text
python3 scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py
# SUMMARY: PASS=11 FAIL=0
```

Plaquette ESS remains diagnostic only and is still not a substitute for target
ESS.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  It
does not treat current chunks as production evidence, does not set
`kappa_s = 1`, and does not use `H_unit`, `yt_ward_identity`, observed top
mass, observed `y_t`, `alpha_LM`, plaquette, or `u0` as proof authority.

## Next Action

Continue the response-stability, scalar-pole derivative/model-class/FV/IR,
and canonical-Higgs identity gates.  The target-observable ESS blocker is
retired for the current ready set, but chunked FH/LSZ output is still not
production evidence or retained closure.
