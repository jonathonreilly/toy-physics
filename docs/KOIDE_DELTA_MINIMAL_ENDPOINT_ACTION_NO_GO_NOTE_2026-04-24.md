# Koide Delta Minimal Endpoint-Action No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_minimal_endpoint_action_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to derive the selected endpoint degree from an action principle.  For a
based circle endpoint map of degree `n`, the simplest Dirichlet action is

```text
S(n,c) = n^2 + c^2.
```

If the physical selected endpoint is the minimal positive orientation-preserving
map, this gives `n=1`, `c=0`, and hence

```text
delta_open = eta_APS = 2/9.
```

## Brainstormed Variants

1. Unconstrained endpoint-action minimization.
2. Minimal based map with fixed degree.
3. Minimal nonzero orientation-preserving map.
4. What if the selected endpoint sector can be zero?  Then the constant map
   wins and delta is not closed.
5. What if nonzero primitive degree is retained?  Then the action principle
   supports `n=1`.

## Exact Audit

The runner writes

```text
delta_open = n eta_APS + c.
```

Closure requires

```text
n = 1
c = 0.
```

But unconstrained based action gives:

```text
min_n n^2 = 0 at n=0.
```

So minimality alone yields:

```text
delta_open = 0.
```

Only after imposing the nonzero positive sector does minimal action give:

```text
min_{n>0} n^2 = 1 at n=1.
```

That conditionally closes delta.

## Hostile Review

This route does not close delta from retained data.  It exposes the missing
primitive:

```text
derive_nonzero_positive_primitive_selected_endpoint_degree.
```

Without that theorem, the based degree-zero endpoint is an exact lower-action
counterstate.

## Verdict

```text
KOIDE_DELTA_MINIMAL_ENDPOINT_ACTION_NO_GO=TRUE
DELTA_MINIMAL_ENDPOINT_ACTION_CLOSES_DELTA_RETAINED_ONLY=FALSE
CONDITIONAL_DELTA_CLOSES_IF_NONZERO_POSITIVE_PRIMITIVE_SECTOR_IS_RETAINED=TRUE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_SCALAR=derive_nonzero_positive_primitive_selected_endpoint_degree
RESIDUAL_FUNCTOR=unconstrained_minimal_action_selects_degree_zero
COUNTERSTATE=based_minimal_degree_zero_delta_0
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_minimal_endpoint_action_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_minimal_endpoint_action_no_go.py
```
