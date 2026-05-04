# Koide `Gamma`-Orbit Selector Bridge Note

**Date:** 2026-04-18
**Status:** exact selector pullback on the fresh `Gamma`/orbit-return route
**Runner:** `scripts/frontier_koide_gamma_orbit_selector_bridge.py`

## Question

The fresh `Gamma`-orbit note already proved the exact linear map
```text
(u, v, w)  ->  (r0, r1, r2)
```
from the physical three-slot return object to the Koide cyclic basis:
```text
r0 = u + v + w,
r1 = 2u - v - w,
r2 = sqrt(3) (v - w).
```

That closed the basis step. But what does the Koide selector itself become on
the microscopic orbit slots?

## Bottom line

It becomes one symmetric quadratic cone:
```text
u^2 + v^2 + w^2 = 4 (uv + uw + vw).
```

Equivalently, the cyclic selector
```text
2 r0^2 = r1^2 + r2^2
```
pulls back exactly to
```text
4 (uv + uw + vw) - (u^2 + v^2 + w^2) = 0.
```

So once the microscopic `Gamma`/orbit-return law produces the three-slot real
object `(u, v, w)`, the remaining selector problem is no longer a law on an
abstract circulant matrix. It is one explicit symmetric quadratic relation on
those physical orbit slots.

## Exact pullback

Using
```text
r0 = u + v + w,
r1 = 2u - v - w,
r2 = sqrt(3) (v - w),
```
the Koide selector becomes
```text
2 r0^2 - r1^2 - r2^2
  = 2 [4 (uv + uw + vw) - (u^2 + v^2 + w^2)].
```

Therefore
```text
2 r0^2 = r1^2 + r2^2
```
is equivalent to
```text
u^2 + v^2 + w^2 = 4 (uv + uw + vw).
```

That is the exact microscopic orbit-slot version of the same Koide cone.

## Bridge to standard Koide

If `(u, v, w)` are the physical charged-lepton amplitudes
```text
(sqrt(m_e), sqrt(m_mu), sqrt(m_tau)),
```
then this pulled-back orbit-slot cone is exactly the standard Koide equation
```text
(u^2 + v^2 + w^2) / (u + v + w)^2 = 2/3.
```

So the `Gamma`/orbit-return route does not introduce any new nonlinear
reparametrization. It lands directly on the same `sqrt(m)` cone.

## Why this matters

This sharpens the positive target again.

The open `Gamma`-route science is now:

1. derive the microscopic orbit-slot **value law** producing `(u, v, w)`;
2. derive the symmetric quadratic selector
   ```text
   u^2 + v^2 + w^2 = 4 (uv + uw + vw);
   ```
3. then the cyclic Koide law follows automatically.

That is cleaner than working directly at the matrix level.

## Observed witness

The observed charged-lepton amplitudes satisfy this pulled-back cone to the
same Koide precision as usual.

So the bridge is not merely formal. It lands on the actual target.

## What this does not yet close

This note does **not** yet derive:

- the microscopic `Gamma`/orbit-return law for `(u, v, w)`;
- the dynamical reason the orbit-slot cone should hold.

But it tells us exactly what that remaining selector must look like on the
fresh physical-lattice route.

The companion
`KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md`
now closes the basis law before this selector: the full `Gamma_i` orbit is
exactly the `C_3` orbit of one local three-slot template.

## Bottom line

The fresh `Gamma`/orbit-return route is now reduced to one very concrete
microscopic target:

> derive a physical three-slot orbit law `(u, v, w)` and the single symmetric
> quadratic cone
> `u^2 + v^2 + w^2 = 4 (uv + uw + vw)`.

That is the Koide law in orbit-slot coordinates.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_gamma_axis_covariant_full_cube_orbit_law_note_2026-04-18](KOIDE_GAMMA_AXIS_COVARIANT_FULL_CUBE_ORBIT_LAW_NOTE_2026-04-18.md)
- [koide_gamma_orbit_cyclic_return_candidate_note_2026-04-18](KOIDE_GAMMA_ORBIT_CYCLIC_RETURN_CANDIDATE_NOTE_2026-04-18.md)
