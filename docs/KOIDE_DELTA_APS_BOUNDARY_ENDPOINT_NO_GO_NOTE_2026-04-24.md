# Koide delta APS-boundary endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_aps_boundary_endpoint_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Test whether an APS boundary condition or a one-dimensional self-adjoint
extension parameter physically identifies the selected-line Berry endpoint
with the retained ambient APS value.

The target bridge remains:

```text
delta_physical = theta_end - theta0 = eta_APS = 2/9.
```

## Executable theorem

The retained ambient scalar is exact:

```text
eta_APS = 2/9.
```

For the standard shifted boundary Dirac model,

```text
eta(alpha) = 1 - 2 alpha,     0 < alpha < 1.
```

Matching the ambient value fixes the boundary spectral shift

```text
alpha = 7/18.
```

But `alpha` is not the selected-line Berry endpoint.  The identity
`delta=alpha` gives `7/18`, not `2/9`.  A general affine bridge

```text
delta = u alpha + v
```

needs an extra normalization:

```text
v = 2/9 - 7u/18,
```

or, with zero offset, `u=4/7`.  Those are bridge choices, not consequences of
the APS boundary condition.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end - theta0 - eta_APS
RESIDUAL_BRIDGE = boundary_alpha_to_selected_line_delta_normalization
```

The APS-boundary route therefore reduces to the same physical endpoint
identification primitive already isolated by the selected-line and
spectral-flow no-gos.

## Why this is not closure

This packet distinguishes three objects that can be conflated:

- the ambient APS eta value `2/9`;
- the boundary spectral shift `alpha=7/18`;
- the selected-line open-path Berry endpoint `theta_end-theta0`.

The boundary condition relates the first two in the model.  It does not supply
the physical map from either one to the selected-line endpoint.

## Falsifiers

- A retained theorem proving `delta=eta(alpha)` for the selected-line Berry
  carrier with unit normalization.
- A boundary-condition derivation that maps `alpha=7/18` to
  `theta_end-theta0=2/9` without adding an affine normalization.
- A physical APS/Berry functor that sends the ambient eta invariant to the
  selected-line endpoint and proves uniqueness.

## Boundaries

- The runner covers the shifted one-dimensional boundary Dirac eta law and
  affine bridge maps from boundary spectral shift to selected-line endpoint.
- It does not exclude a future non-affine physical functor or a higher
  dimensional boundary condition whose endpoint map is independently retained.

## Hostile reviewer objections answered

- **"APS already gives eta, so why not set delta to eta?"**  That sentence is
  exactly the missing bridge.  APS gives the ambient scalar; the selected-line
  endpoint is separate open-path data.
- **"The boundary parameter might be the endpoint."**  The boundary parameter
  fixed by `eta=2/9` is `7/18`, not `2/9`; identifying it with the endpoint
  gives the wrong scalar.
- **"Can an affine normalization fix it?"**  Yes, but the required
  normalization is free unless a retained theorem fixes it.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_aps_boundary_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_DELTA_APS_BOUNDARY_ENDPOINT_NO_GO=TRUE
DELTA_APS_BOUNDARY_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_BRIDGE=boundary_alpha_to_selected_line_delta_normalization
```
