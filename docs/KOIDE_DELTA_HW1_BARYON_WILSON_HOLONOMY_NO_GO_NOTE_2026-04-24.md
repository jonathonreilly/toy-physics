# Koide delta hw1+baryon Wilson holonomy no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_hw1_baryon_wilson_holonomy_no_go.py`  
**Status:** executable no-go; 4x4 support does not identify the selected endpoint

## Theorem Attempt

Use a `4x4` `hw=1+baryon` Wilson holonomy to force the selected charged-lepton
line to carry phase

```text
2/d^2 = 2/9.
```

## Result

Negative.  A `3+1` carrier can host the total APS/anomaly phase, but determinant
or total-anomaly constraints fix only

```text
theta_selected + theta_baryon = eta_APS.
```

The selected open endpoint has

```text
delta_open = theta_selected + c.
```

Therefore

```text
delta_open - eta_APS = -theta_baryon + c.
```

Closure requires both

```text
theta_baryon = 0
c = 0.
```

Those are precisely the selected-channel support theorem and endpoint
basepoint theorem.

## Counterstates

The runner verifies exact total-support-preserving counterstates:

```text
all phase on baryon
half selected / half baryon
selected phase plus nonzero endpoint offset
```

All preserve the total support structure while failing selected delta closure.

## Residual

```text
RESIDUAL_CHANNEL = selected_channel_carries_whole_eta_not_retained
RESIDUAL_TRIVIALIZATION = selected_endpoint_offset_c_equals_zero_not_retained
COUNTERSTATE = total_eta_carried_by_baryon_or_split_channel
NEXT_ATTACK = derive_selected_channel_support_law_or_close_residual_as_explicit_primitive
```

## Hostile Review

This does not demote the 4x4 route as support.  It says the support is
insufficient for closure until a non-uniform Wilson holonomy law proves that
the selected charged-lepton channel, not the baryon/spectator channel, carries
the whole APS phase with zero endpoint offset.

## Verification

```bash
python3 scripts/frontier_koide_delta_hw1_baryon_wilson_holonomy_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_hw1_baryon_wilson_holonomy_no_go.py
```
