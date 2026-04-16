# Plaquette Self-Consistency: `<P>` as a Derived Same-Surface Constant

**Date:** 2026-04-15  
**Status:** retained evaluation theorem (no free parameter), with analytic support stack
**Script:** `scripts/frontier_plaquette_self_consistency.py`

## Claim

The plaquette expectation

`<P>(beta = 6, SU(3), 4D) ~= 0.5934`

is a uniquely determined observable of the axiom-defined partition function on
the retained graph-first `SU(3)` Wilson-plaquette evaluation surface. It is not
a fit parameter and it is not an experimental import.

Computing the number requires non-perturbative evaluation. That is evaluation
of a derived quantity, not introduction of a free degree of freedom.

## Why This Matters

The current quantitative stack uses the canonical plaquette chain

`<P> -> u_0 = <P>^(1/4) -> alpha_s(v) = alpha_bare / u_0^2`

and then reuses `u_0`, `alpha_s(v)`, and downstream quantities across the
hierarchy, EW, CKM, confinement, Yukawa, and Higgs lanes.

The review-safe point is:

- `<P>` is not an externally chosen knob
- `<P>` is not a hidden fit parameter
- `<P>` is a same-surface evaluated observable of the retained theory

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

### 3. No phase-transition ambiguity is present at `beta = 6` on symmetric `L^4`

The deconfining transition in `SU(3)` lattice gauge theory is a finite-
temperature transition on asymmetric lattices, not a bulk transition on
symmetric `L^4` lattices. So the plaquette on the symmetric `L^4` surface is
the smooth same-phase observable that the framework actually uses.

### 4. Monte Carlo evaluates the observable; it does not parameterize it

Monte Carlo is the numerical evaluation method for this partition-function
expectation value, exactly as numerical quadrature evaluates an analytically
defined integral. The computation is non-perturbative, but the quantity is
still framework-derived.

## Verification Surface

The runner checks:

1. self-consistency of the uniqueness argument
2. multi-volume plaquette convergence at `beta = 6`
3. smooth monotone `beta`-dependence on a symmetric lattice
4. perturbative-window sanity checks
5. downstream consistency of `u_0` and `alpha_s(v)`

## Analytic support stack on `main`

The live repo now also carries a stronger analytic support package:

- exact local `SU(3)` one-plaquette block
- exact scalar `3+1` bridge endpoint ratio
  `A_inf / A_2 = 2 / sqrt(3)`
- exact `3+1` plaquette/link incidence factor `6 / 4 = 3 / 2`

Combined with the bridge-conditioned dimension-4 scalar-density insertion
candidate

`Gamma_sc,cand = (2 / sqrt(3))^(1/4)`,

these give the analytic plaquette candidate

`P_cand(6) = 0.593530679977098`.

This sits only `1.3068e-4` (`0.022%`) above the canonical same-surface value
`0.5934`, so it materially strengthens the plaquette lane.

Current authorities for that support stack:

- [GAUGE_VACUUM_PLAQUETTE_ANALYTIC_SUPPORT_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_ANALYTIC_SUPPORT_NOTE.md)
- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](./SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)

Current support runners:

- `scripts/frontier_gauge_vacuum_plaquette_analytic_support.py`
- `scripts/frontier_scalar_3plus1_temporal_ratio.py`

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

This note does **not** claim a closed-form analytic expression for `<P>`.

The remaining missing theorem is the final local-to-vacuum insertion:

> why the physical gauge-vacuum plaquette must inherit the scalar `3+1` bridge
> as its unique observable-level completion.

It claims the narrower and sufficient point needed by the package:

> the plaquette is a uniquely determined observable of the retained theory, and
> Monte Carlo is same-surface evaluation of that observable rather than
> parameter fitting.
