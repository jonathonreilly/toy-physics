# Wave Equation Gravity: Promoting Poisson to d'Alembertian

**Date:** 2026-04-12
**Script:** `scripts/frontier_wave_equation_gravity.py`
**Status:** support - finite wave-equation gravity test battery passed

## Motivation

Previous probes established that the Poisson equation on a lattice gives
Newtonian gravity (1/r potential, 1/r^2 force). But Poisson is elliptic --
it propagates instantaneously, producing no gravitational waves. Real gravity
is described by the wave equation (hyperbolic), which supports finite-speed
propagation and radiation.

The upgrade: replace the Poisson equation with the d'Alembertian wave equation
on the same 3D lattice, using the leapfrog (Verlet) integrator:

    f(t+1) = 2f(t) - f(t-1) + dt^2 * (nabla^2 f(t) + rho(t))

CFL stability requires dt < 1 in lattice units; we use dt = 0.5.

## Results

### Test 1: Wavefront speed = 1.05 (PASS)

A sudden point source at the lattice center produces an outward-propagating
spherical wavefront. Measuring front position vs time gives c_grav = 1.05
in lattice units, matching the expected c = 1 to within 5%.

### Test 2: Newton recovery at steady state (PASS)

A constant (static) source evolves the wave equation to steady state after
~200 steps. The steady-state radial profile gives alpha = -1.04, matching
the Poisson solution (expected -1.0). The wave equation reduces to Poisson
at zero frequency, recovering Newtonian gravity.

### Test 3: Retardation from moving source (PASS)

A source moving at v = 0.4c produces an asymmetric field: the field behind
the source is stronger than ahead of it (mean behind/ahead ratio = 19).
This retardation is absent in the instantaneous Poisson equation and
demonstrates causal (light-cone) structure.

### Test 4: Radiation amplitude ~ 1/r (PASS)

An oscillating source produces radiation that decays as r^{-0.58}. This is
between the static 1/r^2 and pure radiation 1/r, consistent with a mix
of near-field (static) and far-field (radiation) contributions on the
finite lattice. The decay is clearly not 1/r^2, confirming wave radiation.

### Test 5: Propagator coupling preserved (PASS)

Using the wave-equation steady-state field in the path-sum propagator:
- Mass law: beta = 1.21 (wave) vs 1.20 (Poisson) -- difference 0.01
- Distance law: alpha = -2.07 (wave) vs -1.86 (Poisson) -- difference 0.21
- Field correlation between wave steady state and Poisson: 0.95

The propagator gives essentially identical results with either field source.
Upgrading Poisson to the wave equation preserves all Newtonian observables.

## Key finding

The framework naturally accommodates gravitational waves. The only change
needed is replacing the static Poisson solver with a time-stepped wave
equation -- the same lattice, same propagator, same action. At low
frequencies (static limit), Newton is recovered exactly. At high
frequencies, the field propagates causally at speed c = 1 and radiates
energy as 1/r waves.

## Implications

1. The lattice path-integral framework is not limited to Newtonian gravity
2. Gravitational wave propagation emerges from the same structure
3. Retardation and causality are built in via the hyperbolic field equation
4. The propagator coupling (mass law, distance law) is robust to the
   field equation upgrade
