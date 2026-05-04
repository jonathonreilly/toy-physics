# YT FH/LSZ Chunks053-056 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks053, 054, 055, and 056 completed under the selected-mass-only and
normal-equation-cache FH/LSZ production harness. This extends the honest v2
multi-tau target-timeseries population to chunks017-056 and the ready L12 set
to `56/63` chunks.

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved. The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Outputs

Chunk053:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk053_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk053/L12xT24/ensemble_measurement.json`
- seed: `2026051053`
- runtime: `4083.0142228603363` seconds
- source slope: `1.4293653630051477`
- source slope error: `25.058395151119647`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9220828693706165 GeV`, `y_t(v) = 0.02252729539098569`

Chunk054:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk054_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk054/L12xT24/ensemble_measurement.json`
- seed: `2026051054`
- runtime: `4187.703878164291` seconds
- source slope: `7.061144932574286`
- source slope error: `13.632696480335577`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9221252877697883 GeV`, `y_t(v) = 0.022527539029848`

Chunk054 is another mixed-window/high-slope fitted-response row. It is retained
as source-coordinate evidence, while the common-window provenance gate remains
the only accepted explanation of the fit-window instability. This does not
authorize a physical readout switch.

Chunk055:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk055_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk055/L12xT24/ensemble_measurement.json`
- seed: `2026051055`
- runtime: `4180.777122974396` seconds
- source slope: `1.4219250305991056`
- source slope error: `23.632180461916068`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9317585797366115 GeV`, `y_t(v) = 0.02258286983772536`

Chunk056:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk056_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk056/L12xT24/ensemble_measurement.json`
- seed: `2026051056`
- runtime: `4137.691448926926` seconds
- source slope: `1.4051480558663294`
- source slope error: `24.32621587744469`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9234820510860957 GeV`, `y_t(v) = 0.022535331880998797`

The proxy top results are harness outputs only. They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk053_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk054_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk055_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk056_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk053_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk054_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk055_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk056_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `56/63` ready L12 chunks, `896/1000` saved configurations
- target-observable ESS: passed with limiting ESS `783.2344666684801`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- fitted response stability: still not passed; relative stdev
  `0.9004720441599772`, spread ratio `5.934886855129659`
- common-window response provenance: fixed `tau=10..12` central slope mean
  `1.4248300242966516`, relative stdev `0.00554095978762345`
- common-window pooled response estimator: relative standard error
  `0.0007404418971135232`
- response-window acceptance: not passed; v2 rows are present for
  chunks017-056, chunks001-016 still lack v2 rows, and fitted production
  response stability remains open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-056
- paired x8/x16 variance calibration gate: passed as launch support only
- retained-route certificate: `PASS=155 FAIL=0`
- campaign-status certificate: `PASS=181 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, response-window
acceptance, or canonical-Higgs normalization. They are source-coordinate
FH/LSZ production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: monitor chunks057-060, let the wave orchestrator launch
chunks061-063 as slots free, and package only completed root outputs with
passing local and aggregate gates. PR #230 remains draft/open.
