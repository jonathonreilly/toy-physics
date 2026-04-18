# Koide `Gamma` Axis-Covariant Full-Cube Orbit Law

**Date:** 2026-04-18  
**Status:** exact physical-lattice basis law on the `Gamma_i` / full-cube route  
**Runner:** `scripts/frontier_koide_gamma_axis_covariant_full_cube_orbit_law.py`

## Question

The fresh `Gamma`-orbit note reduced the Koide lane to a three-slot return
object
```text
diag(u, v, w)
```
on a selected axis, but it left one cross-axis step as a candidate:

> why should the `Gamma_i` returns on the other two spatial axes be the cyclic
> orbit of that same triple?

That was the last missing positive **basis law** before the selector.

## Bottom line

It is now exact on the physical lattice.

Let `U` be the exact full-cube `C_3[111]` cycle on the `3+1` Clifford carrier
`C^16`, rotating the spatial bits
```text
(a, b, c) -> (c, a, b)
```
and acting trivially on taste. Then:

1. `U` preserves `T_1`;
2. `U|_{T_1}` is exactly the retained species cycle `C`;
3. the native axis family `Gamma_i` already satisfies the exact second-order
   return identity on `T_1` for each axis.

On the current Jordan-Wigner matrix realization, one should **not** state the
stronger literal matrix identity `Gamma_2 = U Gamma_1 U^dagger`: the
April 17 shape-theorem stress tests already warn that naive bit-permutation
conjugation is a matrix-realization artifact. The exact statement used here is
weaker and sufficient: the full-cube cycle transports the slot projectors, and
the native `Gamma_i` family reads those transported slots with the exact same
shape theorem on each axis.

Now define one local axis-1 full-cube template on the reachable intermediate
slots:
```text
W_1(u,v,w,z)
  = u P_{O_0} + v P_{110} + w P_{101} + z P_{011}.
```

Transport that template by the exact same full-cube cycle:
```text
W_2 = U W_1 U^dagger,
W_3 = U^2 W_1 (U^dagger)^2.
```

Then the axis-matched second-order returns
```text
D_i = P_{T_1} Gamma_i W_i Gamma_i P_{T_1} |_{species}
```
obey the exact law
```text
D_1 = diag(u, v, w),
D_2 = diag(w, u, v),
D_3 = diag(v, w, u).
```

Equivalently,
```text
D_2 = C D_1 C^dagger,
D_3 = C^2 D_1 (C^dagger)^2.
```

So the old “axis-oriented orbit-slot universality” step is no longer a fresh
candidate. It is forced by exact full-cube `C_3[111]` transport of one local
template.

## Exact full-cube transport facts

The runner verifies directly that the full-cube cycle transports the carrier
and that each native `Gamma_i` has the exact same second-order slot geometry:

```text
U P_{T_1} U^dagger = P_{T_1},
U|_{T_1} = C,
P_{T_1} Gamma_i (P_{O_0}+P_{T_2}) Gamma_i P_{T_1} = I_3  for each axis i.
```

So the cross-axis relation is not an ansatz layered on top of the lattice. It
is the exact slot geometry of the lattice plus the native axis family.

## Template-slot transport

On the full `8`-corner cube:

- `O_0` is fixed by `U`;
- the `T_2` states rotate as
  ```text
  110 -> 011 -> 101 -> 110.
  ```

Therefore one axis-1 template
```text
u P_{O_0} + v P_{110} + w P_{101} + z P_{011}
```
generates the whole axis family by exact `C_3` transport.

## Why the axis returns are exactly cyclic

For the axis-1 return:

- species `100` hops to `O_0`,
- species `010` hops to `110`,
- species `001` hops to `101`.

So
```text
D_1 = diag(u, v, w).
```

After exact cycle transport:

- `W_2 = U W_1 U^dagger` places the same orbit data on the axis-2 reachable
  slots,
- the native `Gamma_2` reads that rotated template on the axis-2 route with
  the same exact shape theorem,

and similarly for axis 3.

The result is exactly
```text
D_2 = diag(w, u, v),
D_3 = diag(v, w, u).
```

So the full `Gamma_i` orbit is the species-cycle orbit of a single diagonal
template.

## The fourth slot is null

The extra template weight `z` on the unreachable `T_2` slot is still present
in the full-cube template, but for each axis it rotates into that axis’s own
unreachable slot. Therefore it contributes identically zero to the
axis-matched return family.

So the physical basis law really is three-slot:
```text
(u, v, w),
```
not four-slot.

## Consequence for the Koide lane

This closes the only remaining **basis** ambiguity in the positive
`Gamma_i` route.

Combined with the earlier notes:

- [KOIDE_GAMMA_ORBIT_CYCLIC_RETURN_CANDIDATE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_CYCLIC_RETURN_CANDIDATE_NOTE_2026-04-18.md)
  gave the exact axis-1 reduction
  ```text
  diag(u,v,w) -> (r0,r1,r2);
  ```
- [KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_SELECTOR_BRIDGE_NOTE_2026-04-18.md)
  pulled the selector back to
  ```text
  u^2 + v^2 + w^2 = 4(uv + uw + vw).
  ```

This note supplies the missing bridge in between:

> the full physical `Gamma_i` orbit on the `3+1` carrier is exactly the
> `C_3` orbit of one local three-slot template.

## What remains open

This note does **not** yet derive:

- the microscopic law fixing the values of `(u, v, w)` from the retained
  lattice dynamics;
- the selector mechanism forcing
  ```text
  u^2 + v^2 + w^2 = 4(uv + uw + vw).
  ```

But it does mean the basis law before the selector is no longer open.

## Bottom line

The positive `Gamma_i` / full-cube route is now reduced to:

```text
exact full-cube C_3 transport
  + one local template W_1(u,v,w,z)
  -> exact orbit family D_1, D_2, D_3
  -> exact three-slot law (u,v,w)
  -> one remaining selector cone
```

So the next singular science target is no longer a basis law. It is the value
law for `(u,v,w)` and then the selector.
