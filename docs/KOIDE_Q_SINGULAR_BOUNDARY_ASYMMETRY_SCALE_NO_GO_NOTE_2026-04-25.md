# Koide Q Singular-Boundary Asymmetry/Scale No-Go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_singular_boundary_asymmetry_scale_no_go.py`  
**Status:** executable no-go; not Q closure

## Theorem Attempt

Endpoint exchange failed because the exchange center was free.  This route
tries the asymmetric alternative: retain the fact that `rho=-1` is a finite
singular source boundary and `rho=+infinity` is a different endpoint.  Perhaps
that asymmetry fixes the source unit section `rho=0`.

## Result

The route fails.  Distinguishing the finite singular boundary forbids the
endpoint-exchange reflections, but it leaves the full boundary-preserving
positive scaling group:

```text
T_alpha(rho) = alpha*(rho+1)-1, alpha>0.
```

These maps preserve:

- the singular boundary `rho=-1`;
- the infinity endpoint;
- the source cone `rho>-1`;
- orientation;
- the Hessian metric.

They act transitively on the interior.  In particular:

```text
T_2(0)=1.
```

So the nonclosing full-determinant section `rho=1` has the same
boundary-asymmetric status as the conditional closing section `rho=0`.

## Boundary Distance

In the Hessian geodesic coordinate

```text
x = log(1+rho),
```

the finite singular boundary is at `x=-infinity`.  The cutoff distance from
`eps` to `rho` is:

```text
d_eps(rho) = log(1+rho) - log(eps).
```

As `eps -> 0+`, this diverges for every interior `rho`.  A finite
distance-from-boundary rule gives:

```text
rho = eps exp(ell) - 1.
```

Selecting `rho=0` requires `ell=-log(eps)`, which is a supplied cutoff/scale
choice.  Changing the cutoff is exactly the positive scaling freedom.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_singular_boundary_scale_section_e_equals_zero
RESIDUAL_SOURCE = singular_boundary_preserving_scalings_leave_unit_section_free
COUNTERSECTION = e_1_full_determinant_Q_1_K_TL_3_over_8
```

The missing law is still the retained unit section, now sharpened as a
boundary-scale normalization law.

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
KOIDE_Q_SINGULAR_BOUNDARY_ASYMMETRY_SCALE_NO_GO=TRUE
Q_SINGULAR_BOUNDARY_ASYMMETRY_SCALE_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_BOUNDARY_SCALE_SECTION_RHO_EQUALS_ZERO=TRUE
```

Singular-boundary asymmetry removes endpoint exchange but does not select the
source unit.  It leaves the positive scaling torsor untouched.
