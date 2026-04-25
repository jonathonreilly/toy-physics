# Koide delta post-unit-endpoint reassessment no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_post_unit_endpoint_reassessment_no_go.py`  
**Status:** reassessment/no-go; delta remains open

## Purpose

This note consolidates the post-atlas attacks:

- spectral-flow degree normalization;
- Callan-Harvey degree functor;
- primitive anomaly-channel uniqueness;
- Picard torsor unit/basepoint;
- determinant-line universal endpoint.
- source-response covariance transfer from the strict Q readout.
- primitive degree-one endpoint generator.
- minimal endpoint-action principle.
- selected-line nonzero winding as support for, but not derivation of,
  primitive endpoint degree.
- local `Cl(3)` boundary source grammar for selected/spectator channels and
  endpoint-exact offsets.
- selected-line projector retention as support for, but not derivation of,
  physical boundary source support.

## Unified Residual

With normalized total anomaly cancellation:

```text
selected_channel + spectator_channel = 1.
```

The selected endpoint has:

```text
delta_open = selected_channel eta_APS + c.
```

Therefore:

```text
delta_open / eta_APS - 1 =
  -spectator_channel + c / eta_APS.
```

Closure requires:

```text
spectator_channel = 0
c = 0.
```

## Interpretation

The remaining theorem is no longer vague.  It must prove that:

1. the selected Brannen line is the unique primitive anomaly channel;
2. the selected endpoint torsor has a retained zero/basepoint;
3. the selected determinant-line map is based, orientation-preserving, and
   degree one.

The covariance-transfer audit sharpens this further: Q-style basepoint
preservation can at most remove the offset `c`; it does not fix the endpoint
degree/channel multiplier `mu`.  The remaining positive theorem must derive
`mu=1`.

The primitive-degree audit verifies that a based, orientation-preserving
primitive endpoint map would force `mu=1`, but the retained packet does not
derive primitivity, orientation, or the endpoint basepoint.  Degree two remains
a based orientation-preserving countermap.

The minimal-action audit verifies that minimal positive degree would select
`mu=1`, but unconstrained minimal action selects the based degree-zero map.
Thus minimality cannot replace the missing nonzero primitive selected-channel
theorem.

The selected-line nonzero-degree audit verifies that the retained `CP1`
carrier has nonzero conjugate-pair winding `n_eff=2`, but this support does
not determine the physical endpoint functor.  Degree zero, raw degree two, and
offset counterstates remain until a descent theorem derives endpoint degree
one.

The higher `Cl(3)` boundary source-grammar audit verifies that local retained
boundary words do not force the selected projector or zero endpoint exact
counterterm.  They leave `A_odd=A_even` and `B_odd=-B_even` as physical
endpoint identity laws.

The selected-line projector-retention audit verifies that the retained `CP1`
line gives a canonical rank-one projector `P_chi`, but retained boundary
sources still admit `rho=p P_chi+(1-p)(I-P_chi)` and independent endpoint
offset `c`.  Projector existence is not the same as physical source support
on that projector.

## Next Attack

The highest-priority next route is:

```text
lattice_Wilson_selected_eigenline_theorem
```

Projector retention has now been exhausted.  The next route should test
whether an explicit finite Wilson selected eigenline canonically supplies the
unit anomaly channel and basepoint, rather than merely constructing another
selected line.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_CHANNEL = selected_line_unique_primitive_channel_not_retained
RESIDUAL_TRIVIALIZATION = selected_endpoint_zero_basepoint_not_retained
RESIDUAL_SCALAR = selected_endpoint_degree_mu_minus_one
RESIDUAL_PRIMITIVE = selected_endpoint_based_orientation_preserving_primitive_generator
RESIDUAL_ACTION = nonzero_positive_primitive_endpoint_sector_not_retained
RESIDUAL_DESCENT = selected_line_winding_to_endpoint_degree_one_not_retained
RESIDUAL_PROJECTOR = selected_line_projector_support_law_not_retained
NEXT_ATTACK = lattice_Wilson_selected_eigenline_theorem
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_post_unit_endpoint_reassessment_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_DELTA_POST_UNIT_ENDPOINT_REASSESSMENT_NO_GO=TRUE
DELTA_POST_UNIT_ENDPOINT_REASSESSMENT_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_CHANNEL=selected_line_unique_primitive_channel_not_retained
RESIDUAL_TRIVIALIZATION=selected_endpoint_zero_basepoint_not_retained
NEXT_ATTACK=lattice_Wilson_selected_eigenline_theorem
```
