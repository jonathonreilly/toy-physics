# Top-Yukawa Large-Nc Pole-Dominance Boundary

**Date:** 2026-05-01  
**Status:** exact negative boundary / large-`N_c` pole dominance not PR230 closure  
**Runner:** `scripts/frontier_yt_large_nc_pole_dominance_boundary.py`  
**Certificate:** `outputs/yt_large_nc_pole_dominance_boundary_2026-05-01.json`

```yaml
actual_current_surface_status: exact-negative-boundary
conditional_surface_status: conditional-support if a finite-Nc continuum bound is later derived
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Finite-Nc continuum suppression is not derived from the current retained surface."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

A possible scalar-residue repair is to invoke large-`N_c` pole dominance and
treat the scalar continuum as negligible.  This note checks whether that can
certify PR #230 at physical `N_c=3`.

## Result

```text
python3 scripts/frontier_yt_large_nc_pole_dominance_boundary.py
# SUMMARY: PASS=6 FAIL=0
```

At `N_c=3`, a natural `1/N_c^2` continuum allowance changes the canonical
Yukawa proxy by more than five percent.  A `1/N_c` allowance is much larger.
Sub-percent closure would require a percent-level or stronger continuum bound,
not just an asymptotic slogan.

## Consequence

Large-`N_c` pole dominance remains useful intuition, but it is not retained
closure for PR #230.  A future route must derive either:

1. pole saturation directly at `N_c=3`;
2. a finite-`N_c` continuum bound strong enough for the target uncertainty; or
3. the scalar pole residue by direct measurement.

## Non-Claims

- This note does not reject large-`N_c` support as intuition.
- This note does not use observed top, Higgs, or Yukawa values.
- This note does not define `y_t` through an `H_unit` matrix element.
- This note does not use `alpha_LM`, plaquette, or `u_0` as proof input.
