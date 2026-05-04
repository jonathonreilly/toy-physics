# YT FH/LSZ Chunks037-040 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks037, 038, 039, and 040 completed under the selected-mass-only and
normal-equation-cache FH/LSZ production harness.  Each chunk records the v2
multi-tau target-timeseries schema, the legacy tau1 target rows, scalar LSZ
target rows for the four configured finite modes, and numba gauge seed control.

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved.  The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Outputs

Chunk037:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk037_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk037/L12xT24/ensemble_measurement.json`
- seed: `2026051037`
- runtime: `4018.0686690807343` seconds
- source slope: `1.4151717810783384`
- source slope error: `24.33326422286424`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.925312348041539 GeV`, `y_t(v) = 0.022545844570695`

Chunk038:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk038_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk038/L12xT24/ensemble_measurement.json`
- seed: `2026051038`
- runtime: `4056.6307289600372` seconds
- source slope: `1.4348818805350183`
- source slope error: `24.687083397940878`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.919602649595434 GeV`, `y_t(v) = 0.02251304973494756`

Chunk039:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk039_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk039/L12xT24/ensemble_measurement.json`
- seed: `2026051039`
- runtime: `4062.6055550575256` seconds
- source slope: `1.4234239046540305`
- source slope error: `24.66767378753579`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.910717747074582 GeV`, `y_t(v) = 0.022462017456876534`

Chunk040:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk040_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk040/L12xT24/ensemble_measurement.json`
- seed: `2026051040`
- runtime: `4044.1909189224243` seconds
- source slope: `1.2392686775356556`
- source slope error: `0.17807427770256884`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 4.128151710991288 GeV`, `y_t(v) = 0.023710894468486076`

The proxy top results are harness outputs only.  They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk037_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk038_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk039_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk040_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk037_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk038_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk039_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk040_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `40/63` ready L12 chunks, `640/1000` saved configurations
- target-observable ESS: passed with limiting ESS `564.3761930946672`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- response stability: still not passed; relative stdev
  `0.901108695274814`, spread ratio `5.934886855129659`
- response-window forensics: tau1 target diagnostic remains stable with
  relative stdev `0.006124109649771714`, while fitted response slopes remain
  unstable
- response-window acceptance: not passed; v2 rows are present for
  chunks017-040, chunks001-016 still lack v2 rows, finite-source-linearity is
  not passed, and production response stability is still open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-040
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

Exact next action: keep chunks041-046 running under the chunk-wave
orchestrator.  Foreground closure remains blocked on a real same-surface
canonical-Higgs/source-overlap certificate, W/Z response identity, Schur
A/B/C rows, neutral-sector irreducibility, or enough production evidence to
pass the current gates.  PR #230 remains draft/open.
