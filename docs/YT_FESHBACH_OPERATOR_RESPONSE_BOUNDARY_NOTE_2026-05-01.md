# Top-Yukawa Feshbach Operator-Response Boundary

**Date:** 2026-05-01  
**Status:** exact support / Feshbach response boundary  
**Runner:** `scripts/frontier_yt_feshbach_operator_response_boundary.py`  
**Certificate:** `outputs/yt_feshbach_operator_response_boundary_2026-05-01.json`

```yaml
actual_current_surface_status: exact-support
conditional_surface_status: conditional-support for future scalar/gauge dressing theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Feshbach covariance preserves responses but does not equate distinct microscopic scalar and gauge residues."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The existing gauge crossover companion suggests that exact Feshbach projection
preserves the gauge spectral response.  This note asks whether that idea closes
the PR #230 scalar/gauge dressing blocker.

## Result

```text
python3 scripts/frontier_yt_feshbach_operator_response_boundary.py
# SUMMARY: PASS=5 FAIL=0
```

The runner verifies the Schur/Feshbach resolvent identity on a finite block
operator:

```text
P (z-H)^-1 P = (z-H_eff(z))^-1.
```

For projected gauge and scalar sources, the full and effective low-energy
responses agree to numerical precision, and the scalar/gauge response ratio is
preserved by the exact projection.

## Boundary

This is exact support, not top-Yukawa closure.  Feshbach projection preserves
operator-specific responses; it does not prove that the microscopic scalar
residue equals the microscopic gauge residue.  Scaling the scalar source changes
the scalar/gauge response ratio while the Feshbach identity remains exact.

Therefore the crossover route cannot supply the missing common-dressing theorem
for PR #230.  The remaining theorem must derive the scalar source/residue from
the interacting substrate and then either prove equality to the gauge response
or carry an independently measured scalar/gauge dressing ratio.

## Non-Claims

- This note is not a retained `y_t` derivation.
- This note is not a production measurement.
- This note does not use observed top, Higgs, or Yukawa values.
- This note does not define `y_t` through an `H_unit` matrix element.
- This note does not promote the gauge crossover companion theorem.
