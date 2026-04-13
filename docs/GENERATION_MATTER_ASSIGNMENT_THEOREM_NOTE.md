# Generation Matter Assignment: Canonicality Test

**Date:** 2026-04-12  
**Status:** bounded negative - the orbit algebra is exact, but the canonical matter-assignment theorem is still open
**Script:** `scripts/frontier_generation_matter_assignment_theorem.py`
**Scope:** test whether the current graph/taste surface canonically identifies the two size-3 Z3 orbit classes as physical fermion families

## What is exact

The audited Z3 action on the 8 taste states gives the exact orbit algebra

`8 = 1 + 1 + 3 + 3`.

The two size-3 orbit classes are symmetry-related, and the current surface can
attach useful diagnostics to them:

- gauge-like quantum number distributions after choosing a weak-axis embedding
- toy radiative / coupling proxies after choosing deformation parameters
- a chirality / parity grading from Hamming weight

Those are real diagnostics. They are not yet a canonical generation theorem.

## What is not proven

The following remain open:

- that the orbit classes are canonically physical generations rather than
  symmetry-related model sectors
- that the gauge quantum numbers are intrinsic to the orbit classes rather than
  tied to a chosen weak-axis embedding / commutant presentation
- that the coupling and mass proxies are derived from the graph/taste axiom
  rather than inserted deformation parameters
- that the parity / index proxy is a genuine topological index theorem on the
  graph side, rather than a chirality grading
- that the observed hierarchy follows without an additional Z3-breaking input

The sharp obstruction is not the orbit count. It is that the two triplets are
exchanged by an exact complement symmetry and are isomorphic as Z3
representations.  Any physical-family identification uses extra structure:

- a chosen weak-axis embedding
- a chosen deformation scale
- or an additional symmetry-breaking / index datum

## Paper-safe wording

Use this, not the stronger claim:

> The audited Z3 taste action yields two symmetry-distinct triplet sectors with
> useful model diagnostics, but the canonical identification of those sectors
> with physical fermion generations remains open.  A Z3-breaking hierarchy can
> be discussed only after an additional matter-assignment theorem or topological
> index result is supplied.

## Prior work on this axis

`docs/GENERATION_PHYSICALITY_NOTE.md` shows the orbit algebra and the Wilson
pressure test, but it already stops short of canonical generation closure.

`scripts/frontier_generation_physicality.py` and
`scripts/frontier_generations_rigorous.py` establish the exact orbit structure
and several model diagnostics, but they also leave the matter assignment open.

This note sharpens that boundary:

- exact orbit algebra: retained
- canonical physical-generation identification: open
- hierarchy language: allowed only as a conditional, Z3-breaking follow-on
