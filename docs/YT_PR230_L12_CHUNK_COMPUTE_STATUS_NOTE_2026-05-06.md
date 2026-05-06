# PR230 completed-L12 chunk compute status

**Status:** bounded-support / completed L12 same-source chunk compute status; physical `y_t` closure still open
**Runner:** `scripts/frontier_yt_pr230_l12_chunk_compute_status.py`
**Certificate:** `outputs/yt_pr230_l12_chunk_compute_status_2026-05-06.json`

## Result

The completed chunk campaign provides real L12 same-source FH/LSZ support data,
not physical top-Yukawa closure.

The four-mode/x16 and eight-mode/x8 streams are both complete at `63/63` chunks
and `1008` saved configurations.  Their source-response summaries agree within
one sigma:

| Stream | Source response | Standard error |
| --- | ---: | ---: |
| four-mode/x16 | 1.2448751329919734 | 0.035821721982903024 |
| eight-mode/x8 | 1.245372948398497 | 0.03175795951253233 |

The cross-stream difference is `z = 0.010398804406050486`, so the completed L12
source-response support is internally consistent.

## Negative Boundary

The same completed polefit8x8 rows block the tempting finite-shell scalar-LSZ
shortcut.  The finite-shell `C_ss` proxy increases with `p_hat^2`, and the
inverse proxy `Gamma_ss = 1/C_ss` decreases with `p_hat^2`.  That behavior is
not a strict positive Stieltjes two-point certificate and not a
complete-Bernstein inverse-denominator certificate.

The runner records both data-side blockers:

- Stieltjes proxy shortcut blocked by seven adjacent shell increases in `C_ss`;
- complete-Bernstein inverse shortcut blocked by seven adjacent shell decreases
  in `Gamma_ss`.

## Boundary

This artifact does not compute `m_t(pole)` or `y_t(v)`.  It remains
single-volume, finite-shell, same-source support.  The missing closure inputs
are still:

- L16/L24 finite-volume control;
- FV/IR/threshold authority;
- scalar-LSZ denominator authority;
- canonical `O_H` or source-Higgs overlap rows;
- matching/running closure;
- aggregate retained-route authorization.

The runner does not use `H_unit`, `yt_ward_identity`, observed targets,
`alpha_LM`, plaquette, or `u0`.  It does not define `y_t_bare` or set
`kappa_s`, `c2`, `Z_match`, or `cos(theta)` to one.
