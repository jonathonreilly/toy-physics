# Literature Anomaly Search: Framework Predictions vs Experimental Record

**Date:** 2026-04-12
**Status:** literature survey, bounded claims only

## Purpose

Systematic search of the experimental literature for anomalies or precision
measurements that could be compared with predictions of the graph-propagator
gravity framework. The framework produces: unitary propagation on a discrete
graph, self-consistent Poisson field, Born rule (I3 = 0 exact), inverse-square
force law with finite-lattice corrections of order (a/L)^2.

---

## 1. Big G Measurement Scatter

### Experimental status

The Newtonian gravitational constant G = 6.67430(15) x 10^-11 m^3 kg^-1 s^-2
(CODATA 2018) has a relative uncertainty of 22 ppm, making it by far the least
precisely known fundamental constant. The scatter among published measurements
exceeds 500 ppm peak-to-peak, and many results disagree at 5-7 sigma.

Key references:
- CODATA 2018 adjustment (Tiesinga et al., Rev. Mod. Phys. 2021)
- PNAS overview (Schlamminger, 2016)
- Nature 2018 (Li et al., two independent methods)

Different experimental geometries (torsion balance, beam balance, atom
interferometry, pendulum) give systematically different values. The BIPM
torsion balance results are ~200 ppm above the CODATA mean. NIST is currently
repeating the BIPM measurement with the original apparatus to investigate.

### Framework prediction

The framework predicts finite-lattice corrections to the gravitational
potential: V(r) -> V(r) * [1 + C_lat * (a/r)^2], where a is the graph
spacing. At Planck scale (a ~ l_P), this correction is ~10^-58 for
laboratory separations and completely undetectable.

However, the framework also predicts that the effective coupling depends on
the self-consistent field solution, which in turn depends on the geometry of
the experimental mass distribution. Different experimental geometries probe
different regions of the self-consistent field, and finite-size corrections
to the Poisson solver depend on boundary conditions. On a finite graph, the
effective G measured by different experimental setups could differ by
O((a/L_experiment)^2) corrections.

### Assessment

**Consistent but not explanatory.** If a = l_Planck, the predicted geometry
dependence is negligible (~10^-58). The observed ~500 ppm scatter requires
either a >> l_Planck (constrained by gamma-ray dispersion to a < 10^-19 m)
or conventional systematic errors. The framework does not explain Big G
scatter unless the effective lattice spacing is far above the Planck scale,
which is already ruled out by other observations.

**Verdict: No match.** The scatter is almost certainly experimental
systematics, not new physics.

---

## 2. Short-Range Gravity (Sub-Millimeter Inverse-Square Law Tests)

### Experimental status

The Eotvos-Washington group (Adelberger, Kapner et al.) has tested the
gravitational inverse-square law down to 59 micrometers at 95% confidence,
finding no deviation. Constraints on Yukawa-type deviations |alpha| < 1 for
lambda > 59 um (Lee et al., PRL 2020). Earlier work constrained deviations
at 218 um to the 10^-3 level (Kapner et al., PRL 2007).

The Huazhong University group (Tan et al., PRL 2020) independently tested at
the sub-millimeter range with dual modulation, again finding no deviation.

No anomaly has been reported at any tested range.

### Framework prediction

The framework's distance law analysis shows:

- On a 3D lattice, valley-linear path summation with Coulomb field produces
  deflection delta(b) ~ 1/b^alpha with alpha = -1.001 +/- 0.004 (N >= 56).
- The force law F ~ M/r^2 is confirmed to 0.1% on the lattice.
- Finite-size corrections go as (a/r)^2, producing deviations at distances
  comparable to the lattice spacing.
- At a = l_Planck, the first detectable deviation would require probing
  distances of order l_Planck itself.

### Assessment

**Fully consistent.** The framework predicts exact 1/r^2 in the continuum
limit, with corrections only at the lattice scale. Current experiments at
59 um are 30+ orders of magnitude above the Planck length. No deviation is
predicted and none is observed.

The null result does constrain non-Planckian lattice models: if a > 59 um,
the framework would predict O(1) deviations that are ruled out.

**Verdict: Consistent null. No anomaly to explain.**

---

