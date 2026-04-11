# Field Equation Derivation — Variational Argument

**Date:** 2026-04-11

## The Problem

The screened Poisson equation (L + μ²)Φ = G·ρ was chosen by convention.
Four alternatives (bare Laplacian, biharmonic, heat kernel) all pass the
same consistency tests. Is the field equation a free parameter?

## The Variational Argument

The total action for the coupled matter-field system on a graph is:

    S = S_matter[ψ] + S_field[Φ] + S_coupling[ψ, Φ]

where the matter action is fixed by the staggered Dirac structure and
the coupling is fixed by the parity prescription (m + Φ)·ε(x).

The simplest local quadratic field action on a graph is:

    S_field = (1/2) Σ_edges w_ij (Φ_i − Φ_j)² + (μ²/2) Σ_nodes Φ_i² − G Σ_nodes ρ_i Φ_i

The first term is the graph gradient energy (penalizes spatial variation).
The second is the mass term (penalizes large field values).
The third is the source coupling.

Extremizing δS_field/δΦ_i = 0 gives:

    Σ_j w_ij (Φ_i − Φ_j) + μ² Φ_i = G ρ_i

which in matrix form is exactly:

    (L + μ²I) Φ = G ρ

The screened Poisson equation is the Euler-Lagrange equation of the
simplest local quadratic graph field action.

## What This Means

The field equation is NOT "chosen by convention." It is DERIVED from
the requirement that the field-matter system is at a stationary point
of the combined action, under the constraint that the field action is:

1. **Local** — involves only nearest-neighbor differences (the graph gradient)
2. **Quadratic** — leading-order field theory (no self-interaction)
3. **Positive-definite** — the field has a unique minimum (stability)

Any other choice (biharmonic, heat kernel, etc.) corresponds to a
DIFFERENT field action with higher-order terms or non-local structure.
The screened Poisson equation is the unique lowest-order local field
equation on the graph.

## What Remains Free

- **G** (coupling constant) — analogous to Newton's G_N
- **μ** (screening mass) — analogous to the Compton wavelength of the
  graviton; sets the range of the gravitational interaction
- **The graph itself** — which bipartite graph is not predicted

These are free parameters, like coupling constants in any field theory.
Having free coupling constants is standard physics, not a weakness.

## Connection to Einstein's Equation

The graph Laplacian L is the discrete analog of the spatial Laplacian ∇².
In the weak-field (linearized) limit, Einstein's equation reduces to:

    ∇²Φ = 4πG ρ

which on the graph becomes L Φ = G ρ. The screened version (L + μ²)Φ = G ρ
corresponds to massive gravity (Yukawa-type potential with range 1/μ).

So the field equation on the graph IS the linearized Einstein equation
with a mass term. The static lattice corresponds to the linearized-gravity
limit where the metric perturbation Φ is small compared to the background.
