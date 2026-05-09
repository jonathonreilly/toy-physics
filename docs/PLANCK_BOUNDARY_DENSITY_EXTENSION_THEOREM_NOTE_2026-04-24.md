# Planck Boundary-Density Extension Theorem

**Date:** 2026-04-24
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only. This note is conditional
Planck-lane support and does not set or predict an audit outcome.
**Runner:** `scripts/frontier_planck_boundary_density_extension.py`

## Dependency and authority context

- [`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)
  — source-unit normalization separating bare
  `G_kernel = 1/(4π)` from conditional physical `G_Newton,lat = 1`.
- `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`
  — context for the primitive-coframe carrier construction. This bounded
  note keeps `c_cell = 1/4` and the carrier bridge as explicit premises
  rather than adding a new graph edge through the already-cyclic Planck/BH
  carrier chain.
- `BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
  — composition context recording the conditional chain
  `c_cell = 1/4 ⇒ S_BH = A · c_cell = A/(4 G_Newton,lat)` with
  `G_Newton,lat = 1` in framework lattice units, conditional on the
  Wald-Noether formula admitted as universal physics input and on the
  same gravitational boundary/action density bridge premise. It is not a
  one-hop dependency here because that composition surface already cites this
  extension theorem.

The one-hop dependency above fixes the source-unit normalization used in the
conditional Planck match. The Planck/BH carrier files are named as authority
context only; the present bounded theorem remains explicit about the premises
it assumes and does not add a circular dependency edge.

## Purpose

This note closes a constructive sub-gap in the conditional Planck packet.

The packet already derives the primitive source-free coefficient

```text
c_cell = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4.
```

via the cited primitive-coframe boundary carrier theorem. What was implicit
in the present note's earlier formulation is the finite-boundary extension:
if the primitive boundary count is accepted as the microscopic gravitational
boundary/action carrier, does the one-cell coefficient extend consistently
from one primitive face to arbitrary finite boundary patches?

Yes. Locality, additivity, and cubic-frame orientation symmetry force the
unique finite-boundary density

```text
N_A(P) = c_cell * A(P) / a^2
```

on every finite boundary patch `P` that is a finite disjoint union of
primitive faces. Rectangular patches are the simplest examples; the theorem is
really a finite face-union extension.

## The theorem

Let `P` be a finite boundary patch tiled by primitive lattice faces. Assume:

1. **locality:** the boundary count is a sum of primitive face contributions;
2. **additivity:** disjoint primitive-face unions add;
3. **cubic-frame orientation symmetry:** `xy`, `yz`, and `zx` primitive faces
   carry the same source-free coefficient;
4. **primitive normalization:** one primitive face carries `c_cell = 1/4`.

Then for any finite patch with `n` primitive faces,

```text
N_A(P) = n * c_cell.
```

Since `A(P) = n a^2`, this is equivalently

```text
N_A(P) = c_cell * A(P) / a^2.
```

The extension is unique: any local additive rule agreeing on one primitive
face must agree on every finite patch because every finite patch is a finite
union of primitive faces.

## Planck normalization consequence

With the gravitational carrier premise accepted, the extended microscopic
boundary/action density is

```text
S_patch / k_B = c_cell * A / a^2.
```

Equating it to the standard gravitational area/action density,

```text
S_grav / k_B = A / (4 l_P^2),
```

gives

```text
c_cell / a^2 = 1 / (4 l_P^2),
a / l_P = sqrt(4 c_cell) = 1.
```

So the bounded closure here is not merely single-cell arithmetic. The exact
`1/4` coefficient now has a unique additive finite-boundary extension on the
conditional carrier surface.

## Conditional carrier-identification chain

A prior review identified the load-bearing physical step beyond finite
additivity:

> the finite additivity theorem is algebraically valid under its
> assumptions, but the Planck-normalization consequence depends on
> accepting that the primitive boundary/worldtube count is the
> microscopic gravitational boundary/action carrier.

This section makes the structure of that bridge explicit on the live
authority chain. It does **not** derive the bridge from `A_min`; that
remains the named open target. What it does is record the exact form the
carrier identification takes once the same admitted-physics-input chain
already used by the BH-quarter Wald-Noether composition surface is in scope.

### Bridge premise (admitted, not derived)

```text
(BP)  the framework's first-order coframe boundary carrier P_A is
      the microscopic gravitational boundary/action density carrier.
```

This is the same bridge premise named in
`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM`
§5 ("Why this is positive but not lane closure") and inherited verbatim by
the present note. The point here is to cite that named open premise rather
than letting it remain implicit.

### Conditional carrier-share derivation

Granted (BP) and the Wald-Noether formula as admitted universal physics
input on the framework's discrete GR action surface
(per the BH-Wald composition note), the Bekenstein-Hawking entropy of any
stationary Killing horizon of cross-section area `A` is

```text
S_BH = A / (4 G_Newton,lat).                                        (W)
```

The boundary-density extension theorem above gives, on the same surface,

```text
N_A(P) = c_cell * A(P) / a^2,    c_cell = 1/4.                       (E)
```

Identifying `S_BH` with the extended boundary count on a horizon patch
(this *is* the (BP) identification, applied at the macroscopic horizon
scale), and matching (W) to (E) at `A(P) = A`,

```text
A * c_cell / a^2  =  A / (4 G_Newton,lat),
c_cell / a^2      =  1 / (4 G_Newton,lat).                           (M)
```

In the framework's natural lattice units (`a = 1` and the source-unit
normalization `G_kernel = 1/(4π) → G_Newton,lat = 1` from
[`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)),
(M) reduces to the algebraic identity

```text
c_cell = 1/4.                                                        (C)
```

The chain (W) ↔ (E) ↔ (M) ↔ (C) is consistent: each primitive face carries
exactly `c_cell = 1/4` of the gravitational entropy/action share, summing
locally and additively to `A/(4G_Newton,lat)` on any finite patch tiled by
primitive faces.

### What the bridge IS, on this surface

Conditional on (BP) and the Wald admission, the carrier identification is
not free. It is forced to:

```text
each primitive face contributes exactly c_cell = 1/4 (in lattice units)
of the gravitational boundary/action density carrier, and a finite patch
of n primitive faces carries exactly n * c_cell = n/4 of that carrier,
matching A/(4G_Newton,lat) at G_Newton,lat = 1.
```

This is a sharper articulation of the carrier-identification step than the
earlier "boundary count = gravitational carrier" assertion: the *share per
face* is fixed at `1/4` by the cited authorities, not chosen.

### What this section does NOT close

The above is a conditional structural identity, not a derivation of (BP).
The Wald-Noether formula remains an admitted universal physics input, and
(BP) itself remains the named open bridge premise carried forward from the
primitive-coframe carrier theorem §5. Any future ratification belongs to the
independent audit lane after (BP) is derived from `A_min`.

## What this closes

This closes the finite-boundary extension sub-gap:

> Once the primitive boundary count is accepted as the microscopic
> gravitational boundary/action carrier, the primitive `c_cell = 1/4`
> coefficient extends uniquely and additively to finite boundary patches.

This is a bounded support theorem for the Planck conditional packet.
With the explicit authority context above, the conditional carrier-share
identification is sharpened to "each primitive face carries exactly
`c_cell = 1/4` of the gravitational boundary/action density carrier on
the same surface where the Planck/BH carrier authorities live."

## What remains open

This note still does **not** derive the carrier premise (BP) itself.

The remaining positive Planck target, restated in the precise form of
`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM`
§5, is:

> `derive_gravitational_boundary_action_density_as_first_order_coframe_carrier`
>
> i.e. derive that the framework's first-order coframe boundary carrier
> `P_A` is the microscopic gravitational boundary/action density carrier
> from `A_min` alone, without the Wald-Noether admission.

The no-go notes remove two shortcuts to that target; this note adds the
positive extension theorem and the conditional carrier-share identity that
apply once the target is accepted or derived.

## Verification

Run:

```bash
python3 scripts/frontier_planck_boundary_density_extension.py
```

The runner checks:

1. `c_cell = 1/4`;
2. constant density on multiple finite rectangular patches;
3. subdivision invariance;
4. constant density on non-rectangular finite face unions;
5. cubic-frame orientation symmetry;
6. uniqueness from unit-cell normalization on rectangular and non-rectangular
   finite face unions;
7. the extended density still yields conditional `a/l_P = 1`;
8. the result is an extension theorem, not a carrier-identification theorem;
9. conditional carrier-share consistency: under the bridge premise (BP) and
   the admitted Wald formula, the per-face contribution `c_cell = 1/4`
   matches `1/(4 G_Newton,lat)` at `G_Newton,lat = 1` on every finite patch
   (chain (W) ↔ (E) ↔ (M) ↔ (C) above).
