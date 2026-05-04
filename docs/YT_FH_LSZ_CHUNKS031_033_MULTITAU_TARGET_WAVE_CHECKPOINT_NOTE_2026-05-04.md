# YT FH/LSZ Chunks031 and 033 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks031 and 033 completed under the selected-mass-only and
normal-equation-cache FH/LSZ production harness.  Chunk031 first left a
per-volume ensemble artifact without the root output certificate; it was
relaunched with `--resume` under the same seed and wrote the missing root
certificate.  Chunk033 landed normally.

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

Chunk031:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk031_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk031/L12xT24/ensemble_measurement.json`
- seed: `2026051031`
- runtime: `4155.430456876755` seconds
- source slope: `1.4223885055818306`
- source slope error: `24.278916294201405`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.921146372233049 GeV`, `y_t(v) = 0.022521916425687547`

Chunk033:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk033_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk033/L12xT24/ensemble_measurement.json`
- seed: `2026051033`
- runtime: `4110.513936042786` seconds
- source slope: `1.4125650847943865`
- source slope error: `24.937530032163565`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.935843874875866 GeV`, `y_t(v) = 0.02260633457659665`

The proxy top results are harness outputs only.  They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk031_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk033_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk031_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk033_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `34/63` ready L12 chunks, `544/1000` saved configurations
- target-observable ESS: passed with limiting ESS `477.3528176804397`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- response stability: still not passed; relative stdev
  `0.9051016912824127`, spread ratio `5.929584606166269`
- response-window forensics: tau1 target diagnostic remains stable with
  relative stdev `0.005939579923659181`, while fitted response slopes remain
  unstable
- response-window acceptance: not passed; v2 rows are present for
  chunks017-034, chunks001-016 still lack v2 rows, multiple source radii are
  absent, finite-source-linearity is not passed, and production response
  stability is still open
- retained-route certificate: `PASS=144 FAIL=0`
- campaign-status certificate: `PASS=170 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, finite-source
linearity, or canonical-Higgs normalization.  They are source-coordinate
FH/LSZ production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: keep chunks035-040 running under the chunk-wave
orchestrator.  Foreground closure remains blocked on a real same-surface
canonical-Higgs/source-overlap certificate, W/Z response identity, Schur
A/B/C rows, neutral-sector irreducibility, or enough production evidence to
pass the current gates.  PR #230 remains draft/open.
