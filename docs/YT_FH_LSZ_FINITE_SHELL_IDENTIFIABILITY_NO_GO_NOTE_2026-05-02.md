# PR #230 FH/LSZ Finite-Shell Pole-Fit Identifiability No-Go

**Status:** exact negative boundary / FH-LSZ finite-shell pole-fit identifiability no-go
**Runner:** `scripts/frontier_yt_fh_lsz_finite_shell_identifiability_no_go.py`
**Certificate:** `outputs/yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json`

## Claim

Finite same-source Euclidean `Gamma_ss(p^2)` shell rows do not by themselves
fix the LSZ inverse-propagator derivative at a scalar pole.

The runner constructs analytic deformations of a base inverse propagator:

```text
Gamma_epsilon(x) = slope * (x - x_pole)
                 + epsilon * (x - x_pole) * product_i (x - x_i)
```

For every sampled shell `x_i`, the deformation vanishes.  It also vanishes at
the chosen negative `x_pole`, so all models share the same finite shell values
and the same pole.  But

```text
d Gamma_epsilon / dx | x_pole
```

changes by `epsilon * product_i (x_pole - x_i)`.

## Boundary

This does not say a future production pole fit is useless.  It says finite
shell rows need an additional analytic model-class theorem, pole saturation
argument, continuum control, or production acceptance gate before the fitted
`dGamma_ss/dp^2` can be load-bearing retained evidence.

## Non-Claims

- Does not set `kappa_s = 1`.
- Does not use `H_unit`, Ward authority, observed targets, alpha/plaquette/u0,
  or reduced pilots as proof input.
- Does not claim retained or proposed-retained closure.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_fh_lsz_finite_shell_identifiability_no_go.py
python3 scripts/frontier_yt_fh_lsz_finite_shell_identifiability_no_go.py
# SUMMARY: PASS=7 FAIL=0
```
