# Koide Q Hessian-Metric Unit-Section No-Go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_hessian_metric_unit_section_no_go.py`  
**Status:** executable no-go; not Q closure

## Theorem Attempt

The retained logdet source-response Hessian might add enough geometry to pick
the missing source-fibre unit section.  The proposed closure was that the
Hessian metric, Legendre covector, or Hessian geodesic distance canonically
selects `rho=0`, hence `K_TL=0`.

## Result

The route fails.  On the source cone `rho>-1`, the retained potential

```text
phi(rho) = -log(1+rho)
```

has Hessian metric

```text
g(rho) = d^2 phi = (1+rho)^-2.
```

This metric is exactly invariant under the same boundary-fixing positive
scalings exposed by the previous no-go:

```text
T_alpha(rho) = alpha*(rho+1)-1.
```

The pullback satisfies:

```text
T_alpha^* g = g.
```

Thus the Hessian geometry preserves the whole family of source-cone scalings;
it does not distinguish `rho=0`.

## Exact Obstruction

In geodesic coordinate

```text
x = log(1+rho),
```

the metric is just:

```text
g = dx^2.
```

The scaling action becomes:

```text
x -> x + log(alpha).
```

So the Hessian metric is a flat torsor.  It measures distances after a
basepoint is supplied, but it has no retained origin.

Normal coordinates based at `e` are:

```text
s_e(rho) = log((1+rho)/(1+e)).
```

The least-distance condition gives `rho=e` for every chosen basepoint.  Hence:

```text
e=0 -> Q=2/3, K_TL=0
e=1 -> Q=1,   K_TL=3/8
```

Both are exact sections of the same Hessian geometry.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_hessian_metric_unit_section_e_equals_zero
RESIDUAL_SOURCE = hessian_metric_flat_log_torsor_has_no_canonical_origin
COUNTERSECTION = e_1_full_determinant_Q_1_K_TL_3_over_8
```

The missing law is not a metric formula.  It is the retained physical choice of
the metric origin or unit section.

## Hostile Review

This no-go does **not** use:

- PDG masses;
- the observational `H_*` pin;
- assumed `K_TL=0`;
- assumed `Q=2/3`;
- assumed `delta=2/9`;
- a hidden selector primitive.

It uses `rho=0` only as the conditional closing section and tests it against
the exact `rho=1` countersection.

## Verdict

```text
KOIDE_Q_HESSIAN_METRIC_UNIT_SECTION_NO_GO=TRUE
Q_HESSIAN_METRIC_UNIT_SECTION_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_HESSIAN_BASEPOINT_E_EQUALS_ZERO=TRUE
```

The Hessian/Legendre structure sharpens the obstruction: Q closure needs a
retained physical origin in the flat log source torsor.
