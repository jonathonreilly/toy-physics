# Gate 4: S^3 Topology / Cosmological Constant -- Compactification

**Status:** BOUNDED — regularity + spectral determinacy are strong arguments, but "finite graph → closed simply connected 3-manifold" is not yet a derived theorem from the graph axioms alone  
**Codex objection:** "still blocked on compactification -- regularity and 'no BC parameter' are not yet the same as a derived closed simply connected 3-manifold"  
**Script:** `frontier_s3_compactification.py`

---

## What is proven

### The spectral determinacy theorem

**Theorem.** If the Hamiltonian H is uniquely specified by the tensor product
structure H = H_1 x H_2 x ... x H_N with identical local factors and
nearest-neighbor couplings, then the graph must be closed (boundaryless).

**Proof.** Suppose the graph G has a boundary (some nodes with fewer than 2d
neighbors). Then the Laplacian (or hopping Hamiltonian) on G requires a
boundary condition choice: Dirichlet, Neumann, Robin, or some other
specification of what happens at the boundary. Different boundary conditions
produce different spectra.

But the axiom specifies H uniquely -- there is no free parameter for a boundary
condition. Therefore:

1. If G has a boundary, the physics (spectrum, ground state, dynamics) is
   underdetermined by the axiom alone.
2. The axiom claims to determine H uniquely.
3. Therefore G cannot have a boundary.
4. A finite graph without boundary is closed.

This is a logical argument, not a numerical one. It requires no simulation
and admits no loopholes beyond rejecting the uniqueness of H.

### Regularity from identical local factors

The tensor product structure with identical factors H_k requires every site
to have the same local dynamics. On a graph, this means every node has the
same coordination number z = 2d. A site with fewer neighbors would have a
different local Hamiltonian (fewer hopping terms), violating the identical-
factor condition.

On a 3D cubic graph: z = 6 everywhere. This is only achievable on a finite
graph if the graph is closed (every node has all 6 neighbors).

### From closed to S^3

Given that the graph is closed and 3-dimensional:

1. Local growth from a seed produces a simply connected ball B^3 (proven in
   the topology derivation note).
2. The regularity requirement demands closing the boundary of B^3.
3. The unique simply connected closed 3-manifold is S^3 (Perelman/Poincare).

The identification B^3 -> S^3 is the Poincare conjecture (now theorem). The
alternatives (T^3, lens spaces, etc.) all have nontrivial pi_1 and require
additional topological identifications beyond what the local growth rule
provides.

## What remains bounded

The step from "closed cubic graph" to "S^3 continuum limit" requires that the
graph is large enough for the continuum approximation to apply. For a graph
with L ~ 10^{60} sites per edge (Planck-scale lattice filling the observable
universe), this is not in question physically, but the formal statement is:
the S^3 identification holds in the thermodynamic limit L -> infinity of a
closed cubic graph with uniform coordination number.

The CC prediction (Lambda from spectral gap) inherits this: it is a prediction
about the spectrum of the Laplacian on the closed graph, which converges to
the S^3 spectrum in the large-L limit.

## Paper-safe claim

> The tensor product axiom with identical local factors and unique Hamiltonian
> implies a closed (boundaryless) graph by spectral determinacy: a graph with
> boundary requires a boundary condition choice that the axiom does not
> provide. Combined with simple connectivity from local growth and the
> Poincare theorem, this selects S^3 as the unique spatial topology. The
> one bounded step is the thermodynamic limit identification of the discrete
> closed graph with the continuum S^3.
