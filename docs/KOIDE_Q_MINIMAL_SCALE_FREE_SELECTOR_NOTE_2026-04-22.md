# Koide Q Minimal Scale-Free Selector

**Date:** 2026-04-22
**Status:** science-only branch-local strengthening note; not woven through
review or publication surfaces
**Purpose:** tighten the `Q` route once the second-order returned carrier is
accepted by showing that the selector variable is not an arbitrary quadratic
choice.

The key statement is:

> on the exact second-order returned mass carrier, there is no nontrivial
> scale-free `C_3`-covariant scalar at linear order, and at quadratic order
> there is exactly **one** nontrivial scale-free invariant ratio.

That ratio is equivalently:

- `E_perp / E_+`,
- `(r1^2 + r2^2) / r0^2`,
- `1 / kappa`,
- or `Q`.

So once the second-order carrier is admitted, the selector variable itself is
already unique up to reparametrization.

**Primary runner:** `scripts/frontier_koide_q_minimal_scale_free_selector.py`

---

## 1. Carrier

The returned charged-lepton mass object on `T_1` is the three-slot real vector

```text
x = (u, v, w),
```

or equivalently its cyclic Fourier image

```text
H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2.
```

The selector should be:

- `C_3`-covariant / invariant,
- local to the returned carrier,
- and scale-free.

---

## 2. Linear order

A real linear scalar on `x` has the form

```text
L(x) = a u + b v + c w.
```

Imposing invariance under the species 3-cycle forces

```text
a = b = c,
```

so the only invariant linear scalar is

```text
L(x) ∝ u + v + w = r0.
```

But `r0` is degree-1 and therefore not scale-free:

```text
r0(t x) = t r0(x).
```

So there is no nontrivial scale-free invariant at linear order.

---

## 3. Quadratic order

At quadratic order, the invariant scalar space is exactly two-dimensional:

```text
Q(x) = A r0^2 + C (r1^2 + r2^2).
```

Both basis elements are degree-2, so after quotienting by overall scale there
is exactly one nontrivial ratio:

```text
rho = (r1^2 + r2^2) / r0^2
    = 2 E_perp / E_+
    = 2 / kappa.
```

Equivalently,

```text
Q = (1 + rho) / 3.
```

Therefore the minimal nontrivial scale-free invariant selector on the returned
carrier is unique up to reparametrization.

---

## 4. Consequence

This removes another apparent choice from the branch-local `Q` close candidate.

The remaining theory choices are now:

1. identify the physical selector carrier with the exact second-order returned
   mass operator,
2. identify the physical selector **value law** on the unique minimal scale-free
   invariant of that carrier.

The selector variable itself is no longer a separate ambiguity.

---

## 5. Bottom line

Once the second-order returned carrier is accepted, the unique minimal
scale-free `C_3`-invariant selector variable is already fixed:

```text
E_perp / E_+   <->   1/kappa   <->   Q.
```

So the only remaining substantive question is not "which invariant?" but
"what physical value law picks the relevant point on that one-variable family?"
