# FH-LSZ Multi-Tau Target-Timeseries Harness

**Status:** bounded-support / FH-LSZ multi-tau target time-series harness extension  
**Runner:** `scripts/frontier_yt_fh_lsz_multitau_target_timeseries_harness_certificate.py`  
**Certificate:** `outputs/yt_fh_lsz_multitau_target_timeseries_harness_certificate_2026-05-03.json`  
**Smoke:** `outputs/yt_direct_lattice_correlator_multitau_target_timeseries_smoke_2026-05-03.json`

## Purpose

The response-window acceptance gate showed stable chunk-level central slopes
across tau windows 0-9, but the current production rows serialized only
per-configuration tau=1 target slopes.  That left no per-configuration
multi-tau covariance surface for a future readout-window acceptance test.

This block extends `scripts/yt_direct_lattice_correlator_production.py` so the
scalar source-response analysis preserves the legacy tau=1 target rows and
also writes versioned multi-tau rows:

- `target_timeseries_schema_version = fh_lsz_target_timeseries_v2_multitau`;
- `per_configuration_multi_tau_effective_energies`;
- `per_configuration_multi_tau_slopes`;
- `multi_tau_window_range`;
- explicit non-readout metadata.

## Result

The reduced smoke run passes the schema certificate:

```bash
python3 scripts/frontier_yt_fh_lsz_multitau_target_timeseries_harness_certificate.py
# SUMMARY: PASS=14 FAIL=0
```

The smoke confirms:

- legacy `per_configuration_effective_energies` and
  `per_configuration_slopes` are still present;
- multi-tau effective-energy and slope rows are present;
- at least one finite multi-tau slope diagnostic is serialized;
- scalar two-point `C_ss_timeseries` rows remain present;
- `rng_seed_control.seed_control_version = numba_gauge_seed_v1`;
- selected-mass-only and normal-cache metadata remain present.

## Claim Boundary

This is infrastructure support only.  The smoke run is reduced scope and is not
production evidence.  Multi-tau source-response rows do not derive `kappa_s`,
do not identify the source pole with the canonical Higgs, and do not authorize
a response-window readout switch.

The response-window acceptance gate still needs production chunks rerun with
the v2 schema, per-configuration multi-tau covariance across those chunks, and
multiple source radii / finite-source-linearity evidence before any readout
switch can be considered.
