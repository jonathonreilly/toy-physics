# YT FH/LSZ Chunks049-052 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks049, 050, 051, and 052 completed under the selected-mass-only and
normal-equation-cache FH/LSZ production harness.  This closes the live
chunks047-052 wave and extends the honest v2 multi-tau target-timeseries
population to chunks017-052.

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved.  The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Outputs

Chunk049:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk049_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk049/L12xT24/ensemble_measurement.json`
- seed: `2026051049`
- runtime: `4126.695409297943` seconds
- source slope: `1.420574471095689`
- source slope error: `24.73403983356421`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.927340787300807 GeV`, `y_t(v) = 0.02255749533175695`

Chunk050:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk050_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk050/L12xT24/ensemble_measurement.json`
- seed: `2026051050`
- runtime: `4145.228160142899` seconds
- source slope: `1.42810978733373`
- source slope error: `24.285457660450124`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9125341308445485 GeV`, `y_t(v) = 0.022472450233309935`

Chunk051:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk051_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk051/L12xT24/ensemble_measurement.json`
- seed: `2026051051`
- runtime: `3991.5869047641754` seconds
- source slope: `1.4196706505806211`
- source slope error: `24.131274703979344`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9326434637564986 GeV`, `y_t(v) = 0.022587952352390826`

Chunk052:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk052_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk052/L12xT24/ensemble_measurement.json`
- seed: `2026051052`
- runtime: `4045.297065973282` seconds
- source slope: `1.4267349938298886`
- source slope error: `24.10608519497453`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.910176737390988 GeV`, `y_t(v) = 0.022458910055692616`

The proxy top results are harness outputs only.  They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk049_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk050_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk051_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk052_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk049_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk050_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk051_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk052_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `52/63` ready L12 chunks, `832/1000` saved configurations
- target-observable ESS: passed with limiting ESS `731.9910843504125`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- fitted response stability: still not passed; relative stdev
  `0.8996605522066465`, spread ratio `5.934886855129659`
- common-window response gate: bounded support passed; no physical readout
  switch authorized
- response-window acceptance: not passed; v2 rows are present for
  chunks017-052, chunks001-016 still lack v2 rows, and fitted production
  response stability remains open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-052
- paired x8/x16 variance calibration gate: still open because calibration
  outputs are absent
- retained-route certificate: `PASS=155 FAIL=0`
- campaign-status certificate: `PASS=181 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, response-window
acceptance, or canonical-Higgs normalization.  They are source-coordinate
FH/LSZ production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: monitor the paired x8/x16 variance calibration stream and
package it only after both production outputs land and the calibration gates
pass or honestly fail.  PR #230 remains draft/open.
