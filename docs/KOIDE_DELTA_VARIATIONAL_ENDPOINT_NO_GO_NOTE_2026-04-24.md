# Koide delta variational endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_variational_endpoint_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use a physical variational principle to select the Brannen endpoint:

```text
endpoint action extremum
  -> theta_end - theta0 = eta_APS.
```

## Executable theorem

For a quadratic endpoint action:

```text
S = (delta - c)^2 / 2,
```

the runner verifies:

```text
stationary endpoint = c.
```

To get the APS endpoint:

```text
c = 2/9.
```

## Obstruction

A natural minimum-norm phase action:

```text
S = delta^2 / 2
```

selects:

```text
delta = 0,
```

not `2/9`.  A periodic action likewise selects its supplied phase center modulo
periods.  The variational route therefore moves the primitive into the action
center or boundary condition.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_ACTION_CENTER = endpoint_variational_center_not_retained
```

## Why this is not closure

The variational mechanism is not enough by itself.  A Nature-grade proof must
derive the endpoint action center from retained structure rather than placing
`2/9` into the action.

## Falsifiers

- A retained endpoint action whose unique stationary point is `2/9` before
  importing the APS value as a target.
- A proof that minimum-norm zero phase is physically inadmissible and the next
  natural extremum is `2/9`.
- A boundary variational principle whose center is fixed by `Cl(3)/Z^3` data.

## Boundaries

- Covers quadratic and periodic endpoint actions with free phase center.
- Does not refute a future retained action deriving its center.

## Hostile reviewer objections answered

- **"Physical endpoints extremize actions."**  The extremum is determined by
  the supplied action center.
- **"Use minimum phase."**  That gives zero.
- **"Use a periodic potential."**  It still contains a phase center or period
  branch choice.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_variational_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_VARIATIONAL_ENDPOINT_NO_GO=TRUE
DELTA_VARIATIONAL_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_ACTION_CENTER=endpoint_variational_center_not_retained
```
