# YT FH/LSZ Chunks058-060 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks058, 059, and 060 completed under the selected-mass-only and
normal-equation-cache FH/LSZ production harness. This extends the honest v2
multi-tau target-timeseries population to chunks017-060 and the ready L12 set
to `60/63` chunks.

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved. The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Outputs

Chunk058:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk058_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk058/L12xT24/ensemble_measurement.json`
- seed: `2026051058`
- runtime: `4107.215244054794` seconds
- source slope: `7.182006782740703`
- source slope error: `13.420086796010848`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.907983848916603 GeV`, `y_t(v) = 0.02244631474649919`

Chunk058 is another mixed-window/high-slope fitted-response row. It is retained
as source-coordinate support, while the common-window provenance gate remains
the accepted explanation of the fit-window instability. This does not
authorize a physical readout switch.

Chunk059:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk059_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk059/L12xT24/ensemble_measurement.json`
- seed: `2026051059`
- runtime: `3976.618183851242` seconds
- source slope: `1.4314398930989933`
- source slope error: `24.67140918721843`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.92504758581447 GeV`, `y_t(v) = 0.02254432385400027`

Chunk060:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk060_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk060/L12xT24/ensemble_measurement.json`
- seed: `2026051060`
- runtime: `4041.2102761268616` seconds
- source slope: `1.4153773994312473`
- source slope error: `24.650592816970537`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.909813086969812 GeV`, `y_t(v) = 0.022456821354171066`

The proxy top results are harness outputs only. They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk058_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk059_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk060_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk058_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk059_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk060_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `60/63` ready L12 chunks, `960/1000` saved configurations
- target-observable ESS: passed with limiting ESS `847.2344666684801`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- fitted response stability: still not passed; relative stdev
  `0.9015853947143765`, spread ratio `5.934886855129659`
- common-window response provenance: fixed `tau=10..12` central slope mean
  `1.424925815621466`, relative stdev `0.005490444253610517`
- common-window pooled response estimator: relative standard error
  `0.0007088133052504581`
- response-window acceptance: not passed; v2 rows are present for
  chunks017-060, chunks001-016 still lack v2 rows, and fitted production
  response stability remains open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-060
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

Exact next action: continue monitoring chunks061-063 and package only completed
root outputs with passing local and aggregate gates. PR #230 remains
draft/open.
