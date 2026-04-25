# Koide Q/delta readout-retention split audit

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_q_delta_readout_retention_split_no_go.py`
**Status:** conditional support; neither Q nor the full lane closes retained-only

## Theorem Attempt

Remove the operational-quotient descent condition by deriving strict readout
from existing retained source-response and APS observability notes.

## Result

Split, but not a retained closure on either side.

## Q Side

The retained observable-principle notes support local scalar source-response
readout:

```text
physical scalar observables = coefficients in the local source expansion
of W[J] after subtracting the zero-source baseline.
```

On the exact normalized second-order carrier, the zero-background member gives:

```text
W_red(K) = log(1+K_plus) + log(1+K_perp)
dW/dK |_{K=0} = (1,1).
```

Conditionally, this gives:

```text
K_TL = 0
Q = 2/3.
```

But source-response coefficients are zero-probe coefficients around a chosen
background. The current retained packet does not prove that the physical
charged-lepton background source is zero. A nonzero traceless background is
still an exact source-response background and is the surviving `Z` source
coordinate.

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
RESIDUAL_Q = derive_physical_background_source_zero_equiv_Z_erasure
RESIDUAL_SCALAR = derive_Q_background_zero_and_closed_APS_to_open_endpoint_functor
RESIDUAL_DELTA = selected_line_endpoint_transition_tau_not_removed_by_closed_readout
```

## Consequence

The condition is sharpened:

```text
Q source condition:       zero-probe readout is retained, but zero physical
                          background remains to be derived;
delta endpoint condition: still open.
```

Full dimensionless Koide closure still needs the endpoint functor/descent
theorem and the Q background-zero/Z-erasure theorem.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_delta_readout_retention_split_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_DELTA_READOUT_RETENTION_SPLIT_NO_GO=TRUE
Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_Q=FALSE
Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_DELTA=FALSE
Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_FULL_LANE=FALSE
CONDITIONAL_Q_CLOSES_IF_PHYSICAL_BACKGROUND_SOURCE_IS_ZERO=TRUE
RESIDUAL_Q=derive_physical_background_source_zero_equiv_Z_erasure
RESIDUAL_SCALAR=derive_Q_background_zero_and_closed_APS_to_open_endpoint_functor
RESIDUAL_DELTA=selected_line_endpoint_transition_tau_not_removed_by_closed_readout
```
