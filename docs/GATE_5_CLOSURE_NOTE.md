# Gate 5: Dark Matter Freeze-Out

**Status:** Bounded -- structural inputs derived, thermal mechanism universal  
**Codex objection:** "still open -- freeze-out imports Boltzmann/Friedmann"  
**Scripts:** `frontier_dm_ratio_sommerfeld.py` (20/20), `frontier_freezeout_from_lattice.py`

---

## What is proven (framework-specific inputs)

The dark matter ratio R = Omega_DM / Omega_b = 5.48 uses three categories of
input. The framework derives the first two; the third is universal cosmology.

### 1. Particle content (derived)

The taste spectrum on Z^3 under the Z_3 orbifold gives:

- 3 generations of SM fermions (from the two triplet orbits)
- 2 singlet states: one light (Hamming weight 0, sterile), one heavy
  (Hamming weight 3, decoupled at M_Planck)
- The light singlet is the DM candidate: a color-singlet, SU(2)-singlet,
  hypercharge-zero state

This particle content follows from the same orbit algebra that gives
generations (Gate 2). No additional particle content is assumed.

### 2. Cross-section and coupling (derived)

The annihilation cross-section sigma*v ~ pi * alpha_s^2 / m^2 uses:

- alpha_s from the lattice gauge coupling (the plaquette action gives
  g^2 = 1 at the lattice scale; RG running to M_Z gives alpha_s ~ 0.092)
- The Sommerfeld enhancement factor from the lattice Green's function
  (computed structurally, 20/20 PASS)
- The group-theory factor from the SU(3) representation of the DM candidate

These are structural: they follow from the gauge group and its coupling, both
derived from the lattice construction.

### 3. Thermal freeze-out mechanism (universal cosmology)

The freeze-out calculation uses:

- The Boltzmann equation: dn/dt + 3Hn = -<sigma*v>(n^2 - n_eq^2)
- The Friedmann equation: H^2 = (8pi/3) G rho
- g_* = 106.75 relativistic degrees of freedom
- x_F = m/T_F ~ 25 (freeze-out temperature)

**These are not framework-specific.** Every dark matter model -- WIMPs, SIMPs,
hidden-sector models, SUSY neutralinos -- uses the same thermal freeze-out
machinery. The Boltzmann and Friedmann equations describe the thermal history
of the expanding universe. They are as universal as Newton's second law: they
are the dynamics, not the model.

The framework-specific inputs are WHAT freezes out (particle content), HOW
STRONGLY it interacts (cross-section from alpha_s and group theory), and WHAT
MASS it has (from the taste spectrum). The WHEN and HOW of freeze-out are
universal.

### g_* and x_F are not free parameters

Even these "imported" quantities are determined by the framework:

- g_* = 106.75 is the SM particle count. The framework derives the SM
  particle content (gauge groups + 3 generations), so g_* follows.
- x_F ~ 25 is a logarithmic consequence of perturbative freeze-out. It
  depends only weakly (logarithmically) on the DM mass and cross-section.
  For any perturbative annihilation channel, x_F falls in the range 15-45.

## What remains bounded

The honest boundary is between structural inputs and dynamical mechanism:

- **Structural (derived):** particle content, gauge coupling, cross-section,
  Sommerfeld factor, g_*
- **Universal (not derived, not needed to derive):** thermal equilibrium in
  the early universe, Boltzmann transport, Friedmann expansion

The framework does not derive the Big Bang or the thermal history of the
universe. It derives the INPUTS to that history. This is the same status as
every other DM model in the literature -- none of them derive the Boltzmann
equation from their particle physics.

## Paper-safe claim

> The dark matter ratio R = 5.48 uses framework-derived structural inputs
> (particle content from the taste spectrum, cross-section from alpha_s and
> SU(3) group theory, Sommerfeld enhancement from the lattice Green's
> function) combined with the universal thermal freeze-out mechanism of
> standard cosmology. The structural inputs are specific to the framework;
> the freeze-out dynamics are common to all thermal dark matter models.
> The ratio is a structural consistency result, not a pure first-principles
> derivation, because the thermal cosmological mechanism is imported as
> universal physics.
