# Architecture Portability Sweep

**Primary runner:** [`scripts/frontier_architecture_portability_sweep.py`](../scripts/frontier_architecture_portability_sweep.py)

## Purpose

Assess source-mass portability for the key retained observables:
mass exponent beta, gravitational attraction sign, and Born rule I_3.

## Architectures tested

| # | Architecture | Topology | Hamiltonian type |
|---|---|---|---|
| 1 | Ordered 3D cubic | Regular, side=14 | Scalar Schrodinger, real hopping |
| 2 | Staggered 3D cubic | Regular, side=14 | Parity-alternating mass, anti-Hermitian hopping |
| 3 | Wilson 3D cubic | Regular, side=14 | Wilson fermion (mass + Wilson term) |
| 4 | Random geometric (2D, mass-only) | Irregular 2D, n=100 | Scalar Schrodinger, distance-weighted hopping |

## Protocol

For each architecture:

1. Place a static Gaussian source at the lattice center
2. Solve the screened Poisson equation for the gravitational potential
3. Place a normalized test packet at distance d from the source
4. Evolve via Crank-Nicolson (or matrix exponential for Wilson) for 15 steps
5. Subtract free-evolution control to isolate gravitational displacement
6. Vary source amplitude across 5 values: A = 0.4, 0.6, 0.8, 1.0, 1.5
7. Fit |displacement| vs source mass to extract mass exponent beta

Born rule I_3 measured via Sorkin inclusion-exclusion on ordered and staggered
lattices (3-slit barrier configuration, side=12).

## Results

| Architecture | beta | R^2 | Attractive | I_3 |
|---|---|---|---|---|
| Ordered 3D | 1.0001 | 1.0000 | Yes (5/5) | 2.3e-09 |
| Staggered 3D | 1.013 | 1.0000 | Yes (5/5) | 2.2e-11 |
| Wilson 3D | 1.001 | 1.0000 | Yes (5/5) | n/a |
| Random geometric | 0.999 | 1.0000 | Yes (5/5) | n/a |

## Acceptance gate

- beta within 10% of 1.0: **4/4 PASS**
- Attractive force: **4/4 PASS**
- Born rule I_3 < 1e-6: **all measured PASS**
- Overall: **PASS**

## Boundary

- This is a portability companion, not a standalone Newton closure.
- It demonstrates architecture portability of source-mass scaling and
  attraction sign across ordered 3D cubic, staggered 3D cubic, Wilson 3D
  cubic, and a 2D random geometric control row.
- Lattice sizes are small (side 10-14) for tractability; finite-size effects
  contribute to the I_3 floor (~1e-9 on ordered vs ~1e-11 on staggered).
- The random geometric architecture is 2D (n=100), not 3D, so the distance
  law exponent is not directly comparable. Only mass scaling is tested there.
- Wilson Born rule is not measured because the Wilson Hamiltonian requires
  a different barrier implementation; the mass law and attraction are sufficient
  for the portability claim.
- The mass exponent beta measures deflection proportional to source mass
  (F proportional to M), not the full Newton law F = GMm/r^2 which requires
  both-masses and distance-law closure on each architecture separately.
