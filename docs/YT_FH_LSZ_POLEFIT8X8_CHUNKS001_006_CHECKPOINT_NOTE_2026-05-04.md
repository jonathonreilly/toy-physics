# FH/LSZ Eight-Mode/x8 Chunks001-006 Checkpoint

Date: 2026-05-04

PR: #230

Status: bounded production and finite-shell diagnostic support only; closure
proposal is not authorized.

## Scope

Chunks001 through 006 completed in the homogeneous eight-mode/x8 pole-fit
stream launched after the complete four-mode L12 support surface proved
non-fit-ready.  This stream is separate from the four-mode/x16 FH/LSZ chunks
and must not be combined with them as one production ensemble.

The completed slice contains:

- volume: `12^3 x 24`
- mass: `m_lat = 0.75`
- source shifts: `-0.01, 0.0, 0.01`
- scalar-LSZ modes:
  `0,0,0;1,0,0;1,1,0;1,1,1;2,0,0;2,1,0;2,1,1;2,2,0`
- scalar-LSZ noises: `8`
- completed chunks: `6/63`
- saved configurations: `96/1008`

## Production Outputs

| Chunk | Output | Runtime (s) | Source slope | Source slope error | dGamma/dp_hat^2 | Residue proxy |
|---|---|---:|---:|---:|---:|---:|
| 001 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk001_2026-05-04.json` | 3976.337839126587 | 7.181350018490193 | 13.704309069750739 | -0.6965571108006535 | 1.435632462140191 |
| 002 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk002_2026-05-04.json` | 3939.768128156662 | 1.4333305980019257 | 24.826024136840758 | -0.7586848911818095 | 1.3180702708370693 |
| 003 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk003_2026-05-04.json` | 4024.0606021881104 | 1.2434191693220038 | 0.17691959483671785 | -0.7128776350082191 | 1.4027652866237983 |
| 004 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk004_2026-05-04.json` | 4028.0176560878754 | 1.2429217008430031 | 0.10935849762624371 | -0.7324075183056526 | 1.365360096675952 |
| 005 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk005_2026-05-04.json` | 3962.836716890335 | 1.4324630057841239 | 24.358662544694983 | -0.7232719045065232 | 1.3826058965781118 |
| 006 | `outputs/yt_pr230_fh_lsz_polefit8x8_L12_T24_chunk006_2026-05-04.json` | 3911.5403831005096 | 1.4261649641457175 | 24.497735037097236 | -0.7286886195809245 | 1.372328280047943 |

The source-slope rows are source-coordinate diagnostics.  They are not
physical top/Yukawa evidence and are not used to define `y_t`.

## Diagnostic Fit State

After the six completed chunks, the combiner and postprocessor report:

- polefit8x8 combiner: `PASS=6 FAIL=0`
- polefit8x8 postprocessor: `PASS=5 FAIL=0`
- retained-route certificate: `PASS=158 FAIL=0`
- campaign-status certificate: `PASS=184 FAIL=0`
- readiness: `mode_rows=8`, `distinct_shells=8`,
  `positive_shells=7`, `has_zero_shell=true`
- diagnostic saved configurations: `96`
- complete L12 target: `false`
- model-class gate: still blocks retained use

The finite-shell diagnostic fit is numerically well-formed over the current
eight mode rows, but it is not a physical scalar-pole extraction.  The
postprocessor records the current fit as diagnostic support only; finite-volume
scaling, FV/IR control, pole-saturation/model-class authority, and
canonical-Higgs/source-overlap closure remain load-bearing blockers.

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

The live wave orchestrator continued after this checkpoint with chunks007-012
running.

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
