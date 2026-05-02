# PR #230 FH/LSZ Production Postprocess Gate

**Status:** open / FH-LSZ production postprocess gate blocks manifest-as-evidence

## Question

The joint Feynman-Hellmann / same-source scalar-LSZ route now has exact
production launch commands.  The remaining risk is procedural: a manifest, a
partial production file, or a reduced smoke output must not be mistaken for
physical `y_t` evidence.

This note adds an executable gate for the postprocess step.  It answers:

```text
What must exist before the FH/LSZ route may attempt a retained-proposal
certificate?
```

## Inputs

- `outputs/yt_fh_lsz_production_manifest_2026-05-01.json`
- Expected manifest outputs:
  - `outputs/yt_pr230_fh_lsz_production_L12_T24_2026-05-01.json`
  - `outputs/yt_pr230_fh_lsz_production_L16_T32_2026-05-01.json`
  - `outputs/yt_pr230_fh_lsz_production_L24_T48_2026-05-01.json`

## Gate

The route is not eligible for retained-proposal wording unless all of the
following are true:

1. Every manifest output exists.
2. Every output declares `metadata.phase == "production"`.
3. Every output contains common-ensemble scalar source response data with
   source shifts `[-0.01, 0.0, 0.01]`, a `linear_dE_ds` fit, and finite
   `slope_dE_ds_lat`.
4. Every output contains same-source scalar two-point LSZ data with at least
   sixteen noise vectors and the four declared momentum modes.
5. A postprocess fit isolates the scalar pole and derives
   `dGamma_ss/dp^2` at the pole.
6. The finite-volume, IR, and zero-mode limiting order is controlled in the
   analysis or by a separate theorem certificate.
7. The proof does not import `kappa_s = 1`, `H_unit`, `yt_ward_identity`,
   observed top mass or observed `y_t`, `c2 = 1`, `Z_match = 1`,
   `alpha_LM`, plaquette, or `u0` as proof input.
8. A retained-proposal certificate passes after the production pole analysis.

## Result

Current status remains open.  The manifest is valid launch planning, but the
three production outputs are absent, and no scalar pole-fit / inverse
derivative postprocess certificate exists.

Therefore this block is an exact acceptance boundary, not closure:

```text
proposal_allowed: false
retained_proposal_gate_ready: false
```

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_production_postprocess_gate.py
python3 scripts/frontier_yt_fh_lsz_production_postprocess_gate.py
# SUMMARY: PASS=9 FAIL=0
```

## Next Action

Either launch/schedule the production manifest and later run this gate on the
completed production files plus a pole-fit certificate, or pivot to a new
analytic scalar denominator / residue theorem.