## 3. Sorkin I3 / Born Rule Tests (Triple-Slit Experiments)

### Experimental status

The Sorkin parameter I3 measures third-order quantum interference. Born's
rule predicts I3 = 0 exactly. Experimental tests include:

- Sinha et al. (Science 2010): photon triple slit, |kappa| < 10^-2
- Sollner et al. (Found. Phys. 2012): single-photon, |kappa| < 10^-2
- Jin et al. (PRA 2017): NV center in diamond, |kappa| < 10^-4
- Kauten et al. (New J. Phys. 2017): improved photonic, |kappa| < 10^-4
- Atom interferometry proposals (2025): targeting |kappa| < 10^-6

The tightest current bounds are at the 10^-4 level (normalized
kappa = I3 / I_max). Some nonlinear-optics experiments have observed
apparent higher-order interference, but this is attributed to exotic looped
trajectories of photons (Sawant et al., PRL 2014), not Born rule violation.

### Framework prediction

The framework produces I3 = 0 at machine precision (~10^-15) across all
tested graph families, lattice sizes, and propagator architectures. This is
exact, not approximate -- it follows from the linearity of the path-sum
propagator and the Born rule structure of the probability assignment.

Specific retained values:
- Directional measure propagator: |I3|/P = 9.2e-16
- Mirror family: |I3|/P = 1.08e-15
- Grown geometry: |I3|/P = 1.456e-15
- All tested families: |I3|/P < 2e-15 (machine epsilon)

### Assessment

**Fully consistent, and a strong structural prediction.** The framework
predicts I3 = 0 exactly, and all experiments confirm I3 = 0 within their
sensitivity. The framework's prediction is 11 orders of magnitude sharper
than the tightest experimental bound.

This is not an anomaly match -- it is a consistency check. But the strength
of the prediction (exact zero from linearity, not approximate zero from
cancellation) is notable. Any future detection of I3 != 0 would falsify
the framework.

**Verdict: Strong consistency. Framework predicts exact zero; experiments
confirm zero to 10^-4. Future tightening to 10^-6 remains consistent.**

---

## 4. Neutron Quantum Bouncer (GRANIT / qBounce)

### Experimental status

Ultra-cold neutrons bouncing in Earth's gravitational field occupy discrete
quantum states with energy spacings of order peV (10^-12 eV). Two
collaborations probe these states:

- GRANIT (ILL, Grenoble): flow-through measurement, confirmed quantized
  states (Nesvizhevsky et al., Nature 2002).
- qBounce (TU Wien / ILL): Ramsey gravity resonance spectroscopy with
  resolution dE = 2 x 10^-15 eV.

The qBounce 2021 measurement (Micko et al., arXiv:2301.08583, 2023)
reported a systematic shift: the inferred local g = 9.8120(18) m/s^2
vs the classical value g_c = 9.8049 m/s^2 at the experimental site.
This is a 3.9-sigma discrepancy (delta_g/g ~ 7 x 10^-4).

The collaboration attributes this to potential systematic effects (surface
roughness, neutron velocity selection, waveguide geometry) and states it
"deserves further investigation." It has not been claimed as new physics.

### Framework prediction

The framework predicts that neutron energy levels in a gravitational
field follow standard quantum mechanics (Schrodinger equation in linear
potential) with corrections of order (a/L)^2 where L is the neutron
bouncing height (~10 um for the ground state).

At a = l_Planck: correction ~ (10^-35 / 10^-5)^2 = 10^-60. Not
detectable by any foreseeable experiment.

### Assessment

**The 3.9-sigma qBounce discrepancy is interesting but almost certainly
not explained by this framework.** The observed shift of 7 x 10^-4 in g
would require an effective lattice spacing of a ~ 10 um (comparable to the
neutron bouncing height), which is ruled out by many other experiments.

If the qBounce discrepancy persists after systematic effects are resolved,
it would be a very important result for gravitational physics generally, but
this framework does not predict a detectable shift at these scales.

**Verdict: Interesting anomaly exists (3.9 sigma), but framework
correction is 56 orders of magnitude too small to explain it.**

---

## 5. Gravitational Decoherence

### Experimental status

