# Koide Q/delta retained-observability descent no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_delta_retained_observability_descent_no_go.py`  
**Status:** no-go; current retained observability does not remove the descent condition

## Theorem Attempt

Remove the operational-quotient descent condition by deriving it from the
current retained notion of physical observability.

## Result

Negative.  Current retained observability is too broad.

## Q Obstruction

The central projectors are retained `C3`-invariant effects:

```text
P_plus^2 = P_plus
P_perp^2 = P_perp
P_plus + P_perp = I
[C3, P_plus] = [C3, P_perp] = 0.
```

A retained central state may assign arbitrary probability:

```text
rho(u) = u P_plus + ((1-u)/2) P_perp
probabilities = (u, 1-u).
```

The descended state is the special case `u = 1/2`.  Retained observability
alone does not force it.

## Delta Obstruction

The retained APS computation fixes the closed value:

```text
eta_APS = 2/9.
```

But a closed phase decomposes as:

```text
eta_APS = delta_open + tau.
```

Many open/complement splits preserve the same closed holonomy.  Retained closed
APS observability does not choose the open selected endpoint.

## Residual

```text
RESIDUAL_SCALAR = stricter_quotient_descended_readout_not_retained
RESIDUAL_Q = central_projectors_are_retained_observable_effects
RESIDUAL_DELTA = open_endpoint_split_not_fixed_by_closed_APS_observability
```

## Consequence

To remove the descent condition, the next theorem cannot be generic
observability.  It must prove a stricter statement:

```text
physical charged-lepton readout uses only quotient-descended effects/phases.
```

Without that stricter readout theorem, the previous countermodels remain.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_delta_retained_observability_descent_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_NO_GO=TRUE
Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_CLOSES_Q=FALSE
Q_DELTA_RETAINED_OBSERVABILITY_DESCENT_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=stricter_quotient_descended_readout_not_retained
RESIDUAL_Q=central_projectors_are_retained_observable_effects
RESIDUAL_DELTA=open_endpoint_split_not_fixed_by_closed_APS_observability
```
