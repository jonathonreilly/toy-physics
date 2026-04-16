# Plaquette Self-Consistency: `<P>` as a Derived Same-Surface Constant

**Date:** 2026-04-15  
**Status:** retained same-surface law + evaluation theorem (no free parameter)  
**Script:** `scripts/frontier_plaquette_self_consistency.py`

## Claim

The plaquette expectation

`<P>(beta = 6, SU(3), 3+1) ~= 0.5934`

is a uniquely determined observable of the axiom-defined partition function on
the retained graph-first `SU(3)` Wilson-plaquette evaluation surface. It is not
a fit parameter and it is not an experimental import.

The exact finite-`beta` law is now also known on that same finite periodic
surface: `docs/CHARACTER_INTERTWINER_FOAM_LAW_NOTE.md` derives `<P>` as an
exact absolutely convergent `SU(3)` character/intertwiner foam ratio.
`docs/POISSONIZED_OCCUPATION_INTERTWINER_COMPRESSION_NOTE.md` then rewrites
that exact infinite-carrier law as an exact Poissonized plaquette
occupation/intertwiner law with finite local alphabets after truncation and
explicit normalized-law tail bounds.

Computing the number still requires non-perturbative evaluation of that exact
law. That is evaluation of a derived quantity, not introduction of a free
degree of freedom.

## Why This Matters

The current quantitative stack uses the canonical plaquette chain

`<P> -> u_0 = <P>^(1/4) -> alpha_s(v) = alpha_bare / u_0^2`

and then reuses `u_0`, `alpha_s(v)`, and downstream quantities across the
hierarchy, EW, CKM, confinement, Yukawa, and Higgs lanes.

The review-safe point is:

- `<P>` is not an externally chosen knob
- `<P>` is not a hidden fit parameter
- `<P>` is an analytically derived same-surface observable of the retained
  theory

## Argument

### 1. The partition function is well-defined

On the retained graph-first gauge surface:

- the gauge group is `SU(3)`
- the Wilson plaquette action at `g_bare^2 = 1` gives `beta = 2 N_c / g^2 = 6`
- the finite periodic lattice gives a finite product of compact Haar integrals

So

`Z(beta) = integral DU exp(-S_W[U])`

is finite and well-defined.

### 2. The plaquette is a unique observable

The average plaquette is

`<P> = (1 / N_plaq) d(ln Z) / d beta`.

Since `Z(beta)` is well-defined, `<P>` is a unique observable of the same
partition function. There is no independent freedom to choose it.

On the retained finite periodic `3+1` surface, the partition function and
anchored plaquette numerator also admit exact absolutely convergent
character/intertwiner foam sums, so the observable now has an explicit analytic
representation rather than only an implicit integral definition.

### 3. No phase-transition ambiguity is present at `beta = 6` on symmetric `L^4`

The deconfining transition in `SU(3)` lattice gauge theory is a finite-
temperature transition on asymmetric lattices, not a bulk transition on
symmetric `L^4` lattices. So the plaquette on the symmetric `L^4` surface is
the smooth same-phase observable that the framework actually uses.

### 4. Monte Carlo evaluates the exact same-surface law; it does not parameterize it

Monte Carlo is the numerical evaluation method for this partition-function
expectation value, exactly as numerical quadrature evaluates an analytically
defined integral or an exact convergent series. The computation is
non-perturbative, but the quantity is still framework-derived.

## Verification Surface

The runner checks:

1. self-consistency of the uniqueness argument
2. multi-volume plaquette convergence at `beta = 6`
3. smooth monotone `beta`-dependence on a symmetric lattice
4. perturbative-window sanity checks
5. downstream consistency of `u_0` and `alpha_s(v)`

## Safe Reuse Rule

Downstream lanes may safely treat the following as canonical same-surface
evaluated quantities:

- `<P> = 0.5934`
- `u_0 = <P>^(1/4)`
- `alpha_s(v) = alpha_bare / u_0^2`

with the understanding that the number is:

- not structural in the same sense as an exact symmetry theorem
- not imported from experiment
- not a free parameter

## Scope

This note does **not** claim a compact closed-form analytic expression for
`<P>`.

It claims the narrower and sufficient point needed by the package:

> the plaquette is a uniquely determined observable of the retained theory,
> it now has an exact finite-periodic-lattice character/intertwiner foam law on
> that same surface, and Monte Carlo is same-surface evaluation of that
> observable rather than parameter fitting.
