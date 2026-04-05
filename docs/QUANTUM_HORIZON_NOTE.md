# Quantum Horizon: k-Dependent Trapping Threshold

**Date:** 2026-04-05
**Status:** novel prediction — the horizon depends on particle wavelength

## Result

On the 3D lattice with absorbing kernel exp(-α·f):

| k | α_crit (50% escape) | Regime |
|---|---------------------|--------|
| 1.0 | 1.16 | Low-k: trapped easily |
| 2.0 | 1.27 | |
| 3.0 | 1.27 | |
| 5.0 | 1.42 | High-k: harder to trap |
| 7.0 | < 0.05 | Above Nyquist: trivially trapped |
| 10.0 | < 0.05 | Above Nyquist: trivially trapped |

## Interpretation

The trapping threshold α_crit INCREASES with k for k < π/h.
Higher-momentum (shorter wavelength) particles need stronger
absorption to be trapped. This is OPPOSITE to classical GR,
where all particles have the same Schwarzschild radius.

At k > π/h (Nyquist): the phase aliasing already depletes the
beam (gravity reverses), so trapping is trivial without absorption.

## Physical picture

Low-k particles have long wavelengths → they "see" the mass as
a smooth phase valley → they get deflected and trapped coherently.

High-k particles have short wavelengths → they resolve the lattice
structure → the phase varies rapidly across the mass → partial
destructive interference PROTECTS them from trapping.

Above Nyquist: the lattice can't resolve the wavelength → the
phase signal aliases → the beam is disrupted regardless of trapping.

## The prediction

On any discrete spacetime with lattice spacing a:
  - Particles with λ >> 2a: classical horizon (easy to trap)
  - Particles with λ ~ 2a: quantum-corrected horizon (harder to trap)
  - Particles with λ < 2a: Nyquist trapping (automatic)

The transition scale is the lattice Nyquist wavelength λ = 2a.
