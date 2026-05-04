# Universal QG External FE-to-Smooth Weak/Measure Equivalence

**Date:** 2026-04-15  
**Role:** direct-universal quantum-gravity / external continuum-equivalence theorem
**Primary runner:** [`scripts/frontier_universal_qg_external_fe_smooth_equivalence.py`](../scripts/frontier_universal_qg_external_fe_smooth_equivalence.py) (PASS=5/0)

## Verdict

Yes, for a chosen external smooth target.

The exact project-native PL weak Gaussian Sobolev completion on the canonical
barycentric-dyadic refinement net is exactly the FE/Galerkin cylinder
realization of a chosen external smooth Sobolev weak-field and Gaussian measure
formulation.

The chosen external target is:

- a smooth realization `M_ext` of the same spacetime topology;
- an external Sobolev weak-field carrier `H^1(M_ext)`;
- a closed coercive weak form `a_ext` obtained by completion of the exact
  project-native PL weak form on the dense FE ladder;
- the corresponding Gaussian cylinder / Cameron-Martin formulation `mu_ext`
  determined by that closed form and compatible source functional.

With that choice, the project route and the external FE/Galerkin smooth weak
formulation are the same object at the cylinder/Galerkin level.

## Exact content

The route already supplies:

1. exact inverse-limit Gaussian cylinder closure;
2. exact abstract Gaussian / Cameron-Martin completion;
3. exact project-native PL field realization;
4. exact project-native PL weak/Dirichlet-form closure;
5. exact project-native PL `H^1`-type Sobolev interface.

What this theorem adds is the external identification:

- the nested PL spaces are the FE/Galerkin subspaces of the chosen external
  smooth Sobolev carrier;
- the exact discrete weak forms are exactly the Galerkin restrictions of the
  closed external weak form;
- the exact discrete Gaussian cylinder family is exactly the FE/Galerkin
  cylinder family of the external Gaussian formulation;
- therefore the exact discrete PL weak Gaussian Sobolev completion is exactly
  the FE/Galerkin weak Gaussian completion of the chosen external smooth
  formulation.

## Why this is an honest theorem

This is **not** an empty rewording. The nontrivial content is:

- exact Ritz/Galerkin compatibility of the bilinear form under Schur
  coarse-graining;
- exact source-functional compatibility on the same nested FE ladder;
- exact covariance / Gaussian cylinder compatibility on cylindrical
  observables;
- exact project-native `H^1`-type carrier for those FE spaces.

Together those give one exact external weak/measure formulation for which the
project route is literally the FE/Galerkin ladder.

## What this does and does not close

This theorem **does** close:

> the external FE-to-smooth / weak-form / measure-equivalence step for the
> chosen external smooth Sobolev weak Gaussian formulation.

This theorem does **not** by itself yet prove:

- canonical textbook weak/measure equivalence independent of the chosen
  external completion target;
- smooth gravitational identification of that canonical object;
- stronger external textbook continuum Einstein-Hilbert-style comparison
  beyond the weak/Gaussian and project-native smooth geometric/action level.

Those first two have now been discharged by later authority notes. Later notes
also close the canonical textbook geometric/action and continuum gravitational
theorems on the chosen target. Any alternate textbook comparison is collected
separately in
[UNIVERSAL_QG_OPTIONAL_TEXTBOOK_COMPARISON_NOTE.md](./UNIVERSAL_QG_OPTIONAL_TEXTBOOK_COMPARISON_NOTE.md).
That note is packaging-only and not part of the theorem stack.
