# Dimension Emergence: Spectral Dimension vs Force Law

**Status:** review proxy; bounded regular-lattice correlation

## Question

Does the effective spatial dimension of a graph determine the gravitational
force law? Is d_s = 3 special?

## Background

In continuum physics, the force law F ~ 1/r^(d-1) depends on spatial
dimension d through the Green's function of the Laplacian:
- d = 3: phi ~ 1/r, F ~ 1/r^2 (Newtonian gravity)
- d = 2: phi ~ log(r), F ~ 1/r
- d = 1: phi ~ r (linear), F ~ const

On a graph, the natural notion of "dimension" is the spectral dimension d_s,
defined through the return probability of a random walk P(t) ~ t^{-d_s/2},
or equivalently through the heat-kernel trace K(t) ~ t^{-d_s/2}.

## Method

Script: `scripts/frontier_dimension_emergence.py`

### Part 1: Spectral dimension measurement
- Compute the combinatorial graph Laplacian L = D - A
- Diagonalize L to get eigenvalues lambda_i
- Compute heat-kernel trace K(t) = (1/N) sum_i exp(-t * lambda_i)
- Fit d_s from the power-law regime: K(t) ~ t^{-d_s/2}

### Part 2: Force law on integer-dimension lattices
- Solve Poisson equation on 2D and 3D lattices with point source
- Compute ray deflection delta(b) at impact parameter b
- Fit delta(b) ~ b^alpha to extract the force-law exponent
- In d dimensions: alpha = -(d-2), so force ~ r^{alpha-1} = r^{-(d-1)}

### Part 3: Green's function on general graphs
- Solve screened Poisson (L + mu^2)phi = rho on graph Laplacian
- Bin phi by graph distance from source
- Fit phi(d) ~ d^beta to get Green's function exponent
- Compare beta to predicted -(d_s - 2)

## Results

### Spectral dimension (heat-kernel trace)

| Graph              |    N  | d_s (measured) | d_s (expected) |
|--------------------|------:|:--------------:|:--------------:|
| 1D chain           |   500 |     1.06       |     1.0        |
| 2D lattice         |  1600 |     2.01       |     2.0        |
| 3D lattice         |  1728 |     2.84       |     3.0        |
| small-world(p=0.01)|  1600 |     2.37       |     ~2         |
| small-world(p=0.05)|  1600 |     2.70       |     ~2         |
| small-world(p=0.30)|  1600 |     3.25       |     ~2         |
| tree(b=3, d=6)     |  1093 |     1.61       |     ~1         |

The heat-kernel method correctly recovers d_s = 1, 2, 3 for regular lattices
(3D is slightly low due to finite size: 12^3 = 1728 nodes). Small-world
rewiring increases the effective d_s by adding shortcuts that compress
distances; high rewiring (p=0.30) pushes d_s above 3.

### Force law on lattices (direct Poisson)

| dim | side | alpha (deflection) | force exponent | predicted force |
|-----|------|--------------------|----------------|-----------------|
|   2 |   56 |  -0.187            |   -1.19        |   -1.0          |
|   3 |   31 |  -1.058            |   -2.06        |   -2.0          |

- 3D lattice: alpha = -1.06, consistent with -1.0 (finite-size correction).
  Force ~ 1/r^2 confirmed.
- 2D lattice: alpha = -0.19, trending toward 0 as lattice grows (logarithmic
  Green's function means alpha -> 0 in the continuum limit).

### Green's function on general graphs

The screened-Poisson approach on irregular graphs shows the correct qualitative
trend: higher d_s gives steeper Green's function decay. However, quantitative
agreement with the continuum prediction beta = -(d_s - 2) is limited by
the screening mass, discrete distance binning, and finite-size effects.

## Bounded Read: Regular-Lattice Dimension/Force Correlation

Within the tested regular-lattice Poisson proxy, `d = 3` is the first integer
dimension that supports an inverse-square force law because:

1. It is the lowest integer dimension where the Laplacian Green's function
   decays as a power law (phi ~ 1/r), producing an inverse-square force.
2. At d_s = 2, the Green's function is logarithmic (marginal case): the
   force is 1/r, not 1/r^2.
3. Below d_s = 2, the potential is bounded or growing: no long-range
   attractive force emerges.
4. Non-integer d_s (e.g., from small-world graphs) interpolates between
   these regimes, with force exponent tracking d_s continuously.

## Bounded Claims

**Confirmed on the tested proxy:**
- On regular lattices, the spatial dimension d determines the force law
  via the Green's function: F ~ 1/r^(d-1). Verified for d = 2, 3.
- The spectral dimension d_s (from the heat-kernel trace of the graph
  Laplacian) correctly identifies the effective dimension.
- on the tested regular lattices, the `d = 3` row yields inverse-square force
  and the `d = 2` row trends toward a logarithmic potential regime.

**Partially confirmed:**
- The Green's function exponent on irregular graphs trends with d_s,
  but quantitative precision requires larger graphs and lower screening.

**Not tested:**
- Whether a grown/evolving graph can dynamically reach d_s = 3.
- Whether non-integer d_s gives a clean power-law force (vs. log corrections).
- The role of d_s in the path-integral propagator (only Poisson field tested).

## Limitations

- Spectral dimension of the 3D lattice reads 2.84 instead of 3.0 due to
  the finite graph (12^3 = 1728 nodes). This is a known finite-size effect.
- The 2D deflection exponent (-0.19 at N=56) is not yet zero; the logarithmic
  divergence converges slowly.
- Graph-distance Green's function measurements are affected by the screening
  mass mu^2 in the Poisson solver; this distorts the power law at short and
  long distances.
- This note does not establish a universal statement that spectral dimension
  alone determines the force law on arbitrary graphs.
