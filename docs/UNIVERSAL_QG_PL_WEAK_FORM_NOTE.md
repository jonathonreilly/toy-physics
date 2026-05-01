# Universal QG Canonical PL Weak-Form Closure on `PL S^3 x R`

**Date:** 2026-04-15  
**Role:** direct-universal quantum-gravity / project-native weak-form theorem
**Status:** support - canonical PL weak-form closure

## Verdict

Yes. The exact project-native PL Gaussian completion already carries a
canonical coercive weak/Dirichlet form and exact stationary weak equation on
the canonical barycentric-dyadic refinement net.

Concretely:

- each finite refinement level carries a symmetric coercive bilinear form
  `a_(n,m)` and source functional `ℓ_(n,m)` on the PL field space;
- the weak stationary problem

  `a_(n,m)(u_(n,m), v) = ℓ_(n,m)(v)` for all test fields `v`

  is exactly the same stationary equation as the discrete Gaussian/GR route;
- under exact Schur coarse-graining, the induced weak form on the coarse PL
  space is exactly the coarse weak form again;
- therefore the PL ladder is already an exact project-native weak-form system.

So the remaining stronger issue is no longer missing variational or weak-form
structure on the project route, or absence of one chosen external smooth
weak-field / measure realization. It is now:

> compare that exact project-native PL weak Gaussian/Dirichlet system to more
> canonical external continuum weak-field / measure formulations.

## Exact setup

The route already supplies:

1. exact UV-finite partition-density family with local quadratic operator
   `K`;
2. exact Schur/projective coarse-graining closure;
3. exact canonical barycentric-dyadic refinement net;
4. exact abstract Gaussian / Cameron-Martin completion;
5. exact project-native PL field realization.

At each finite level, coefficient vectors on the PL field space determine one
quadratic action

`I(u) = 1/2 a(u,u) - ℓ(u)`

with

`a(u,v) := <u, K v>`,
`ℓ(v) := <J, v>`.

Because the route is symmetric positive definite on the positive-background
sector, `a` is coercive.

## Weak-form content

The stationary equation `K u_* = J` is equivalent to the exact weak problem

`a(u_*, v) = ℓ(v)` for every test field `v`.

Under admissible coarse/fine splitting:

- Schur reduction gives the exact coarse operator `K_eff`;
- the induced coarse bilinear form is

  `a_eff(u,v) := <u, K_eff v>`;
- the induced coarse source is

  `ℓ_eff(v) := <J_eff, v>`;
- the coarse stationary solution is exactly the projected fine stationary
  solution.

So the projective Schur theorem is already a weak-form compatibility theorem on
the project-native PL field ladder.

## What this changes

Before this theorem, the strongest honest statement was:

> the route has an exact project-native PL Gaussian completion, but the
> remaining stronger continuum question is still smooth / external
> identification.

After this theorem, that becomes sharper:

> the route already has its exact project-native PL weak/Dirichlet-form
> structure and stationary weak equation; what remains is only the external
> smooth identification of that weak system.

So the frontier is no longer missing:

- a project-native field carrier;
- a project-native Gaussian limit object;
- a project-native weak variational structure.

It is comparison to more canonical external continuum targets beyond one chosen
external smooth weak-field / measure formulation.

## Honest status

This note still does **not** prove:

- equivalence to a specific smooth Sobolev weak formulation;
- convergence to a particular external differential operator;
- a stronger canonical / textbook external continuum GR-QG theorem.

It does prove that the exact discrete route already determines its own
project-native PL weak Gaussian / Dirichlet system.
