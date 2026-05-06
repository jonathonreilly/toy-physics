# Koide delta lattice Wilson selected-eigenline no-go

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py`
**Status:** no-go; finite Wilson support selects a spectral subspace, not the physical selected line

## Theorem Attempt

Upgrade the finite L=3 Wilson-Dirac support model into a positive Brannen
endpoint bridge.  The hoped-for theorem was:

```text
Wilson operator + body-diagonal Z3 action
  -> canonical rank-one boundary eigenline
  -> selected open endpoint is the unit APS/anomaly channel.
```

## Result

Negative.  In this finite Wilson realization, the ambient eta proxy equals the
exact APS comparator `2/9` for the frozen L=3 construction, so this note no
longer claims a retained ambient eta-mismatch residual.  The no-go is narrower:
the zero-mode character sector relevant to the selected endpoint has rank two.
The retained data select a spectral projector/eigenspace, not a unique rank-one
line inside it.

The runner constructs two orthonormal zero-mode lines with the same spin-lift
`Z3` character.  Every normalized mixture:

```text
psi(alpha) = cos(alpha) psi_0 + sin(alpha) psi_1
```

is still a Wilson zero mode with the same character.

## Unified Residual

The rank-two line freedom gives:

```text
selected_channel = cos(alpha)^2
spectator_channel = sin(alpha)^2
```

and therefore:

```text
delta_open / eta_APS - 1 =
  -spectator_channel + c / eta_APS.
```

Closure requires:

```text
alpha = 0
c = 0.
```

Those are a selected rank-one eigenline theorem and an endpoint-lift theorem.
They are not consequences of the finite Wilson data.

## Endpoint Lift

Even after the finite ambient scalar matches the APS comparator, selecting a
rank-one line is still independent data.  Multiplying a selected lift by:

```text
exp(i s t)
```

leaves the projector and Wilson eigenline unchanged while shifting the open
endpoint by `s`.  Thus the endpoint basepoint remains an independent residual.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_EIGENLINE = rank_two_zero_mode_character_sector_not_canonically_split
RESIDUAL_TRIVIALIZATION = wilson_eigenline_endpoint_lift_not_fixed
RESIDUAL_SCALAR = minus_spectator_channel_plus_c_over_eta_APS
```

## Falsifiers

- A retained theorem proving the physical Brannen line is a unique rank-one
  summand of the finite Wilson zero-mode character sector.
- A retained theorem excluding the orthogonal zero-mode line as a spectator.
- A retained theorem fixing the Wilson eigenline endpoint lift/basepoint.

## Verification

2026-05-06 rerun transcript:
`outputs/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go_2026-05-06.txt`.

Run:

```bash
python3 scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO=TRUE
DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_EIGENLINE=rank_two_zero_mode_character_sector_not_canonically_split
RESIDUAL_TRIVIALIZATION=wilson_eigenline_endpoint_lift_not_fixed
RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS
```
