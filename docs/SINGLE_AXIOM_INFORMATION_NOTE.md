# Single Axiom: Conserved Information Flow Unifies Graph + Unitarity

**Date:** 2026-04-12
**Status:** confirmed (all four tests pass)
**Runner:** `scripts/frontier_single_axiom_information.py`

**Scope note:** this is a reduction/support note for framework compression and
physical-lattice scoping. It is not the load-bearing accepted input ledger for
the current paper package, whose framework statement remains `Cl(3)` on `Z^3`
with the audited package boundary recorded in
`docs/MINIMAL_AXIOMS_2026-04-11.md`.

**Planck-branch update:** for the Planck-scale branch, this surface is now
explicitly promoted as Axiom Extension P1 for local source-free state semantics;
see
`docs/PLANCK_SCALE_ONE_AXIOM_EXTENSION_ACCEPTANCE_THEOREM_2026-04-23.md`.
This file remains the reduction/support note; the Planck packet's load-bearing
governance move is recorded in that extension theorem.

## The claim

The two axioms of the model (graph substrate + unitary dynamics) are not
independent. They are inseparable aspects of a single axiom:

> "There exist distinguishable things, and information flows between them
> without being created or destroyed."

- "Distinguishable things" gives nodes.
- "Flows between them" gives edges (locality).
- "Without being created or destroyed" gives unitarity.

The mathematical realization: a sparse Hermitian operator H on a finite set.
Its nonzero entries define the graph, its exponentiation exp(iHt) defines
the unitary dynamics, and the Schrodinger equation generates a locally
conserved probability current. These three structures are one object.

## What was tested

### Test 1: Conserved flow derives graph + unitarity

Start with a sparse real symmetric matrix H on N states.

| N  | Unitarity err  | Conservation err | Locality ratio |
|----|---------------|-----------------|----------------|
| 8  | 2.2e-16       | 5.6e-17         | 10.7x          |
| 16 | 2.2e-16       | 1.4e-17         | 20.9x          |
| 32 | 5.6e-16       | 6.9e-18         | 54.4x          |
| 64 | 4.4e-16       | 1.7e-18         | 154.4x         |

- exp(iHt) is unitary to machine precision (Hermitian => unitary).
- The probability current J_ij = 2 Im(psi_i* H_ij psi_j) satisfies
  local conservation to machine precision.
- The unitary U is concentrated on graph edges: the locality ratio
  (mean |U_ij| on-graph vs off-graph) grows with N, reaching 154x at N=64.

One algebraic object H simultaneously defines graph + current + unitary.

### Test 2: Locality is forced

Poisson field on three graph types:

| Graph type          | phi(r) exponent | Clean power law? |
|--------------------|----------------|-----------------|
| 3D cubic lattice    | -1.80          | Yes (finite-size steepened) |
| Complete graph      | flat (0.0)     | No: only 2 distinct values |
| Random Erdos-Renyi  | -1.32          | No: residual 0.83 |

The fully-connected graph has no notion of distance: the Poisson equation
gives a flat potential (all non-source nodes equivalent). Only the
geometrically-local lattice produces a 1/r-like field with attraction.

### Test 3: Unitarity is forced

Dissipative per-hop loss (gamma) applied to the Poisson field:

| gamma | M_eff CV | Effective alpha | Norm at 10 hops |
|-------|----------|----------------|-----------------|
| 0.00  | 0.34     | -1.82          | 1.000           |
| 0.02  | 0.37     | -1.90          | 0.668           |
| 0.05  | 0.41     | -2.02          | 0.358           |
| 0.10  | 0.49     | -2.21          | 0.122           |
| 0.30  | 0.77     | -3.01          | 0.001           |

Dissipation steepens the effective power law from -1.8 toward -3.0 and
doubles the variation of M_eff(r) = phi(r) * r. The "mass seen at distance r"
becomes distance-dependent, breaking beta = 1. Unitarity is required for the
mass law to hold.

### Test 4: (G, U) is irreducible

Three topologies with 64 nodes each:

| Topology    | Bandwidth | Min gap  | P(0->0) | Participation |
|-------------|-----------|----------|---------|---------------|
| 1D chain    | 4.00      | 0.0070   | 0.333   | 2.6 sites     |
| 2D lattice  | 7.52      | 0.0419   | 0.111   | 6.9 sites     |
| 3D lattice  | 9.71      | 0.2361   | 0.037   | 18.0 sites    |

- Pairwise spectral distances: 0.31 to 0.57 (all > 0).
- Adding one weak edge to the 3D lattice shifts the spectrum by 0.009
  and changes the propagator by up to 0.11.
- Fidelity of 1D evolution vs 3D evolution: 0.11 (far from 1.0).
  U from one graph produces wrong physics on another.

The pair (G, U) cannot be factored: changing G changes U, and vice versa.

## The irreducible object

The "graph-unitary" (G, U) is a single mathematical object: a sparse
Hermitian operator H on a finite set S. From H alone:

1. **Graph**: the nonzero pattern of H defines edges.
2. **Unitary**: exp(iHt) is unitary (Hermitian exponentiation).
3. **Current**: J_ij = 2 Im(psi_i* H_ij psi_j) is locally conserved.
4. **Locality**: for small t, U inherits H's sparsity.
5. **Physics**: the spectrum of H determines all physical observables.

You cannot have unitarity without a substrate (the graph defines H's
support), and a graph without dynamics is inert (H = 0 gives U = I).
The two axioms are two faces of the same coin.

## What this is

A numerical demonstration that "conserved information flow on a network"
is a single axiom that simultaneously produces:
- A graph (from the flow's support)
- Unitary dynamics (from conservation + Hermiticity)
- Locality (from sparsity, required for self-consistent physics)

The four tests confirm that removing any component (the graph, the
unitarity, or the coupling between them) breaks the physics.

## What this is not

- This is not a proof that H must be sparse (locality is tested
  empirically, not derived from first principles here).
- The finite-size steepening of alpha (-1.8 at N=24 vs -1.0 at N->inf)
  is a known lattice artifact, not a failure of the argument.
- The construction assumes finite-dimensional Hilbert space. Extension
  to infinite dimensions requires additional care.
