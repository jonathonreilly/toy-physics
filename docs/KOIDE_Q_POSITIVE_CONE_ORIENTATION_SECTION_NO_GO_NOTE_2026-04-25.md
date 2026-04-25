# Koide Q Positive-Cone Orientation/Section No-Go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_positive_cone_orientation_section_no_go.py`  
**Status:** executable no-go; not Q closure

## Theorem Attempt

After basepoint-independence erased the absolute source coordinate, try a
stronger retained structure: the physical source cone has admissible interior
`rho > -1`, singular boundary `rho=-1`, an orientation, and positive scale
covariance.  The proposed closure was that this cone geometry might pick the
zero source section `rho=0`, hence `K_TL=0`.

## Result

The route fails.  The boundary-fixing positive affine maps

```text
T_alpha(rho) = alpha*(rho + 1) - 1, alpha > 0
```

preserve:

- the boundary `rho=-1`;
- the interior cone `rho>-1`;
- orientation;
- the positive scale ray `1+rho`;
- the log-cone translation structure.

They also act transitively on the interior.  In particular:

```text
T_2(0) = 1.
```

Thus the closing section `rho=0` and the full-determinant countersection
`rho=1` are related by retained positive-cone covariance.

## Exact Checks

The runner verifies:

```text
1 + T_alpha(rho) = alpha*(1+rho)
T_alpha(T_beta(rho)) = T_(alpha beta)(rho)
T_alpha(e) - e = (alpha - 1)*(e + 1)
```

The only universal fixed point is the boundary `e=-1`, which is singular for
the normalized carrier.  No interior point is canonically fixed by the cone.

In log coordinates,

```text
x = log(1+rho)
```

the action is translation by `log(alpha)`.  The closing section has `x=0`,
while `rho=1` has `x=log(2)`.  Translation by `log(2)` is allowed, so the log
coordinate does not retain a distinguished origin.

## Q Consequences

The two audited sections give:

```text
rho=0 -> Q=2/3, K_TL=0
rho=1 -> Q=1,   K_TL=3/8
```

The nonclosing `rho=1` section remains positive and is obtained from `rho=0`
by a retained cone scaling.  Therefore positivity, orientation, and boundary
data do not reject it.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_positive_cone_unit_section_e_equals_zero
RESIDUAL_SOURCE = positive_cone_scalings_leave_unit_distance_from_boundary_free
COUNTERSECTION = e_1_full_determinant_Q_1_K_TL_3_over_8
```

The missing law is now even sharper: derive the physical unit section, or
derive why the positive source cone is based at exactly one unit above its
singular boundary.  Without that, `rho=0` is a normalization choice.

## Hostile Review

This no-go does **not** use:

- PDG masses;
- the observational `H_*` pin;
- assumed `K_TL=0`;
- assumed `Q=2/3`;
- assumed `delta=2/9`;
- a hidden selector primitive.

It uses `rho=0` only as the conditional closing section and tests it against
the exact nonclosing `rho=1` countersection.

## Verdict

```text
KOIDE_Q_POSITIVE_CONE_ORIENTATION_SECTION_NO_GO=TRUE
Q_POSITIVE_CONE_ORIENTATION_SECTION_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_UNIT_SECTION_RHO_EQUALS_ZERO=TRUE
```

Positive-cone geometry names the boundary and ray structure, but it does not
derive the unit/basepoint section required for Q closure.
