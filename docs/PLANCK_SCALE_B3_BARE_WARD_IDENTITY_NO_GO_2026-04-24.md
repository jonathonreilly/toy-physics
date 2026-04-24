# Planck-Scale B3 Bare Ward-Identity No-Go

**Date:** 2026-04-24
**Status:** theorem-grade B3 reduction/no-go; B3 is not closed
**Verifier:** `scripts/frontier_planck_b3_bare_ward_identity_no_go_2026_04_24.py`

## Question

Can retained `Cl(3)` / `Z^3`, after the flat edge-Clifford soldering theorem,
derive a local metric/coframe response or a conserved symmetric spin-2 Ward
identity without adding a metric/coframe object class by definition?

## Admitted Bare Data

The proof uses only:

1. the primitive `Z^3` translation module with its three nearest-neighbor axes;
2. the retained Clifford generators `Gamma_i` with
   `{Gamma_i, Gamma_j} = 2 delta_ij I`;
3. the flat soldering already derived on the retained cell,
   `edge_i <-> Gamma_i`;
4. finite-range, additive, translation-compatible local response symbols built
   from those retained cell data.

No step assumes a variable metric, a coframe field, a local frame gauge group, a
preselected "geometric sector", or a conservation law for a symmetric tensor
source.

## Result

The bare data do not force the requested dynamical response.

The exact missing primitive is:

> a **local gaugeable defect-to-coframe response primitive**: a derived map from
> local translation defects to one coframe/metric response variable, together
> with a continuous local redundancy whose Noether identity forces the response
> source to be symmetric and conserved.

Without that primitive, the retained cell has a native flat frame but not a
dynamical metric/coframe Ward identity.

## Theorem 1: The Retained Frame Group Has No Local Ward Generator

The automorphisms preserving both the primitive cubic incidence and the flat
edge-Clifford pairing are exactly signed axis permutations:

`B_3 = O(3,Z) = {signed permutation matrices}`.

The full flat translation automorphism group is `Z^3 semidirect O(3,Z)`. The
`Z^3` factor is a discrete basepoint-shift group, not a local frame or coframe
variation. The cell/frame stabilizer relevant to metric/coframe response is the
`O(3,Z)` factor.

This stabilizer has `48` elements. It is finite and discrete. Therefore its
identity component is trivial and its Lie algebra is zero.

A local Ward identity of spin-2 type requires an infinitesimal local parameter,
for example a local coframe variation `delta e^a_mu(x)` or an equivalent local
frame-gauge parameter. The retained signed-permutation group only supplies
pointwise finite relabelings and sign flips. Its local product over cells is
still totally disconnected, so it cannot supply the differentiable local
parameter needed for a Noether identity of the form "divergence of a symmetric
source vanishes."

Thus flat edge-Clifford soldering closes the kinematic frame, but not the
dynamical Ward generator.

## Theorem 2: Bare-Compatible Local Responses Are Not Unique

Let a local first response be represented, at one retained cell, by a real
matrix `M_ij` mapping primitive edge labels to Clifford-vector labels. The
retained frame group acts by

`M -> P M P^T`, with `P in O(3,Z)`.

The nine-dimensional response space decomposes into invariant bare channels:

1. scalar trace channel: `M = lambda I`, dimension `1`;
2. antisymmetric channel: `M^T = -M`, dimension `3`;
3. symmetric traceless channel: `M^T = M`, `tr M = 0`, dimension `5`.

Each channel supports a finite-range additive quadratic local symbol, for
example the onsite norm of the projected channel plus optional finite
difference terms. These symbols are compatible with `Z^3` locality, additivity,
and the retained signed-permutation frame symmetry.

The scalar and antisymmetric witnesses are not symmetric spin-2 responses, yet
they obey the same admitted bare constraints. Therefore the bare algebra does
not select the symmetric tensor response as the unique admissible response.

## Theorem 3: What Would Close B3

B3 would be closed by deriving the missing primitive above in any equivalent
form:

1. a defect-to-coframe map showing that local translation defects are one
   coframe/metric variable rather than independent scalar, antisymmetric, or
   other retained channels;
2. a continuous local redundancy acting on that variable, not merely the finite
   signed-permutation symmetry of the flat cell;
3. a Ward identity from that redundancy forcing the source to be symmetric and
   conserved.

These are not extra names for an already assumed "geometric sector"; they are
the specific structure absent from the retained `Cl(3)` / `Z^3` primitives.

## Consequence

The B3 status is sharply reduced but not closed:

- **closed:** native flat edge-Clifford soldering and induced flat cell metric;
- **reduced:** the missing item is exactly the local gaugeable
  defect-to-coframe response primitive;
- **open:** a derivation of that primitive from retained `Cl(3)` / `Z^3` alone.

## Safe Claim

Use:

> Retained `Cl(3)` / `Z^3` derives the flat edge-Clifford frame but does not
> derive the local gaugeable defect-to-coframe response primitive. B3 is reduced
> to deriving that primitive, or equivalently the conserved symmetric spin-2
> Ward identity, from the bare retained algebra.

Do not use:

> A fixed flat edge-Clifford frame already implies a dynamical metric/coframe
> response.

Do not use:

> Finite cubic frame symmetry alone gives a conserved symmetric spin-2 Ward
> identity.
