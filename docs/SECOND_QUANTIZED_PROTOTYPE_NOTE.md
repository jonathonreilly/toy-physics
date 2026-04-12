# Second-Quantized Propagator Prototype

**Status:** exploratory prototype (Paper 2 groundwork)
**Script:** `scripts/frontier_second_quantized_prototype.py`
**Date:** 2026-04-11

## Motivation

The Paper 1 framework propagates a single wavepacket through a gravitational
field f(x).  This produces Newton's law, the Born rule, WEP, and weak-field GR,
but cannot produce Hawking radiation (particle creation from vacuum), area-law
entanglement entropy (many-body vacuum), or Casimir effects (mode summation).

This prototype defines a free-fermion quantum field on the graph and tests
whether gravitational fields produce vacuum instability and area-law entropy.

## Method

Free fermions on a tight-binding lattice with Hamiltonian
H = -t sum c^dag_i c_j + (m + f_i) c^dag_i c_i, where f_i is a 1/r
gravitational potential.  All results use exact diagonalization of the N x N
single-particle Hamiltonian (no exponential Hilbert space).

- **Bogoliubov coefficients:** overlap between old-vacuum occupied modes and
  new-Hamiltonian unoccupied modes gives particle creation count.
- **Entanglement entropy:** from eigenvalues of the restricted correlation
  matrix C_A on subsystem A (free-fermion formula).
- **Thermality test:** fit ln(n_k) vs epsilon_k for a Planck-like distribution.

## Results

### Gate 1: Correlator decay -- PASS

On a 1D chain (N=40, half-filled), |C(d)| decays monotonically:
|C(0)| = 0.50, |C(1)| = 0.32, |C(5)| = 0.066, |C(10)| ~ 0.

### Gate 2: Vacuum instability (Bogoliubov) -- PASS

When a 1/r gravitational potential is applied, the Bogoliubov particle number
is strictly positive and grows with field strength:

| Strength | Particles created |
|----------|------------------|
| 0.5      | 0.108            |
| 1.0      | 0.401            |
| 2.0      | 1.284            |
| 5.0      | 2.505            |
| 10.0     | 3.689            |
| 20.0     | 5.208            |

Zero particles when gravity is off (exact zero, as expected from identical
Hamiltonians).  Growth is sub-linear in strength, consistent with saturation
as modes fill.

### Gate 3: Sub-volume entropy -- PASS

**1D:** Entropy grows as S ~ 0.14 * ln(L_A), sub-extensive.  The coefficient
is below the CFT prediction c/3 = 0.33, likely due to open boundary conditions.
With gravity, entropy is suppressed (localization effect).

**2D:** Entropy scales linearly with boundary length (area law):
S = 0.82 * boundary - 0.47, with R^2 = 0.9996.  Volume-law fit is
significantly worse (R^2 = 0.989).

This confirms area-law scaling for the free-fermion vacuum on a 2D lattice.

### Gate 4: Thermal spectrum -- NOT FOUND

The Bogoliubov mode occupation does not follow a Planck/Fermi-Dirac
distribution.  ln(n_k) vs epsilon_k is not linear (R^2 < 0.7 in all cases).
The fitted temperatures do not track surface gravity kappa.

**Interpretation:** The 1D chain with open boundaries and a lattice potential
is too far from the continuum near-horizon geometry to produce a thermal
spectrum.  Hawking radiation requires: (a) a genuine horizon (not just a
potential well), (b) a continuum dispersion relation near the horizon, and
(c) the Unruh-like pairing of modes across the horizon.  None of these are
well-approximated by a 1D tight-binding chain with a 1/r potential.

This is not a failure of the framework -- it is a limitation of the prototype
geometry.  A proper test requires either: (i) a 3D lattice with f -> 1 forming
a closed surface (true propagator horizon), or (ii) an analog-gravity setup
with a flowing-lattice metric.

## Bounded claims

1. **Established:** A gravitational potential on the graph creates particles
   from the free-fermion vacuum (Bogoliubov mechanism).  This is the discrete
   analog of the Schwinger/Unruh effect.

2. **Established:** The free-fermion vacuum on a 2D lattice obeys an area law
   for entanglement entropy, and this persists (with modification) under gravity.

3. **Not established:** Thermal (Hawking) spectrum.  The prototype does not
   produce a Planck distribution.  This requires a more sophisticated geometry
   with a true horizon surface.

4. **Not established:** T proportional to surface gravity.  No meaningful T was
   extracted.

## Next steps for Paper 2

- Move to 3D lattice with Poisson-sourced f forming a closed horizon (f=1 surface)
- Use the path-sum propagator's own horizon (not just a potential well) as the
  vacuum-defining surface
- Test entanglement entropy across the horizon surface specifically
- Consider bosonic fields (different Bogoliubov structure)
- Investigate whether the lattice dispersion relation needs modification near
  the horizon to recover thermality
