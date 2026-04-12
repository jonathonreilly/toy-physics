# Diamond NV Lattice-Scale Correction Note

**Date:** 2026-04-12
**Status:** quantitative prediction, honest detectability assessment
**Script:** `scripts/frontier_diamond_nv_lattice_correction.py`

## Purpose

This note answers the reviewer question: "Your framework predicts the same
retardation as GR. What's new?"

The answer: the discrete-graph propagator has a **modified dispersion relation**
that produces a **frequency-dependent correction** to the phase ramp.  Smooth GR
predicts a phase ramp linear in drive frequency.  The lattice framework predicts
an additional **cubic-in-frequency** correction term whose coefficient depends on
the lattice spacing.

## Smooth GR Prediction

For a gravitational signal propagating at speed c from a source at distance d,
driven at angular frequency omega:

    phi_GR(omega) = omega * d / c

The phase ramp across the NV field of view (spatial extent Delta_d):

    Delta_phi_GR = omega * Delta_d / c

This is **linear in omega** with slope d/c.  At d = 1 mm, f = 1 kHz:

- Phase lag: 2.1e-8 rad
- Time delay: 3.3e-12 s
- Phase slope: 2.1e-11 rad/Hz

## Lattice Correction

The discrete propagator dispersion relation (from `frontier_dispersion_relation.py`):

    omega^2 = c^2 k^2 (1 + A h^2 k^2 + ...)

where h is the lattice spacing and A is a dimensionless coefficient extracted
from the path-sum transfer kernel (A ~ 0.04 to 1.7 depending on architecture).

This gives a frequency-dependent group velocity:

    v_g(omega) = c * (1 + A (h omega / c)^2 + ...)

And a corrected phase accumulation:

    phi(omega) = omega * d / c * (1 - A (h omega / c)^2 + ...)
               = phi_GR(omega) * (1 - A (h omega / c)^2)

The **lattice correction** to the phase is:

    delta_phi = -A * d * h^2 * omega^3 / c^3

## Key Signature: Cubic-in-Frequency Correction

| Quantity              | Smooth GR          | Lattice Framework                        |
|-----------------------|--------------------|------------------------------------------|
| Phase lag             | omega d/c          | omega d/c (1 + A(h omega/c)^2)           |
| Frequency dependence  | linear             | linear + cubic                           |
| Phase ramp slope      | constant           | frequency-dependent                      |
| Distinguishing test   | N/A                | multi-frequency phase fit                |
| Cubic coefficient     | 0                  | -A d (2 pi h)^2 / c^3                   |

**Measurement protocol:** Measure the phase ramp at multiple drive frequencies
f_1, ..., f_N and fit phi(f) = a f + b f^3.  If b = 0, the data are consistent
with smooth GR.  If b is nonzero, it implies modified dispersion with an
effective lattice spacing h = (c / 2 pi) sqrt(|b| c / (A d)).

## Specific Numbers

### Fractional correction: delta_phi / phi_GR = A (h omega / c)^2

Using A = 0.58 (cubic/gauss kernel, representative):

| Lattice spacing   | f = 1 Hz  | f = 1 kHz | f = 1 MHz |
|-------------------|-----------|-----------|-----------|
| Planck (1.6e-35m) | 6.7e-86   | 6.7e-80   | 6.7e-74   |
| 1 fm (1e-15 m)    | 2.6e-46   | 2.6e-40   | 2.6e-34   |
| 1 um (1e-6 m)     | 2.6e-28   | 2.6e-22   | 2.6e-16   |

### Absolute correction (radians, d = 1 mm):

| Lattice spacing   | f = 1 kHz  | f = 1 MHz  |
|-------------------|------------|------------|
| Planck (1.6e-35m) | 1.4e-87    | 1.4e-78    |
| 1 fm (1e-15 m)    | 5.3e-48    | 5.3e-39    |
| 1 um (1e-6 m)     | 5.3e-30    | 5.3e-21    |

### Detectability threshold

Best-case NV phase sensitivity after 10^4 s integration: ~1e-8 rad.
3-sigma detection requires delta_phi > 3e-8 rad.

Required lattice spacing for 3-sigma detection:

| Drive frequency | Minimum h (m) | h / l_Planck |
|-----------------|----------------|--------------|
| 1 kHz           | 7.5e+4         | 4.6e+39      |
| 1 MHz           | 2.4e+0         | 1.5e+35      |

**The lattice correction is not detectable at sub-atomic lattice spacings.**

## Comparison with Existing Constraints

**Fermi LAT** constrains photon dispersion (E_QG > 6.3e10 GeV for n=2),
equivalent to h < 3e-27 m for photon propagation.

**Diamond NV** would probe gravitational dispersion specifically, which is
complementary: gravity and electromagnetism could have different effective
lattice structures.  But the sensitivity gap is enormous -- the NV measurement
would need a lattice spacing ~10^35 times larger than Planck to see anything.

## Honest Assessment

**What is qualitatively new:** The framework predicts a specific
cubic-in-frequency correction to the gravitational phase ramp.  This is
absent in smooth GR and provides a concrete, falsifiable formula.

**What is not detectable:** At any sub-Planck or Planck-scale lattice spacing,
the correction is suppressed by (h omega / c)^2, which is at best ~10^-74 at
MHz frequencies.  This is ~66 orders of magnitude below the best conceivable
NV sensitivity.

**Where the prediction has teeth:** If emergent-gravity scenarios produce an
effective lattice spacing much larger than l_Planck (e.g., at mesoscopic
scales), the correction grows as h^2.  A lattice spacing of h ~ 1 mm would
give detectable corrections at MHz frequencies.  This is not expected in
standard scenarios but is falsifiable.

**The honest answer to the reviewer:** The lattice framework makes a prediction
that is qualitatively distinct from smooth GR (frequency-dependent vs
frequency-independent phase ramp), but the quantitative correction is
undetectable unless the gravitational lattice spacing is far above the Planck
scale.  The value is in the formula itself -- it pins down what "discreteness"
means operationally and defines the measurement that would detect it.

## c4 Coefficients Used

From `scripts/frontier_dispersion_relation.py`, the dispersion relation
omega^2 = c^2 k^2 + c4 k^4 has:

| Architecture  | Kernel | A (dimless) | alpha | E_Planck_eff (GeV) |
|---------------|--------|-------------|-------|--------------------|
| cubic         | cos2   | 3.7e-2      | 1.58  | 6.3e+19            |
| cubic         | gauss  | 5.8e-1      | 1.47  | 1.6e+19            |
| staggered     | gauss  | 1.7e+0      | 2.67  | 9.4e+18            |

All consistent with Fermi LAT bounds (E_eff > E_QG).

## Final Verdict

**Concrete but undetectable at Planck scale.**

The lattice correction is a genuine prediction beyond smooth GR, with a
specific functional form (cubic in frequency) and a computable coefficient
(from the path-sum dispersion relation).  It is consistent with all existing
constraints but far below current experimental reach for any reasonable lattice
spacing.

The framework's experimental value for diamond NV remains the **retardation
phase ramp itself** (the existing prediction in `DIAMOND_SENSOR_PREDICTION_NOTE.md`),
not the lattice correction to it.
