# Cosmological Expansion from Graph Growth Rules

**Date:** 2026-04-11
**Status:** review hold; growth-proxy study

## One-line read

Graph growth rules produce measurable expansion histories in the chosen
graph-distance proxy. Exponential node-addition gives a de Sitter-like signal
on its own growth clock, but no tested rule produces matter- or
radiation-dominated expansion at `N = 300`.

## Primary artifact

Script:

- `scripts/frontier_cosmological_expansion.py`

## What it tests

If the universe is a graph, cosmic expansion means the graph is growing.
Different node-attachment rules should produce different expansion histories
analogous to Friedmann solutions. The Friedmann equation H^2 = (8piG/3)rho
relates the Hubble rate to energy density. On a growing graph, the scale
factor proxy is the average graph distance between nodes.

Four growth rules are tested:

1. **Uniform random** -- each new node connects to k random existing nodes
2. **Preferential attachment** -- connection probability proportional to degree
3. **Spatial attachment** -- nodes placed in R^3, connect to k nearest neighbors
4. **Exponential** -- node addition rate proportional to current N (de Sitter analog)

For each rule, the script tracks N(t), spectral dimension, average graph
distance (scale factor proxy), and random-walk mean-squared displacement.

A separate gravity-survival test checks whether the two-body gravitational
attraction (from the staggered fermion framework) persists on growing-graph
snapshots at different sizes.

## Key findings

### Expansion histories

| Rule | a(t) power-law alpha | R^2_pow | H_exp | R^2_exp | H_cv | Best fit |
|------|---------------------|---------|-------|---------|------|----------|
| Uniform random | 0.060 | 0.83 | 0.0012 | 0.91 | 1.17 | weak de Sitter |
| Preferential | 0.060 | 0.86 | 0.0011 | 0.89 | 1.38 | novel t^0.06 |
| Spatial | 0.101 | 0.82 | 0.0020 | 0.94 | 0.99 | weak de Sitter |
| Exponential | 0.062 | 0.80 | 0.0042 | 0.998 | 0.09 | de Sitter |

The exponential growth rule (N grows as exp(Ht)) produces a clean de Sitter
expansion in the scale factor, with nearly constant Hubble parameter
(coefficient of variation 0.09). This is expected by construction: if N grows
exponentially and average distance grows logarithmically with N, the scale
factor grows exponentially in time.

No growth rule produces matter-dominated (a ~ t^{2/3}) or radiation-dominated
(a ~ t^{1/2}) expansion. All power-law exponents are much smaller than 0.5.
This suggests that decelerated expansion requires a mechanism beyond simple
node addition -- perhaps edge deletion, dimensional reduction, or
energy-density feedback on growth rate.

### Spectral dimension

All rules show d_s ~ 0.2-0.6 and decreasing with growth. This is far below
the expected d_s ~ 4 for a 4D manifold. The small spectral dimension is a
known finite-size artifact at N=300 with only 10 eigenvalues. The decreasing
trend likely reflects the small-world effect: as the graph grows, average
distances grow slowly (logarithmically), compressing the effective dimension.

### Gravity survival

Gravitational attraction (positive force between two wavepackets) survives on
all four growing-graph snapshots tested (N=40, 80, 150, 250). The screened
Poisson mechanism that generates attraction on static graphs continues to work
on graph snapshots taken during growth.

## Bounded claims

**C1** (supported): Graph growth produces measurable expansion histories with
well-defined scale factor a(t) and Hubble parameter H(t). The measurement
framework works.

**C2** (partially supported): exponential node-addition gives a de Sitter-like
signal in this proxy, but that result is partly tautological and the rules are
not compared on a common time coordinate. No tested rule produces matter or
radiation domination.

**C3** (supported): Gravitational attraction survives on growing-graph
snapshots (4/4 pass). The force law does not break when the background
geometry is expanding.

## Limitations

- Small graphs (N=300) severely limit continuum-limit claims
- Scale factor proxy (average graph distance) is not unique; diameter or
  spectral radius could give different results
- Spectral dimension estimates are unreliable at this scale
- The gravity test uses small separations (graph distance 2) due to the
  small-world property of dense random graphs
- No backreaction of matter content on growth rate (the Friedmann equation
  couples expansion to energy density; here growth rules are imposed)
- The exponential de Sitter result is partially tautological: we impose
  exponential growth and measure exponential expansion
- The non-exponential and exponential rules do not share a common clock in the
  current implementation, so cross-rule Friedmann comparisons remain provisional

## What would strengthen this

1. **Backreaction**: growth rate that depends on energy density on the graph
   (mimicking the Friedmann equation directly)
2. **Larger graphs** (N > 10^4) to get reliable spectral dimension and
   approach continuum behavior
3. **Edge deletion** or rewiring rules that could produce deceleration
4. **Multiple scale-factor proxies** compared for consistency
5. **Connection to the Regge calculus** or causal dynamical triangulations
   literature for comparison with established discrete-gravity results
