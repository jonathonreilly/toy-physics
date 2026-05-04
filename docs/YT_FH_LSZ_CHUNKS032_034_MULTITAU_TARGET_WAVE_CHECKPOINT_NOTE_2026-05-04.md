# YT FH/LSZ Chunks032 and 034 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks032 and 034 completed under the selected-mass-only and
normal-equation-cache FH/LSZ production harness.  The chunks used fixed seeds,
chunk-isolated output directories, and the v2 multi-tau target schema.

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

Chunk032:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk032_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk032/L12xT24/ensemble_measurement.json`
- seed: `2026051032`
- runtime: `4062.953722000122` seconds
- source slope: `1.240376834598461`
- source slope error: `0.20864958322738597`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 4.1264432962522095 GeV`, `y_t(v) = 0.02370108183454657`

Chunk034:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk034_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk034/L12xT24/ensemble_measurement.json`
- seed: `2026051034`
- runtime: `3983.909504175186` seconds
- source slope: `1.42281505348896`
- source slope error: `24.99517342939876`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9274867227021795 GeV`, `y_t(v) = 0.022558333541964185`

The proxy top results are harness outputs only.  They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk032_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk034_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk032_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk034_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `32/63` ready L12 chunks, `512/1000` saved configurations
- target-observable ESS: passed with limiting ESS `445.3528176804397`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- response stability: still not passed; relative stdev
  `0.9053910980725465`, spread ratio `5.929584606166269`
- response-window forensics: tau1 target diagnostic remains stable with
  relative stdev `0.005971633174944663`, while fitted response slopes remain
  unstable
- response-window acceptance: not passed; v2 rows are present for
  chunks017-030 plus chunks032 and 034, chunks001-016 still lack v2 rows,
  multiple source radii are absent, finite-source-linearity is not passed, and
  production response stability is still open
- retained-route certificate: `PASS=144 FAIL=0`
- campaign-status certificate: `PASS=170 FAIL=0`

Chunk031 exited without the root output certificate while leaving its
per-volume ensemble artifact present.  It has been relaunched with `--resume`
under the same seed and isolated output directory; it is not counted as ready
in this checkpoint.

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, finite-source
linearity, or canonical-Higgs normalization.  They are source-coordinate
FH/LSZ production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: keep chunk031-resume and chunks033, 035-038 running under
the chunk-wave campaign.  Foreground closure remains blocked on a real
same-surface canonical-Higgs/source-overlap certificate, W/Z response identity,
Schur A/B/C rows, neutral-sector irreducibility, or enough production evidence
to pass the current gates.  PR #230 remains draft/open.