Pikovski et al. (Nature Physics 2015) predicted universal decoherence from
gravitational time dilation: composite objects in spatial superposition
decohere because internal degrees of freedom entangle with the center-of-mass
position via gravitational redshift. The predicted decoherence time for
micron-scale objects is ~seconds.

Current experimental status:
- No direct observation of gravitational decoherence yet.
- Molecular interferometry (Fein et al., Nature Physics 2019) has achieved
  quantum interference with ~2000-atom molecules (~25,000 amu), setting
  indirect upper bounds on environmental decoherence.
- MAQRO space mission proposal (Kaltenbaek et al.) targets direct tests with
  ~10^9 amu particles in microgravity, with projected sensitivity to the
  Diosi-Penrose decoherence rate.
- Bouwmeester group (Leiden) working on optomechanical tests.
- Current bounds are still several orders of magnitude from detecting the
  Pikovski effect or Diosi-Penrose collapse.

Donadi et al. (Nature Physics 2021) used X-ray emission data from
germanium detectors to constrain the Diosi-Penrose parameter, ruling out
the original Diosi-Penrose model with a sharp cutoff.

### Framework prediction

The framework computes the Diosi-Penrose decoherence rate with a lattice
correction:

    gamma_lattice = gamma_DP * [1 + (pi^2/6) * (a/delta_x)^2]

For MAQRO parameters (m = 10^-15 kg, delta_x = 1 um):
- gamma_DP = 0.63 Hz (tau = 1.58 s)
- Lattice fractional correction at a = l_Planck: 4.3 x 10^-58
- Required a for 1% correction: a > 78 nm

The framework also predicts decoherence from the self-consistent field
(tracing over field configurations), but the current model has not yet
produced a scalable decoherence mechanism on growing graphs (see
DECOHERENCE_DECISION_NOTE.md). This is an open problem.

### Assessment

**Consistent but not yet predictive for the decoherence rate itself.**
The lattice correction to the Diosi-Penrose rate is undetectable. The
framework's own decoherence mechanism is still under development and
does not yet produce specific quantitative predictions for comparison
with experiment.

The framework does predict that gravity mediates decoherence (via field
tracing), which is qualitatively consistent with the Pikovski mechanism.
But the quantitative prediction cannot yet be compared.

**Verdict: No anomaly. Framework consistent with current null results.
Quantitative decoherence prediction not yet available.**

---

## 6. BMV Experiment (Gravity-Mediated Entanglement)

### Experimental status

The Bose-Marletto-Vedral (BMV) experiment proposes testing whether gravity
can mediate entanglement between two masses in spatial superposition. A
positive result would demonstrate that gravity has quantum degrees of
freedom.

Current status (2025-2026):
- No experiment has been performed yet.
- Nanodiamond interferometer proposals (Pedernales et al., arXiv:2405.21029,
  2024; Mariani et al., arXiv:2410.19601, 2024) represent the closest
  approach to implementation, using nanodiamonds with NV centers as the
  quantum probes.
- Estimated mass requirement: ~10^-14 kg nanodiamonds.
- Estimated separation: ~500 um.
- Estimated coherence time: ~2 s.
- The experiment is "within the next decade" according to multiple groups.
- Theoretical debate continues about what a positive result would actually
  prove about quantum gravity (Anastopoulos and Hu, PRD 2023).

### Framework prediction

The framework predicts:
- Gravity DOES mediate entanglement (confirmed by Bogoliubov mechanism).
- Entanglement phase scales as s^2 (exact, verified across 5 orders).
- The separation exponent converges to the continuum prediction
  (-2.0) as lattice spacing decreases: alpha = -1.21 at h=0.25 (slow
  convergence, correction ~ h^0.17).
- At a = l_Planck, the lattice correction to the BMV phase is ~2.7 x 10^-63.

The framework does NOT produce a unique discrete-spacetime signature in the
BMV observable. The s^2 coupling is the same as the continuum prediction.

Qualitative prediction: a POSITIVE BMV result is expected. A NEGATIVE result
(no gravity-mediated entanglement) would falsify the framework.

### Assessment

**Consistent, with a strong qualitative prediction (gravity mediates
entanglement) but no unique quantitative signature.** The framework agrees
with all quantum gravity theories on the BMV prediction. It does not produce
a discrete correction that could distinguish lattice from continuum gravity.

