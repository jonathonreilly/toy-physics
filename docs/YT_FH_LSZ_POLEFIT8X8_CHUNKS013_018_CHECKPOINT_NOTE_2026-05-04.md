# FH/LSZ Eight-Mode/x8 Chunks013-018 Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production and finite-shell diagnostic support only; closure
proposal is not authorized.

## Scope

Chunks013 through 018 completed in the homogeneous eight-mode/x8 pole-fit
stream.  Together with chunks001-012, the stream now has `18/63` ready chunks
and `288/1008` saved configurations.

This remains a separate namespace from the completed four-mode/x16 L12 support
surface.  The two streams must not be mixed as one physical ensemble.

## Production Outputs

| Chunk | Output | Runtime (s) | Seed | Source slope | Source slope error |
|---|---|---:|---:|---:|---:|
| 013 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk013_2026-05-04.json` | 3186.2328350543976 | 2026051913 | 1.248322182088491 | 0.08831615078274661 |
| 014 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk014_2026-05-04.json` | 3180.616758108139 | 2026051914 | 1.4324249468868333 | 24.871979421126877 |
| 015 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk015_2026-05-04.json` | 3184.0728561878204 | 2026051915 | 6.811404498177325 | 13.42056949773107 |
| 016 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk016_2026-05-04.json` | 3191.770659685135 | 2026051916 | 1.4174699753546902 | 24.317868513824884 |
| 017 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk017_2026-05-04.json` | 3182.1574301719666 | 2026051917 | 1.4265587183514068 | 24.79764853035926 |
| 018 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk018_2026-05-04.json` | 3160.8979461193085 | 2026051918 | 1.4172278330481936 | 24.702138218358364 |

The source-slope rows are source-coordinate diagnostics.  They are not a
physical top/Yukawa readout and are not used to define `y_t`.

## Diagnostic Fit State

After the 18 completed chunks, the combiner and postprocessor report:

- polefit8x8 combiner: `PASS=6 FAIL=0`
- polefit8x8 postprocessor: `PASS=5 FAIL=0`
- retained-route certificate: `PASS=172 FAIL=0`
- campaign-status certificate: `PASS=198 FAIL=0`
- full positive closure assembly gate: `PASS=23 FAIL=0`
- readiness: `mode_rows=8`, `distinct_shells=8`,
  `positive_shells=7`, `has_zero_shell=true`
- diagnostic saved configurations: `288`
- combined source-response summary: `1.2459077261334814 +/- 0.06117241631664582`
- diagnostic finite-shell slope: `dGamma/dp_hat^2 = -0.6666571877936004`
- diagnostic pole proxy: `p_hat^2 = 12.233872065671168`
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
# SUMMARY: PASS=172 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=198 FAIL=0

python3 scripts/frontier_yt_pr230_full_positive_closure_assembly_gate.py
# SUMMARY: PASS=23 FAIL=0
```

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
