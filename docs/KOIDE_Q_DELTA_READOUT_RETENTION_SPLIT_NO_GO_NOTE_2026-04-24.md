# Koide Q/delta readout-retention split audit

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_delta_readout_retention_split_no_go.py`  
**Status:** split result; Q advances, full lane does not close

## Theorem Attempt

Remove the operational-quotient descent condition by deriving strict readout
from existing retained source-response and APS observability notes.

## Result

Split.

## Q Side

The retained observable-principle notes support strict zero-source local scalar
readout:

```text
physical scalar observables = coefficients in the local source expansion
of W[J] after subtracting the zero-source baseline.
```

On the exact normalized second-order carrier:

```text
W_red(K) = log(1+K_plus) + log(1+K_perp)
dW/dK |_{K=0} = (1,1).
```

Therefore:

```text
K_TL = 0
Q = 2/3.
```

This reframes nonzero `K` as an external probe/source coordinate, not the
physical baseline readout.

## Delta Side

The retained APS computation fixes the closed topological value:

```text
eta_APS = 2/9.
```

But the selected-line Brannen parameter is still an open endpoint coordinate:

```text
eta_APS = delta_open + tau.
```

Closed readout alone leaves the split free:

```text
tau = 2/9 - delta_open.
```

So replacing the selected-line endpoint by the closed APS value is a readout
bridge, not a derivation from APS alone.

## Residual

```text
RESIDUAL_SCALAR = closed_APS_to_open_selected_line_endpoint_functor
RESIDUAL_DELTA = selected_line_endpoint_transition_tau_not_removed_by_closed_readout
```

## Consequence

The condition is partly reduced:

```text
Q source condition:       removed if strict source-response readout is accepted;
delta endpoint condition: still open.
```

Full dimensionless Koide closure still needs the endpoint functor/descent
theorem.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_delta_readout_retention_split_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO=TRUE
Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_Q=TRUE
Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_DELTA=FALSE
Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_FULL_LANE=FALSE
RESIDUAL_SCALAR=closed_APS_to_open_selected_line_endpoint_functor
RESIDUAL_DELTA=selected_line_endpoint_transition_tau_not_removed_by_closed_readout
```
