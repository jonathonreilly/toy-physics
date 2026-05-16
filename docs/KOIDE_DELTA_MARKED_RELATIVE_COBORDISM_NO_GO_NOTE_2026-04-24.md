# Koide delta marked-relative-cobordism no-go

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_delta_marked_relative_cobordism_no_go.py`
**Status:** no-go; a derived relative mark is scalar on the proposed_retained multiplicity space

## Theorem Attempt

Strengthen relative cobordism by adding a boundary marking derived from the
retained Wilson/APS data.  The hoped-for theorem was:

```text
derived mark
  -> unique rank-one selected Brannen line
  -> based endpoint section
  -> theta_end - theta0 = eta_APS.
```

## Result

Negative from retained data alone.  A mark closes the gap only if it is already
a non-scalar rank-one selector plus a based endpoint section.

On the relevant rank-two zero-mode character multiplicity space, the retained
Wilson/APS data act as:

```text
lambda I.
```

This scalar mark commutes with every candidate rank-one selector and gives the
same expectation value on every line:

```text
psi(alpha) = (cos(alpha), sin(alpha)).
```

Therefore the retained mark does not derive a unique selected line.

### Bridge for the scalar premise

The premise that every retained Wilson/APS-derived mark acts as `lambda I`
on the rank-two zeta-character multiplicity space `M_zeta` is now derived,
not asserted, by the narrow bridge theorem in
[`docs/KOIDE_RETAINED_WILSON_APS_SCALAR_ACTION_ON_RANK_TWO_MULTIPLICITY_BRIDGE_NARROW_THEOREM_NOTE_2026-05-16.md`](./KOIDE_RETAINED_WILSON_APS_SCALAR_ACTION_ON_RANK_TWO_MULTIPLICITY_BRIDGE_NARROW_THEOREM_NOTE_2026-05-16.md)
and its runner
[`scripts/frontier_koide_retained_wilson_aps_scalar_action_on_rank_two_multiplicity_bridge_narrow.py`](./../scripts/frontier_koide_retained_wilson_aps_scalar_action_on_rank_two_multiplicity_bridge_narrow.py).
The bridge re-uses the Wilson construction from the sibling no-go
`KOIDE_DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_NO_GO_NOTE_2026-04-24`
(which already certifies `dim ker(D) = 4` and the rank-two
zeta-isotypic decomposition of `U` on `ker(D)`) and shows that every
polynomial in the generators `{D, U, U^dag, P_lambda(D)}` restricts to
a scalar `lambda_A I_2` on `M_zeta`. The parent runner additionally
re-verifies a representative subset of those scalar restrictions inside
its own Section B.0a-B.0f so the load-bearing scalar premise is no
longer asserted in the parent runner either.

## Endpoint Section

A marked open endpoint still has:

```text
open_phase = h + s1 - s0.
```

An exact endpoint shift moves the open endpoint while preserving closed APS
data.  The zero endpoint condition:

```text
s1 = s0
```

is a boundary-section theorem, not a consequence of relative cobordism alone.

## Unified Residual

After total anomaly normalization:

```text
delta_open / eta_APS - 1 =
  -spectator_channel + c / eta_APS.
```

Closure requires both:

```text
spectator_channel = 0
c = 0
```

The marked relative route does not derive either from retained data.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_MARK = derived_boundary_mark_is_scalar_on_multiplicity
RESIDUAL_TRIVIALIZATION = marked_endpoint_section_not_based
RESIDUAL_SCALAR = minus_spectator_channel_plus_c_over_eta_APS
```

## Falsifiers

- A retained non-scalar boundary mark on the rank-two zero-mode character
  multiplicity space.
- A retained theorem proving that mark selects the physical rank-one Brannen
  line.
- A retained boundary-section theorem deriving `c = 0`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_marked_relative_cobordism_no_go.py
python3 scripts/frontier_koide_retained_wilson_aps_scalar_action_on_rank_two_multiplicity_bridge_narrow.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_DELTA_MARKED_RELATIVE_COBORDISM_NO_GO=TRUE
DELTA_MARKED_RELATIVE_COBORDISM_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_MARK=derived_boundary_mark_is_scalar_on_multiplicity
RESIDUAL_TRIVIALIZATION=marked_endpoint_section_not_based
RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS
```
