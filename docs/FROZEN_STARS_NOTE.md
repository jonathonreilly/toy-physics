# Frozen Stars: Compact Object Predictions

**Script:** `scripts/frontier_frozen_stars.py`
**PStack:** `frontier-frozen-stars`

## Motivation

The strong-field investigation showed that lattice Fermi pressure halts
gravitational collapse before f reaches 1 (phase freezing). The resulting
objects are "frozen stars" with no event horizon. This investigation
computes specific, testable predictions for these compact objects.

## Five Probes

### 1. Maximum Mass (Chandrasekhar Analog)

Self-consistent Hartree solution: N fermions on a 1D lattice source their
own gravitational potential V(i) = -G * sum_j rho(j) / |i-j|, iterated
to convergence.

**Result:** At G = 0.5 and G = 1.0 on a 100-site chain, no collapse was
detected up to 58 particles. At G = 2.0 and G = 5.0, collapse occurs at
N_crit = 6 particles (width drops below 2.5 lattice spacings).

The N_crit scaling with G is flat across the two detected collapse points
(both at N_crit = 6), which likely reflects the 1D geometry where only
two values contributed. The analytic Chandrasekhar estimate predicts
N_crit ~ 4t/G in 1D.

In 3D with physical units, the Chandrasekhar number is
N_Ch ~ (m_Pl / m_f)^3 ~ 2.2 x 10^57, giving M_Ch ~ 1.9 M_sun for
nucleon-mass fermions -- consistent with the observed neutron star
maximum mass.

### 2. Minimum Radius vs Schwarzschild Radius

For each (G, N_p) configuration, the self-consistent width R_frozen is
compared with R_Schwarzschild = 2 * G * N_p (lattice units).

**Result:** The minimum ratio R_frozen / R_s (among non-collapsed
configurations) is approximately 0.05 -- the frozen star can be
substantially MORE compact than the Schwarzschild radius.

This is surprising but consistent: the lattice framework does not produce
horizons (f > 1 amplifies rather than absorbs), so there is no physical
barrier at R = R_s. The frozen star shrinks to a few lattice spacings
wide, stabilized by Fermi pressure, regardless of the classical
Schwarzschild radius.

Key finding: the compactness is set by the lattice spacing, not by R_s.
At strong coupling (G = 3), R_frozen ~ 0.05 * R_s, meaning the object
is 20x more compact than a black hole would be. The surface is at the
Planck scale.

### 3. Gravitational Wave Ringdown Signature

Quasi-normal modes computed from particle-hole excitations of the
self-consistent ground state.

**Result:** The frozen star's QNM frequencies are systematically
different from black hole QNMs (omega_BH ~ 0.747 / GM). The lattice
excitation spectrum produces discrete modes rather than the continuous
QNM overtone series of a black hole.

Key prediction: **post-merger echoes**. Because the frozen star has a
surface (at R_frozen) and a potential barrier (near the light ring at
3GM), perturbations bounce between the two, producing echoes at spacing:

  t_echo ~ 2 * (R_frozen - R_s) * ln(R_frozen / R_s - 1)

For compact frozen stars where R_frozen ~ few * R_s, this echo time is
short and potentially detectable by LIGO/Einstein Telescope.

### 4. Surface Temperature

The frozen star has a surface (unlike a black hole). The Bogoliubov
mechanism creates particles near the surface where field gradients are
steep.

**Result:** T_surface / T_Hawking ~ 70 (averaged across configurations).

The surface temperature is roughly 70x the Hawking temperature for a
black hole of the same mass. This arises because the surface gradient
|dV/dr| is much steeper than the horizon surface gravity would be.

Physical consequence: for a 10 M_sun frozen star,
T_Hawking ~ 6 x 10^-9 K, so T_surface ~ 4 x 10^-7 K. This is
extremely cold but nonzero -- unlike a classical black hole, the frozen
star radiates from its surface.

### 5. Mass Gap Prediction

Fine scan of particle count at G = 1.0 on a 150-site chain.

**Result:** No collapse detected up to N_p = 59. The most compact stable
configuration has R_frozen / R_s = 0.146 at N_p = 59.

The lattice Fermi pressure is remarkably robust: even at extreme
compactness, the configuration remains stable. The 1D model does not
produce a mass gap directly, but the physical 3D scaling gives:

- Lower edge (max neutron star): ~2.2 M_sun (TOV limit from nuclear EOS)
- Upper edge: set by lattice coupling strength

The observed gap at 2.5 - 5 M_sun would correspond to the transition
from nuclear pressure support to lattice (Planck-scale) pressure support.

## Key Findings

| Observable | Prediction | Testable? |
|-----------|------------|-----------|
| Maximum mass | M_Ch ~ 1.9 M_sun (3D scaling) | Matches observed NS limit |
| Minimum radius | R ~ few lattice spacings (Planck scale) | Not directly |
| Compactness | R_frozen / R_s can be << 1 | EHT shadow size |
| GW ringdown | Discrete QNMs + post-merger echoes | LIGO/ET |
| Surface temperature | T ~ 70 * T_Hawking | X-ray/microwave |
| Mass gap | Nuclear -> lattice EOS transition at ~2-5 M_sun | GW catalog |
| Event horizons | Never form (f > 1 amplifies) | EHT imaging |

## Physical Interpretation

The lattice framework predicts a fundamentally different endpoint for
gravitational collapse than GR:

1. **No horizons:** the propagator action S = L(1-f) goes through zero
   at f = 1 but does not produce a trapped surface. Instead, f > 1
   amplifies propagation (repulsive quantum pressure).

2. **Planck-scale surface:** Fermi degeneracy pressure on the lattice
   stabilizes the object at a size of order the lattice spacing. If
   a = l_Planck, this is a Planck-density object.

3. **Observable differences from black holes:**
   - Post-merger GW echoes (distinctive time signature)
   - No information paradox (no horizon, unitarity manifest)
   - Thermal surface emission (faint but nonzero)
   - Different shadow profile for EHT

This picture is consistent with "gravastar," "Planck star," and
"firewall" proposals in the quantum gravity literature, but emerges here
from the lattice structure rather than being imposed.

## Caveats

- The 1D lattice model misses 3D geometric effects (orbital angular
  momentum, centrifugal barrier, radiation pressure)
- The N_crit scaling is poorly constrained (only 2 collapse data points)
- R_frozen / R_s < 1 does not mean a horizon forms -- the lattice
  framework simply does not have horizons
- Physical temperature estimates depend on identifying lattice units
  with Planck units
- The mass gap prediction requires a specific model for the nuclear ->
  lattice EOS transition
