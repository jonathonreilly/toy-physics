# Strong-Field GR Investigation

**Script:** `scripts/frontier_strong_field_gr.py`
**PStack:** `frontier-strong-field-gr`

## Motivation

The framework reproduces weak-field GR: Newtonian gravity, geodesic
equation, gravitational waves, factor-of-2 light bending. But at f -> 1
the single-particle propagator has S = L(1 - f) -> 0 (phase freezing),
and for f > 1 the action inverts (amplification, not absorption). This
means the framework does NOT naturally form event horizons.

This investigation asks: what strong-field phenomena CAN the framework
produce?

## Five Probes

### 1. Gravitational Self-Interaction

The wave equation (box f = -rho) is linear, but rho = |psi|^2 depends
on f through the propagator. This back-reaction loop creates effective
nonlinearity.

**Result:** Self-interaction IS present. The self-consistent iteration
converges, with a deflection shift of ~3.75 lattice units between the
fixed-background and self-consistent solutions. The propagator density
sources additional field, which modifies the propagator, creating a
genuine nonlinear feedback loop analogous to GR's gravitational
self-energy.

### 2. Second-Quantized vs Single-Particle Strong-Field

The Bogoliubov vacuum detects field gradients through mode mixing. Near
f -> 1, gradients diverge and particle creation increases.

**Result:** Particle creation scales as n ~ strength^0.50 and vacuum
energy as |E_vac| ~ strength^0.78. But gravitational energy scales as
~strength^2. Since 0.78 < 2.0, vacuum pressure alone does NOT resist
gravitational collapse. The many-body vacuum provides a correction but
not a qualitative change in the strong-field regime.

### 3. Quantum Pressure from Lattice UV Cutoff

Fermions on the lattice obey exclusion. As a gravitational well deepens,
particles are squeezed into fewer sites, raising kinetic energy (Fermi
pressure).

**Result:** Lattice pressure IS present and DOES resist collapse. Even at
80x the free-field gravity strength, the particle distribution retains
nonzero width. At low filling (10%), the width saturates near ~2.4 lattice
spacings. At half-filling, the width remains ~13.5 spacings at the
strongest tested potential. The lattice UV cutoff provides a genuine
Fermi-like degeneracy pressure.

### 4. Maximum Mass (Chandrasekhar-Like Limit)

Self-consistent iteration: N fermions source their own gravitational
potential, which is solved and fed back until convergence.

**Result:** For G = 0.5 on an 80-site chain, no collapse was detected up
to 40 particles. Lattice pressure supports all tested configurations.
The virial ratio (2E_kin + E_grav) is consistently negative (not in
virial equilibrium), indicating the lattice's kinetic energy dominance.
A Chandrasekhar-like limit likely exists at higher G or larger particle
counts, but the framework's UV cutoff makes it fundamentally different
from classical GR collapse.

### 5. Gravitational Wave Scattering

Two crossing wave packets on a 2D lattice, compared to single-packet
evolution.

**Result:**
- Linear wave equation: perfect superposition (residual ~10^-15).
  No scattering.
- With f^2 back-reaction coupling: scattering IS detected, with
  amplitude scaling as coupling^2.03.
- This matches the GR prediction (scattering ~ G^2) and confirms
  that GW-GW interaction requires nonlinear coupling, which comes
  naturally from the propagator back-reaction.

## Key Findings

| Phenomenon | Present? | Mechanism |
|-----------|----------|-----------|
| Gravitational self-interaction | Yes | Propagator density sources field (rho <-> f loop) |
| Vacuum particle creation resists collapse | No | Vacuum energy scales too slowly (~M^0.78 vs M^2) |
| Lattice quantum pressure | Yes | Fermi degeneracy from UV cutoff |
| Maximum mass limit | Likely | Lattice pressure vs gravity; not reached at tested G |
| GW-GW scattering | Yes (with coupling) | Effective f^2 term from back-reaction; scales as G^2 |
| Event horizons | No | f > 1 amplifies rather than absorbs |

## Physical Interpretation

The framework predicts "frozen stars" rather than black holes:
- Gravitational collapse is halted by lattice Fermi pressure before
  f reaches 1
- The resulting object has maximum compactness set by the lattice
  spacing (Planck-scale cutoff)
- No information paradox: there is no horizon, so unitarity is manifest
- The strong-field object still produces Hawking-like radiation via
  Bogoliubov particle creation (see Probe 2)

This is reminiscent of "gravastar" or "Planck star" proposals in
quantum gravity, where quantum effects prevent horizon formation.

## What the Framework Cannot Do (Strong-Field Gaps)

1. **No event horizons or trapped surfaces** -- fundamental limitation
   of S = L(1 - f)
2. **No Kerr metric** -- rotation not yet implemented
3. **No gravitational collapse singularity** -- lattice cutoff prevents it
   (arguably a feature, not a bug)
4. **No post-Newtonian orbital precession** -- not yet tested in the
   self-consistent loop
5. **No ringdown / quasi-normal modes** -- would require dynamical
   strong-field merger simulation
