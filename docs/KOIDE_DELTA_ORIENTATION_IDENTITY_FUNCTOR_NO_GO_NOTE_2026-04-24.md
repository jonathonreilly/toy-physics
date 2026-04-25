# Koide delta orientation identity functor no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_orientation_identity_functor_no_go.py`  
**Status:** no-go; orientation and unit close only after an identity-functor law is retained

## Theorem Attempt

Use determinant-line orientation, unit preservation, and selected-line
orientation to force the endpoint functor:

```text
F(eta) = eta.
```

## Result

Conditional positive reduction, not retained closure.

If the closed-to-open map is a unit-preserving orientation-preserving group
isomorphism, then:

```text
c = 0
n = +1
F(eta_APS) = eta_APS.
```

That would close delta.

## Obstruction

The current retained packet does not prove that the selected-line endpoint map
is that isomorphism.

Two exact counterfunctors remain:

```text
orientation reversal:
  theta -> -theta
  delta_open -> -delta_open
  F(eta) = -eta.
```

```text
endpoint basepoint shift:
  theta0 -> theta0 + s
  delta_open -> delta_open - s
  F(eta) = n eta + c.
```

Closed APS sign-pinning fixes the ambient sign.  It does not by itself orient
the selected open endpoint coordinate or identify its basepoint with the
determinant-line unit.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR_DEGREE = n_minus_one_orientation_alignment_not_retained
RESIDUAL_FUNCTOR_OFFSET = c_endpoint_basepoint_not_retained
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_orientation_identity_functor_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_ORIENTATION_IDENTITY_FUNCTOR_NO_GO=TRUE
DELTA_ORIENTATION_IDENTITY_FUNCTOR_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR_DEGREE=n_minus_one_orientation_alignment_not_retained
RESIDUAL_FUNCTOR_OFFSET=c_endpoint_basepoint_not_retained
```
