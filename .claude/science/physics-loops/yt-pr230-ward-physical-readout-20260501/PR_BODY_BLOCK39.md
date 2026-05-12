## Block39 checkpoint - FH/LSZ target-timeseries full set

Packaged the old FH/LSZ target-timeseries replacement campaign as complete for
the current L12 ready set:

- combiner: `present=63`, `ready=63`, `missing=0`, `1008` saved configs;
- target-timeseries coverage: `complete_count=63`,
  `complete_for_all_ready_chunks=true`;
- replacement queue: `[]`;
- target-observable ESS remains passed, limiting ESS
  `895.2344666684801`;
- full-set checkpoint verifies `numba_gauge_seed_v1`, 63 distinct seeds,
  production target schema, source-response target rows, and scalar
  `C_ss_timeseries` rows for the four target modes.

Validation:

```text
python3 -m py_compile scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py scripts/frontier_yt_fh_lsz_target_timeseries_full_set_checkpoint.py scripts/frontier_yt_retained_closure_route_certificate.py scripts/frontier_yt_pr230_campaign_status_certificate.py scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
python3 scripts/frontier_yt_fh_lsz_chunk_combiner_gate.py
# SUMMARY: PASS=9 FAIL=0
python3 scripts/frontier_yt_fh_lsz_autocorrelation_ess_gate.py
# SUMMARY: PASS=11 FAIL=0
python3 scripts/frontier_yt_fh_lsz_target_observable_ess_certificate.py
# SUMMARY: PASS=8 FAIL=0
python3 scripts/frontier_yt_fh_lsz_target_timeseries_replacement_queue.py
# SUMMARY: PASS=9 FAIL=0
python3 scripts/frontier_yt_fh_lsz_target_timeseries_full_set_checkpoint.py
# SUMMARY: PASS=9 FAIL=0
```

No closure claim: this is production-processing support only.  It does not
derive `kappa_s`, canonical `O_H`, `C_sH/C_HH` pole rows, W/Z response rows,
strict `g2`, scalar-LSZ model-class/FV/IR authority, retained, or
`proposed_retained` top-Yukawa closure.  PR #230 remains draft/open.

Current live queue: higher-shell Schur/scalar-LSZ chunks001-002 are still
running under the separate higher-shell roots and remain run-control state only
until completed JSON and completed-mode checkpoints pass.
