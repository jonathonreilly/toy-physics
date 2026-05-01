# Top-Yukawa Scalar Ladder Eigen-Derivative Gate

**Date:** 2026-05-01
**Status:** exact-support / scalar ladder eigen-derivative gate
**Runner:** `scripts/frontier_yt_scalar_ladder_eigen_derivative_gate.py`
**Certificate:** `outputs/yt_scalar_ladder_eigen_derivative_gate_2026-05-01.json`

```yaml
actual_current_surface_status: exact-support / scalar ladder eigen-derivative gate
conditional_surface_status: conditional-support if the momentum-dependent scalar Bethe-Salpeter kernel derivative is derived or measured
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The eigen-derivative gate is exact support, but the momentum-dependent kernel derivative remains open."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Gate

The matrix Bethe-Salpeter form of the scalar pole condition is:

```text
lambda_max(pole) = 1
```

The LSZ residue is not fixed by that crossing alone.  It requires

```text
d lambda_max / d p^2 at the crossing.
```

Validation:

```text
python3 scripts/frontier_yt_scalar_ladder_eigen_derivative_gate.py
# SUMMARY: PASS=7 FAIL=0
```

## Result

The runner holds the candidate pole eigenvalue fixed at `lambda_max = 1` and
varies only the momentum derivative of the ladder matrix.  The residue proxy
and FH/LSZ readout factor move by large factors while the pole-location test
continues to pass.

Therefore a finite ladder eigenvalue witness is not enough for PR #230
closure.  The route needs:

- total-momentum dependence of the scalar Bethe-Salpeter kernel
  `K(k,k';p)`;
- fixed finite-volume, gauge-zero-mode, and IR prescription before
  differentiation;
- `d lambda_max / d p^2` at the scalar pole;
- insertion of that derivative into the same-source FH/LSZ invariant readout.

## Claim Boundary

This is exact support, not retained closure.  It does not set `kappa_s = 1`,
does not use `H_unit` or `yt_ward_identity`, and does not use observed top or
Yukawa values.
