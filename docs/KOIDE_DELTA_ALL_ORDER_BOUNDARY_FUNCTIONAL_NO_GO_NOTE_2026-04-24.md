# Koide delta all-order boundary-functional no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_all_order_boundary_functional_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Extend the endpoint audit to all smooth boundary counterterms/trivializations:

```text
closed APS curvature + smooth endpoint naturality
  -> selected open endpoint
  -> theta_end - theta0 = eta_APS.
```

## Executable theorem

A general open endpoint phase has the form:

```text
delta_open = I_path + B_end - B_start.
```

Adding a smooth endpoint functional shifts:

```text
delta_open -> delta_open + chi_end - chi_start.
```

The runner verifies that the same exact term cancels on a closed loop, so
closed APS holonomy/curvature remains fixed.

## Obstruction

For any open path, endpoint functionals can shift the open phase to:

```text
-1/9, 0, 1/9, 2/9, 1/3, ...
```

without changing the closed APS support.  The value `2/9` is one smooth
boundary-functional choice, not a consequence of smoothness or closed APS data.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_BOUNDARY_FUNCTIONAL = smooth_endpoint_counterterms_preserve_closed_APS
```

## Why this is not closure

All-order smooth boundary freedom preserves the closed invariant and leaves the
open endpoint movable.  A Nature-grade bridge still needs a physical endpoint
functional or boundary condition selecting the APS value for the Brannen line.

## Falsifiers

- A retained naturality theorem forbidding all nonzero endpoint counterterms.
- A canonical boundary functional derived from the selected line before using
  the `2/9` value.
- A proof that smooth endpoint variations are physically gauge, while only the
  `2/9` representative is observable.

## Boundaries

- Covers smooth endpoint functionals/counterterms compatible with fixed closed
  APS holonomy.
- Does not refute a future physical boundary condition selecting one endpoint.

## Hostile reviewer objections answered

- **"Closed APS is fixed."**  Yes; endpoint counterterms cancel on closed
  loops.
- **"Use smoothness/naturality."**  Smoothness still allows endpoint
  differences.
- **"Pick the representative with `2/9`."**  That is the missing physical
  boundary-functional law.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_all_order_boundary_functional_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_ALL_ORDER_BOUNDARY_FUNCTIONAL_NO_GO=TRUE
DELTA_ALL_ORDER_BOUNDARY_FUNCTIONAL_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_BOUNDARY_FUNCTIONAL=smooth_endpoint_counterterms_preserve_closed_APS
```