**Verdict: Qualitative prediction (entanglement exists) is testable in
~5-10 years. Framework will be falsified by a negative result. No unique
lattice signature.**

---

## 7. Other Anomalies

### Tabletop gravitational wave detectors

The QUEST experiment (2025) achieved sensitivity to length changes of
10^-19 m, setting new limits on very high-frequency gravitational waves.
No anomalous signals reported. The framework does not predict detectable
high-frequency gravitational radiation from the lattice structure.

### Pioneer anomaly

The Pioneer spacecraft anomaly (anomalous deceleration of ~8.7 x 10^-10
m/s^2) was resolved by Turyshev et al. (PRL 2012) as thermal radiation
pressure. Not relevant to this framework.

### Flyby anomaly

Unexplained velocity changes during Earth flybys of spacecraft
(Anderson et al., PRL 2008) remain partially unexplained. The
magnitudes are ~mm/s, corresponding to fractional changes of ~10^-6.
This is in the regime of special-relativistic and tidal corrections,
not lattice corrections.

### 5th force searches

Dark-energy-scale fifth force searches (Adelberger et al., Prog. Part.
Nucl. Phys. 2009) constrain Yukawa couplings at the dark energy length
scale (~85 um). No deviations found. Consistent with the framework's
prediction of exact 1/r^2 in the continuum limit.

---

## Summary Table

| Area | Best experiment | Framework prediction | Match? | Anomaly? |
|---|---|---|---|---|
| Big G scatter | 500 ppm spread, CODATA 2018 | O((a/L)^2) correction, ~10^-58 at l_P | Consistent | No explanation |
| Short-range gravity | 1/r^2 to 59 um (Eotvos-Wash) | Exact 1/r^2 in continuum, alpha = -1.001 +/- 0.004 | Consistent | No anomaly |
| Born rule / I3 | |kappa| < 10^-4 (NV center) | I3 = 0 exact (10^-15) | Consistent | No anomaly |
| Neutron bouncer | g shifted 3.9 sigma (qBounce 2023) | Correction ~10^-60 | Consistent with QM | Cannot explain |
| Gravitational decoherence | No detection yet (orders of magnitude away) | gamma_DP + O(10^-58) correction | Consistent | No anomaly |
| BMV entanglement | Not yet performed (~2030) | Entanglement exists; no lattice signature | Prediction | N/A |
| Tabletop GW / 5th force | Null results | Null predicted | Consistent | No anomaly |

## Honest Assessment

**No anomaly match was found.** The framework's lattice corrections are
uniformly suppressed by (a/L)^2 ~ 10^-60 for a = l_Planck, making them
undetectable in all current and foreseeable experiments.

The framework IS consistent with the entire experimental record -- it
produces exact 1/r^2, exact I3 = 0, and predicts gravity-mediated
entanglement. But it does not explain any existing anomaly.

The most interesting experimental result encountered is the qBounce
3.9-sigma discrepancy in neutron gravitational spectroscopy (Micko et al.,
2023). This is worth monitoring, but the framework predicts corrections
56 orders of magnitude smaller than the observed shift. If this discrepancy
is confirmed as real (not systematic), it would be a major result for
gravitational physics, but this framework cannot claim it.

The one genuinely testable prediction is qualitative: the BMV experiment
should observe gravity-mediated entanglement. A negative result would
falsify the framework. But this prediction is shared by essentially all
quantum gravity theories.

## Implications for the Paper

The literature survey supports the following paper-level claims:

1. **Consistency:** The framework is consistent with all existing
   experimental tests of gravity at accessible scales.

2. **Falsifiability:** The framework makes a clear prediction for the BMV
   experiment and predicts exact I3 = 0 for arbitrarily tight Born rule
   tests.

3. **Honesty:** The framework does not predict detectable deviations from
   smooth GR at any currently accessible scale, assuming Planckian lattice
   spacing.

4. **Future observational targets:** If the lattice spacing is above the
   Planck scale (but below current gamma-ray dispersion bounds of ~10^-19 m),
   the framework predicts specific corrections to gravitational decoherence,
   BMV entanglement, and the neutron bouncer that scale as (a/L)^2 and
   could in principle be detected by future experiments.
