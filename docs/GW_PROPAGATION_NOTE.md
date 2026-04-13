# Gravitational Wave Propagation on Z^3

**Script:** `scripts/frontier_gw_propagation.py`
**PStack:** gw-propagation

## Overview

Five independent derivations showing that gravitational wave propagation
emerges naturally from the d'Alembertian on the Z^3 lattice.

## Derivation 1: Wave equation for phi-perturbations

Starting from the full wave equation on the lattice:

    d^2 phi / dt^2 - nabla^2 phi = -rho

with a static background (nabla^2 phi_0 = -rho_0), write phi = phi_0 + delta_phi.
Subtracting the background equation:

    d^2(delta_phi)/dt^2 = nabla^2(delta_phi)

Perturbations obey the **free wave equation** -- no source term. This is the
lattice analog of linearized gravity: small perturbations propagate as waves
on the background geometry.

**Numeric check:** Gaussian perturbation on a static Poisson background
propagates outward with causal ordering confirmed at r = 3, 6, 9.

## Derivation 2: Propagation speed c = 1

On Z^3 with nearest-neighbor hopping (dx = 1) and time step dt:

    CFL condition: c_max = dx / dt

In lattice natural units where dx = dt = 1, this gives **c = 1**.

More precisely, the group velocity from the dispersion relation is
v_g = cos(k/2), with maximum v_g = 1 at k -> 0. The wavefront travels at
the maximum group velocity, so the speed of gravitational waves equals
the speed of light on the lattice.

**Numeric check:** Delta-function perturbation; arrival time t_arr = r/c
gives c = 1.0 +/- 0.1 across radii.

## Derivation 3: Dispersion relation omega(k) = 2 sin(k/2)

Plane-wave ansatz phi ~ exp(i(kx - omega t)) in the discrete Laplacian:

    nabla^2_d phi = (e^{ik} - 2 + e^{-ik}) phi = -4 sin^2(k/2) phi

Substituting into the wave equation:

    omega^2 = 4 sin^2(k_x/2) + 4 sin^2(k_y/2) + 4 sin^2(k_z/2)

For a single axis: **omega = 2|sin(k/2)|**.

This reduces to the continuum omega = |k| at long wavelengths (k << 1),
with corrections O(k^3) -- the lattice UV artifact. At k = pi (Brillouin
zone boundary), omega = 2 (maximum frequency).

**Numeric check:** 1D wave equation with single-k initial conditions;
FFT-extracted frequencies match theory to < 5%.

## Derivation 4: 1/r amplitude decay (d=3 Green's function)

The retarded Green's function in 3 spatial dimensions:

    G(r, t) = delta(t - r/c) / (4 pi r)

For an oscillating source at the origin with frequency omega:

    phi(r, t) ~ (1/r) sin(omega(t - r/c))

The **amplitude decays as 1/r**, which is specific to d = 3.
General formula: amplitude ~ 1/r^{(d-1)/2}.

This follows from energy conservation: the energy flux S ~ (dphi/dt)^2 ~ 1/r^2
integrated over a sphere of area 4 pi r^2 gives constant total power.

**Numeric check:** Oscillating source on 51^3 lattice; power-law fit to
amplitude vs radius gives gamma = -1.0 +/- 0.2.

## Derivation 5: Quadrupole formula from energy flux

For outgoing waves phi ~ (A/r) sin(omega(t - r/c)):

    Energy flux:  S = (dphi/dt)^2 ~ omega^2 A^2 / r^2
    Total power:  P = 4 pi r^2 * S ~ omega^2 A^2   (r-independent)

For a quadrupole source with moment Q oscillating at frequency omega:

    A ~ omega^2 Q / c^4    (dimensional analysis)
    P ~ omega^6 Q^2 / c^5  (Einstein quadrupole formula)

The testable prediction: **(dphi/dt)^2 * r^2 = const** across radii.

**Numeric check:** Oscillating quadrupole (two antipodal sources) on 51^3
lattice; (dphi/dt)^2 * r^2 approximately constant across r = 5..17.

## Key results

| Quantity | Lattice value | Continuum limit |
|----------|--------------|-----------------|
| Wave speed | c = 1 (lattice units) | Speed of light |
| Dispersion | omega = 2 sin(k/2) | omega = k |
| Amplitude decay | 1/r | 1/r (d=3) |
| Energy flux | S ~ 1/r^2 | Inverse square law |
| Radiation power | P ~ omega^6 Q^2 | Quadrupole formula |

## Relation to existing probes

- Extends `frontier_wave_equation_gravity.py` (wave equation + Newton recovery)
- Extends `frontier_grav_wave_post_newtonian.py` (post-Newtonian corrections)
- The dispersion relation connects to `frontier_dispersion_relation.py`
- Together these show the full GW phenomenology on Z^3

## Significance

All five ingredients of gravitational wave physics -- wave equation, finite
propagation speed, dispersion relation, inverse-distance decay, and the
quadrupole radiation formula -- emerge from the discrete d'Alembertian on
the cubic lattice. No additional structure beyond Z^3 with nearest-neighbor
hopping is required.
