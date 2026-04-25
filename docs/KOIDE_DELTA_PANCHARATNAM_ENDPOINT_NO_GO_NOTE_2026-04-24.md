# Koide delta Pancharatnam endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_pancharatnam_endpoint_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use the gauge-invariant Pancharatnam open-phase prescription:

```text
selected-line Pancharatnam phase
  -> canonical open endpoint
  -> theta_end - theta0 = eta_APS.
```

## Executable theorem

For:

```text
psi(theta,phi) = (cos(theta/2), exp(i phi) sin(theta/2)),
```

the Pancharatnam open geometric phase along `phi:0->Phi` is:

```text
arg(cos(theta/2)^2 + exp(i Phi) sin(theta/2)^2)
  - Phi sin(theta/2)^2.
```

The runner verifies that endpoint gauge shifts cancel in this expression after
the endpoint states are supplied.

## Obstruction

Gauge invariance is not endpoint selection.  The phase still depends on the
chosen endpoint projectors and path:

```text
theta = pi/2, Phi = pi/2 -> gamma_P = 0
theta = pi/3, Phi = pi/2 -> gamma_P = atan(1/3) - pi/8.
```

Neither value is `2/9`.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_SELECTION = Pancharatnam_gauge_invariance_does_not_select_endpoint
```

## Why this is not closure

The Pancharatnam prescription answers a gauge question for an already chosen
open path.  The Koide/Brannen bridge needs a physical theorem selecting the
path endpoint or proving that the selected endpoint equals the closed APS eta
value.

## Falsifiers

- A retained endpoint/path theorem that fixes the Pancharatnam phase to `2/9`
  before using the APS value as a target.
- A proof that the selected Brannen path has no admissible endpoint variation.
- A canonical Pancharatnam endpoint section derived from the retained
  `Cl(3)/Z^3` structure.

## Boundaries

- Covers gauge-invariant open Pancharatnam phases for selected two-level line
  paths.
- Does not refute a future physical endpoint-selection theorem.

## Hostile reviewer objections answered

- **"Open Berry phase can be gauge invariant."**  Yes, after endpoint states
  are specified.
- **"Use Pancharatnam instead of raw Berry phase."**  The runner does; the
  result still varies with endpoint/path data.
- **"Pick the endpoint giving `2/9`."**  That is the residual endpoint
  selection.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_pancharatnam_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_PANCHARATNAM_ENDPOINT_NO_GO=TRUE
DELTA_PANCHARATNAM_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_SELECTION=Pancharatnam_gauge_invariance_does_not_select_endpoint
```
