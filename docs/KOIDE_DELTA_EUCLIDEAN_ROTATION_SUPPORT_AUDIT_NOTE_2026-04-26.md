# Koide `delta` Euclidean-Rotation Support Audit

**Date:** 2026-04-26
**Status:** exact support audit on the charged-lepton Brannen `delta` lane.
This note does **not** promote retained closure of `delta = 2/9 rad`.
**Runner:** `scripts/frontier_koide_delta_euclidean_rotation_support_audit.py`

## Decision

The reviewed `claude/koide-delta-euclidean-rotation-2026-04-25` branch
contains one useful theorem and one overpromotion.

What lands is narrower:

```text
on the retained selected-line Fourier carrier,
  p_1 + i p_2 = 2^(-1/2) exp(i(pi/6 - theta)),
therefore
  alpha(theta) = pi/6 - theta,
  alpha(theta_*) - alpha(theta_0) = -delta_*.
```

At a point with Brannen offset `delta_* = 2/9`, the Euclidean angle difference
is exactly `-2/9`. This is a real support strengthening because it upgrades
the previous selected-line rotation-angle check from numerical compatibility
to a closed-form carrier identity.

What does **not** land is the branch's stronger claim that this identity alone
closes the physical Brannen readout law. Current `main` still does not derive
why the physical charged-lepton selected-line observable must read the
Type-B rational `2/9` as this Euclidean radian angle.

## Exact selected-line identity

Use the retained selected-line form

```text
s(theta) = 2^(-1/2) v_1
         + (1/2) exp(i theta) v_omega
         + (1/2) exp(-i theta) v_omega_bar,
```

with

```text
v_1 = (1,1,1)/sqrt(3),
v_omega = (1, omega, omega^2)/sqrt(3),
omega = exp(2 pi i / 3).
```

On the real doublet plane `W = <(1,1,1)>^perp`, take the canonical frame

```text
e_1 = (1,-1,0)/sqrt(2),
e_2 = (1,1,-2)/sqrt(6).
```

Direct projection gives

```text
p_1(theta) = s(theta) dot e_1 = 2^(-1/2) sin(theta + pi/3),
p_2(theta) = s(theta) dot e_2 = 2^(-1/2) cos(theta + pi/3).
```

Equivalently,

```text
p_1(theta) + i p_2(theta) = 2^(-1/2) exp(i(pi/6 - theta)).
```

Thus the lifted Euclidean angle on the first branch is

```text
alpha(theta) = atan2(p_2, p_1) = pi/6 - theta.
```

If `delta = theta - 2pi/3`, and the unphased reference has
`theta_0 = 2pi/3`, then

```text
alpha(theta_0) = -pi/2,
alpha(theta) - alpha(theta_0) = -delta.
```

This proves that Brannen offset differences are exactly Euclidean rotation
angle differences on this selected-line carrier, up to the orientation sign
fixed by the chosen `C_3` frame.

## What this supports

This identity is worth retaining as support science because it shows:

1. the Brannen selected-line offset is not merely numerically compatible with
   an ambient rotation angle;
2. the first-branch coordinate is an ordinary contractible Euclidean angle
   lift, not a closed `R/Z` holonomy;
3. the `cos(delta + 2pi k/3)` Brannen parameterization is exactly the
   real-coordinate readout of the selected-line Fourier carrier;
4. the `Q` lane and the `delta` lane remain separated: the already retained
   SO(2) phase-erasure support theorem shows `Q=(c^2+2)/6`, independent of
   `delta`.

## What remains open

The exact identity above is not the missing physical theorem. It starts with a
selected-line Brannen parameter `delta` and identifies its Euclidean-coordinate
meaning on the carrier. It does not derive that the physical charged-lepton
observable must pick the point with `delta = 2/9`, nor does it derive the
Type-B rational-to-radian observable law.

The remaining `delta` primitive is still:

```text
derive the selected-line local boundary-source law,
derive the based endpoint section,
derive why the Type-B rational 2/9 is read as the Euclidean radian
  Brannen offset rather than through the canonical period-2pi phase map.
```

The branch's anti-check inventory is therefore useful only as route hygiene:
it does not prove uniqueness of the physical readout category on current
`main`.

## Relationship to the A1/radian audit

The April 24 A1/radian audit showed that retained periodic phase sources land
in `q*pi`, while the Brannen target is a pure rational `2/9` used as a radian.
This note does not contradict that result. It clarifies what would happen
**after** the physical selected-line readout has been fixed to the Euclidean
angle coordinate:

```text
if delta = 2/9 on the Brannen selected-line carrier,
then the Euclidean rotation angle difference is -2/9 rad.
```

It does not derive the antecedent.

## Closeout flags

```text
KOIDE_DELTA_EUCLIDEAN_ROTATION_SUPPORT=TRUE
SELECTED_LINE_EUCLIDEAN_ANGLE_IDENTITY=TRUE
SELECTED_LINE_FIRST_BRANCH_LIFT_CONTRACTIBLE=TRUE
EUCLIDEAN_ROTATION_TO_PHYSICAL_BRANNEN_READOUT_PROVED=FALSE
KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE
KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE
TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE
RESIDUAL_DELTA=selected_line_boundary_source_plus_based_endpoint_plus_Type_B_radian_readout
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_euclidean_rotation_support_audit.py
```

Expected final flags:

```text
EUCLIDEAN_ROTATION_TO_PHYSICAL_BRANNEN_READOUT_PROVED=FALSE
KOIDE_DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE
TYPE_B_TO_RADIAN_IDENTIFICATION_REMAINS_PRIMITIVE=TRUE
```
