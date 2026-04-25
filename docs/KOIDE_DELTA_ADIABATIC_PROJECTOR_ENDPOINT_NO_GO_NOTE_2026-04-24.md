# Koide delta adiabatic spectral-projector endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_adiabatic_projector_endpoint_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use the adiabatic selected spectral line itself to derive the Brannen endpoint:

```text
selected spectral projector path
  -> open Berry endpoint
  -> theta_end - theta0 = eta_APS = 2/9.
```

## Executable theorem

For the two-level line:

```text
psi(theta,phi) = (cos(theta/2), exp(i phi) sin(theta/2)),
```

the open Berry integral along `phi:0->Phi` is:

```text
gamma_open = sin(theta/2)^2 * Phi.
```

Matching the APS value requires:

```text
Phi = (2/9) / sin(theta/2)^2.
```

That is an endpoint/path selection, not a consequence of the projector theorem.

## Obstruction

The projector is invariant under a phase lift:

```text
psi -> exp(i chi) psi
|psi><psi| unchanged.
```

The open Berry integral shifts by endpoint gauge:

```text
gamma_open -> gamma_open + chi_end - chi0.
```

The runner verifies that unchanged projector data can fit `2/9` by choosing
endpoint gauge:

```text
chi_end = chi0 - gamma_open + 2/9.
```

## Closed APS split

The closed APS value can be decomposed into many open/complement segments:

```text
open = 0,   complement = 2/9
open = 1/9, complement = 1/9
open = 2/9, complement = 0
open = 1/3, complement = -1/9.
```

Selecting the open segment equal to `eta_APS` is exactly the missing endpoint
functor.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION = open_selected_line_projector_endpoint_lift_not_retained
```

## Why this is not closure

The adiabatic theorem gives the correct mathematical object, the selected
spectral line.  It does not provide a canonical open endpoint phase lift or a
physical path endpoint that makes the open phase equal to closed APS eta.

## Falsifiers

- A retained spectral-projector path with endpoint lift fixed before using the
  APS value.
- A canonical selected-line trivialization whose open Berry integral is
  independent of endpoint gauge.
- A theorem that the Brannen selected segment is the whole APS closed loop,
  rather than an open part of it.

## Boundaries

- Covers open Berry phases of selected projector paths and endpoint phase-lift
  freedom.
- Does not refute a future physical endpoint-trivialization theorem.

## Hostile reviewer objections answered

- **"The spectral line is selected."**  Selection of the line is not selection
  of the endpoint phase lift.
- **"Adiabatic Berry phase is physical."**  Closed holonomy is; open phase
  needs endpoint data.
- **"Choose the open segment to be the full APS loop."**  That is the residual
  endpoint identification.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_adiabatic_projector_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_ADIABATIC_PROJECTOR_ENDPOINT_NO_GO=TRUE
DELTA_ADIABATIC_PROJECTOR_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION=open_selected_line_projector_endpoint_lift_not_retained
```
