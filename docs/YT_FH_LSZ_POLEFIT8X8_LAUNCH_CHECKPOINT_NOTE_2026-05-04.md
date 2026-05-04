# FH/LSZ Eight-Mode/x8 Pole-Fit Launch Checkpoint

Status: bounded-support / production run-control checkpoint, not retained or proposed_retained.

This note records the next PR230 physics-loop target after completing the
four-mode L12 FH/LSZ support surface.  The completed four-mode stream has
1008 saved configurations, but its scalar two-point rows occupy only the zero
shell and one positive momentum shell.  The pole-fit postprocessor therefore
cannot form an isolated scalar-pole derivative from that stream.

## New Stream

The new stream is intentionally separate:

- namespace: `yt_pr230_fh_lsz_polefit8x8_L12_T24`
- volume: `12^3 x 24`
- mass: `m_lat = 0.75`
- source shifts: `-0.01, 0.0, 0.01`
- scalar-LSZ modes:
  `0,0,0;1,0,0;1,1,0;1,1,1;2,0,0;2,1,0;2,1,1;2,2,0`
- scalar-LSZ noises: `8`
- chunks: `63 x 16` saved configurations, for `1008` target configurations

The mode set has a zero shell plus at least three positive `p_hat^2` shells.
The x8 noise count is accepted only as launch support by the paired x8/x16
variance calibration gate.  It is not scalar-LSZ normalization and it is not a
physical Yukawa readout.

## Artifacts

The new run-control surfaces are:

```bash
python3 scripts/frontier_yt_fh_lsz_polefit8x8_chunk_manifest.py
# SUMMARY: PASS=8 FAIL=0

python3 scripts/frontier_yt_fh_lsz_polefit8x8_chunk_combiner_gate.py
# SUMMARY: PASS=6 FAIL=0

python3 scripts/frontier_yt_fh_lsz_polefit8x8_postprocessor.py
# SUMMARY: PASS=5 FAIL=0

python3 scripts/frontier_yt_retained_closure_route_certificate.py
# SUMMARY: PASS=158 FAIL=0

python3 scripts/frontier_yt_pr230_campaign_status_certificate.py
# SUMMARY: PASS=184 FAIL=0
```

The active orchestrator command is:

```bash
python3 scripts/frontier_yt_fh_lsz_polefit8x8_wave_orchestrator.py \
  --start-index 1 \
  --end-index 63 \
  --max-concurrent 6 \
  --global-max-production-jobs 6 \
  --runtime-minutes 720 \
  --poll-seconds 60 \
  --launch \
  --run-gates
```

At launch, chunks001-006 were running.  The orchestrator records state in:

```text
outputs/yt_fh_lsz_polefit8x8_wave_orchestrator_status_2026-05-04.json
```

## Claim Boundary

This stream does not close PR230.  It still lacks:

- L16/L24 finite-volume scaling;
- FV/IR and zero-mode control;
- a model-class or analytic-continuation theorem for finite-shell pole fits;
- canonical-Higgs/source-overlap closure;
- W/Z response, Schur rows, or a neutral-sector rank-one substitute.

The stream also does not mix with the completed four-mode/x16 L12 ensemble.
Any future combined pole-fit support must consume only homogeneous
eight-mode/x8 chunks from this namespace.

## Forbidden Shortcuts

This checkpoint does not use `H_unit`, `yt_ward_identity`,
`y_t_bare`, observed top mass, observed `y_t`, `alpha_LM`, plaquette, or `u0`
as proof inputs.  It does not set `kappa_s`, `c2`, `Z_match`, or
`cos(theta)` to one.
