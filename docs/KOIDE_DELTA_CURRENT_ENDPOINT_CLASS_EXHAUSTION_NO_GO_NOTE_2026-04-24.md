# Koide delta current endpoint-class exhaustion no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_current_endpoint_class_exhaustion_no_go.py`  
**Status:** no-go/exhaustion over current audited classes; not closure

## Purpose

This artifact consolidates the current branch-local delta packet.  It is a
bounded theorem over audited endpoint/APS bridge classes, not a claim that no
future boundary theory can close the Brannen phase.

## Audited classes

The runner checks that the packet covers:

- selected-line `CP^1` Berry endpoint geometry;
- selected-line nonzero winding versus primitive endpoint degree;
- selected-line projector retention versus physical boundary source support;
- historical actual-route Berry closure review;
- fractional-period and octahedral-domain endpoint arithmetic;
- APS boundary endpoint and Callan-Harvey descent normalization;
- local `Cl(3)` boundary source grammar;
- determinant-line closed holonomy versus open phase;
- primitive degree-one endpoint generator audits;
- Dai-Freed open determinant-line trivialization;
- spectral-flow and Maslov/open-phase quantization;
- minimal endpoint-action audits;
- `Z_3` character holonomy and quadratic refinement;
- Chern-Simons level normalization;
- spin-c/lens eta refinement;
- joint finite `C_3` boundary inflow.
- source-response covariance transfer from the strict Q readout.

## Common residual

All audited routes reduce to one endpoint bridge:

```text
theta_end - theta0 - eta_APS
```

equivalently:

```text
selected-line open endpoint trivialization
closed APS eta to open Berry endpoint functor
endpoint gauge / smooth open Berry contribution
fractional endpoint unit map
spin-c closed eta sector to selected-line endpoint map
source-response covariance leaves selected endpoint degree mu - 1
based orientation-preserving primitive endpoint generator not derived
minimal endpoint action selects degree zero unless nonzero primitive sector is retained
selected-line nonzero winding does not fix endpoint degree
Cl3 boundary source grammar leaves selected projector and endpoint exact offset free
selected-line projector exists but physical source support on it is not retained
```

## Exhaustion boundary

The exact closed support value remains:

```text
eta_APS = 2/9.
```

The open problem is not the number.  It is the physical theorem that reads this
closed invariant as the selected open Berry endpoint without fitting `eta` as a
root target.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR = physical_open_selected_line_Berry_APS_identification
RESIDUAL_SCALAR = selected_endpoint_degree_mu_minus_one
RESIDUAL_PRIMITIVE = selected_endpoint_based_orientation_preserving_primitive_generator
RESIDUAL_ACTION = nonzero_positive_primitive_endpoint_sector_not_retained
```

## Why this is not closure

The packet proves narrowing, not the Brannen bridge.  A future positive closure
must derive the open endpoint functor or equivalent boundary condition.

## Falsifiers

- A retained open determinant-line trivialization that maps closed APS eta to
  the selected line.
- A boundary/variational theorem selecting the endpoint before APS matching.
- A physical functor from spin-c/lens eta data to the selected-line open
  Berry phase.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_current_endpoint_class_exhaustion_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_CURRENT_ENDPOINT_CLASS_EXHAUSTION_NO_GO=TRUE
DELTA_CURRENT_ENDPOINT_CLASS_EXHAUSTION_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_FUNCTOR=physical_open_selected_line_Berry_APS_identification
```
