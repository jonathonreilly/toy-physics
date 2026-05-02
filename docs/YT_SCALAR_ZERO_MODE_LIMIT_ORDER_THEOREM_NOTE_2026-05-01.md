# YT Scalar Zero-Mode Limit-Order Theorem Note

**Date:** 2026-05-01  
**Status:** exact negative boundary / scalar zero-mode limit-order theorem  
**Runner:** `scripts/frontier_yt_scalar_zero_mode_limit_order_theorem.py`  
**Certificate:** `outputs/yt_scalar_zero_mode_limit_order_theorem_2026-05-01.json`

## Purpose

This block attacks the next exact residual after the scalar ladder
residue-envelope and Ward-kernel obstructions.  It asks whether the current
finite Wilson-exchange ladder already contains a selected scalar-channel
zero-mode / IR / finite-volume limit that could make the LSZ denominator
derivative load-bearing.

It does not.  The obstruction is not merely numerical scatter in a finite
ladder witness.  The zero-mode contribution has an exact path dependence.

## Exact Zero-Mode Piece

For the finite ladder matrix used by the existing scalar-channel scouts,
retaining the gauge zero mode adds

```text
Delta M_ii = (4/3) w_i / (V mu_IR^2)
```

where `V=N^4` and `w_i` is the scalar-source fermion-bubble weight.  The
runner verifies directly that

```text
M_included - M_removed = diag(Delta M)
```

with zero off-diagonal remainder on the tested lattice.

This immediately gives different limits:

| Order or path | zero-mode behavior |
|---|---|
| `mu_IR^2 -> 0` at fixed `N` | diverges as `1 / mu_IR^2` |
| `N -> infinity` at fixed `mu_IR^2` | vanishes as `1 / N^4` |
| `mu_IR^2 proportional to N^-4` | finite nonzero contribution |
| `mu_IR^2 proportional to N^-6` | grows with `N` |

The current PR #230 surface has no retained theorem selecting one of these as
the physical scalar-channel denominator limit.

## Runner Result

```text
python3 scripts/frontier_yt_scalar_zero_mode_limit_order_theorem.py
# SUMMARY: PASS=8 FAIL=0
```

The runner checks:

- parent ladder derivative/residue/Ward-kernel obstructions are loaded;
- the zero-mode term is exactly diagonal;
- fixed-volume behavior scales as `1 / mu_IR^2`;
- fixed-IR volume-first behavior removes the zero-mode term;
- box-scaled regulator paths can leave finite or growing zero-mode terms;
- the included kernel eigenvalue is bounded below by the zero-mode piece.

## Claim Boundary

This is not retained closure and not proposed-retained support.  It does not
derive `kappa_s`, does not set `kappa_s = 1`, and does not use `H_unit`,
`yt_ward_identity`, observed top/Yukawa values, alpha/plaquette/`u0`, reduced
pilots, `c2 = 1`, or `Z_match = 1` as proof input.

The next analytic theorem must supply the gauge fixing, zero-mode prescription,
IR/finite-volume limiting order, and convergence of the pole derivative.  The
alternative is production same-source scalar pole data with that prescription
fixed before the LSZ fit.
