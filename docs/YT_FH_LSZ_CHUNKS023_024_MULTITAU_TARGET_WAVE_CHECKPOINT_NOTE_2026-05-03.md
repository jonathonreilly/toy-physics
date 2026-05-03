# YT FH/LSZ Chunks023-024 Multi-Tau Target Wave Checkpoint

Date: 2026-05-03

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks023-024 were completed in
`/Users/jonBridger/CI3Z2-pr230-status-20260503` using the selected-mass-only
and normal-equation-cache FH/LSZ production harness.  The wave used two
concurrent workers, fixed seeds, no `--resume`, and chunk-isolated output
directories.

Both chunks carry the v2 multi-tau source-response target schema:

- `target_timeseries_schema_version = fh_lsz_target_timeseries_v2_multitau`
- legacy tau1 `per_configuration_effective_energies`
- legacy tau1 `per_configuration_slopes`
- v2 `per_configuration_multi_tau_effective_energies`
- v2 `per_configuration_multi_tau_slopes`
- scalar LSZ `C_ss_timeseries` for modes `0,0,0`, `1,0,0`, `0,1,0`, `0,0,1`
- `rng_seed_control.seed_control_version = numba_gauge_seed_v1`

The scalar FH/LSZ rows are intentionally selected-mass-only at
`m_bare = 0.75`; the three-mass top correlator scan is still preserved.

## Production Outputs

Chunk023:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk023_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk023/L12xT24/ensemble_measurement.json`
- seed: `2026051023`
- runtime: `2274.8532021045685` seconds
- source slope: `6.800776826038631`
- source slope error: `13.377804591819606`
- finite multi-tau slope values: `368`

Chunk024:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk024_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk024/L12xT24/ensemble_measurement.json`
- seed: `2026051024`
- runtime: `2278.1163148880005` seconds
- source slope: `1.4363176487241531`
- source slope error: `24.412742085648553`
- finite multi-tau slope values: `368`

Chunk023 joins the current high-slope group in the ready set.  It is retained
in the production-support set because seed-control and schema gates pass; its
effect is reflected in the response-stability diagnostic rather than filtered
out by hand.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk023_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk024_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk023_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk024_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `24/63` ready L12 chunks, `384/1000` saved configurations
- target-observable ESS: passed with limiting ESS `323.8130499055201`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- response stability: still not passed; relative stdev
  `0.8942414475625226`, spread ratio `5.920283844112204`
- response-window forensics: tau1 target diagnostic remains stable with
  relative stdev `0.006234178244122134`, while fitted response slopes remain
  unstable
- response-window acceptance: not passed; v2 multi-tau rows are present only
  for chunks017-024, chunks001-016 still lack v2 rows, multiple source radii
  are absent, finite-source-linearity is absent, and production response
  stability is still open
- replacement queue: empty for the current ready set
- retained-route certificate: `PASS=128 FAIL=0`
- campaign-status certificate: `PASS=154 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, finite-source
linearity, or canonical-Higgs normalization.  They are source-coordinate
FH/LSZ production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: continue v2 production chunks or rerun older chunks with v2
multi-tau rows only as production support, while the foreground closure route
remains a real same-surface canonical-Higgs/source-overlap certificate, a W/Z
response identity, or a scalar-pole identity theorem.  PR #230 remains
draft/open.
