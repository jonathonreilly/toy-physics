# Koide Q monoidal-unit source-basepoint no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_monoidal_unit_source_basepoint_no_go.py`  
**Status:** no-go; Q not closed

## Theorem attempt

Try to turn the source-fibre unit into the missing physical law.  The live
log-source coordinate is

```text
x = log(1 + rho).
```

If retained source composition, empty-boundary gluing, or unit-preserving
readout forced the physical charged-lepton source to be the absolute unit

```text
x = 0,
```

then `rho=0`, `K_TL=0`, and the conditional Q support chain would give
`Q=2/3`.

## Brainstormed routes

The runner tests:

1. monoidal source composition might make the physical source the unit;
2. empty-boundary state might force the absolute source coordinate `x=0`;
3. unit-preserving readout might make zero coordinate canonical;
4. torsor naturality might select one basepoint over its translates;
5. idempotent/unit uniqueness might force the unit to be retained at `e=0`;
6. wrong-assumption inversion: `e=log(2)` is also a valid unit after retorsoring.

## Result

The retained source-fibre algebra has the structure of a torsor.  For every
basepoint `e`, it admits the translated product

```text
x *_e y = x + y - e,
```

with identity `e` and exact associativity:

```text
e *_e x = x,
x *_e e = x,
(x *_e y) *_e z = x *_e (y *_e z).
```

These identities hold symbolically for arbitrary `e`.  Translating the source
coordinate by `c` transports the unit law:

```text
tau_c(x *_e y) = tau_c(x) *_(e+c) tau_c(y).
```

So the unit law defines a family of equivalent monoidal descriptions, not a
retained equation `e=0`.

The empty-boundary readout has the same obstruction.  Its neutral source is the
relative coordinate

```text
x - e = 0,
```

which gives

```text
x = e,
```

not `e=0`.  Simultaneous shifts preserve that readout:

```text
(x+c) - (e+c) = x - e.
```

Unit-preserving trivializations also do not close Q.  For every supplied
basepoint,

```text
F_e(x) = x - e
```

sends the unit to coordinate zero.  Requiring `F_e(0)=0` would force `e=0`,
but that requirement is exactly the missing absolute-origin law.

## Countersection

The conditional closing unit remains:

```text
e = 0 -> rho = 0 -> K_TL = 0 -> Q = 2/3.
```

But the same exact unit, empty-boundary, and unit-preserving-trivialization laws
also admit

```text
e = log(2) -> rho = 1 -> K_TL = 3/8 -> Q = 1.
```

Therefore the monoidal-unit / empty-boundary route is not a retained Q closure
theorem.

## Hostile review

- No Koide target is assumed.  The closing and counterclosing basepoints are
  audited under the same equations.
- No PDG masses, observational `H_*` pin, `delta=2/9`, or Brannen-phase input
  appears.
- No new selector primitive is renamed as a theorem.  The missing theorem is
  named directly.
- "The physical source is the unit" closes only after the unit's absolute
  coordinate is already retained as `e=0`.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_monoidal_unit_source_basepoint_equals_zero
RESIDUAL_SOURCE = monoidal_unit_empty_boundary_leaves_basepoint_e_free
COUNTERSECTION = unit_basepoint_e_log2_rho_1_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 -m py_compile scripts/frontier_koide_q_monoidal_unit_source_basepoint_no_go.py
python3 scripts/frontier_koide_q_monoidal_unit_source_basepoint_no_go.py
```

Expected result:

```text
KOIDE_Q_MONOIDAL_UNIT_SOURCE_BASEPOINT_NO_GO=TRUE
Q_MONOIDAL_UNIT_SOURCE_BASEPOINT_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_MONOIDAL_UNIT_BASEPOINT_E_EQUALS_ZERO=TRUE
RESIDUAL_SCALAR=derive_retained_monoidal_unit_source_basepoint_equals_zero
```
