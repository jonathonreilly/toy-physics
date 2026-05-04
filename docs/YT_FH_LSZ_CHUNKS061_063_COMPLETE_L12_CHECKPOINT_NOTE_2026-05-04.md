# YT FH/LSZ Chunks061-063 Complete L12 Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production/infrastructure support only; closure proposal is
not authorized.

## Scope

Chunks061, 062, and 063 completed the seed-controlled four-mode L12 FH/LSZ
chunk wave. The L12 support surface now has `63/63` combiner-ready chunks and
`1008/1000` saved configurations. The combiner writes the combined L12 support
summary:

```text
outputs/yt_pr230_fh_lsz_production_L12_T24_chunked_combined_2026-05-01.json
```

The scalar FH/LSZ rows remain selected-mass-only at `m_bare = 0.75`; the
three-mass top correlator scan is preserved. The rows are source-coordinate
support, not a physical Yukawa readout.

## Production Outputs

Chunk061:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk061_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk061/L12xT24/ensemble_measurement.json`
- seed: `2026051061`
- runtime: `3841.553` seconds
- source slope: `1.2450193754835581`
- source slope error: `0.0987908397636767`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 4.128184140854922 GeV`, `y_t(v) = 0.02371108073612546`

Chunk062:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk062_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk062/L12xT24/ensemble_measurement.json`
- seed: `2026051062`
- runtime: `3966.651` seconds
- source slope: `1.4346893296253975`
- source slope error: `24.949835378730512`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.912566882626859 GeV`, `y_t(v) = 0.02247263834995593`

Chunk063:

- output: `outputs/yt_pr230_fh_lsz_production_L12_T24_chunk063_2026-05-01.json`
- artifact: `outputs/yt_direct_lattice_correlator_production_fh_lsz_chunks/L12_T24_chunk063/L12xT24/ensemble_measurement.json`
- seed: `2026051063`
- runtime: `3913.131` seconds
- source slope: `1.4410497231371737`
- source slope error: `24.815579188512853`
- finite multi-tau slope values: `368`
- proxy top result: `m_t = 3.9103585155738423 GeV`, `y_t(v) = 0.022459954136339857`

The proxy top results are harness outputs only. They are not physical
top/Yukawa evidence because strict production, scale matching, scalar pole
identity, response-window acceptance, and canonical-Higgs/source-overlap gates
remain open.

## Aggregate State

Chunk-local certificates:

- `outputs/yt_fh_lsz_chunk061_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk062_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk063_target_timeseries_generic_checkpoint_2026-05-02.json`: `PASS=14 FAIL=0`
- `outputs/yt_fh_lsz_chunk061_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk062_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`
- `outputs/yt_fh_lsz_chunk063_multitau_target_timeseries_checkpoint_2026-05-03.json`: `PASS=19 FAIL=0`

Aggregate certificates after the final wave:

- chunk combiner: `63/63` ready L12 chunks, `1008/1000` saved configurations,
  complete L12 support summary constructed
- target-observable ESS: passed with limiting ESS `895.2344666684801`
- autocorrelation ESS gate: passed for target observables over the full L12
  ready set
- fitted response stability: still not passed; relative stdev
  `0.9014700698097433`, spread ratio `5.934886855129659`
- common-window response provenance: fixed `tau=10..12` central slope mean
  `1.4254094730430789`, relative stdev `0.00561579672777511`
- common-window pooled response estimator: relative standard error
  `0.0007075238835801541`
- response-window acceptance: not passed; v2 rows are present for
  chunks017-063, chunks001-016 still lack v2 rows, and fitted production
  response stability remains open
- v2 target-response stability: bounded support passed for positive
  `tau=0..9` windows over chunks017-063
- pole-fit postprocessor: input exists, `4` mode rows, `2` distinct shells;
  not fit-ready because the four-mode surface lacks three positive shells
- retained-route certificate: `PASS=155 FAIL=0`
- campaign-status certificate: `PASS=181 FAIL=0`

The complete L12 combiner summary gives a finite-difference residue proxy:

```text
dGamma/dp_hat^2 = -0.7168380257823943
finite residue proxy = 1.3950152810442051
```

This is explicitly not `kappa_s` and not a scalar pole derivative.

## Claim Boundary

This checkpoint completes the L12 four-mode support surface, not PR #230
retained closure. It does not derive `kappa_s`, `Z_match`, `c2`,
source-Higgs overlap, W/Z response identity, scalar-pole model-class control,
FV/IR control, response-window acceptance, or canonical-Higgs normalization.

Forbidden proof authorities remain unused: `H_unit`, `yt_ward_identity`,
observed top mass, observed `y_t`, `alpha_LM`, plaquette/u0, reduced pilots,
and undeclared unit normalizations.

Exact next action: either launch a separate eight-mode/x8 pole-fit support
stream, or pursue a non-source-only canonical-Higgs/source-overlap route. PR
#230 remains draft/open.
