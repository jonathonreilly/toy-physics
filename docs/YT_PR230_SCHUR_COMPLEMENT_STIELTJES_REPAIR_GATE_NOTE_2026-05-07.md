# PR #230 Schur-Complement Stieltjes Repair Gate

**Status:** bounded-support / Schur-complement Stieltjes repair split; scalar-LSZ authority absent
**Runner:** `scripts/frontier_yt_pr230_schur_complement_stieltjes_repair_gate.py`
**Certificate:** `outputs/yt_pr230_schur_complement_stieltjes_repair_gate_2026-05-07.json`

## Claim

The completed two-source taste-radial chunks001-022 contain a stricter finite
object than the raw `C_ss` proxy:

```text
G(q) = [[C_ss(q), C_sx(q)], [C_sx(q), C_xx(q)]]
C_s|x(q) = det(G(q)) / C_xx(q)
C_x|s(q) = det(G(q)) / C_ss(q)
```

The runner tests these Schur-complement residuals against the same necessary
positive Stieltjes condition used by the strict scalar-LSZ gate:

```text
C(x2) - C(x1) <= 0        for x2 > x1,        x = q_hat^2.
```

## Current Result

The source residual `C_s|x` does not repair the raw-source problem.  It is
positive, but it increases from the zero mode to the first shell across the
ready chunks.

The complement residual `C_x|s` is the useful new artifact: it is positive and
decreases from the zero mode to the first shell across the ready chunks.  This
survives the first-shell necessary Stieltjes check and gives a targeted
candidate for later complement-scalar diagnostics.

This is not scalar-LSZ closure.  A first-shell monotonicity pass is only a
necessary one-volume finite-row test.  The current surface still lacks:

- the complete `63/63` row packet;
- isolated-pole/model-class authority;
- multivolume FV/IR limiting authority;
- canonical `O_H` identity or measured `C_spH/C_HH` pole-overlap rows;
- W/Z physical-response bypass rows.

## Boundary

The result sharpens the next route without weakening the claim firewall.
Future work should track `C_x|s` as the better finite Schur residual, but it
cannot be read as canonical Higgs or physical top-Yukawa evidence unless a
same-surface `O_H` theorem, source-overlap rows, W/Z response rows, or strict
pole/FV/IR theorem makes it load-bearing.

No retained or proposed-retained closure is authorized.  The gate does not set
`kappa_s`, `c2`, or `Z_match` to one and does not use `H_unit`,
`yt_ward_identity`, `alpha_LM`, plaquette/`u0`, or observed top/y_t inputs.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_schur_complement_stieltjes_repair_gate.py
python3 scripts/frontier_yt_pr230_schur_complement_stieltjes_repair_gate.py
# SUMMARY: PASS=22 FAIL=0
```
