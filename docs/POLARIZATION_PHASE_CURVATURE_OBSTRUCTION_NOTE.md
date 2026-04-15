# Polarization Phase-to-Curvature Obstruction

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Scope:** universal-side phase-localization only  
**Purpose:** test whether the exact support-side dark phase from `B_R^phase` can be canonically identified with a universal complement angle, or whether the exact residual obstruction remains an orbit-gauge freedom

## Verdict

The exact support-side dark phase can be matched to a universal complement
angle only at the level of the shared residual orbit.

There is **no canonical section-valued phase-to-curvature map** from the
current atlas alone.

The strongest exact map currently forced by the universal / support
interface is the orbit-valued identification:

`vartheta_R  ~  alpha_curv   (mod SO(2))`

where:

- `vartheta_R` is the exact support dark phase on the residual dark `T1`
  plane;
- `alpha_curv` is the corresponding complement angle in the universal
  `E \oplus T1` orbit bundle after the `Pi_A1` core is fixed;
- the equivalence is the shared connected residual gauge `SO(2)`.

So the current atlas gives an exact **phase-orbit correspondence**, but not
an exact canonical phase-to-curvature **section**.

## Exact support-side input

The new exact phase-lift candidate is:

`B_R^phase := (K_R^phase, I_TB^phase, Xi_TB^phase)`

with:

`K_R^phase(q) := (u_E, u_T, delta_A1 u_E, delta_A1 u_T, d_y, d_z)`.

Equivalently, the dark data are:

`D_R(q) := (d_y, d_z)`

with

- `rho_R := ||D_R||`
- `vartheta_R := atan2(d_z, d_y)`

Under the residual connected dark-plane `SO(2)`:

- `rho_R` is invariant;
- `vartheta_R` shifts by the gauge angle.

So `vartheta_R` is a genuine exact support-side phase coordinate.

## Exact universal-side input

The exact universal core is the invariant rank-2 projector:

`Pi_A1 = diag(1,0,0,0,1,0,0,0,0,0)`.

That core is exact, but the complementary `E \oplus T1` channels are still
an orbit bundle over valid `3+1` frames. The natural candidate connection is
the orbit / Maurer-Cartan connection, but the current atlas does not force a
distinguished connection.

Thus the universal side supplies:

- an exact invariant core;
- an exact complement orbit bundle;
- no canonical complement angle section.

## Glue result

The glue audit already reduced the common residual gauge to:

`SO(2)`.

That is the stabilizer of the shared bright axis once the `Pi_A1` core and
the support bright block are both imposed.

This is the key point:

> the support phase and the universal complement angle are both orbit
> coordinates for the same residual `SO(2)`, but the current atlas does not
> choose a preferred origin on that orbit.

Therefore the best exact statement is not a section theorem. It is an orbit
equivalence theorem:

`vartheta_R` and `alpha_curv` are the same connected gauge coordinate modulo
`SO(2)`.

## Exact residual obstruction

The obstruction is exactly the absence of a distinguished phase-fixing
primitive on the dark complement plane.

More concretely:

1. `B_R^phase` carries the dark phase exactly on the support side;
2. `Pi_A1` fixes the universal core exactly;
3. the universal complement is still only an `SO(3)` orbit bundle;
4. the common residual gauge is still `SO(2)`;
5. every exact common object in the current atlas is invariant under that
   `SO(2)`.

So there is no way, from the current exact objects alone, to choose a
canonical zero-angle section that would turn the orbit equivalence into a
unique curvature-localization map.

## Strongest exact map

The strongest exact phase-to-curvature map supported by the current atlas is:

`[vartheta_R]_{SO(2)}  <->  [alpha_curv]_{SO(2)}`

or, equivalently, an `SO(2)`-equivariant identification of the shared dark
orbit.

That is exact, but it is not canonical as a section.

## Bottom line

The support dark phase does lift to the universal complement only as a shared
orbit coordinate. The exact residual obstruction is the remaining connected
`SO(2)` gauge, which the current atlas does not canonically fix.

