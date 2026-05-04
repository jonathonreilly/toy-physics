# FH/LSZ Eight-Mode/x8 Chunks007-012 Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production and finite-shell diagnostic support only; closure
proposal is not authorized.

## Scope

Chunks007 through 012 completed in the homogeneous eight-mode/x8 pole-fit
stream.  Together with chunks001-006, the stream now has `12/63` ready chunks
and `192/1008` saved configurations.

This remains a separate namespace from the completed four-mode/x16 L12 support
surface.  The two streams must not be mixed as one physical ensemble.

## Production Outputs

| Chunk | Output | Runtime (s) | Source slope | Source slope error | dGamma/dp_hat^2 | Residue proxy |
|---|---|---:|---:|---:|---:|---:|
| 007 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk007_2026-05-04.json` | 4158.75469994545 | 7.277646263068838 | 13.757056834984022 | -0.6978281292411902 | 1.4330176129291146 |
| 008 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk008_2026-05-04.json` | 4144.666440248489 | 7.171594686166061 | 13.556591272959663 | -0.7256475138573788 | 1.3780795508885921 |
| 009 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk009_2026-05-04.json` | 4191.840656995773 | 1.442719668970029 | 24.96612862180435 | -0.7199271198227629 | 1.3890294898825142 |
| 010 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk010_2026-05-04.json` | 4139.072726964951 | 1.4333027881300549 | 24.467523453433078 | -0.7298145412223657 | 1.370211120108817 |
| 011 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk011_2026-05-04.json` | 4250.1118149757385 | 1.2412108348448005 | 0.20663917245248184 | -0.7032374769987659 | 1.4219947495798135 |
| 012 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk012_2026-05-04.json` | 4162.741101264954 | 1.4275173351591353 | 24.66705064073789 | -0.7124274509937443 | 1.403651696190439 |

The source-slope rows are source-coordinate diagnostics.  They are not a
physical top/Yukawa readout and are not used to define `y_t`.

## Diagnostic Fit State

After the 12 completed chunks, the combiner and postprocessor report:

- polefit8x8 combiner: `PASS=6 FAIL=0`
- polefit8x8 postprocessor: `PASS=5 FAIL=0`
- retained-route certificate: `PASS=158 FAIL=0`
- campaign-status certificate: `PASS=184 FAIL=0`
- readiness: `mode_rows=8`, `distinct_shells=8`,
  `positive_shells=7`, `has_zero_shell=true`
- diagnostic saved configurations: `192`
- complete L12 target: `false`
- model-class gate: still blocks retained use

The finite-shell diagnostic fit remains numerically formed over the eight mode
rows, but it is still not physical scalar-pole evidence.  Complete L12
production, L16/L24 scaling, FV/IR control, pole-saturation/model-class
authority, and canonical-Higgs/source-overlap closure remain load-bearing
blockers.

## Commands

```bash
python3 scripts/frontier_yt_fh_lsz_polefit8x8_chunk_combiner_gate.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_fh_lsz_polefit8x8_postprocessor.py
# SUMMARY: PASS=5 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=158 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=184 FAIL=0
```

The live wave orchestrator continued after this checkpoint and backfilled the
next chunk slots.

## Claim Boundary

This checkpoint does not close PR230 and does not authorize retained or
proposed_retained wording.  It still lacks:

- completed homogeneous L12 polefit8x8 production statistics;
- L16/L24 finite-volume scaling;
- FV/IR and zero-mode control;
- scalar-pole model-class or analytic-continuation authority;
- canonical-Higgs/source-overlap closure;
- W/Z response, Schur rows, or a neutral-sector rank-one substitute.

Forbidden proof shortcuts remain unused: `H_unit`, `yt_ward_identity`,
`y_t_bare`, observed top mass, observed `y_t`, `alpha_LM`, plaquette, `u0`,
and undeclared unit normalizations.
