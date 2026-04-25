# Koide delta primitive anomaly-channel no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_primitive_anomaly_channel_no_go.py`  
**Status:** no-go; anomaly primitivity does not identify the selected open line

## Theorem Attempt

Use anomaly cancellation plus channel primitivity to remove the reduced endpoint
condition:

```text
delta_open = mu eta_APS + c.
```

If the selected Brannen line were forced to be the unique primitive
Callan-Harvey inflow channel, then `mu = 1`, and with `c = 0` delta would
close.

## Result

Negative from retained data alone.  In normalized variables, anomaly
cancellation gives:

```text
selected_channel + spectator_channel = 1.
```

The selected endpoint is:

```text
delta_open = selected_channel eta_APS + c.
```

After imposing the total anomaly equation, the exact residual is:

```text
delta_open / eta_APS - 1 =
  -spectator_channel + c / eta_APS.
```

Delta closure requires:

```text
spectator_channel = 0
c = 0.
```

The first statement says the selected Brannen line is the unique primitive
anomaly channel.  That is not derived by the retained total anomaly scalar.

## Counterchannels

The same total anomaly support permits:

```text
selected = 1,   spectator = 0,   c = 0    -> closing endpoint
selected = 0,   spectator = 1,   c = 0    -> selected endpoint 0
selected = 1/2, spectator = 1/2, c = 0    -> selected endpoint eta_APS/2
selected = 1,   spectator = 0,   c = 1/9 -> shifted endpoint
```

If nonnegative integer primitivity is added, the residual narrows to a discrete
support-selection question: whether the selected line is the channel with unit
charge.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_CHANNEL = selected_line_is_unique_primitive_anomaly_channel_not_retained
RESIDUAL_SCALAR = minus_spectator_channel_plus_c_over_eta_APS
```

## Falsifiers

- A retained theorem proving the selected Brannen line carries the primitive
  anomaly unit.
- A retained theorem excluding spectator anomaly channels.
- A retained endpoint basepoint theorem proving `c = 0`.

## Hostile Reviewer Objections Answered

**"But the anomaly must cancel."**  
Yes.  The runner imposes total cancellation.  The obstruction is that total
cancellation does not identify the selected open readout channel.

**"Primitivity should force one unit."**  
It forces a unit somewhere only after integer/nonnegative channel assumptions.
It still does not say the selected Brannen line is that unit channel.

**"Set the spectator to zero."**  
That is exactly the missing physical theorem.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_primitive_anomaly_channel_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_PRIMITIVE_ANOMALY_CHANNEL_NO_GO=TRUE
DELTA_PRIMITIVE_ANOMALY_CHANNEL_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_CHANNEL=selected_line_is_unique_primitive_anomaly_channel_not_retained
RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS
```
