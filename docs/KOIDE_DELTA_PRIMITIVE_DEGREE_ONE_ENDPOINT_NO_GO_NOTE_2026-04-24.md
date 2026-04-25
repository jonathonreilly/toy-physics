# Koide Delta Primitive Degree-One Endpoint No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_primitive_degree_one_endpoint_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to derive the selected endpoint degree `mu=1` from primitive circle-degree
and endpoint orientation.  A based, orientation-preserving primitive endpoint
map is the identity generator, so it would give

```text
delta_open = eta_APS = 2/9.
```

## Brainstormed Variants

1. Based endpoint map: kills the additive offset `c`.
2. Primitive circle degree: restricts degree to `+/-1`.
3. Orientation preservation: selects `+1` from `+/-1`.
4. What if the map is based and orientation-preserving but nonprimitive?
   Degree two remains a countermap.
5. What if the map is primitive and based but orientation-reversing?  Degree
   minus one remains a countermap.

## Exact Audit

Write:

```text
delta_open = n eta_APS + c.
```

Then:

```text
delta_open / eta_APS - 1 = n - 1 + c/eta_APS.
```

Closure requires:

```text
n = 1
c = 0.
```

The runner verifies:

```text
primitive circle degree => n in {-1,+1}
orientation preserving primitive degree => n = +1
based + orientation-preserving primitive endpoint => delta_open=2/9.
```

## Countermaps

The retained endpoint-degree family still admits exact nonclosing maps unless
primitive, orientation, and basepoint are derived:

```text
n=0, c=0   -> delta_open=0
n=2, c=0   -> delta_open=4/9
n=-1, c=0  -> delta_open=-2/9
n=1, c=1/9 -> delta_open=1/3.
```

## Musk Simplification Pass

1. Make requirements less wrong: delta closure is not another APS value; it is
   the endpoint map degree and basepoint.
2. Delete: reduce all endpoint functor structure to `(n,c)`.
3. Simplify: the proof obligation is `n=1` and `c=0`.
4. Accelerate: test primitive/orientation/basepoint as exact integer
   conditions.
5. Automate: add `derive_selected_endpoint_degree_mu_equals_one` to the delta
   exhaustion packet.

## Hostile Review

This route is not retained closure.  It proves that a based,
orientation-preserving primitive endpoint theorem would close delta, but that
theorem is not derived by the current retained APS/Brannen support.

Residual:

```text
derive_selected_endpoint_degree_mu_equals_one.
```

## Verdict

```text
KOIDE_DELTA_PRIMITIVE_DEGREE_ONE_ENDPOINT_NO_GO=TRUE
DELTA_PRIMITIVE_DEGREE_ONE_ENDPOINT_CLOSES_DELTA_RETAINED_ONLY=FALSE
CONDITIONAL_DELTA_CLOSES_IF_BASED_ORIENTATION_PRESERVING_PRIMITIVE_ENDPOINT=TRUE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_SCALAR=derive_selected_endpoint_degree_mu_equals_one
RESIDUAL_FUNCTOR=selected_endpoint_based_orientation_preserving_primitive_generator_not_derived
COUNTERSTATE=based_covariant_orientation_preserving_degree_two_delta_4_over_9
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_primitive_degree_one_endpoint_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_primitive_degree_one_endpoint_no_go.py
```
