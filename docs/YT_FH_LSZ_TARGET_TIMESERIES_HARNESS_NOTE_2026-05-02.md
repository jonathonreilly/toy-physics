# PR #230 FH/LSZ Target Time-Series Harness Extension

**Status:** bounded-support / FH-LSZ target time-series harness extension  
**Runner:** `scripts/frontier_yt_fh_lsz_target_timeseries_harness_certificate.py`  
**Certificate:** `outputs/yt_fh_lsz_target_timeseries_harness_certificate_2026-05-02.json`

## Purpose

The autocorrelation/ESS gate needs target-observable time series, not only
aggregate fits.  This block extends the direct lattice harness so future
FH/LSZ production chunks serialize per-configuration source-response and
same-source scalar two-point rows.

## Harness Change

The production harness now emits:

- `scalar_source_response_analysis.per_configuration_effective_energies`;
- `scalar_source_response_analysis.per_configuration_slopes`;
- `scalar_two_point_lsz_analysis.mode_rows[*].C_ss_timeseries`.

The source-response rows use the same additive scalar source coordinate
already present in the harness.  They are diagnostic target time series for
blocking, bootstrap, and ESS gates.  They are not a physical `dE/dh` readout.

The scalar two-point rows serialize per-configuration `C_ss(q)` and
`Gamma_ss(q)` samples for accepted modes.  They do not determine `kappa_s`
without the scalar pole, FV/IR/model-class, and canonical-Higgs identity gates.

## Claim Firewall

This block does not claim retained or proposed-retained `y_t` closure.  The
smoke run is reduced-scope infrastructure evidence only.  It does not set
`kappa_s = 1`, does not use reduced pilots as production evidence, and does
not import `H_unit`, `yt_ward_identity`, observed top mass, observed `y_t`,
`alpha_LM`, plaquette, or `u0` as proof authority.

## Next Action

Rerun future FH/LSZ production chunks with the extended harness, then rerun
the autocorrelation/ESS gate on the emitted target time series before using
chunked FH/LSZ output as production evidence.
