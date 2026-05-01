# Wave Equation Gravity: Promoting Poisson to d'Alembertian

**Date:** 2026-04-12 (claim narrowed 2026-05-01)
**Script:** `scripts/frontier_wave_equation_gravity.py`
**Status:** support - finite-speed wave propagation + static-limit Newton recovery established; 1/r radiation tail and Newton-like propagator distance law NOT cleanly established on the current finite box

## Motivation

Previous probes established that the Poisson equation on a 3D lattice gives
Newtonian gravity (1/r potential, 1/r² force). Poisson is elliptic — it
propagates instantaneously and supports no gravitational waves. The intended
upgrade is the d'Alembertian wave equation on the same lattice with leapfrog
(Verlet) integration:

    f(t+1) = 2 f(t) − f(t−1) + dt² · (∇² f(t) + ρ(t))

CFL stability requires `dt < 1` in lattice units; the runner uses `dt = 0.5`.

## What this note now claims

The runner's checks are now classified into per-claim PASS/FAIL lines so
each physical assertion is auditable on its own. Concretely:

### ESTABLISHED by the runner

1. **Finite-speed wavefront propagation.** A point source at the lattice
   centre produces an outward spherical wavefront with speed
   `c_grav = 1.05 ± few %` in lattice units, matching the lattice signal
   speed `c = 1`. (Test 1)
2. **Static-limit Newton recovery.** After ~200 steps with a constant
   source, the steady-state radial profile fits `r^α` with
   `α ≈ −1.04`, matching the Poisson 1/r solution. The wave equation
   reduces to Poisson at zero frequency. (Test 2)
3. **Qualitative retardation from a moving source.** A source at v = 0.4c
   produces a strongly asymmetric trailing/leading field
   (mean ratio ~19), absent in the instantaneous Poisson equation. This
   is a sign-of-causality check, not a quantitative GR retardation
   measurement. (Test 3)
4. **Wave/Poisson agreement on the propagator scaling.** Switching the
   path-sum propagator's source field from Poisson to the wave-equation
   steady state preserves the propagator mass exponent
   `β` to within `Δβ ≈ 0.01` and the propagator distance exponent `α`
   to within `Δα ≈ 0.21`. The wave-equation upgrade does not disrupt
   the existing propagator pipeline. (Test 5c)
5. **Propagator mass linearity.** The propagator mass exponent
   `β ≈ 1.21 ≈ 1.0 ± 21%`, consistent with mass-linear coupling. (Test 5a)

### NOT established by the runner

6. **1/r gravitational radiation.** With an oscillating source the
   measured amplitude exponent is `γ ≈ −0.58`, NOT the `γ ≈ −1` that
   would certify a 1/r far-field radiation tail. The current geometry
   has the absorbing boundary too close, mixing near-field and reflected
   contributions, so the radiation tail is not isolated. The runner's
   strict claim Test 4a (|γ + 1| < 0.2) FAILS; only the loose
   non-static check Test 4b passes. (Earlier drafts of this note
   reported Test 4 as PASS for "1/r radiation"; that was over-permissive.)
7. **Newton-like propagator distance law.** The propagator's measured
   distance exponent is `α ≈ −2.07`, not `α ≈ −1`. The framework's
   path-sum propagator reads a force-law-like distance scaling on the
   tested geometry, not a 1/r potential. Test 5b (|α + 1| < 0.3) FAILS.
   The earlier framing "preserves... Newton-like distance law" is
   replaced by the more honest claim above (4): wave/Poisson agreement
   on the propagator's own scaling, whatever it is.

## Honest summary

What the runner cleanly demonstrates is the **kinematic upgrade**:

- the d'Alembertian replaces the Poisson source-to-field map
- finite-speed propagation appears
- the static limit recovers Poisson exactly
- the path-sum propagator pipeline still works after the upgrade
- moving sources produce qualitative retardation

What the runner does **not** demonstrate is the **dynamical-radiation**
or **continuum-Newton** content:

- a clean 1/r gravitational-wave tail (would need a much larger box
  with a properly absorbing far-field boundary, or near-field
  subtraction)
- the analytic 1/r distance law on the propagator (would need either
  a different propagator definition or a refinement of the existing
  one)

These two open items do not invalidate the kinematic upgrade; they are
honest open items, not silent failures.

## Implications

1. The lattice path-integral framework can host a hyperbolic field
   equation on the same operator stack used for Poisson.
2. Finite-speed signal propagation and qualitative retardation emerge
   from this upgrade.
3. Quantitative gravitational-wave radiation and continuum Newton-like
   distance laws on the propagator require additional work beyond the
   minimal upgrade demonstrated here.
