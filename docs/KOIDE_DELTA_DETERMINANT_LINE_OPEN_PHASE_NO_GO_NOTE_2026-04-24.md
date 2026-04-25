# Koide delta determinant-line open-phase no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_determinant_line_open_phase_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use determinant-line/Bismut-Freed holonomy from the APS eta invariant to fix
the selected-line Brannen endpoint.

APS eta gives a closed-loop holonomy:

```text
Hol_loop = exp(2*pi*i*eta_APS).
```

The bridge needs an open selected-line phase:

```text
delta_open = theta_end - theta0.
```

## Executable theorem

The ambient value remains exact:

```text
eta_APS = 2/9
Hol_loop = exp(4*pi*i/9).
```

But open phases depend on endpoint trivialization:

```text
delta_open -> delta_open + chi_end - chi_start.
```

For any open segment phase, a complementary closing phase can reproduce the
same closed holonomy:

```text
open + closing = eta_APS.
```

Examples verified by the runner:

```text
open=0,   closing=2/9
open=1/9, closing=1/9
open=2/9, closing=0
open=1/3, closing=-1/9
```

All have the same closed determinant-line holonomy.

## Residual

```text
RESIDUAL_SCALAR = theta_end - theta0 - eta_APS
RESIDUAL_ENDPOINT = theta_end - theta0 - eta_APS
RESIDUAL_TRIVIALIZATION = selected_line_open_phase_endpoint_trivialization
```

## Why this is not closure

Closed APS holonomy is gauge-invariant support.  The selected-line Brannen
phase is an open-path endpoint.  Turning a closed holonomy into a specific open
segment phase requires endpoint trivializations or an equivalent physical
Berry/APS functor.

## Falsifiers

- A retained trivialization theorem fixing the selected-line endpoints.
- A determinant-line functor proving the selected open segment, not only the
  closed loop, has phase `eta_APS`.
- A physical construction where the complementary closing segment is canonical
  and has zero phase.

## Boundaries

- The runner covers the distinction between closed determinant-line holonomy
  and open selected-line Berry phase.
- It does not exclude a future theorem that supplies the missing endpoint
  trivialization.

## Hostile reviewer objections answered

- **"APS gives the holonomy."**  Yes, for a closed determinant line.  The
  Brannen phase is an open endpoint.
- **"Take the logarithm of the holonomy."**  That picks a closed-loop phase
  modulo integers; it still does not choose which open segment carries it.
- **"Set the closing segment to zero."**  That is the missing trivialization
  theorem.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_determinant_line_open_phase_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_DELTA_DETERMINANT_LINE_OPEN_PHASE_NO_GO=TRUE
DELTA_DETERMINANT_LINE_OPEN_PHASE_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=theta_end-theta0-eta_APS
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION=selected_line_open_phase_endpoint_trivialization
```
