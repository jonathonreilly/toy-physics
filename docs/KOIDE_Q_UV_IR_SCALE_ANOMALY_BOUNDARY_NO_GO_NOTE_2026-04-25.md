# Koide Q UV/IR endpoint and scale-anomaly boundary no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_uv_ir_scale_anomaly_boundary_no_go.py`  
**Status:** no-go; Q not closed

## Theorem attempt

Try to derive the charged-lepton Q source law from UV/IR endpoint regularity
or scale-anomaly boundary conditions on the live normalized source fibre:

```text
x = log(1 + rho).
```

If those retained boundary data fixed the absolute origin `x = 0`, then
`rho = 0`, `K_TL = 0`, and the conditional support chain would give `Q = 2/3`.

## Brainstormed routes

The runner tests:

1. UV endpoint regularity might anchor finite source origin `x = 0`;
2. IR endpoint regularity might anchor finite source origin `x = 0`;
3. UV/IR paired cutoffs might define a canonical midpoint;
4. scale anomaly might fix the finite intercept of `W = a*x + b`;
5. boundary counterterm cancellation might select a unique finite part;
6. wrong-assumption inversion: UV/IR pairing `A = 4` selects `x = log(2)`.

The decisive tests are the cutoff midpoint and anomaly finite-intercept
calculations.

## Result

Endpoint regularity preserves the two ends

```text
x = -infinity,
x = +infinity,
```

but translations `x -> x + c` preserve both endpoints and the endpoint slope.
Therefore endpoint data alone do not choose a finite interior point.

For paired cutoffs

```text
x_UV = log(eps),
x_IR = log(A/eps),
```

the finite midpoint is

```text
(x_UV + x_IR)/2 = (1/2) log(A).
```

The conditional closing choice is

```text
A = 1 -> x = 0 -> rho = 0 -> Q = 2/3.
```

But the same endpoint structure admits

```text
A = 4 -> x = log(2) -> rho = 1 -> Q = 1.
```

The scale-anomaly audit is the same obstruction in Ward form.  A local anomaly
equation

```text
dW/dx = a
```

fixes the slope of

```text
W = a*x + b,
```

but not the finite constant `b`.  The zero of `W` is

```text
x = -b/a.
```

Thus `b = 0` closes only conditionally, while `b = -a log(2)` gives the exact
nonclosing countersection.

## Hostile review

- No Koide target is assumed.  Closing and counterclosing finite parts are
  audited symmetrically.
- No PDG masses, observational `H_*` pin, `delta=2/9`, or Brannen-phase input
  appears.
- No new selector primitive is renamed as a theorem.  The missing theorem is
  named directly.
- The anomaly fixes a slope; the finite intercept/cutoff pairing remains
  underived.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_uv_ir_scale_anomaly_absolute_origin_A_equals_one
RESIDUAL_SOURCE = endpoint_anomaly_data_leave_cutoff_pairing_and_finite_intercept_free
COUNTERSECTION = uv_ir_pairing_A_4_or_b_minus_a_log2_selects_x_log2_rho_1_Q_1
```

## Verification

Run:

```bash
python3 -m py_compile scripts/frontier_koide_q_uv_ir_scale_anomaly_boundary_no_go.py
python3 scripts/frontier_koide_q_uv_ir_scale_anomaly_boundary_no_go.py
```

Expected result:

```text
KOIDE_Q_UV_IR_SCALE_ANOMALY_BOUNDARY_NO_GO=TRUE
Q_UV_IR_SCALE_ANOMALY_BOUNDARY_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_UV_IR_PAIRING_A_EQUALS_ONE_OR_B_EQUALS_ZERO=TRUE
RESIDUAL_SCALAR=derive_retained_uv_ir_scale_anomaly_absolute_origin_A_equals_one
```
