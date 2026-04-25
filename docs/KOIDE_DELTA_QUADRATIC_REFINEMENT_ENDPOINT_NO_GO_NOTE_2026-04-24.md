# Koide delta quadratic-refinement endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_quadratic_refinement_endpoint_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

The retained `Z_3` tangent weights are `(1,2)`.  The ambient APS value is
quadratic in those weights:

```text
w1*w2 / 3^2 = 2/9.
```

Test whether that quadratic refinement forces the selected-line Berry endpoint

```text
theta_end - theta0 = eta_APS.
```

## Executable theorem

The product quadratic is exact:

```text
w1*w2/3^2 = 2/9 = eta_APS.
```

This is strong support for the ambient APS scalar.  But the selected-line Berry
phase is still an open-path endpoint variable:

```text
delta = theta_end - theta0.
```

The residual is

```text
RESIDUAL_ENDPOINT = theta_end - theta0 - eta_APS.
```

An affine bridge

```text
delta = u q_product + v
```

needs `u=1,v=0` to identify the endpoint with the quadratic APS density.  That
identity bridge is the missing physical functor, not a consequence of the
quadratic arithmetic alone.

## Why this is not closure

The runner separates two facts:

- ambient fixed-point APS density is exactly `2/9`;
- selected-line open-path endpoint still needs a physical endpoint law.

The first is retained support.  The second is the closure gap.

## Falsifiers

- A retained Berry/APS functor proving `theta_end-theta0 = w1*w2/3^2`.
- A selected-line boundary theorem that turns the ambient fixed-point density
  into an open-path endpoint with unit normalization.
- A uniqueness theorem showing no other endpoint is compatible with the same
  quadratic APS support.

## Boundaries

- The runner covers exact `Z_3` weights `(1,2)`, product quadratic arithmetic,
  comparison with the ABSS/APS value, and affine endpoint bridges.
- It does not exclude a future physical functor from ambient quadratic APS data
  to selected-line Berry endpoints.

## Hostile reviewer objections answered

- **"But `2/9` is exactly `w1*w2/9`."**  Correct; that is support.  It is not
  an endpoint theorem.
- **"Why not use the identity map?"**  Because that is precisely the missing
  Berry/APS bridge.  It must be derived, not selected.
- **"Does this undermine the APS route?"**  No.  It narrows the route: the only
  missing piece is the physical functor from quadratic APS density to the
  selected-line endpoint.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_quadratic_refinement_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_DELTA_QUADRATIC_REFINEMENT_ENDPOINT_NO_GO=TRUE
DELTA_QUADRATIC_REFINEMENT_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR=selected_line_endpoint_equals_quadratic_APS_density
```
