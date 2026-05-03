# YT FH/LSZ Chunks019-020 Multi-Tau Target Wave Checkpoint

Date: 2026-05-03

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks019-020 were run with the selected-mass-only and normal-equation-cache
FH/LSZ production harness, using two concurrent workers, fixed seeds, no
`--resume`, and chunk-isolated output directories.

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

Chunk019:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk019_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk019/L12xT24/ensemble_measurement.json`
- seed: `2026051019`
- runtime: `1952.710295677185` seconds
- source slope: `1.4327032836709572`
- finite multi-tau slope values: `368`

Chunk020:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk020_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk020/L12xT24/ensemble_measurement.json`
- seed: `2026051020`
- runtime: `1954.869423866272` seconds
- source slope: `1.2428759927942465`
- finite multi-tau slope values: `368`

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk019_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk020_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk019_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk020_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `20/63` ready L12 chunks, `320/1000` saved configurations
- target-observable ESS: passed with limiting ESS `268.13169763211454`
- response stability: still not passed; relative stdev `0.8885692945249242`
- response-window acceptance: not passed; v2 multi-tau rows are present only
  for chunks017-020, chunks001-016 still lack v2 rows, multiple source radii
  are absent, and production response stability is still open
- retained-route certificate: `PASS=116 FAIL=0`
- campaign-status certificate: `PASS=142 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, finite-source
linearity, or canonical-Higgs normalization.  They are source-coordinate FH/LSZ
production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: continue v2 production chunks or rerun older chunks with v2
multi-tau rows only as production support, while the foreground closure route
remains a real same-surface canonical-Higgs/source-overlap certificate, a W/Z
response identity, or a scalar-pole identity theorem.  PR #230 remains
draft/open.
