# YT FH/LSZ Chunks027-028 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks027-028 completed with the selected-mass-only and normal-equation-cache
FH/LSZ production harness. The wave used two fixed seeds, no `--resume`, and
chunk-isolated output directories.

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

Chunk027:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk027_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk027/L12xT24/ensemble_measurement.json`
- seed: `2026051027`
- runtime: `2886.7090549468994` seconds
- source slope: `1.2405616478339947`
- source slope error: `0.2069771509175122`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 4.118187776097191 GeV`, `y_t(v) = 0.023653664544465654`

Chunk028:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk028_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk028/L12xT24/ensemble_measurement.json`
- seed: `2026051028`
- runtime: `2882.234740972519` seconds
- source slope: `1.2468986960487285`
- source slope error: `0.0734139596188983`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 4.126471097293686 GeV`, `y_t(v) = 0.023701241515587074`

The proxy top results are recorded only as harness output. They are not
physical top/Yukawa evidence because strict production, scale matching, scalar
pole identity, and canonical-Higgs/source-overlap gates remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk027_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk028_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk027_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk028_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `28/63` ready L12 chunks, `448/1000` saved configurations
- target-observable ESS: passed with limiting ESS `387.5962268377635`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- response stability: still not passed; relative stdev
  `0.9039137213179782`, spread ratio `5.9287012436035536`
- response-window forensics: tau1 target diagnostic remains stable with
  relative stdev `0.006179373302816849`, while fitted response slopes remain
  unstable
- response-window acceptance: not passed; v2 multi-tau rows are present for
  chunks017-028, chunks001-016 still lack v2 rows, multiple source radii are
  absent, finite-source-linearity is not passed, and production response
  stability is still open
- retained-route certificate: `PASS=140 FAIL=0`
- campaign-status certificate: `PASS=166 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, finite-source
linearity, or canonical-Higgs normalization. They are source-coordinate
FH/LSZ production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: continue v2 production chunks 029/030 and finish the
multi-radius finite-source-linearity calibration. The foreground closure route
remains a real same-surface canonical-Higgs/source-overlap certificate, a W/Z
response identity, or a scalar-pole identity theorem. PR #230 remains
draft/open.
