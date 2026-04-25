# Planck Boundary-Density Extension Theorem

**Date:** 2026-04-24
**Status:** retained positive support theorem for the Planck coframe lane
**Runner:** `scripts/frontier_planck_boundary_density_extension.py`

## Purpose

This note closes a constructive sub-gap in the Planck packet.

The packet already derives the primitive source-free coefficient

```text
c_cell = Tr((I_16 / 16) P_A) = 4 / 16 = 1/4.
```

What was implicit is the finite-boundary extension: once the primitive boundary
count is used as the microscopic gravitational boundary/action carrier, does
the one-cell coefficient extend consistently from one primitive face to
arbitrary finite boundary patches?

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

With the retained coframe/CAR carrier supplied separately, the extended microscopic
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

So the positive closure here is not merely single-cell arithmetic. The exact
`1/4` coefficient now has a unique additive finite-boundary extension on the
retained coframe carrier surface.

## What this closes

This closes the finite-boundary extension sub-gap:

> Once the primitive boundary count is accepted as the microscopic
> gravitational boundary/action carrier, the primitive `c_cell = 1/4`
> coefficient extends uniquely and additively to finite boundary patches.

This is a positive support theorem for the Planck coframe packet.

## Guardrail

This note still does **not** derive the carrier premise by itself.

The carrier premise is supplied by:

> `PLANCK_TARGET3_COFRAME_RESPONSE_DERIVATION_THEOREM_NOTE_2026-04-25.md`,
> which derives `D(v)^2=||v||^2 I` on `P_A H_cell` from the retained
> first-order coframe structure.

The no-go notes remove shortcuts to that target; this note adds the positive
extension theorem that applies on the retained coframe/CAR carrier surface.

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
7. the extended density still yields coframe-surface `a/l_P = 1`;
8. the result is an extension theorem, not a carrier-identification theorem.
