# YT FH/LSZ Chunks041-042 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks041 and 042 completed under the selected-mass-only and normal-equation-
cache FH/LSZ production harness.  They extend the honest v2 multi-tau target-
timeseries population to chunks017-042.

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved.  The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Outputs

Chunk041:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk041_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk041/L12xT24/ensemble_measurement.json`
- seed: `2026051041`
- runtime: `4180.554522037506` seconds
- source slope: `7.151329203358232`
- source slope error: `13.72071735632016`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9144248853698174 GeV`, `y_t(v) = 0.022483310173581777`

Chunk042:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk042_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk042/L12xT24/ensemble_measurement.json`
- seed: `2026051042`
- runtime: `4218.395290136337` seconds
- source slope: `6.868485321212869`
- source slope error: `13.674000655397203`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9239578103743935 GeV`, `y_t(v) = 0.022538064503021187`

The proxy top results are harness outputs only.  They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk041_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk042_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk041_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk042_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `42/63` ready L12 chunks, `672/1000` saved configurations
- target-observable ESS: passed with limiting ESS `593.8640255444543`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- response stability: still not passed; relative stdev
  `0.9022091040980633`, spread ratio `5.934886855129659`
- response-window forensics: tau1 target diagnostic remains stable with
  relative stdev `0.0061873738305449795`, while fitted response slopes remain
  unstable
- response-window acceptance: not passed; v2 rows are present for
  chunks017-042, chunks001-016 still lack v2 rows, finite-source-linearity is
  not passed, and production response stability is still open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-042
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

Exact next action: continue chunks043-048 under the live chunk-wave monitors
and launch the remaining chunks049-052 as slots open.  Foreground closure
remains blocked on a real same-surface canonical-Higgs/source-overlap
certificate, W/Z response identity, Schur A/B/C rows, neutral-sector
irreducibility, or enough production evidence to pass the current gates.
PR #230 remains draft/open.
