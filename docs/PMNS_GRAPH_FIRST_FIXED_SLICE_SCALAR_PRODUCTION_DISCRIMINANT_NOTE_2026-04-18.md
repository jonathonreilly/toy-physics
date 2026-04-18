# PMNS Graph-First Fixed-Slice Scalar Production Discriminant

**Date:** 2026-04-18  
**Status:** exact scalar reduction of the PMNS-native production frontier; the
remaining native production lane is one fixed-slice holonomy discriminant
certificate, and the current bank still does not realize it  
**Script:** `scripts/frontier_pmns_graph_first_fixed_slice_scalar_production_discriminant_2026_04_18.py`

## Question

After the PMNS-native lane has been reduced to one minimal fixed-slice
two-holonomy production certificate, can that remaining production frontier be
compressed one scalar step further?

## Answer

Yes.

Fix one slice `w = w0` and any independent angle pair `(phi_1, phi_2)` with

`sin(phi_2 - phi_1) != 0`.

Define the centered holonomy vector

`c_(phi1,phi2) := (h_(phi1) - w0, h_(phi2) - w0)`

and the scalar discriminant

`Delta_(phi1,phi2) := ||c_(phi1,phi2)||^2`.

Because the fixed-slice two-holonomy map is invertible, one has

`Delta_(phi1,phi2) = 0  <=>  chi = 0`.

So the whole remaining PMNS-native fixed-slice production frontier may now be
stated as one scalar certificate:

- produce `Delta_(phi1,phi2) > 0`.

The current bank still does **not** realize even that scalar certificate.

## Setup

From
[PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md](./PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_COLLAPSE_NOTE_2026-04-17.md):

- at fixed `w = w0`, any independent native holonomy pair reconstructs `chi`
  exactly.

From
[PMNS_GRAPH_FIRST_FIXED_SLICE_MINIMAL_PRODUCTION_CERTIFICATE_NOTE_2026-04-18.md](./PMNS_GRAPH_FIRST_FIXED_SLICE_MINIMAL_PRODUCTION_CERTIFICATE_NOTE_2026-04-18.md):

- the whole remaining PMNS-native lane is already one minimal fixed-slice
  two-holonomy production certificate.

The only remaining question is whether that pair certificate can be compressed
one scalar step further.

## Theorem 1: exact scalar discriminant form of the PMNS-native production frontier

Fix an independent angle pair `(phi_1, phi_2)`.

Then the following are equivalent:

1. production of a nontrivial fixed-slice holonomy pair;
2. production of nonzero `chi = J_chi`;
3. production of positive scalar discriminant
   `Delta_(phi1,phi2) > 0`.

### Proof

The collapse theorem gives the exact fixed-slice linear system

`c_(phi1,phi2) = M_(phi1,phi2) (u,v)^T`

with invertible matrix `M_(phi1,phi2)`.

Therefore:

- `c_(phi1,phi2) = 0` if and only if `(u,v) = (0,0)`,
- and `(u,v) = (0,0)` if and only if `chi = 0`.

But `Delta_(phi1,phi2) = ||c_(phi1,phi2)||^2`, so

`Delta_(phi1,phi2) = 0` if and only if `c_(phi1,phi2) = 0`.

Therefore all three statements are equivalent.

## Corollary 1: canonical `C3` scalar witness

For the native pair

- `phi_1 = 0`,
- `phi_2 = 2 pi / 3`,

the scalar discriminant is

`Delta_C3 = (h_0 - w0)^2 + (h_(2pi/3) - w0)^2`.

This vanishes exactly when `chi = 0`.

So the PMNS-native production frontier now has a canonical scalar `C3`
witness.

## Corollary 2: the current bank still does **not** realize the scalar certificate

The current retained PMNS-native bank still forces `J_chi = chi = 0`.

Therefore it still forces `Delta_(phi1,phi2) = 0`, and so still does **not**
realize the scalar production discriminant certificate.

## What this closes

- exact scalar reduction of the PMNS-native production frontier
- exact equivalence between nonzero `chi`, nontrivial holonomy-pair production,
  and one scalar discriminant
- exact current-bank failure at that scalar level

## What this does not close

- a sole-axiom theorem producing positive discriminant
- a Wilson-to-PMNS descendant theorem
- a positive global PF selector

## Why this matters

The PMNS-native frontier is now sharper than a pair certificate.

It is one scalar nonvanishing certificate on a fixed slice.

## Command

```bash
python3 scripts/frontier_pmns_graph_first_fixed_slice_scalar_production_discriminant_2026_04_18.py
```
