# Spectral Question — Closed

**Date:** 2026-04-09
**Status:** Closed as a bounded negative for broadband attraction.

## The question

Does the model produce net gravitational attraction when the propagator
sums over a range of phase wavenumbers k?

## The answer

**No, not under any physically motivated spectral weighting.**

### What was tested

1. **Raw equal-amplitude broadband** (frontier_spectral_on_lattice.py,
   frontier_lorentzian_spectral.py): AWAY for both Euclidean and
   Lorentzian models. All broad spectra, all flat spectra.

2. **Detector-flux equalized** (frontier_natural_weight_spectral.py):
   TOWARD when weighting by 1/P_detector or 1/sqrt(P_detector). But
   this is a post-hoc outcome equalizer defined from detector outputs,
   not a source-side spectrum.

3. **Source-side controls** (frontier_lorentzian_source_weight_spectral.py,
   on codex/source-weight-spectral branch): AWAY under all three source-
   defined weightings (raw, source-coupling, equal incident flux). Only
   detector-equalization flips signs, and even there the Lorentzian
   model is only 3/9 TOWARD.

### What this means

- **Narrowband attraction is real.** At specific k values (k=1-6
  Euclidean, k=6.5-7.5 Lorentzian), the model produces TOWARD gravity
  with F∝M=1.00. This passes all closure-card tests.

- **Broadband attraction does not survive.** Under any source-defined
  spectral control, the net deflection is AWAY. The attractive window
  is a minority of the spectrum in amplitude-weighted terms.

- **The detector-equalization TOWARD was a post-hoc artifact.** It
  suppressed the dominant high-probability AWAY mode, which is a valid
  diagnostic (it identified the amplification bias) but is not a
  physical source spectrum.

- **The "just a source-spectrum question" framing was too optimistic.**
  Source-side weighting does not rescue broadband attraction.

### The honest model summary

The model produces a k-dependent dispersive force from scalar field
perturbations on a discrete causal graph. Within specific frequency
windows (the "attractive window"), the force mimics Newtonian gravity
with F∝M=1.00 and distance-dependent falloff. Outside those windows,
the force is repulsive. The attractive window is broad on the 3D
ordered lattice (spanning k=1-6 in the Euclidean model, k=6.5-7.5
in the Lorentzian model) but does not survive broadband spectral
averaging under source-defined controls.

The model also produces (independently of the gravity question):
- Born rule (structural, kernel-independent)
- Gauge connections (U(1), Aharonov-Bohm modulation)
- Self-regulating dynamic graph growth (Born-compliant)
- Causal set structure (valid poset, metric from chains at r=0.997)
- F∝M=1.00 at all k values (structural to valley-linear action)

### What remains open

1. Whether a specific PHYSICAL mechanism selects k (analogous to
   de Broglie k = p/hbar), making the single-k result physical
2. Whether the Lorentzian split-delay action has other advantages
   beyond shifting the attractive window
3. Whether the model's k-dependent force has physical analogs
   (optical gradient force, AC Stark effect)
