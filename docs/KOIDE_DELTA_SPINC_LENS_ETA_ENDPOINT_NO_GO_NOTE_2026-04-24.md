# Koide delta spin-c/lens eta endpoint no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_spinc_lens_eta_endpoint_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Refine the ambient APS eta calculation by spin or spin-c/lens-space data:

```text
spin-c refined eta -> selected-line open endpoint -> delta = 2/9.
```

## Executable theorem

For the retained `Z_3` lens/orbifold data with weights `(1,2)`, the spin
structure count is trivial because `p=3` is odd:

```text
spin structures = 1.
```

Spin-c or flat character twists are labeled by:

```text
m in Z_3.
```

The runner computes the twisted closed eta values:

```text
eta_0 = 2/9
eta_1 = -1/9
eta_2 = -1/9.
```

The closed eta differences are:

```text
eta_0 - eta_1 = eta_0 - eta_2 = 1/3.
```

## Obstruction

These are closed APS refinements.  The selected Brannen phase remains an open
selected-line endpoint:

```text
theta_end - theta0.
```

Each closed eta value would still require an endpoint identification:

```text
theta_end - theta0 = eta_m.
```

Choosing the untwisted `m=0` value recovers the known ambient support number
`2/9`, but it does not prove that this closed invariant is the physical open
endpoint.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION = open_selected_line_endpoint_not_fixed_by_closed_spinc_eta
```

## Why this is not closure

Spin-c refinement organizes closed APS eta values.  It does not supply the
selected-line open Berry trivialization or functor.  Endpoint gauge can still
fit any chosen closed eta value.

## Falsifiers

- A retained theorem identifying the selected line with the untwisted spin-c
  sector and proving its open endpoint equals the closed eta invariant.
- A canonical open determinant-line trivialization tied to the spin-c structure.
- A proof that nontrivial twists are physically forbidden and that the remaining
  untwisted closed value must be read as the open endpoint.

## Boundaries

- Covers `Z_3` character twists for the retained `(1,2)` eta formula and the
  odd-`p` spin-count obstruction.
- Does not exclude a future physical functor from spin-c eta data to the
  selected open line.

## Hostile reviewer objections answered

- **"`eta_0` is exactly `2/9`."**  Yes; that is the known ambient support value.
- **"The spin structure is unique."**  That removes spin ambiguity, but it does
  not turn a closed invariant into an open endpoint.
- **"Choose the untwisted spin-c sector."**  That is a sector choice plus an
  endpoint bridge, not a derivation.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_spinc_lens_eta_endpoint_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_SPINC_LENS_ETA_ENDPOINT_NO_GO=TRUE
DELTA_SPINC_LENS_ETA_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION=open_selected_line_endpoint_not_fixed_by_closed_spinc_eta
```
