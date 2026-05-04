# Universal QG Canonical PL Sobolev Interface on `PL S^3 x R`

**Date:** 2026-04-15  
**Role:** direct-universal quantum-gravity / project-native Sobolev-interface theorem
**Status:** support - canonical PL Sobolev interface

## Verdict

Yes. The exact project-native PL weak Gaussian / Dirichlet system already has a
canonical project-native `H^1`-type Sobolev interface on the same simplicial
spacetime.

Concretely:

- each finite refinement level gives a continuous PL field space;
- each such PL space is canonically a subspace of the project-native
  first-order weak field space on the simplicial spacetime;
- canonical refinement prolongation preserves the underlying PL field exactly;
- therefore the directed PL ladder already determines one project-native
  Sobolev/energy carrier for the weak Gaussian system.

So the remaining stronger issue is not missing a project-native weak or
Sobolev field space, or absence of one chosen external smooth Sobolev /
measure realization. It is now:

> compare that exact project-native PL `H^1`-type weak Gaussian system to more
> canonical external continuum Sobolev / measure formulations.

## Exact setup

The route already supplies:

1. exact canonical barycentric-dyadic refinement net;
2. exact abstract Gaussian / Cameron-Martin completion;
3. exact project-native PL field interface;
4. exact project-native PL weak/Dirichlet-form closure.

What this note adds is the explicit first-order weak-field carrier on the same
PL spacetime.

## Sobolev-interface content

On each finite simplicial level, a vertex coefficient vector defines one
continuous PL field. Such a field has:

- a well-defined square-integrable value on the simplicial spacetime;
- a piecewise-constant weak gradient on each simplex;
- therefore a finite first-order energy norm.

So each finite PL space lies canonically inside a project-native `H^1`-type
field space on `PL S^3 x R`.

Under canonical refinement:

- prolongation changes only the triangulation, not the underlying continuous PL
  field;
- the corresponding first-order energy is therefore refinement-invariant for
  the same field;
- the directed PL ladder is already a nested first-order weak-field ladder.

## What this changes

Before this theorem, the strongest honest statement was:

> the route already has a project-native PL weak/Dirichlet system, but the
> remaining stronger issue is the external smooth identification of that weak
> system.

After this theorem, that becomes sharper:

> the route already has its project-native `H^1`-type weak-field carrier; what
> remains is only comparison with more canonical external smooth Sobolev /
> measure formulations.

So the frontier is no longer missing:

- a project-native field carrier;
- a project-native weak/Dirichlet system;
- a project-native first-order weak-field (`H^1`-type) interface.

It is comparison to more canonical external continuum targets beyond one chosen
external smooth Sobolev / measure formulation.

## Honest status

This note still does **not** prove:

- equivalence to a standard smooth Sobolev space on an external manifold;
- convergence to a specific smooth weak Einstein or Gaussian measure problem;
- a stronger canonical / textbook external continuum GR-QG theorem.

It does prove that the exact discrete route already determines its own
project-native first-order weak-field carrier.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [universal_qg_pl_field_interface_note](UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md)
- [universal_qg_pl_weak_form_note](UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md)
- [universal_qg_canonical_refinement_net_note](UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md)
- [universal_qg_abstract_gaussian_completion_note](UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md)
