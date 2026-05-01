# Top-Yukawa Free Staggered Kinetic Coefficient

**Date:** 2026-05-01  
**Status:** exact support / free staggered kinetic coefficient  
**Runner:** `scripts/frontier_yt_free_staggered_kinetic_coefficient.py`  
**Certificate:** `outputs/yt_free_staggered_kinetic_coefficient_2026-05-01.json`

```yaml
actual_current_surface_status: exact-support
conditional_surface_status: conditional-support for a future interacting kinetic/matching theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Exact free-action support only; interacting c2/Z_match and production evidence remain open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The refreshed assumptions exercise identified `c2`, the heavy kinetic-action
coefficient, as a load-bearing import for the nonzero-momentum route.  This
note checks the positive part that can be derived immediately from the free
Wilson-staggered action.

## Result

```text
python3 scripts/frontier_yt_free_staggered_kinetic_coefficient.py
# SUMMARY: PASS=6 FAIL=0
```

For the free Wilson-staggered pole,

```text
sinh(E)^2 = m^2 + sum_i sin(p_i)^2.
```

Therefore the small-momentum kinetic mass is fixed:

```text
M_kin^free = m sqrt(1 + m^2).
```

Finite-momentum estimates converge to this expression; at `L=256`, the maximum
relative error over the tested masses is `9.234e-4`.

## Consequence

This retires one ambiguity only on the free action.  It does not close PR #230:

- interacting SU(3) Wilson gauge dynamics can renormalize the kinetic
  coefficient;
- production nonzero-momentum correlator data are still absent;
- lattice-to-SM top-mass matching is still not derived.

## Non-Claims

- This note is not a production measurement.
- This note is not a `y_t` derivation.
- This note does not use observed top mass as calibration.
- This note does not define `y_t` through an `H_unit` matrix element.
