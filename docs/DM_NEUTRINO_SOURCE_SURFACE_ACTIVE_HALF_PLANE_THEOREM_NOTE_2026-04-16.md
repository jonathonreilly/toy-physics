# DM Neutrino Source-Surface Active Half-Plane Theorem

**Date:** 2026-04-16  
**Status:** exact blocker-reduction theorem on the live source-oriented sheet  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py`

## Question

After reducing the live source-oriented quotient bundle to the active carrier
coordinates `(delta, q_+)`, what exact domain remains, and how much of that
domain is still visible to the current exact source-facing bank?

## Bottom line

The live active bundle is already the exact closed half-plane

```text
q_+ >= sqrt(8/3) - delta.
```

Equivalently, if

```text
s = q_+ - sqrt(8/3) + delta >= 0,
```

then the active inverse chart is

```text
r31(delta, q_+) = sqrt(s^2 + 1/4)
phi_+(delta, q_+) = asin(1 / (2 r31(delta, q_+))).
```

The boundary

```text
q_+ = sqrt(8/3) - delta
```

is exactly

```text
r31 = 1/2
phi_+ = pi/2.
```

Every point on that half-plane already has a source-oriented quotient
representative, hence a positive Hermitian representative after a common
diagonal shift.

Across that whole active half-plane, the currently exact source-facing bank is
constant:

- `gamma = 1/2`
- `delta + rho = sqrt(8/3)`
- `sigma sin(2v) = 8/9`
- intrinsic CP pair `(cp1, cp2)`
- intrinsic slot pair `(a_*, b_*)`
- slot torsion `Im(a_* b_*) = (sqrt(2) + sqrt(6)) / 9`

So the current bank determines the exact active chamber, but not a point
inside it. The remaining mainline object is the post-canonical law that
selects one active-half-plane point.

## Inputs

This note sharpens:

- [DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SLOT_TORSION_BOUNDARY_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SLOT_TORSION_BOUNDARY_THEOREM_NOTE_2026-04-16.md)

## Exact theorem

### 1. The active bundle is an exact half-plane

The earlier reduction already gave

```text
q_+(delta, r31) = sqrt(8/3) - delta + sqrt(r31^2 - 1/4)
```

with `r31 >= 1/2`.

So necessarily

```text
q_+ >= sqrt(8/3) - delta.
```

Conversely, if `q_+ >= sqrt(8/3) - delta`, define

```text
s = q_+ - sqrt(8/3) + delta >= 0
r31 = sqrt(s^2 + 1/4).
```

Then

```text
sqrt(r31^2 - 1/4) = s
```

and therefore

```text
q_+ = sqrt(8/3) - delta + sqrt(r31^2 - 1/4).
```

So the active bundle is exactly the closed half-plane

```text
q_+ >= sqrt(8/3) - delta.
```

Its boundary is exactly `r31 = 1/2`, hence `phi_+ = asin(1) = pi/2`.

### 2. Every active-half-plane point already has the exact carrier response

Pick any `(delta, q_+)` on that half-plane and reconstruct `r31` as above.
Using the source-oriented quotient gauge with any spectator `m`, one gets a
Hermitian representative on the exact live sheet. After adding a sufficiently
large common diagonal shift, that representative becomes positive.

On that whole chamber the exact carrier response remains

```text
gamma = 1/2
rho = sqrt(8/3) - delta
sigma sin(2v) = 8/9
sigma cos(2v) = sqrt(8)/9 - 3 q_+.
```

So the active half-plane is already the exact carrier-side chamber of the live
source-oriented sheet.

### 3. The current exact source-facing bank is constant on the whole chamber

The earlier theorems already imply that on the live source-oriented sheet:

- the source package is fixed,
- the intrinsic CP pair is fixed,
- the intrinsic slot pair is fixed,
- the slot torsion is fixed.

The new point is that this remains true while moving anywhere on the exact
active half-plane.

In particular:

- keeping `delta` fixed while changing `q_+` leaves the current exact
  source-facing bank unchanged,
- keeping `q_+` fixed while changing `delta` also leaves that same bank
  unchanged.

So neither active coordinate is selected by the current bank. The bank fixes
the chamber, not a point inside it.

## The theorem-level statement

**Theorem (Exact active-half-plane reduction on the live source-oriented
sheet).** Assume the exact source-surface shift-quotient bundle, carrier normal
form, `m`-spectator, intrinsic-slot, and slot-torsion boundary theorems. Then
the live active carrier bundle is exactly the closed half-plane
`q_+ >= sqrt(8/3) - delta`, with inverse chart
`r31 = sqrt((q_+ - sqrt(8/3) + delta)^2 + 1/4)` and boundary
`q_+ = sqrt(8/3) - delta <=> r31 = 1/2`, `phi_+ = pi/2`. Every point on that
half-plane has a positive Hermitian representative after a common diagonal
shift and carries the exact source-facing outputs
`gamma = 1/2`, `delta + rho = sqrt(8/3)`, `sigma sin(2v) = 8/9`, the exact
intrinsic CP pair, the exact intrinsic slot pair, and the exact slot torsion
`Im(a_* b_*) = (sqrt(2) + sqrt(6)) / 9`. Therefore the current bank determines
the exact active chamber, but not a point inside it.

## What this closes

This closes the geometry of the remaining active mainline object more sharply.

The branch no longer needs to describe it only as “some exact 2-real active
bundle over `(delta, q_+)`.”

It can now say more concretely:

- the live active object is the exact half-plane `q_+ >= sqrt(8/3) - delta`
- the current exact source-facing bank is constant on that whole chamber
- so the remaining open object is only the selection law inside that chamber

## What this does not close

This note still does **not** derive the post-canonical microscopic law that
selects a specific active-half-plane point.

It only shows that the current exact bank already fixes the chamber itself and
is blind to the choice of point inside it.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py
```
