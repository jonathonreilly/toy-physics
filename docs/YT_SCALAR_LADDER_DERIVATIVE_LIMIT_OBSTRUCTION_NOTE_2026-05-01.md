# Top-Yukawa Scalar Ladder Derivative Limiting-Order Obstruction

**Date:** 2026-05-01
**Status:** exact negative boundary / scalar ladder derivative limiting-order obstruction
**Runner:** `scripts/frontier_yt_scalar_ladder_derivative_limit_obstruction.py`
**Certificate:** `outputs/yt_scalar_ladder_derivative_limit_obstruction_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary / scalar ladder derivative limiting-order obstruction
conditional_surface_status: conditional-support if a retained zero-mode, IR, and finite-volume limiting prescription is derived
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "The scalar ladder derivative has prescription-dependent IR behavior; no retained limiting order is derived."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Obstruction

The total-momentum derivative scout made the missing matrix-LSZ quantity
computable:

```text
d lambda_max / d p^2
```

This runner tests whether that derivative can already be used without a new
zero-mode/IR limiting theorem.  It cannot.

Validation:

```text
python3 scripts/frontier_yt_scalar_ladder_derivative_limit_obstruction.py
# SUMMARY: PASS=8 FAIL=0
```

## Result

On the same `N=4`, `m=0.50` finite ladder surface:

- with the gauge zero mode included, lowering `mu_IR^2` from `0.50` to `0.02`
  changes the local-source derivative magnitude by `13.882x`;
- with the zero mode removed, the same derivative changes by only `1.09046x`;
- the low-IR included/removed derivative split is `24.0024x` for the local
  source and `66.321x` for the normalized point-split source;
- the pole test crosses only in the zero-mode-included prescription:
  `[False, False, True, True, True]` versus `[False, False, False, False,
  False]`.

Therefore a finite total-momentum derivative is not yet a scalar-LSZ residue
theorem.  The route still needs the retained gauge-zero-mode prescription,
IR/finite-volume limiting order, scalar projector/source normalization, and
then either a pole-derivative theorem or production pole data.

## Claim Boundary

This block does not claim retained or proposed-retained top-Yukawa closure.  It
does not set `kappa_s = 1`, does not use `H_unit` or `yt_ward_identity`, and
does not use alpha/plaquette/u0, observed values, or reduced cold pilots as
proof inputs.
