# Accessible Predictions: Where the Framework Differs from GR

**Script:** `scripts/frontier_accessible_prediction.py`
**Date:** 2026-04-12

## Problem

The lattice corrections at Planck spacing are ~10^{-58} -- useless for any
foreseeable experiment. We need predictions from regimes where the framework
and classical GR **disagree**, independent of the lattice spacing.

## Key Insight

The framework treats gravity as sourced by the quantum density rho = |psi|^2.
Classical GR has no such structure. The disagreement appears whenever
**quantum features of the source matter** -- spatial superpositions,
self-consistent backreaction, and the correlation between Born rule
precision and gravitational precision.

## Five Approaches Ranked

### #1: BMV Gravitational Entanglement [TESTABLE, 5-15 years]

**Prediction:** Gravity mediates entanglement between two masses in
spatial superposition. Classical GR predicts no entanglement.

**Numbers:**
- BMV proposal (m = 10 pg, d = 200 um): delta_phi ~ 10^5 rad -- large signal
- MAQRO (m = 1 fg, d = 500 um): delta_phi ~ 0.05 rad -- marginal
- Entanglement phase = G m^2 T / (hbar d)

**Status:** Does NOT depend on lattice spacing. Tests quantum nature of gravity.
Shared prediction with other quantum gravity approaches (not unique to framework).

### #2: Born-Gravity Cross-Constraint [TESTABLE NOW, unique]

**Prediction:** The Born rule (I_3 = 0) and Newton's mass law (beta = 1) are
both consequences of linear amplitude superposition. Any deviation in one
requires a deviation in the other:

    |beta - 1| ~ sqrt(|I_3/I_1|)

**Numbers from existing experiments:**
| I_3 bound | Source | Implied gravity precision |
|-----------|--------|--------------------------|
| 10^{-2} | Sinha 2010 | beta = 1 to 10% |
| 10^{-4} | Kauten 2017 | beta = 1 to 1% |
| 10^{-8} | Future 2030 | beta = 1 to 0.01% |
| 10^{-12} | Ultimate | beta = 1 to 0.0001% |

**Status:** UNIQUE to this framework. No other theory links Born rule to gravity.
Can be checked with CURRENT experimental data. Falsifiable: if I_3 < 10^{-8}
but gravity deviates at 10^{-3}, the framework is killed.

### #3: Extended Source Potential [TESTABLE, 10-20 years]

**Prediction:** A quantum wavepacket of width sigma has gravitational potential:

    phi(r) = -(Gm/r) * erf(r / (sqrt(2) sigma))

At r = sigma, the force deviates from Newton by 80%. At r = 3 sigma, 3%.
At r = 5 sigma, negligible.

**Challenge:** Wavepacket widths for massive objects are tiny:
- Microsphere (10^12 amu) in kHz trap: sigma ~ 10^{-13} m
- Nanoparticle in free fall (100s): sigma ~ 3 nm

Requires creating macroscopic quantum superpositions (sigma > 1 um) and measuring
gravity at that scale simultaneously.

### #4: Mesoscopic Backreaction [TESTABLE, 15-25 years]

**Prediction:** Self-gravitating wavepacket width deviates from free Gaussian when:

    alpha = G m^3 sigma / hbar^2 ~ 1

**Transition mass at sigma = 1 um:** m ~ 5.5 x 10^{-18} kg (3.3 x 10^9 amu)
**Current matter-wave record:** m ~ 10^{-23} kg (10^4 amu)
**Gap:** factor of ~10^5 in mass

The Penrose threshold (~10^{-17} kg) is in the regime where alpha ~ 0.5
(MEASURABLE but not collapsing).

### #5: Next-Order Decoherence Correction [NOT TESTABLE]

**Prediction:** The decoherence rate correction scales as r_S / sigma = 2Gm/(c^2 sigma).
For m = 10^{-14} kg: correction ~ 10^{-35}. Unmeasurable.

## Key Finding

Three of five predictions are **independent of the lattice spacing**. They arise
from the quantum treatment of gravity (rho = |psi|^2 sources Poisson), not from
the discrete graph structure. This escapes the 10^{-58} prison of Planck-scale
corrections.

The **Born-gravity cross-constraint** (#2) is the most powerful because:
1. Testable with current experimental data
2. Unique to this framework
3. Falsifiable
4. Requires no new experiment -- just comparing existing I_3 and ISL data

The **BMV entanglement** (#1) is the most dramatic but is shared with other
quantum gravity approaches.

## Falsification Criteria

The framework is falsified if ANY of the following are observed:
- Gravitational entanglement is absent in a BMV-class experiment
  (classical GR confirmed, quantum gravity ruled out)
- I_3 < 10^{-8} but gravity deviates from Newton at > 10^{-3}
  (violates the cross-constraint)
- A massive object in a verified spatial superposition produces a
  point-mass gravitational field (contradicts rho = |psi|^2 sourcing)
