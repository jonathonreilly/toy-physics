# YT FH/LSZ Chunks017-018 Multi-Tau Target Wave Checkpoint

Date: 2026-05-03

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks017-018 were run after the FH/LSZ selected-mass-only and normal-equation
cache optimization landed.  They are the first L12_T24 production chunks in
this campaign wave to carry the v2 multi-tau source-response target schema:

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

Chunk017:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk017_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk017/L12xT24/ensemble_measurement.json`
- seed: `2026051017`
- runtime: `1943.5069608688354` seconds
- source slope: `1.425822667545628`
- finite multi-tau slope values: `368`

Chunk018:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk018_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk018/L12xT24/ensemble_measurement.json`
- seed: `2026051018`
- runtime: `1934.3256540298462` seconds
- source slope: `1.4324757674234831`
- finite multi-tau slope values: `368`

The wave used two concurrent workers.  No `--resume` was used and no active
chunk collision was observed.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk017_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk018_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk017_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk018_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `18/63` ready L12 chunks, `288/1000` saved configurations
- target-observable ESS: passed with limiting ESS `242.7849819291294`
- response stability: still not passed; relative stdev `0.8900751406619184`
- response-window acceptance: not passed; v2 multi-tau rows are present only for chunks017-018, multiple source radii are absent, and production response stability is still open
- retained-route certificate: `PASS=114 FAIL=0`
- campaign-status certificate: `PASS=140 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, finite-source
linearity, or canonical-Higgs normalization.  They are source-coordinate FH/LSZ
production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: either extend v2 multi-tau production rows to the full ready
set and add multi-radius source-response calibration, or pursue same-surface
`O_H/C_sH/C_HH` or W/Z response observables with the required identity
certificates.  PR #230 remains draft/open.
