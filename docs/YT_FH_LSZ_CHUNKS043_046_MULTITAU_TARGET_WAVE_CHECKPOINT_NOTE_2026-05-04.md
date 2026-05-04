# YT FH/LSZ Chunks043-046 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks043, 044, 045, and 046 completed under the selected-mass-only and
normal-equation-cache FH/LSZ production harness.  They extend the honest v2
multi-tau target-timeseries population to chunks017-046.

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved.  The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Outputs

Chunk043:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk043_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk043/L12xT24/ensemble_measurement.json`
- seed: `2026051043`
- runtime: `4080.2491841316223` seconds
- source slope: `1.4267415505886176`
- source slope error: `23.93108205303368`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.919413332256885 GeV`, `y_t(v) = 0.022511962351597907`

Chunk044:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk044_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk044/L12xT24/ensemble_measurement.json`
- seed: `2026051044`
- runtime: `4089.3712689876556` seconds
- source slope: `1.4461110127928816`
- source slope error: `24.913065301909743`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9031951401345117 GeV`, `y_t(v) = 0.022418809805663277`

Chunk045:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk045_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk045/L12xT24/ensemble_measurement.json`
- seed: `2026051045`
- runtime: `4099.254647016525` seconds
- source slope: `1.2439123094129967`
- source slope error: `0.09777127073031236`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 4.128053130750776 GeV`, `y_t(v) = 0.02371032825245452`

Chunk046:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk046_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk046/L12xT24/ensemble_measurement.json`
- seed: `2026051046`
- runtime: `4006.66184592247` seconds
- source slope: `1.4304361397206893`
- source slope error: `24.44547868662375`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9113915148954157 GeV`, `y_t(v) = 0.02246588738192156`

The proxy top results are harness outputs only.  They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk043_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk044_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk045_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk046_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk043_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk044_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk045_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk046_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `46/63` ready L12 chunks, `736/1000` saved configurations
- target-observable ESS: passed with limiting ESS `650.985890002029`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- response stability: still not passed; relative stdev
  `0.9039685737574564`, spread ratio `5.934886855129659`
- response-window forensics: tau1 target diagnostic remains stable with
  relative stdev `0.006164321153071368`, while fitted response slopes remain
  unstable
- response-window acceptance: not passed; v2 rows are present for
  chunks017-046, chunks001-016 still lack v2 rows, finite-source-
  linearity is not passed, and production response stability is still open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-046
- retained-route certificate: `PASS=150 FAIL=0`
- campaign-status certificate: `PASS=176 FAIL=0`

## Claim Boundary

These chunks do not derive `kappa_s`, `Z_match`, `c2`, source-Higgs overlap, a
W/Z response identity, scalar-pole model-class control, finite-source
linearity, or canonical-Higgs normalization.  They are source-coordinate
FH/LSZ production support only.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: continue chunks047-052 under the live chunk-wave monitor.
Foreground closure remains
blocked on a real same-surface canonical-Higgs/source-overlap certificate,
W/Z response identity, Schur A/B/C rows, neutral-sector irreducibility, or
enough production evidence to pass the current gates.  PR #230 remains
draft/open.
