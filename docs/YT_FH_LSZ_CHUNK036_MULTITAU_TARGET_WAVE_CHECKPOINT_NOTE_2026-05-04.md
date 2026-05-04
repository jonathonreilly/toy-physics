# YT FH/LSZ Chunks035-036 Multi-Tau Target Wave Checkpoint

```yaml
actual_current_surface_status: bounded production support / chunks035-036 packaged
proposal_allowed: false
bare_retained_allowed: false
```

**Root output:** `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk035_2026-05-01.json`
**Root output:** `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk036_2026-05-01.json`
**Per-volume artifact:** `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk035/L12xT24/ensemble_measurement.json`
**Per-volume artifact:** `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk036/L12xT24/ensemble_measurement.json`

## Result

Chunk035 landed with seed `2026051035`, `numba_gauge_seed_v1`, `12^3 x 24`,
1000 thermalization sweeps, 16 measurement configurations, and 20 sweeps
between measurements.

Chunk036 landed with seed `2026051036`, `numba_gauge_seed_v1`, `12^3 x 24`,
1000 thermalization sweeps, 16 measurement configurations, and 20 sweeps
between measurements.

Validation:

```bash
python3 scripts/frontier_yt_fh_lsz_chunk_multitau_target_timeseries_checkpoint.py --chunk-index 35
# SUMMARY: PASS=19 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_multitau_target_timeseries_checkpoint.py --chunk-index 36
# SUMMARY: PASS=19 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 35
# SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_target_timeseries_checkpoint.py --chunk-index 36
# SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0

python3 scripts/frontier_yt_fh_lsz_ready_chunk_set_checkpoint_certificate.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_fh_lsz_ready_chunk_response_stability.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_fh_lsz_response_window_forensics.py
# SUMMARY: PASS=10 FAIL=0

python3 scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py
# SUMMARY: PASS=11 FAIL=0

python3 scripts/frontier_yt_fh_lsz_response_window_acceptance_gate.py
# SUMMARY: PASS=12 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=148 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=174 FAIL=0
```

## Current Production State

The ready L12 set is now 36/63 chunks, 576/1000 saved configurations.
Target-observable ESS passes with limiting ESS `505.20155779504177`.

Response-window acceptance remains open.  The fit-window response surface is
not production-stable, chunks001-016 still lack v2 multi-tau covariance rows,
and finite-source-linearity remains unpassed.  This chunk is bounded
production support only and does not authorize retained or `proposed_retained`
closure.
