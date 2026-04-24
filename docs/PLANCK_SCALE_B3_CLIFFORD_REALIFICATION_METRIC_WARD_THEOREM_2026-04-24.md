# Planck-Scale B3 Clifford Realification Metric-Ward Theorem

**Date:** 2026-04-24
**Status:** positive B3 closure on the canonical real linear-response envelope
**Verifier:** `scripts/frontier_planck_b3_clifford_realification_metric_ward_theorem_2026_04_24.py`

## Question

Can the B3 blocker be closed without importing Einstein/Regge dynamics by name?

The previous B3 no-go showed that bare finite signed-permutation symmetry of
the fixed cubic cell does not, by itself, force a dynamical metric/coframe
response or conserved symmetric spin-2 Ward identity. The remaining possible
positive route is to show that the required response is already forced once
`Cl(3)` on `Z^3` is read in its native linear-response envelope.

## Result

Yes, on the canonical realified edge-Clifford linear-response surface.

The retained lattice module is

`T_Z = Z^3`.

The retained Clifford vector module is the real vector space

`V = Cl_1(3)`.

The canonical linear-response module is not an extra geometry sector; it is the
realification required to compare lattice translations with Clifford vectors:

`T_R = T_Z tensor_Z R`.

The flat soldering theorem supplies the base coframe

`e_0 : T_R -> V`, `edge_i -> Gamma_i`.

A local first-order translation defect is therefore a local perturbation of the
soldering map

`e = e_0 + h`,

with `h in Hom(T_R, V)`. The Clifford anticommutator gives the induced metric

`g_ij(e) = <e_i, e_j> = (1/2) {e_i, e_j}_scalar`.

At the flat cell,

`delta g_ij = h_ij + h_ji`.

Thus:

1. the scalar trace channel is not a rival nonmetric response; it is the trace
   part of the metric perturbation;
2. the symmetric traceless channel is the shear part of the metric
   perturbation;
3. the antisymmetric channel has `delta g = 0` and is the infinitesimal
   Clifford-frame rotation gauge.

So the physical response carrier forced by Clifford realification is the
symmetric metric/coframe carrier, not an arbitrary matrix response.

Local vertex-origin changes act by the exact cochain gauge law

`h -> h + d xi`.

Stationarity under this gauge for arbitrary compactly supported `xi` gives the
discrete Ward identity

`d^* T = 0`.

After the already retained time-lock, this is the `3+1` conserved symmetric
source Ward identity on the realified coframe response. The conditional
metric-sector uniqueness theorem can then be applied without importing the
metric/coframe carrier by hand.

## Inputs

This theorem uses:

1. the retained `Z^3` translation module;
2. the retained real Clifford vector space `Cl_1(3)`;
3. the already proved flat soldering `edge_i <-> Gamma_i`;
4. canonical realification `T_Z tensor_Z R`, needed for first-order response;
5. the source-free rule that unobservable frame rotations are gauge, not
   physical sources.

It does not assume Einstein equations, the Regge action, the GHY term, or a
preselected continuum metric action.

## Theorem 1: Clifford realification is the minimal linear-response envelope

The lattice translation module `Z^3` has no nontrivial infinitesimal tangent
vectors as a discrete group. But the retained Clifford relation is already a
real bilinear relation:

`{Gamma_i, Gamma_j} = 2 delta_ij I`.

Any first-order response that differentiates the edge-Clifford soldering must
therefore live in the realified module

`T_R = Z^3 tensor_Z R`.

This is not a choice of continuum spacetime. It is the universal real linear
envelope of the retained translation module. A map out of `Z^3` into any real
linear response space factors uniquely through `T_R`.

Therefore the B3 question is not whether the finite cell automorphism group has
a Lie algebra. It does not. The question is whether the retained
edge-Clifford soldering has a canonical first-order response envelope. It does:

`Hom_R(T_R, Cl_1(3))`.

## Theorem 2: the induced response is metric/coframe response

Let

`e_i = Gamma_i + h_i^a Gamma_a`.

The Clifford anticommutator gives

`g_ij(e) = (1/2) <{e_i, e_j}>_scalar`.

To first order,

`delta g_ij = h_ij + h_ji`.

So the nine components of `h_ij` split as:

1. `tr h`: metric trace;
2. `h_(ij) - (tr h / 3) delta_ij`: metric shear;
3. `h_[ij]`: frame rotation gauge.

The earlier scalar and antisymmetric countermodels are therefore resolved on
this surface. Scalar trace is part of the metric response. Antisymmetric
response does not change the metric and is killed by frame gauge.

## Theorem 3: local translation gauge gives conservation

A local choice of vertex origins is a zero-cochain

`xi in C^0(cell complex, T_R)`.

Changing origins shifts the coframe perturbation by an exact one-cochain:

`h -> h + d xi`.

Let `T` be the source conjugate to `h`. The source variation is

`delta S = <T, d xi> = <d^* T, xi>`.

If the source-free theory is independent of vertex-origin gauge for all
compactly supported `xi`, then

`d^* T = 0`.

This is the discrete conserved-source Ward identity. Since antisymmetric frame
rotations are gauge and the physical metric variation is symmetric, the
conserved source is the symmetric metric/coframe source.

## Theorem 4: B3 closes on this surface

The previous B3 no-go remains correct for the smaller surface that only admits
finite signed-permutation automorphisms of the fixed cubic cell. That surface
has no infinitesimal local Ward generator.

The present theorem uses the canonical real linear-response envelope of the
retained edge-Clifford soldering. On that surface:

1. translation defects are represented by one coframe perturbation `h`;
2. the Clifford anticommutator induces the metric perturbation `delta g`;
3. antisymmetric perturbations are frame gauge;
4. vertex-origin gauge gives `d^*T = 0`;
5. the physical source is symmetric and conserved.

Thus the missing B3 primitive is supplied, provided the reviewer accepts
canonical realification as native to first-order response of `Cl(3)` on `Z^3`.

## Consequence

With this theorem, the gravity-sector uniqueness attempt becomes active rather
than merely conditional: the metric/coframe object class is earned from the
realified edge-Clifford response, and locality/additivity/second-order
consistency then force the accepted Einstein/Regge boundary-action sector up
to normalization and topological ambiguity.

## Remaining Rejection

The only clean rejection left is:

> first-order realification `Z^3 tensor_Z R` is not an admissible native
> response surface for a physical `Cl(3)` on `Z^3` lattice.

If that rejection is accepted, the older finite-automorphism B3 no-go applies.
If it is rejected, B3 is closed on the canonical real linear-response surface.

## Safe Claim

Use:

> B3 closes on the canonical realified edge-Clifford linear-response surface:
> `Z^3 tensor R` supplies the coframe response, the Clifford anticommutator
> supplies the symmetric metric perturbation, antisymmetric perturbations are
> frame gauge, and vertex-origin gauge gives the conserved source Ward
> identity.

Do not use:

> Finite signed-permutation symmetry of the fixed cubic cell alone gives the
> spin-2 Ward identity.

Do not use:

> Einstein/Regge dynamics was assumed as the B3 input.
