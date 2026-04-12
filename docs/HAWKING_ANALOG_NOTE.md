# Hawking Analog: Thermal Spectrum Near Propagator Horizon

**Script:** `scripts/frontier_hawking_analog.py`
**Date:** 2026-04-11
**Status:** review negative; no thermal spectrum on this setup

## Hypothesis

The tested near-horizon propagator setup would produce Hawking-like thermal
radiation if the `f = 1` surface behaved as a true thermal horizon.

## Method

1. Solve 3D Poisson equation on a 41^3 lattice for a central point mass.
   Mass strengths chosen so f exceeds 1.0 at small radii (horizon forms).
2. Initialize a Gaussian wavepacket in the transverse (y) direction just
   outside the horizon radius r_h.
3. Evolve outward layer-by-layer using the 1D transfer matrix M(x) with
   the local field f(x, y) entering the action.
4. At a far-field detector plane, Fourier-transform the transverse
   wavefunction and fit ln|psi(k)|^2 vs k^2 for thermal shape.
5. Compare near-horizon spectrum to (a) far-field control and (b) free-field
   (no mass) control.

## Key Results

### Field Profile
All four mass strengths (40, 60, 80, 120) produce horizons at r_h = 2.9
to 6.8 lattice spacings. Surface gravity kappa ranges from 0.22 to 0.61.

### Near-Horizon Spectrum
- Gaussian thermal R^2: 0.007 to 0.71 (mean 0.40)
- No mass strength achieves R^2 > 0.9
- **The near-horizon spectrum is NOT thermal**

### Far-Field Control
- Gaussian thermal R^2: 0.82 to 0.94 (mean 0.87)
- Planck/Wien R^2: 0.95 to 0.99
- **The far-field spectrum IS quasi-thermal** (geometric/kernel effect)

### Free-Field Control
- 15 layers with f = 0: R^2 = 0.47 (not thermal)
- Fewer propagation layers than far-field runs

### Hawking Scaling (T vs kappa)
- Linear fit R^2 = 0.13 (no correlation)
- Measured slope c1 = -9.28 (wrong sign; Hawking predicts +0.16)
- **Hawking scaling is falsified**

## Diagnosis: Why It Fails

The critical issue is that f > 1 inside the horizon causes S = L(1-f) to
become negative. This flips the phase gradient and causes **amplitude
amplification**, not trapping. The norm ||psi||^2 grows from 1.0 to 164
for the strongest field (ms = 40) -- the wavepacket gains energy passing
through the high-field region rather than losing it.

This means:
- The f = 1 surface is not an absorbing horizon. It is a phase-inversion
  boundary that amplifies outgoing modes.
- The disrupted spectrum near the horizon is noisier (less thermal) than
  the far-field, the opposite of what Hawking radiation would produce.
- The quasi-thermal shape seen in far-field propagation is a geometric
  artifact of the cos^2 kernel and 1/L^p attenuation, not physics.

## What Would Need to Change

For a genuine Hawking analog, the framework would need:
1. A mechanism to **absorb** or **trap** ingoing amplitude at the horizon
   (f = 1 freezes phase but does not attenuate amplitude)
2. Quantum fluctuations at the horizon that convert frozen-phase modes
   into outgoing thermal radiation (no such mechanism exists in the
   classical path-sum)
3. The action S = L(1-f) does not enforce a one-way membrane; it merely
   reduces phase accumulation

## Verdict

**Negative on this setup.** The tested `f = 1` surface does not produce a
Hawking-like thermal spectrum. The near-horizon spectrum is less thermal than
the far-field control, and the fitted temperature shows no useful correlation
with surface gravity. On this implementation the `f = 1` surface behaves as an
amplifying phase-inversion boundary, not a one-way thermal horizon.

This is a genuine negative result: the two-axiom framework in its current
form does not contain the mechanism needed for Hawking radiation. This is
not unexpected -- Hawking radiation requires quantum field theory on curved
spacetime, and the classical path-sum propagator lacks the vacuum
fluctuation mechanism that produces particle creation at horizons.
