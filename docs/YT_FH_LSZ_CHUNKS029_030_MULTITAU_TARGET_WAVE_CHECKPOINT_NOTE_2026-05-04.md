# YT FH/LSZ Chunks029-030 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks029-030 completed with the selected-mass-only and normal-equation-cache
FH/LSZ production harness.  The wave used fixed seeds, chunk-isolated output
directories, and the same v2 multi-tau target schema as chunks017-028.

Both chunks record:

- `target_timeseries_schema_version = fh_lsz_target_timeseries_v2_multitau`
- legacy tau1 `per_configuration_effective_energies`
- legacy tau1 `per_configuration_slopes`
- v2 `per_configuration_multi_tau_effective_energies`
- v2 `per_configuration_multi_tau_slopes`
- scalar LSZ `C_ss_timeseries` for modes `0,0,0`, `1,0,0`, `0,1,0`, `0,0,1`
- `rng_seed_control.seed_control_version = numba_gauge_seed_v1`

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved.

## Production Outputs

Chunk029:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk029_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk029/L12xT24/ensemble_measurement.json`
- seed: `2026051029`
- runtime: `3824.1231591701508` seconds
- source slope: `7.085662948355276`
- source slope error: `13.740527270335676`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9176941043869764 GeV`, `y_t(v) = 0.022502087610201615`

Chunk030:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk030_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk030/L12xT24/ensemble_measurement.json`
- seed: `2026051030`
- runtime: `3868.302201986313` seconds
- source slope: `1.4213912322931153`
- source slope error: `24.059936002506316`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.930166568159869 GeV`, `y_t(v) = 0.022573725789460795`

The proxy top results are harness outputs only.  They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk029_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk030_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk029_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk030_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `30/63` ready L12 chunks, `480/1000` saved configurations
- target-observable ESS: passed with limiting ESS `415.66719632039644`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- response stability: still not passed; relative stdev
  `0.9010841161455033`, spread ratio `5.9287012436035536`
- response-window forensics: tau1 target diagnostic remains stable with
  relative stdev `0.006030493117884578`, while fitted response slopes remain
  unstable
- response-window acceptance: not passed; v2 rows are present for
  chunks017-030, chunks001-016 still lack v2 rows, multiple source radii are
  absent, finite-source-linearity is not passed, and production response
  stability is still open
- source-Higgs production readiness: launch blocked by missing same-surface
  `O_H` certificate; current chunks have no `C_sH/C_HH` rows
- retained-route certificate: `PASS=143 FAIL=0`
- campaign-status certificate: `PASS=169 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, finite-source
linearity, or canonical-Higgs normalization.  They are source-coordinate
FH/LSZ production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: keep chunks031-036 running under the chunk-wave
orchestrator.  Foreground closure remains blocked on a real same-surface
canonical-Higgs/source-overlap certificate, W/Z response identity, Schur
A/B/C rows, neutral-sector irreducibility, or enough production evidence to
pass the current gates.  PR #230 remains draft/open.
