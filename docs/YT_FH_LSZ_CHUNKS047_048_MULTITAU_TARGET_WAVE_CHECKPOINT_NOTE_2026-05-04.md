# YT FH/LSZ Chunks047-048 Multi-Tau Target Wave Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks047 and 048 completed under the selected-mass-only and
normal-equation-cache FH/LSZ production harness.  They extend the honest v2
multi-tau target-timeseries population to chunks017-048.

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved.  The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Outputs

Chunk047:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk047_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk047/L12xT24/ensemble_measurement.json`
- seed: `2026051047`
- runtime: `4059.4273092746735` seconds
- source slope: `1.4132201666231028`
- source slope error: `24.717437283512464`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9128013000007096 GeV`, `y_t(v) = 0.022473984774700483`

Chunk048:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk048_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk048/L12xT24/ensemble_measurement.json`
- seed: `2026051048`
- runtime: `4130.00709605217` seconds
- source slope: `1.4228990092905442`
- source slope error: `24.225602434057432`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9191009686032556 GeV`, `y_t(v) = 0.02251016822624944`

The proxy top results are harness outputs only.  They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Certificates

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk047_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk048_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk047_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk048_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the wave:

- chunk combiner: `48/63` ready L12 chunks, `768/1000` saved configurations
- target-observable ESS: passed with limiting ESS `678.1515635297619`
- autocorrelation ESS gate: passed for target observables over the current
  ready set
- fitted response stability: still not passed; relative stdev
  `0.9030756407779459`, spread ratio `5.934886855129659`
- common-window response gate: bounded support passed; no physical readout
  switch authorized
- response-window acceptance: not passed; v2 rows are present for
  chunks017-048, chunks001-016 still lack v2 rows, and fitted production
  response stability remains open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-048
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

Exact next action: continue chunks049-052 under the live chunk-wave monitor.
After the current wave frees slots, run the separate paired x8/x16
calibration stream before using eight-mode/x8 pole-fit production support.
PR #230 remains draft/open.
