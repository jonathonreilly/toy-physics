# Koide Delta Selected-Line Berry Endpoint No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_selected_line_berry_endpoint_no_go.py`  
**Status:** executable no-go for deriving the physical Brannen phase endpoint
from selected-line Berry geometry plus ambient APS alone

## Theorem Attempt

After several strong `Q` routes reduced again to a missing scalar law, this
cycle pivots to the permitted delta bridge.  The attempted theorem is:

> the retained selected-line `CP^1` Berry carrier, together with the ambient
> `Z_3` APS value `eta_APS = 2/9`, forces the physical Brannen phase endpoint
> `delta_physical = eta_APS`.

The audit rejects that theorem.  The selected-line carrier gives the exact
local Berry connection and identifies the Brannen offset with an endpoint
difference, but it does not select the endpoint.

## Route Ranking

1. **Selected-line Berry endpoint law:** test whether the actual selected-line
   carrier itself makes `delta = eta_APS` unavoidable.  This is the strongest
   delta route not identical to the Callan-Harvey normalization no-go.
2. **Callan-Harvey descent normalization:** already audited separately; leaves
   `N_desc - 1`.
3. **Fractional-period / projective-loop law:** ask whether `eta=2/9` is a
   forced fraction of the selected-line projective period.
4. **What if the ambient APS value is only support?** invert the premise and
   test whether selected-line geometry can select a physical endpoint without
   APS.
5. **Return to Q:** if every delta bridge remains endpoint-free, resume the
   traceless-source problem and test any genuinely new retained source grammar.

## Exact Selected-Line Geometry

On the actual selected-line doublet ray, use

```text
chi(theta) = (1, exp(-2 i theta)) / sqrt(2).
```

The runner verifies exactly:

```text
<chi|chi> = 1,
i <chi | partial_theta chi> = 1.
```

So the Berry connection is

```text
A = d theta.
```

With the retained unphased base point

```text
theta0 = 2 pi / 3,
```

the selected-line Brannen offset is

```text
delta = theta_end - theta0.
```

This is exact support for the selected-line Berry route.

## Obstruction

The ambient ABSS/APS calculation gives

```text
eta_APS(Z_3; weights 1,2) = 2/9.
```

But the selected-line Berry geometry supplies no equation

```text
theta_end - theta0 = eta_APS.
```

It supplies only the identity

```text
Hol(theta0 -> theta_end) = theta_end - theta0.
```

Therefore the exact residual scalar is

```text
theta_end - theta0 - eta_APS.
```

The counterfamily

```text
delta in {0, 2/9, 1/3}
```

preserves the same normalized selected-line ray and the same `A=dtheta`
connection.  Only one member has `delta=eta_APS`, and it has that value because
the endpoint was chosen.

## Period Audit

The selected-line coordinate has projective period

```text
chi(theta + pi) = chi(theta).
```

The associated period holonomy is `pi`, not `2/9`.  The native `Z_3` angular
increment is `2 pi / 3`, also not `2/9`.  Forcing `eta_APS` as a fraction of
the projective period would require the non-retained fraction

```text
2 / (9 pi).
```

So topology fixes the period structure, not the physical endpoint.

## Hostile Review

This no-go does **not** use:

- `Q = 2/3`;
- PDG masses;
- the observational `H_*` pin;
- `delta = 2/9` as a closure input;
- an assumed equality between selected-line Brannen phase and ambient APS.

The equality `delta = eta_APS` is used only as the proposed endpoint equation
whose missing status is being audited.

## Executable Result

```text
PASSED: 15/15

KOIDE_DELTA_SELECTED_LINE_BERRY_ENDPOINT_NO_GO=TRUE
DELTA_SELECTED_LINE_BERRY_ENDPOINT_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=theta_end-theta0-eta_APS
```

## Consequence

The selected-line Berry route remains strong support: it correctly identifies
the physical Brannen phase as a Berry endpoint offset on the actual selected
line.  It does not by itself derive why that endpoint offset equals the ambient
APS invariant.

The remaining delta bridge is now sharpened to:

```text
derive theta_end - theta0 = eta_APS
```

without assuming the equality or adding an unexplained selected-endpoint
primitive.
