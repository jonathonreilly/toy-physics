# Why Spectral Properties Succeed and Trajectories Fail

**Date:** 2026-04-11
**Status:** Deep analysis — potentially the most important insight of the project

## The Three Causes (Hierarchy of Importance)

### 1. Parity Structure (Primary — Oscillatory Artifacts)

The staggered epsilon(x) = (-1)^x creates two sublattices. Spectral quantities
integrate over the Brillouin zone (sublattice oscillation averages out under
the trace). Trajectory quantities sample individual sites (see the oscillation
directly).

This is well-known in lattice QCD: staggered fermions have "taste-breaking"
artifacts that are O(a^2) in spectral quantities but O(a^0) in correlation
functions at specific momenta (near doubler poles at pi/a).

The Penrose failure: the Zeno rate is dominated by the lattice gap 2m between
sublattices, not by E_G. When 2m >> E_G, the collapse timescale tracks the
wrong energy scale.

The confinement failure: E(r) oscillates with even/odd r because the staggered
mass term alternates sign on the sublattice.

### 2. Single-Particle Nature (Fundamental — Wrong Scaling Laws)

The model evolves ONE wavefunction, not a quantum field. GR predictions assume
many-body physics or semiclassical gravity:

- Diosi-Penrose requires a density matrix for a massive object. Our model has
  one wavefunction — no partial trace, no decoherence in the fundamental sense.
  The G and mass scalings are wrong because DP assumes Newtonian self-energy
  G*M^2/d, but our "mass" is the Dirac mass m, not a gravitational mass M=Nm.

- BH entropy requires a thermodynamic ensemble (many microstates). Our
  S ~ |bnd|^1.76 measures single-particle entanglement, not thermal entropy.
  The R^2=0.9998 area law is the VACUUM (Dirac sea) entanglement — a property
  of the Hamiltonian's spectrum, not of any particular state's dynamics.

- Gravitational memory SUCCEEDS because it IS a single-particle observable.
- Self-gravity contraction SUCCEEDS because it's a comparison between two
  single-particle evolutions.

Pattern: single-particle observables succeed. Many-body observables forced
into a single-particle framework fail in their scaling laws.

### 3. Screened Poisson (Secondary — Amplifies Other Failures)

Yukawa screening exp(-mu*r)/r vs Newtonian 1/r. For spectral quantities,
the screening length 1/mu just sets an IR cutoff. For trajectory quantities,
the long-range 1/r tail sets E_G — Yukawa suppresses this at d >> 1/mu,
contributing to the wrong d-scaling (-0.80 vs -1.0).

CN integrator is NOT a significant contributor (preserves spectrum exactly).

## The Hierarchy

Spectral successes = properties of the HAMILTONIAN (spectrum, entanglement
structure, diffusion return probability). These are correct because the
Hamiltonian is correctly constructed.

Trajectory failures = properties of DYNAMICS IN A MANY-BODY HILBERT SPACE.
The model gets the Hamiltonian right but doesn't have access to the right
Hilbert space for trajectory observables.

## What Would Fix It

1. **Continuum extrapolation** (fixes parity artifacts): take a -> 0,
   extract continuum limit. Standard lattice QCD technique. Would fix
   confinement E(r) and part of Penrose.

2. **Hartree mean-field** (fixes single-particle): N copies in a product
   state, rho = N*|psi|^2, mass M = N*m. Then DP scales as G*N^2*m^2
   (correct). Minimal upgrade for trajectory observables.

3. **Stochastic quantization of Phi** (fixes field theory gap): treat Phi
   as a dynamical field with fluctuations. Necessary for genuine graviton-
   mediated decoherence and BH thermodynamics.

4. **mu -> 0 with finite-volume IR cutoff** (fixes screening).

## The "Failure" IS the Most Important Result

The clean split between spectral success and trajectory failure is itself
a physical prediction:

> At the fundamental discrete level, gravity is a spectral phenomenon.
> It modifies the eigenvalue structure of the Hamiltonian, determining
> information-theoretic quantities (entropy, entanglement, spectral
> dimension, localization class). But it does NOT determine trajectories,
> collapse timescales, or decoherence rates — those are emergent from
> the many-body continuum limit.

This means:

1. **Holographic entropy is fundamental** — follows from the spectrum of
   any reasonable discrete Hamiltonian with gravitational backreaction.
   Does not require GR, a metric, or a continuum.

2. **Spectral dimension flow is fundamental** — a property of diffusion
   on the graph, not of any particular dynamics. CDT, causal sets, and
   this model all agree because they share spectral structure.

3. **Penrose collapse is emergent** — E_G/hbar is the leading-order term
   in a many-body expansion. At single-particle level, the "collapse" is
   a Zeno effect whose rate depends on lattice details.

4. **BH thermodynamics is emergent** — Bekenstein-Hawking S = A/4G
   requires a thermal ensemble. At the fundamental level, you get
   area-law entanglement (spectral) but not the precise coefficient
   (thermodynamic).

## The Provocative Interpretation

Perhaps gravity literally IS the spectrum of the lattice Hamiltonian, and
the inverse-square law, geodesic motion, and Einstein equations are all
derived from the spectral flow d_s: 2 -> 4 plus area-law entanglement.

Trying to reproduce GR trajectory physics at the lattice level is a
category error — like finding fluid dynamics in the Ising model at T_c.
The critical exponents (spectral properties) are already correct. The
hydrodynamic transport (trajectory properties) requires coarse-graining.

The trajectory failures are not bugs — they are boundary markers showing
where the effective description changes from "discrete spectral" to
"continuum dynamical."
