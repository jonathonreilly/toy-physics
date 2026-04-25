# Koide delta relative-cobordism endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_relative_cobordism_endpoint_no_go.py`  
**Status:** no-go; relative cobordism controls the total, not the open endpoint split

## Theorem Attempt

Treat the selected open Brannen line as a relative cobordism boundary.  Maybe
relative eta/cobordism uniqueness identifies the selected open endpoint with
the closed APS invariant.

## Result

Negative.  Relative eta data split as:

```text
eta_closed = eta_relative + boundary_correction.
```

Cobordism invariance controls the closed total.  It does not choose the split.

An exact endpoint shift:

```text
eta_relative -> eta_relative + s
boundary_correction -> boundary_correction - s
```

preserves the closed APS value.

## Residual

The desired endpoint is equivalent to:

```text
boundary_correction = 0.
```

That is the same identity endpoint law in relative-cobordism language.

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_BOUNDARY_CORRECTION =
  selected_relative_boundary_correction_not_forced_zero
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_relative_cobordism_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_RELATIVE_COBORDISM_ENDPOINT_NO_GO=TRUE
DELTA_RELATIVE_COBORDISM_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_BOUNDARY_CORRECTION=selected_relative_boundary_correction_not_forced_zero
```
