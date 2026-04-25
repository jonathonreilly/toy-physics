# Koide delta actual-route Berry closure review no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_actual_route_berry_review_no_go.py`  
**Status:** Nature-grade review no-go; not closure

## Theorem under review

Older actual-route Berry notes state that the selected-line `CP^1` Berry
holonomy closes the Brannen phase offset:

```text
delta = 2/9.
```

The current review standard is stricter: the route must derive the physical
open endpoint, not solve for the point where the endpoint equals the ambient
APS value.

## What survives

The selected-line Berry carrier is exact support.  For

```text
chi(theta) = (1, exp(-2 i theta)) / sqrt(2),
```

the runner verifies:

```text
i <chi | partial_theta chi> = 1,
```

so the canonical connection is:

```text
A = dtheta.
```

The open holonomy is therefore:

```text
delta(m) = theta(m) - theta0.
```

## Review failure

If `m_*` is defined by:

```text
theta(m_*) - theta0 = eta_APS,
```

then the missing endpoint value has been supplied as the root equation.

The same Berry geometry permits:

```text
theta(m) - theta0 = d
```

for any supplied endpoint displacement `d` in the branch.  The connection gives
the observable; it does not choose the endpoint.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR = closed_APS_eta_to_open_selected_line_endpoint
```

## Why this is not closure

The actual-route Berry theorem provides a correct physical carrier for the
phase.  It does not derive why the selected endpoint displacement equals the
closed APS eta invariant.  That is exactly the still-open Brannen bridge.

## Falsifiers

- A retained theorem deriving the endpoint `m_*` without using `eta_APS` as the
  root target.
- A canonical functor from the closed APS determinant-line invariant to the
  open selected-line Berry endpoint.
- A variational or boundary condition on the selected line whose unique
  endpoint has displacement `2/9` before APS matching is invoked.

## Boundaries

- This review does not reject the selected-line Berry carrier.
- It rejects promotion of the historical actual-route Berry note as
  Nature-grade closure under the current no-target-import standard.

## Hostile reviewer objections answered

- **"The Berry connection is canonical."**  Yes.  The endpoint still is not.
- **"The selected point is unique once `delta=2/9` is imposed."**  That is a
  uniqueness-after-target statement.
- **"The ambient APS value is exact."**  Yes.  The missing theorem is the
  closed-to-open endpoint identification.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_actual_route_berry_review_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_ACTUAL_ROUTE_BERRY_REVIEW_NO_GO=TRUE
DELTA_ACTUAL_ROUTE_BERRY_REVIEW_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR=closed_APS_eta_to_open_selected_line_endpoint
```
