# Koide `Q = 2/3` Bridge — Single-Primitive Narrowing

**Date:** 2026-04-22  
**Status:** exact support / bridge-target narrowing on the charged-lepton Koide
lane  
**Runner:** `scripts/frontier_koide_q_bridge_single_primitive.py`

## Question

The current Koide package already has strong executable support for
`Q = 2/3`, but the physical/source-law bridge remains open:

> why must the physical charged-lepton packet extremize the admitted
> block-total Frobenius functional on the accepted framework surface?

After the April 22 support additions, the practical question is no longer
"which arithmetic candidate should we try next?" It is:

> do the surviving candidate faces of the `Q` bridge actually collapse to one
> primitive, so that only one physical-identification problem remains?

## Main statement

Yes. On the current charged-lepton carrier, the surviving arithmetic and
representation-theoretic faces of the `Q` bridge collapse to one scalar
primitive

```text
P_Q := |b|^2 / a^2 = 1/2.
```

Equivalently:

```text
equal cyclic block power
<=> real-irrep-block democracy
<=> a^2 = 2 |b|^2
<=> kappa = a^2 / |b|^2 = 2
<=> Brannen c = sqrt(2)
<=> Koide Q = 2/3.
```

The runner also verifies that three April 22 support faces land on the same
primitive value:

```text
dim(spinor) / dim(Cl^+(3)) = 1/2,
T(T+1) - Y^2 = 1/2,
(T(T+1) - Y^2) / (T(T+1) + Y^2) = 1/2
```

on the charged-lepton Yukawa participant route.

## What is actually sharpened

This note does **not** close the physical/source-law bridge. It sharpens the
target:

- the `Q = 2/3` bridge is no longer best read as a family of unrelated
  candidate arithmetic laws;
- the surviving support routes all point to the same primitive scalar `1/2`;
- the remaining open work is therefore the **physical identification** of that
  primitive on the charged-lepton carrier.

So the current burden is:

1. derive why the physical packet realizes `P_Q = 1/2`, or
2. explicitly retain `P_Q = 1/2` as the missing primitive.

Either route closes the `Q = 2/3` bridge.

## Proof sketch

### 1. Cyclic projector form

On the canonical cyclic image

```text
H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2
```

the exact block powers are

```text
E_+ = r0^2 / 3,
E_perp = (r1^2 + r2^2) / 6.
```

Therefore

```text
E_+ = E_perp
<=> 2 r0^2 = r1^2 + r2^2.
```

### 2. Real-irrep-block democracy

Under the standard circulant coordinates

```text
a = r0 / 3,
|b|^2 = (r1^2 + r2^2) / 36,
```

the same equality becomes

```text
3 a^2 = 6 |b|^2
<=> a^2 = 2 |b|^2
<=> |b|^2 / a^2 = 1/2
<=> kappa = a^2 / |b|^2 = 2.
```

### 3. Brannen and Koide

For the Brannen envelope

```text
sqrt(m_k) = v_0 (1 + c cos(delta + 2 pi k / 3)),
```

the carrier match gives

```text
c = 2 |b| / a.
```

Hence `|b|^2 / a^2 = 1/2` forces `c = sqrt(2)`, and the standard algebraic
identity then gives

```text
Q = 2/3
```

independently of `delta`.

### 4. April 22 support faces

The new support batch adds several axiom-native reformulations. Three of them
hit the same scalar immediately:

```text
dim(spinor) / dim(Cl^+(3)) = 2 / 4 = 1/2,
T(T+1) - Y^2 = 1/2,
(T(T+1) - Y^2) / (T(T+1) + Y^2) = 1/2
```

on the charged-lepton Yukawa participant route.

These do not create new independent bridge values. They collapse onto the
same primitive `P_Q = 1/2`.

## What this does not claim

- It does **not** prove that the physical charged-lepton packet must realize
  `P_Q = 1/2`.
- It does **not** close the Brannen-phase bridge behind `delta = 2/9`.
- It does **not** promote the overall scale `v_0`.

## Bottom line

The `Q = 2/3` bridge is now best read as a **single-primitive problem**:

> identify physically why the charged-lepton packet realizes
> `P_Q = |b|^2 / a^2 = 1/2`.

That is materially sharper than carrying several apparently different
arithmetic candidates at once.
