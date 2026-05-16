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

Negative for the selected-eigenline route.  The zero-mode character sector
relevant to the selected endpoint has rank two: the retained Wilson data
select a spectral projector/eigenspace, not a unique rank-one line inside
it.  This obstruction is structural and `r`-independent.

The runner additionally records, at its frozen `r = 1.0` setting, that the
finite Wilson eta proxy differs from the exact APS value `2/9`.  That
observation is `r`-dependent (at `r = 1.425` the same proxy equals `2/9`
exactly) and is not the load-bearing part of this no-go; see "Scope of the
retained claim" below.

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

Even if the ambient APS value is supplied externally and a rank-one line is
selected, multiplying its lift by:

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
RESIDUAL_AMBIENT = finite_Wilson_eta_proxy_not_exact_APS_value
RESIDUAL_SCALAR = minus_spectator_channel_plus_c_over_eta_APS
```

## Falsifiers

- A retained theorem proving the physical Brannen line is a unique rank-one
  summand of the finite Wilson zero-mode character sector.
- A retained theorem excluding the orthogonal zero-mode line as a spectator.
- A retained theorem fixing the Wilson eigenline endpoint lift/basepoint.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

The primary runner reports 14/14 PASS at the runner's default Wilson
mass `r = 1.0`. Check `A.3` asserts that the finite Wilson eta proxy is
not the exact APS value `2/9`; at `r = 1.0` the computed proxy is
`|eta|/fixed_site = 0.069214821267`, which differs from `2/9 =
0.222222222222`, so A.3 passes.

The runner's no-go flag is therefore the all-pass closeout:

```text
KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO=TRUE
DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_EIGENLINE=rank_two_zero_mode_character_sector_not_canonically_split
RESIDUAL_TRIVIALIZATION=wilson_eigenline_endpoint_lift_not_fixed
RESIDUAL_AMBIENT=finite_Wilson_eta_proxy_not_exact_APS_value
RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS
```

The `KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO=TRUE` flag
reports that, at this runner's frozen `r = 1.0` setting, the
selected-eigenline route returns the negative result documented above:
finite Wilson data select a rank-two character sector rather than a
unique rank-one selected line, and the endpoint lift is not fixed.

## Scope of the retained claim

The structural part of this no-go — that the relevant zero-mode
character sector has rank two, that a CP^1 family of rank-one lines
shares the same Wilson zero-mode and Z3 character data, and that the
selected/spectator residual is `delta/eta_APS - 1 = -spectator_channel +
c / eta_APS` — does not depend on the value of the Wilson mass `r`. It
is a count of multiplicities and an algebraic identity in `alpha` and
`c`.

The `RESIDUAL_AMBIENT` term, by contrast, is `r`-dependent. At the
`build_wilson_lattice` default `r = 1.425` the same construction returns
`|eta|/fixed_site = 0.222222222222 = 2/9` exactly, in which case the
ambient eta proxy matches the APS comparator and `RESIDUAL_AMBIENT`
collapses. The runner records `RESIDUAL_AMBIENT` only as a property of
the frozen `r = 1.0` setting in `main()`; it is not a derived ambient
mismatch and must not be cited as a free-standing obstruction without
also fixing `r`.

Accordingly, the retained no-go content of this note is the rank-two
selected-eigenline obstruction and the endpoint-lift residual. The
ambient-eta line is a recorded observation at the runner's chosen `r`,
not a load-bearing residual.
