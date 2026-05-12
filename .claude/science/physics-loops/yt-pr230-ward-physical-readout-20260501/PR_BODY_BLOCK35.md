## Block35 checkpoint: top mass-scan response harness rows

Final chunk/package status:

- chunk063 is committed and checkpointed (`PASS=15 FAIL=0`);
- the two-source taste-radial package audit is complete (`PASS=10 FAIL=0`);
- the row combiner is at `ready=63/63` with
  `combined_rows_written=true` (`PASS=13 FAIL=0`);
- this completes the finite `C_ss/C_sx/C_xx` row packet, but it is still
  support only and not physical top-Yukawa closure.

Landed a support-only production-harness extension for future W/Z covariance
and subtraction work:

- `scripts/yt_direct_lattice_correlator_production.py` now emits
  `top_mass_scan_response_analysis` from the existing three-mass top
  correlator scan, with per-configuration effective energies, tau=1
  `dE/dm_bare` slopes, and multi-tau slope rows.
- The new rows add no solves; they reuse the already computed top correlators
  for masses `0.45,0.75,1.05`.
- Metadata explicitly records `top_mass_scan_response_v1`,
  `extra_solve_count=0`, `physical_higgs_normalization=not_derived`, and
  `used_as_physical_yukawa_readout=false`.
- A reduced smoke artifact and gate validate schema compatibility while keeping
  scalar FH/LSZ selected-mass-only metadata, scalar source-response time series,
  scalar `C_ss_timeseries`, and `numba_gauge_seed_v1` seed control intact.

Validation:

```text
python3 scripts/yt_direct_lattice_correlator_production.py ... --volumes 2x4 --measurements 2 --engine numba ...
# wrote outputs/yt_pr230_top_mass_scan_response_harness_smoke_2026-05-12.json

python3 scripts/frontier_yt_pr230_top_mass_scan_response_harness_gate.py
# SUMMARY: PASS=14 FAIL=0

python3 scripts/frontier_yt_pr230_assumption_import_stress.py
# SUMMARY: PASS=105 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=164 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=318 FAIL=0

python3 scripts/frontier_yt_pr230_positive_closure_completion_audit.py
# SUMMARY: PASS=73 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=366 FAIL=0

bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict
# OK, 5 known warnings, no errors
```

Claim boundary: this is bounded infrastructure support only.  `dE/dm_bare`
rows are not `dE/dh`, not `kappa_s`, not W/Z response, not strict matched
covariance, not strict `g2`, and not retained or `proposed_retained`
top-Yukawa closure.  Existing production chunks predate this field; future
production reruns are needed before these rows can be used in a strict W/Z
subtraction packet.  PR #230 remains draft/open.
