# Koide delta APS-selector identity-gluing no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_aps_selector_identity_gluing_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use the existing equivariant Berry/APS selector support to derive identity
endpoint gluing:

```text
APS eta support + selected Brannen line
  -> tau = 0
  -> theta_end - theta0 = eta_APS.
```

## What works

The retained APS fixed-point route gives:

```text
eta_APS = 2/9.
```

This remains exact closed support.

## Obstruction

The closed/open bridge has the form:

```text
eta_APS = delta_open + tau.
```

The runner verifies:

```text
tau = 2/9 - delta_open.
```

So many open phases share the same closed APS value:

```text
delta_open = 0   -> tau = 2/9
delta_open = 1/9 -> tau = 1/9
delta_open = 2/9 -> tau = 0
delta_open = 1/3 -> tau = -1/9.
```

The selected-line support runner identifies the matched endpoint.  It does not
prove that the endpoint transition `tau` is physically zero.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_GLUING = derive_tau_zero_identity_endpoint_gluing
```

## Why this is not closure

The APS selector support is necessary, but identity endpoint gluing is the
remaining physical law.  Finding the selected-line point where the open phase
equals `2/9` is not the same as deriving why the physical endpoint transition
must vanish.

## Falsifiers

- A retained theorem deriving `tau=0` from selected-line boundary data.
- A proof that the selected Brannen segment is the entire APS boundary segment.
- A physical exclusion of all nonzero endpoint transitions preserving the
  closed APS value.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_aps_selector_identity_gluing_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_APS_SELECTOR_IDENTITY_GLUING_NO_GO=TRUE
DELTA_APS_SELECTOR_IDENTITY_GLUING_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_GLUING=derive_tau_zero_identity_endpoint_gluing
```
