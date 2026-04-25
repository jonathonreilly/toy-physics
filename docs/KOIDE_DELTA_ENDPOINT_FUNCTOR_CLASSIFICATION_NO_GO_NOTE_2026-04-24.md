# Koide delta endpoint-functor classification no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_endpoint_functor_classification_no_go.py`  
**Status:** no-go; endpoint functoriality alone does not close delta

## Theorem Attempt

Remove the remaining delta condition by functoriality alone.  Classify smooth
additive maps from the closed APS phase group to the selected-line open endpoint
phase group.  Perhaps functoriality forces:

```text
delta_open = eta_APS.
```

## Result

Negative, but sharpened.  Smooth additive phase functors have the form:

```text
F(eta) = n eta + c  (mod 1).
```

Unit preservation removes the offset:

```text
F(0) = 0 -> c = 0.
```

But the degree remains:

```text
n = ..., -1, 0, 1, 2, ...
```

Delta closure requires:

```text
n = 1
c = 0.
```

## Interpretation

The classification reduces the residual to two explicit pieces:

```text
RESIDUAL_FUNCTOR_DEGREE = n_minus_one
RESIDUAL_FUNCTOR_OFFSET = c_endpoint_trivialization
```

Choosing `c` is endpoint trivialization.  Choosing `n=1` is the identity
orientation/normalization of the selected-line endpoint functor.  Neither is
forced by functoriality alone.

## Falsifier

An equally functorial non-closing endpoint map is:

```text
F(eta) = -eta
```

or:

```text
F(eta) = 0.
```

Both are excluded only after adding orientation/identity data for the selected
open endpoint functor.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR_DEGREE = n_minus_one
RESIDUAL_FUNCTOR_OFFSET = c_endpoint_trivialization
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_endpoint_functor_classification_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_ENDPOINT_FUNCTOR_CLASSIFICATION_NO_GO=TRUE
DELTA_ENDPOINT_FUNCTOR_CLASSIFICATION_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR_DEGREE=n_minus_one
RESIDUAL_FUNCTOR_OFFSET=c_endpoint_trivialization
```
