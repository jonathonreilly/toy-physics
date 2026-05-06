# PR #230 FH/LSZ Production Postprocess Gate

**Status:** bounded-support / FH-LSZ L12 chunked postprocess surface complete; closure gates remain open
**Runner:** `scripts/frontier_yt_fh_lsz_production_postprocess_gate.py`
**Certificate:** `outputs/yt_fh_lsz_production_postprocess_gate_2026-05-01.json`

## Question

The joint Feynman-Hellmann / same-source scalar-LSZ route has exact monolithic
production launch commands and a completed seed-controlled L12 replacement
surface.  The remaining risk is procedural and physical: a manifest, a partial
production file, an L12-only combined support row, or a finite-shell diagnostic
must not be mistaken for physical `y_t` evidence.

This note adds an executable gate for the postprocess step.  It answers:

```text
What must exist before the FH/LSZ route may attempt a retained-proposal
certificate?
```

## Inputs

- `outputs/yt_fh_lsz_production_manifest_2026-05-01.json`
- Original expected monolithic manifest outputs:
  - `outputs/yt_pr230_fh_lsz_production_L12_T24_2026-05-01.json`
  - `outputs/yt_pr230_fh_lsz_production_L16_T32_2026-05-01.json`
  - `outputs/yt_pr230_fh_lsz_production_L24_T48_2026-05-01.json`
- Completed replacement support surfaces:
  - `outputs/yt_fh_lsz_chunk_combiner_gate_2026-05-01.json`
  - `outputs/yt_fh_lsz_ready_chunk_set_checkpoint_2026-05-02.json`
  - `outputs/yt_fh_lsz_polefit8x8_chunk_combiner_gate_2026-05-04.json`
  - `outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json`
- Blocking model-class gate:
  - `outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json`

## Gate

The route is not eligible for retained-proposal wording unless all load-bearing
requirements below are true:

1. The original monolithic manifest is not used as evidence by itself.
2. The L12 four-mode/x16 chunked support surface is complete.
3. The dynamic L12 ready-chunk checkpoint agrees with the combiner.
4. The separate L12 eight-mode/x8 finite-shell diagnostic surface is complete.
5. L16/L24 or equivalent multivolume same-source FH/LSZ scaling is accepted.
6. A postprocess fit isolates the scalar pole and derives
   `dGamma_ss/dp^2` at the pole.
7. The finite-volume, IR, and zero-mode limiting order is controlled in the
   analysis or by a separate theorem certificate.
8. Finite-shell fits pass a model-class, scalar-denominator, pole-saturation,
   continuum, moment-threshold, or equivalent strict acceptance certificate.
9. A canonical-Higgs/source-overlap bridge, same-source W/Z response bridge,
   Schur A/B/C bridge, or neutral primitive-cone bridge is present.
10. The proof does not import `kappa_s = 1`, `H_unit`, `yt_ward_identity`,
   observed top mass or observed `y_t`, `c2 = 1`, `Z_match = 1`,
   `alpha_LM`, plaquette, or `u0` as proof input.
11. A retained-proposal certificate passes after the production pole analysis
    and bridge checks.

## Result

Current status is bounded support.  The original monolithic manifest remains
valid launch planning, but the three monolithic production outputs are absent.
The replacement L12 chunked surfaces are complete:

- the four-mode/x16 stream supplies same-source `dE/ds` and `C_ss(q)` support;
- the separate eight-mode/x8 stream supplies a finite-shell diagnostic fit;
- both surfaces explicitly remain non-readout support.

The completed L12 support does not close the physics route.  It still lacks
accepted L16/L24 or equivalent multivolume scaling, an isolated scalar pole
inverse-derivative fit, finite-volume/IR/zero-mode control, model-class
authority, and a canonical-Higgs/source-overlap or same-source W/Z response
bridge.

Therefore this block is a support/readiness boundary, not closure:

```text
proposal_allowed: false
retained_proposal_gate_ready: false
l12_postprocess_support_ready: true
```

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_production_postprocess_gate.py
python3 scripts/frontier_yt_fh_lsz_production_postprocess_gate.py
# SUMMARY: PASS=12 FAIL=0
```

## Next Action

Do not spend closure wording on the completed L12 support rows.  Supply one
fresh same-surface bridge artifact: `O_sp`-Higgs pole rows with canonical
`O_H` identity/normalization, a real source-coordinate transport certificate,
genuine same-source W/Z production response rows with covariance and
non-observed `g2` authority, same-surface Schur A/B/C kernel rows, a strict
scalar-LSZ moment-threshold-FV certificate, or a neutral primitive-cone /
irreducibility certificate.
