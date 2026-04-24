# Planck-Scale Edge-Clifford Kinematic Soldering Theorem

**Date:** 2026-04-24
**Status:** B3 sub-lock closure; kinematic soldering only, not gravity closure
**Verifier:** `scripts/frontier_planck_edge_clifford_kinematic_soldering_theorem.py`

## Question

Does retained `Cl(3)` / `Z^3` at least derive the soldering of primitive
translation directions to a local metric/coframe carrier?

## Result

Yes, at the kinematic flat-cell level.

The retained lattice/taste algebra supplies:

1. three primitive `Z^3` one-step translation axes;
2. three exact cube-shift / staggered phase operators;
3. three Clifford generators `Gamma_i` satisfying

   `{Gamma_i, Gamma_j} = 2 delta_ij I`;

4. the exact site-phase / cube-shift intertwiner between lattice BZ-corner
   modes and the abstract taste cube.

Therefore the primitive edge directions are canonically soldered to Clifford
vectors:

`edge_i <-> Gamma_i`.

The induced flat spatial metric is

`g_ij = (1/2) Tr_norm(Gamma_i Gamma_j + Gamma_j Gamma_i) = delta_ij`.

With the already derived time-lock, this gives the kinematic `3+1` coframe
surface.

## What This Closes

This closes a real subpart of B3:

> the retained `Cl(3)` / `Z^3` package does not need an external choice of a
> flat tangent frame; the primitive translation axes and the Clifford vector
> frame are already soldered on the retained cell.

So the missing B3 primitive is no longer "derive any soldering at all." The
flat-cell soldering is native.

## What This Does Not Close

This does **not** derive the gravitational sector.

The theorem supplies a fixed kinematic coframe on the primitive flat cell. It
does not yet derive:

1. local coframe variability;
2. equivalence between local translation defects and metric/coframe
   deformations;
3. a conserved symmetric stress-response Ward identity;
4. the massless spin-2 self-coupling identity;
5. the Einstein/Regge action as a bare-algebra consequence.

Thus B3 remains open after this theorem. The remaining object-class theorem is
sharper:

> promote native flat edge-Clifford soldering to a dynamical local
> metric/coframe response with the conserved symmetric spin-2 Ward identity.

## Proof Sketch

The retained `Z^3` lattice has three primitive axes. The retained staggered
phase/taste construction gives three Clifford generators. The native gauge
closure note verifies the exact Clifford relation

`{Gamma_i, Gamma_j} = 2 delta_ij I`.

The site-phase / cube-shift intertwiner verifies that the abstract taste-cube
shifts are not detached presentation choices: they are exactly intertwined
with the BZ-corner subspace of the lattice.

Any automorphism preserving the retained cubic structure can permute axes and
flip orientations, but it cannot replace the edge/Clifford pairing with an
inequivalent metric. The induced metric remains `delta_ij`.

Therefore the flat primitive soldering is canonical up to retained cubic frame
symmetry.

## Consequence For B3

The B3 status becomes:

- **closed:** flat primitive edge-Clifford soldering;
- **open:** dynamical soldered metricity / equivalence Ward identity.

The next theorem cannot merely say "the lattice has a tangent frame." That part
is done. It must show that local translation defects are described by a
dynamical coframe/metric whose response source is symmetric and conserved.

## Safe Claim

Use:

> Retained `Cl(3)` / `Z^3` derives the flat primitive edge-Clifford soldering
> `edge_i <-> Gamma_i` and the induced local metric `delta_ij`. B3 now needs the
> dynamical upgrade from this flat soldering to a local metric/coframe Ward
> identity.

Do not use:

> Edge-Clifford soldering alone derives Einstein/Regge gravity.
