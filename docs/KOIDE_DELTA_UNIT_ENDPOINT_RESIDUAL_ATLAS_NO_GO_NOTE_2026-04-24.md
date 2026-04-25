# Koide delta unit-endpoint residual atlas no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_unit_endpoint_residual_atlas_no_go.py`  
**Status:** atlas/no-go; the reduced residual is not closed

## Purpose

After endpoint-functor classification and the spectral-flow/Callan-Harvey
degree audits, the delta residual has a sharper form:

```text
delta_open = mu eta_APS + c.
```

Here `mu` packages endpoint functor degree, descent/current normalization, and
spectral-flow identification.  Closure requires:

```text
mu = 1
c = 0.
```

## What This Adds

This artifact prevents the next step from repeating a local variant of the same
failed route.  It records the reduced residual and ranks new attacks that could
remove it only if they produce a retained theorem.

## Ranked New Routes

1. Primitive anomaly-channel theorem: derive that the selected Brannen line is
   the unique primitive Callan-Harvey inflow channel.
2. Picard torsor unit theorem: derive a based endpoint object from boundary
   data, which could force `c = 0`.
3. Determinant-line universal property: identify the selected endpoint functor
   as the universal determinant-line holonomy map.
4. Marked relative cobordism: derive a marked boundary section that kills the
   boundary correction.
5. Reflection-positive boundary state: use real/antiunitary positivity to fix
   endpoint orientation.
6. Locality and cluster primitive current: exclude multiple selected-line
   current copies.
7. Lattice Wilson endpoint theorem: construct a finite selected boundary
   eigenline and prove unit spectral-flow degree.
8. Source-response covariance transfer: derive delta readout covariance from
   the strict Q readout without importing the operational quotient law.
9. Endpoint variational action with no tunable center: search for a boundary
   functional whose Euler equation gives the unit endpoint.
10. Higher `Cl(3)` boundary source grammar: exhaust local boundary source
   polynomials coupled to the endpoint functor.

## Excluded Shortcuts

- Declare the selected line to be the unit channel.
- Choose an endpoint basepoint because it closes.
- Fit a boundary action to `eta_APS`.
- Identify closed APS and open endpoint by notation.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_SCALAR = mu_minus_one_plus_c_over_eta_APS
NEXT_ATTACK = primitive_anomaly_channel_theorem
```

## Falsifiers

- A retained theorem proving primitive selected-line anomaly-channel uniqueness.
- A retained based Picard/trivialization theorem proving `c = 0`.
- A retained determinant-line universal property proving the selected endpoint
  functor is degree one.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_unit_endpoint_residual_atlas_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_UNIT_ENDPOINT_RESIDUAL_ATLAS_NO_GO=TRUE
DELTA_UNIT_ENDPOINT_RESIDUAL_ATLAS_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_SCALAR=mu_minus_one_plus_c_over_eta_APS
NEXT_ATTACK=primitive_anomaly_channel_theorem
```
