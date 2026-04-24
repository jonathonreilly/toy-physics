# Koide native Brannen real-primitive closure theorem

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_native_brannen_real_primitive_closure_theorem.py`  
**Status:** positive native closure theorem for the dimensionless Koide lane

## Theorem

The retained Brannen endpoint is the real nontrivial `Z3` primitive:

```text
V_perp = L_omega (+) L_omegabar
```

not a freely selected rank-one line inside it.

Reason:

```text
L_omegabar = conj(L_omega)
```

and the charged-lepton Brannen state is real/CPT closed only as the conjugate
pair:

```text
[e^{i theta} : e^{-i theta}].
```

A single complex character line is not closed under conjugation.  A single real
line inside the real doublet is not `Z3` equivariant.  Therefore the minimal
nontrivial real/CPT/`Z3`-closed endpoint object is the whole real primitive.

## Spectator Channel

On the real nontrivial `Z3` primitive, the generator is a rotation by `2pi/3`.
Its real equivariant endomorphisms are:

```text
a I + b J,  J^2 = -I.
```

Solving the idempotent equation gives only:

```text
0
I.
```

So there is no retained equivariant selected/spectator split:

```text
spectator = 0.
```

This removes the first delta residual natively.

## Endpoint Unit

The endpoint readout is the determinant/oriented-volume functor of the real
primitive.  A determinant functor preserves the identity:

```text
det(I) = 1
phase(det I) = 0.
```

For an affine endpoint coordinate:

```text
F(phi) = phi + c,
```

unit preservation gives:

```text
F(0) = 0 -> c = 0.
```

So the endpoint-exact offset is removed by determinant-functor normalization,
not by target fitting.

## Delta Closure

The retained APS/ABSS computation gives:

```text
eta_APS = 2/9.
```

With:

```text
selected = 1
spectator = 0
c = 0
```

the physical Brannen endpoint is:

```text
delta_open = eta_APS = 2/9.
```

## Q Closure

The retained observable principle reads physical scalar observables as
zero-source local source-response coefficients after subtracting the
zero-source determinant baseline.  On the normalized second-order carrier:

```text
z = 0 -> w_plus = w_perp = 1/2
       -> K_TL = 0
       -> Q = 2/3.
```

## Why This Is Native

No new value is chosen.  The load-bearing inputs are:

```text
real/CPT closure;
the retained conjugate-pair Brannen construction;
Z3 equivariance;
determinant functor unit preservation;
zero-source source-response normalization.
```

The old `CP1`/rank-one language is a coordinate presentation of the conjugate
pair phase ratio.  It is not an independent physical selector.  Promoting a
rank-one line to the endpoint object would break the retained real/CPT closure
or add extra non-equivariant boundary data.

## Falsifiers

- A retained proof that the physical charged-lepton endpoint is a non-CPT
  single complex character line.
- A retained nontrivial real `Z3`-equivariant idempotent on the nontrivial
  primitive.
- A physical determinant endpoint readout that does not preserve the identity.
- A native nonzero charged-lepton source not equivalent to the selector value
  in source coordinates.

## Verification

Run:

```bash
python3 scripts/frontier_koide_native_brannen_real_primitive_closure_theorem.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_NATIVE_BRANNEN_REAL_PRIMITIVE_CLOSURE_THEOREM=TRUE
KOIDE_NATIVE_BRANNEN_ENDPOINT_IS_REAL_Z3_PRIMITIVE=TRUE
KOIDE_NATIVE_DETERMINANT_ENDPOINT_UNIT_FORCES_C_ZERO=TRUE
KOIDE_Q_CLOSED_BY_NATIVE_ZERO_SOURCE_READOUT=TRUE
KOIDE_DELTA_CLOSED_BY_NATIVE_REAL_PRIMITIVE_DETERMINANT_READOUT=TRUE
KOIDE_DIMENSIONLESS_LANE_NATIVE_CLOSURE=TRUE
```
