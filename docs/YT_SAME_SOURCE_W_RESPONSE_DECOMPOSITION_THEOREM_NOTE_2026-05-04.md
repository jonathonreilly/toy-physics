# Same-Source W-Response Decomposition Theorem

Status: exact-support / current rows absent, not retained and not
proposed_retained.

This theorem is the real same-source W-response physics needed by PR #230.
It shows exactly what can be extracted if the FH/LSZ top response is paired
with a W-mass response measured under the same scalar source.

Let the scalar source move the canonical Higgs radial coordinate by
`kappa_h ds` and an orthogonal neutral scalar by `kappa_x ds`.  Let the top
couplings to those two neutral directions be `y_h` and `y_x`.  At tree level,
using the existing one-Higgs gauge-mass and Yukawa-selection surfaces,

```text
R_t = d m_t / d s = (y_h kappa_h + y_x kappa_x) / sqrt(2)
R_W = d M_W / d s = g_2 kappa_h / 2
```

so

```text
g_2 R_t / (sqrt(2) R_W)
  = y_h + y_x kappa_x / kappa_h.
```

The unknown source normalization cancels.  This is the useful physics.  The
remaining correction is the orthogonal neutral top-coupling term.

## Consequence

The W-response route can close the source-normalization part of the FH/LSZ
blocker, but only after one of the following is supplied:

- an orthogonal-top null theorem;
- a tomography row measuring and subtracting `y_x kappa_x/kappa_h`;
- source-Higgs Gram-purity rows proving the source pole is the canonical Higgs
  pole.

Without one of these, W response alone is not physical `y_t`.

## Verification

```bash
python3 scripts/frontier_yt_same_source_w_response_decomposition_theorem.py
# SUMMARY: PASS=6 FAIL=0
```

## Non-Claims

This theorem does not provide W rows, top-response rows, scalar-LSZ
model-class control, matching/running, or retained-route approval.  It does
not use `H_unit`, `yt_ward_identity`, observed targets, `alpha_LM`,
plaquette/u0, `kappa_s=1`, `c2=1`, `Z_match=1`, or `cos(theta)=1`.
