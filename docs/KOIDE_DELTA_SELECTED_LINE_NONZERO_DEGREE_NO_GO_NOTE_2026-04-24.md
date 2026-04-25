# Koide Delta Selected-Line Nonzero-Degree No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_selected_line_nonzero_degree_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to use the retained selected-line `CP1` doublet

```text
chi(theta) = (1, exp(-2i theta)) / sqrt(2)
```

to prove that the physical delta endpoint lies in the nonzero positive
primitive degree sector.  The projective coordinate has nonzero conjugate-pair
winding:

```text
d arg(exp(-2i theta))/dtheta = -2
n_eff = 2.
```

If that retained winding support descended to the endpoint functor as the
primitive positive based degree, the minimal endpoint-action route would close
delta.

## Brainstormed Variants

1. Nonzero selected-line winding excludes the trivial endpoint.
2. Raw winding descent gives endpoint degree two.
3. Minimal positive primitive endpoint degree gives degree one.
4. What if carrier winding and endpoint functor degree are independent?  Then
   degree zero remains.
5. What if endpoint basepoint is not retained?  Then offsets remain even at
   degree one.

## Exact Audit

The runner verifies the retained selected-line support:

```text
<chi|chi> = 1
i<chi|partial_theta chi> = 1
n_eff = 2.
```

The endpoint model is:

```text
delta_open = n eta_APS + c,   eta_APS = 2/9.
```

Closure requires:

```text
n = 1
c = 0.
```

But retained support still admits:

```text
n=0,c=0 -> delta_open=0
n=2,c=0 -> delta_open=4/9
n=1,c=1/9 -> delta_open=1/3.
```

## Hostile Review

The selected-line carrier is nontrivial, but that is not yet the endpoint
degree theorem.  The exact residual is:

```text
derive_selected_line_winding_descends_to_endpoint_degree_one.
```

This is stronger than merely proving a nonzero carrier.  It must identify the
physical open endpoint functor and its based primitive degree without importing
`delta=2/9`.

## Verdict

```text
KOIDE_DELTA_SELECTED_LINE_NONZERO_DEGREE_NO_GO=TRUE
DELTA_SELECTED_LINE_NONZERO_DEGREE_CLOSES_DELTA_RETAINED_ONLY=FALSE
CONDITIONAL_DELTA_CLOSES_IF_SELECTED_LINE_WINDING_DESCENDS_TO_PRIMITIVE_ENDPOINT_DEGREE=TRUE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_SCALAR=derive_selected_line_winding_descends_to_endpoint_degree_one
RESIDUAL_FUNCTOR=endpoint_degree_not_fixed_by_CP1_winding_support
COUNTERSTATE=based_endpoint_degree_zero_with_nonzero_selected_line_winding
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_selected_line_nonzero_degree_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_selected_line_nonzero_degree_no_go.py
```
