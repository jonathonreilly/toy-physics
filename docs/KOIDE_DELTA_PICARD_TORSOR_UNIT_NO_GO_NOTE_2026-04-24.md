# Koide delta Picard-torsor unit no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_picard_torsor_unit_no_go.py`  
**Status:** no-go; monoidal unit preservation needs a retained endpoint basepoint

## Theorem Attempt

Remove the endpoint offset `c` by treating the selected open endpoint phases as
a Picard/monoidal target.  A monoidal functor preserves the unit, so perhaps:

```text
c = 0
```

is forced.

## Result

Negative from retained data alone.  Closed APS phases are based group phases.
Open selected-line endpoints are naturally a `U(1)` torsor until a boundary
section is supplied.

An unbased torsor morphism has:

```text
F(eta) = n eta + c.
```

Group additivity gives:

```text
F(x+y)-F(x)-F(y) = -c.
```

So `c = 0` follows only after choosing a target unit/basepoint.  That is the
selected endpoint trivialization law.

## Boundary

If a retained zero endpoint section is supplied, the route does remove `c`:

```text
F(0)=0 -> c=0.
```

But even then the degree residual remains:

```text
F(eta_APS)=eta_APS -> n=1.
```

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION = selected_line_endpoint_basepoint_not_retained
RESIDUAL_SCALAR = n_minus_one_plus_c_over_eta_APS
```

## Falsifiers

- A retained physical zero section for the selected open endpoint torsor.
- A retained based Picard functor from closed APS phase to the selected
  endpoint phase.
- A retained degree-one theorem after the basepoint is fixed.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_picard_torsor_unit_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_PICARD_TORSOR_UNIT_NO_GO=TRUE
DELTA_PICARD_TORSOR_UNIT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION=selected_line_endpoint_basepoint_not_retained
RESIDUAL_SCALAR=n_minus_one_plus_c_over_eta_APS
```
