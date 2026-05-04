# YT FH/LSZ Chunk057 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunk057 completed under the selected-mass-only and normal-equation-cache
FH/LSZ production harness. This extends the honest v2 multi-tau
target-timeseries population to chunks017-057 and the ready L12 set to
`57/63` chunks.

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved. The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Output

Chunk057:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk057_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk057/L12xT24/ensemble_measurement.json`
- seed: `2026051057`
- runtime: `3966.81934094429` seconds
- source slope: `1.431739487908995`
- source slope error: `25.317588821158044`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.909559613844854 GeV`, `y_t(v) = 0.022455365478772766`

The proxy top result is a harness output only. It is not physical top/Yukawa
evidence because strict production, scale matching, scalar pole identity,
response-window acceptance, and canonical-Higgs/source-overlap gates remain
open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk057_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk057_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the chunk:

- chunk combiner: `57/63` ready L12 chunks, `912/1000` saved configurations
- target-observable ESS: passed with limiting ESS `799.2344666684801`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- fitted response stability: still not passed; relative stdev
  `0.8996614607779676`, spread ratio `5.934886855129659`
- common-window response provenance: fixed `tau=10..12` central slope mean
  `1.4249512429565174`, relative stdev `0.005528231310922798`
- common-window pooled response estimator: relative standard error
  `0.0007322321248657349`
- response-window acceptance: not passed; v2 rows are present for
  chunks017-057, chunks001-016 still lack v2 rows, and fitted production
  response stability remains open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-057
- retained-route certificate: `PASS=155 FAIL=0`
- campaign-status certificate: `PASS=181 FAIL=0`

## Claim Boundary

Chunk057 does not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, response-window
acceptance, or canonical-Higgs normalization. It is source-coordinate FH/LSZ
production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: continue monitoring chunks058-063 and package only completed
root outputs with passing local and aggregate gates. PR #230 remains
draft/open.
