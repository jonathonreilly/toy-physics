# Top-Yukawa Scalar Spectral-Saturation No-Go

**Date:** 2026-05-01  
**Status:** exact negative boundary / scalar spectral saturation no-go  
**Runner:** `scripts/frontier_yt_scalar_spectral_saturation_no_go.py`  
**Certificate:** `outputs/yt_scalar_spectral_saturation_no_go_2026-05-01.json`

```yaml
actual_current_surface_status: exact-negative-boundary
conditional_surface_status: conditional-support for a future pole-saturation or continuum-bound theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Pole saturation and continuum control remain open imports."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

A possible scalar-LSZ repair is to use a positive spectral representation:

```text
C(p^2) = sum_i rho_i / (p^2 + m_i^2)
```

and hope that the source curvature fixes the Higgs-carrier pole residue.  This
note tests that assumption.

## Result

```text
python3 scripts/frontier_yt_scalar_spectral_saturation_no_go.py
# SUMMARY: PASS=6 FAIL=0
```

The runner constructs positive pole-plus-continuum spectral models that share
the same low-order source-curvature data:

```text
C(0), C'(0) fixed
```

while the isolated pole residue varies over a factor greater than two.  The
canonical Yukawa proxy therefore varies as `sqrt(residue)` even though the
visible low-order curvature data are unchanged.

## Consequence

Spectral positivity is not enough.  PR #230 still needs one of:

1. a retained scalar-channel pole-saturation theorem;
2. a retained continuum-bound theorem that fixes the pole residue; or
3. direct measurement of the scalar pole residue / top correlator route.

## Non-Claims

- This note does not rule out a future scalar pole theorem.
- This note does not use observed top, Higgs, or Yukawa values.
- This note does not define `y_t` through an `H_unit` matrix element.
- This note does not use `alpha_LM`, plaquette, or `u_0` as proof input.
