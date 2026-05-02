# PR #230 FH/LSZ Stieltjes Model-Class Obstruction

**Status:** exact negative boundary / FH-LSZ Stieltjes model-class obstruction
**Runner:** `scripts/frontier_yt_fh_lsz_stieltjes_model_class_obstruction.py`
**Certificate:** `outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json`

## Claim

Positive spectral/Stieltjes structure is not enough to make finite Euclidean
`C_ss(q)` or `Gamma_ss(q)` shell rows determine the scalar LSZ residue.

The runner constructs positive pole-plus-continuum models:

```text
C(x) = Z_h / (x + m_h^2) + sum_j w_j / (x + M_j^2)
```

with all `w_j >= 0`.  The models share the same finite shell values and the
same pole location, but use different `Z_h`.  Since the inverse-propagator
derivative at the pole scales like `1/Z_h`, the FH/LSZ readout still varies.

## Boundary

This does not rule out a valid production pole fit.  It says the model-class
gate cannot be satisfied by saying only "positive spectral representation."
The gate still needs pole saturation, a continuum threshold/gap theorem,
multi-volume production continuum control, or a microscopic scalar denominator
theorem.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_stieltjes_model_class_obstruction.py
python3 scripts/frontier_yt_fh_lsz_stieltjes_model_class_obstruction.py
# SUMMARY: PASS=6 FAIL=0
```
