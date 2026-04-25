# Koide Q locality/gluing UV-IR pairing no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_locality_gluing_uv_ir_pairing_no_go.py`  
**Status:** no-go; Q not closed

## Theorem attempt

Try to strengthen the UV/IR endpoint audit with retained locality and gluing.
The live log-source coordinate is

```text
x = log(1 + rho).
```

The endpoint audit left a finite UV/IR pairing

```text
A = exp(2m),
```

where `m` is the midpoint of the paired regulators.  If locality or gluing
forced `m = 0`, then `A = 1`, `rho = 0`, `K_TL = 0`, and the conditional Q
support chain would give `Q = 2/3`.

## Brainstormed routes

The runner tests:

1. local interval additivity might force the finite midpoint `m = 0`;
2. gluing cancellation of internal boundary terms might remove finite parts;
3. orientation reversal exchanging UV and IR regulators might center at zero;
4. multiplicative UV/IR pairing might select the identity `A = 1`;
5. local anomaly inflow might forbid nonzero boundary finite constants;
6. wrong-assumption inversion: `m = log(2)`, `A = 4` satisfies the same gluing laws.

## Result

The local segment action

```text
S(x0,x1) = a (x1 - x0)
```

glues exactly:

```text
S(x0,x1) + S(x1,x2) = S(x0,x2).
```

It is invariant under absolute translations `x -> x + c`, so it sees
differences but not the absolute midpoint.  On paired endpoint regulators

```text
x_UV = m - L,
x_IR = m + L,
```

the action is

```text
S = 2aL,
```

independent of `m`.

Orientation reversal also fails to fix the midpoint.  The map

```text
R_m(x) = 2m - x
```

is an involution and exchanges `m-L` with `m+L` for every `m`.

Boundary terms have the same obstruction.  For

```text
B(x) = a*x + b,
```

the glued internal boundary cancels for every finite `b`.  Normalizing
`B(m)=0` gives

```text
b = -a*m,
```

not `m = 0`.

Finally, the pairing parameter

```text
A(m) = exp(2m)
```

is multiplicative:

```text
A(m1 + m2) = A(m1) A(m2).
```

The identity `A=1` is equivalent to `m=0`, but multiplicativity by itself
does not select the identity object.

## Countersection

The conditional closing midpoint remains:

```text
m = 0 -> rho = 0 -> K_TL = 0 -> Q = 2/3.
```

But the same exact locality/gluing laws also admit

```text
m = log(2) -> A = 4 -> rho = 1 -> K_TL = 3/8 -> Q = 1.
```

Therefore locality/gluing is not a retained Q closure theorem.

## Hostile review

- No Koide target is assumed.  The closing and counterclosing midpoints are
  audited under the same equations.
- No PDG masses, observational `H_*` pin, `delta=2/9`, or Brannen-phase input
  appears.
- No new selector primitive is renamed as a theorem.  The missing theorem is
  named directly.
- Locality sees differences and boundary cancellation; it does not choose an
  absolute midpoint in the source torsor.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_locality_gluing_uv_ir_midpoint_m_equals_zero
RESIDUAL_SOURCE = locality_gluing_leaves_uv_ir_midpoint_m_free
COUNTERSECTION = m_log2_A_4_rho_1_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 -m py_compile scripts/frontier_koide_q_locality_gluing_uv_ir_pairing_no_go.py
python3 scripts/frontier_koide_q_locality_gluing_uv_ir_pairing_no_go.py
```

Expected result:

```text
KOIDE_Q_LOCALITY_GLUING_UV_IR_PAIRING_NO_GO=TRUE
Q_LOCALITY_GLUING_UV_IR_PAIRING_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_LOCALITY_GLUING_MIDPOINT_M_EQUALS_ZERO=TRUE
RESIDUAL_SCALAR=derive_retained_locality_gluing_uv_ir_midpoint_m_equals_zero
```
