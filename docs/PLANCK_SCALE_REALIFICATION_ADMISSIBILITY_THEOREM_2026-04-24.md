# Planck-Scale Realification Admissibility Theorem

**Date:** 2026-04-24
**Status:** closes the realification-admissibility objection for first-order physical response
**Verifier:** `scripts/frontier_planck_realification_admissibility_theorem_2026_04_24.py`

## Question

Can a reviewer reject the realified response module

`Z^3 tensor_Z R`

while still demanding a first-order physical response of the retained
edge-Clifford soldering?

## Result

No.

The finite signed-permutation cell has no infinitesimal automorphism group.
That no-go is correct for a frozen combinatorial cell. But the moment the
reviewer asks for a first-order physical response of the retained soldering

`edge_i <-> Gamma_i`,

the target is no longer the finite automorphism group. It is the universal real
linear response envelope of the translation module:

`T_R := Z^3 tensor_Z R`.

This is forced by the universal property of tensoring with `R`. Every additive
map from primitive lattice translations into a real response space factors
uniquely through `T_R`. Since the Clifford vector module `Cl_1(3)` and the
Clifford anticommutator are real-linear / real-bilinear objects, any
first-order response of the edge-Clifford soldering must use this realified
module.

So the remaining reviewer choice is a dichotomy:

1. **Finite-automorphism-only reading.** Then there is no infinitesimal
   response and no dynamical gravity question. The old B3 no-go applies, but it
   is a rejection of physical first-order response, not an objection to the
   realified response theorem.
2. **Physical first-order response reading.** Then `Z^3 tensor_Z R` is the
   initial admissible response module, and the B3 Clifford realification
   metric-Ward theorem applies.

## Theorem 1: universal real response envelope

Let

`T_Z = Z^3`

be the retained primitive translation module, and let `W` be any real vector
space carrying a first-order response observable.

For every additive map

`f : T_Z -> W`,

there is a unique real-linear map

`f_R : T_Z tensor_Z R -> W`

such that

`f = f_R o i`,

where `i : T_Z -> T_Z tensor_Z R` is the canonical inclusion.

Thus `T_Z tensor_Z R` is not a chosen continuum background. It is the initial
real linear response object attached to the retained translation module.

## Theorem 2: Clifford soldering already targets a real response space

The retained soldering maps primitive translations into the real Clifford
vector module:

`edge_i -> Gamma_i in Cl_1(3)`.

The Clifford relation

`{Gamma_i, Gamma_j} = 2 delta_ij I`

uses real coefficients and a real symmetric bilinear form. A first-order
perturbation

`Gamma_i -> Gamma_i + h_i`

is therefore a variation in a real vector space. By Theorem 1, that variation
factors through `T_Z tensor_Z R`.

Rejecting realification while demanding a differentiable response would ask for
real derivatives without the real response envelope that makes such derivatives
well-defined.

## Theorem 3: the finite automorphism no-go is reclassified

The finite signed-permutation group

`O(3,Z)`

is still the exact automorphism group of the fixed primitive cubic frame. Its
Lie algebra is zero. Therefore it cannot produce an infinitesimal Ward
identity by itself.

But this does not block first-order response of a physical lattice. A response
is not an automorphism of the fixed cell; it is a variation of the retained
soldering map. The correct first-order object is

`Hom_R(T_Z tensor_Z R, Cl_1(3))`.

The previous no-go therefore becomes a scope theorem:

> finite automorphisms alone do not give dynamics; physical first-order
> response forces realification.

## Consequence

The objection

> `Z^3 tensor_Z R` is an imported continuum sector

is not valid once the question is first-order response. Realification imports
no metric dynamics, no Einstein/Regge action, and no continuum spacetime. It is
only the universal real linear envelope of the retained translation module.

The B3 realification theorem can therefore be cited as native to physical
first-order response of `Cl(3)` on `Z^3`.

## Safe Claim

Use:

> Canonical realification is forced by the universal property of first-order
> response into the real Clifford vector module. The finite automorphism no-go
> applies only to the frozen-cell reading, not to physical response.

Do not use:

> Finite signed-permutation symmetry itself has an infinitesimal Ward
> generator.

Do not use:

> Realification imports Einstein/Regge dynamics or a continuum metric action.
