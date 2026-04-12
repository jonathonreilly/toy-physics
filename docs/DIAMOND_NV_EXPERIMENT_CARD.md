# Diamond NV Center Experiment Card

**Date:** 2026-04-12
**For:** Experimentalist collaborator (NV center lab)
**Status:** bounded review candidate -- lab-facing experiment card

---

## Overview

This card describes three experiments using a nitrogen-vacancy (NV) center
in diamond, each testing a different prediction from a discrete spacetime
framework. They are ordered by feasibility: Experiment 1 is doable with
equipment most NV labs already have. Experiment 3 is a reach goal.

All three share the same NV platform and most of the same hardware. A lab
that sets up for Experiment 1 is most of the way to Experiment 2.

## Claim boundary

- this is a lab-facing proposal card, not a retained result
- the gravitational Born-rule experiment is the highest-feasibility proposal,
  but it is not yet an executed experiment
- the retardation / lattice-correction lane remains below detectability in the
  current support note

---

## Experiment 1: Born Rule Test in a Gravitational Field

### What we are testing

The Born rule says that quantum probabilities come from squaring amplitudes.
A consequence: when you have three possible paths through an interferometer,
ALL interference is pairwise. There is no genuine three-way interference.

This is quantified by the Sorkin parameter:

    I_3 = P_123 - P_12 - P_13 - P_23 + P_1 + P_2 + P_3

where P_ij is the detection probability with paths i and j open, etc.

Standard quantum mechanics predicts I_3 = 0 exactly. This has been tested
optically (Sinha et al., Science 2010) but never in a gravitational field.

**Why gravity matters:** Some quantum gravity proposals (e.g., nonlinear
modifications to quantum mechanics near mass) predict I_3 deviates from zero
when gravity is involved. Our framework predicts I_3 = 0 exactly, as a
structural theorem -- not an assumption. Testing this with a nearby mass is
the cleanest way to probe whether gravity modifies the Born rule.

### The NV three-path interferometer

The NV center ground state has three spin sublevels: m_s = -1, 0, +1.
These serve as three paths in a spin interferometer.

**Key advantage over optical setups:** The three paths are internal spin
states of a single defect in a rigid crystal lattice. There is no beam
alignment, no slit diffraction, no classical-path ambiguity. The "which
path" control is done with microwave pulses.

### Equipment

| Item | Specification | Purpose |
|------|---------------|---------|
| Diamond sample | Electronic-grade CVD, [NV] > 10 ppb, [N] < 1 ppm | Host crystal |
| Cryostat | 4 K closed-cycle (optional; RT works with shorter T2) | Extend coherence |
| Microwave source | 2.87 GHz +/- 200 MHz, <1 ns pulse edges | Spin rotations |
| Microwave antenna | Coplanar waveguide on diamond surface | Uniform drive |
| 532 nm laser | >100 mW, pulsed (AOM-switched, <1 us rise) | NV initialization and readout |
| Photon counter | SPCM or sCMOS, >60% QE at 637-800 nm | Fluorescence detection |
| Permanent magnet | ~50 G aligned along NV axis | Split m_s = +/-1 |
| Source mass | 1 kg tungsten alloy sphere, 31 mm diameter | Gravitational perturbation |
| Positioning stage | Micrometer stage, 5-50 mm travel | Set source-NV distance |
| Vibration isolation | Optical table with active legs | Suppress seismic noise |

### Pulse sequence

The protocol uses generalized Ramsey interferometry across all three
sublevels. One full measurement cycle:

```
Step 1:  532 nm laser pulse, 3 us        → initialize into |0>
Step 2:  MW1 pulse at f_(-1,0), angle a  → create |0> + c1|-1> superposition
Step 3:  MW2 pulse at f_(0,+1), angle b  → distribute into |-1>, |0>, |+1>
Step 4:  Free evolution, time tau         → accumulate phase (gravity acts here)
Step 5:  MW2 pulse, angle b'             → recombine
Step 6:  MW1 pulse, angle a'             → recombine
Step 7:  532 nm laser pulse, readout      → measure fluorescence (projects onto |0>)
```

The angles a, b, a', b' are chosen to implement all seven slit
configurations needed for the Sorkin test:

| Configuration | Open paths | How to set |
|---------------|-----------|------------|
| P_1 | m_s = -1 only | a = pi, b = 0 |
| P_2 | m_s = 0 only | a = 0, b = 0 |
| P_3 | m_s = +1 only | a = 0, b = pi |
| P_12 | -1 and 0 | a = pi/2, b = 0 |
| P_13 | -1 and +1 | a = pi, b = pi/2 |
| P_23 | 0 and +1 | a = 0, b = pi/2 |
| P_123 | all three | a = pi/2, b = pi/2 |

(Exact angles require calibration. The table gives the concept; the lab
should optimize using state tomography before running.)

### With and without the source mass

Run the full Sorkin protocol twice:

1. **Mass absent (control):** Source mass retracted to >1 m away.
   Measures I_3 under normal lab conditions.
   Expected: I_3 = 0 within statistical error.

2. **Mass present:** 1 kg tungsten sphere positioned 1 cm from diamond.
   Gravitational acceleration at NV: g_source = GM/r^2 = 6.67e-7 m/s^2.
   Gravitational potential difference across NV: delta_phi_grav ~ 2e-26 eV
   (for 1 nm NV extent -- tiny, but the test is about I_3 = 0 vs nonzero,
   not the absolute phase).

### Expected signal size

The Sorkin parameter is a *difference of probabilities*, not a tiny phase.
Each P value is measured as a fluorescence contrast, typically 5-30%
depending on readout fidelity.

**Framework prediction:** I_3 / P_123 < 10^-14 (structural zero, limited
only by floating-point arithmetic in theory; in practice by counting
statistics).

**Statistical sensitivity:** With single-NV readout (~0.03 photons per
shot distinguishing bright vs dark):
- Per-shot Sorkin uncertainty: ~0.1 (dominated by photon shot noise)
- After N = 10^9 shots (typical, ~3 hours at 100 kHz rep rate):
  delta(I_3/P) ~ 3e-5
- After N = 10^12 shots (~100 hours):
  delta(I_3/P) ~ 3e-6

**Best existing optical bound:** |I_3/P| < 10^-2 (Sinha et al. 2010).
This NV measurement should beat that by 3 orders of magnitude because the
interferometer is intrinsically stable (no beam pointing drift).

### Integration time

| Target precision | Shots needed | Time at 100 kHz | Comment |
|------------------|-------------|-----------------|---------|
| 10^-2 (match optical) | 10^6 | 10 sec | Trivial |
| 10^-4 | 10^10 | 28 hours | Publishable |
| 10^-5 | 10^12 | 4 months | Deep bound |

**Recommendation:** Run for 10^10 shots total (split equally between mass
present and mass absent). This gives a publishable result in a few days.

### Control measurements

1. **No mass (baseline):** Full Sorkin protocol, mass retracted.
   Establishes instrument-level I_3 floor.

2. **Mass present, no free evolution (tau = 0):** Verifies the MW pulses
   are not affected by the source mass (e.g., stray magnetic fields from
   paramagnetic impurities in the tungsten).

3. **Mass present, known magnetic source substituted:** Replace tungsten
   with a small permanent magnet at same position. The magnetic field
   produces large, known spin splittings. If I_3 remains zero with the
   magnet, the protocol is validated; if not, there is a systematic error
   in the pulse calibration.

4. **Mass position varied (1 cm, 2 cm, 5 cm, retracted):** If I_3 is
   truly gravitational, it should depend on distance. If it does not, the
   signal is an artifact.

5. **Permutation check:** Relabel which sublevel is "path 1" vs "path 2"
   vs "path 3" by changing the magnetic field alignment. I_3 should be
   invariant under relabeling.

### What constitutes a result

**If I_3 = 0 (within error) with mass present:**
- First matter-wave Born rule test in a gravitational field.
- Confirms framework prediction (structural theorem, not a tunable parameter).
- Sets a quantitative bound: |I_3/P| < X at 95% CL in presence of
  gravitational potential.
- Write-up: "Born rule holds to [X] in gravitational field: test with
  diamond NV spin interferometer."

**If I_3 is nonzero with mass present (but zero without):**
- Discovery of gravity-induced violation of the Born rule.
- Falsifies the framework's structural theorem.
- Also falsifies standard quantum mechanics near gravitating masses.
- Would be the biggest result in quantum foundations in decades.
- Write-up: immediate Physical Review Letters, then extended analysis.

### How the Nature paper looks

**Title:** "Testing the Born Rule in a Gravitational Field with a Diamond
Spin Interferometer"

**Key result figure:** Plot I_3/P vs gravitational potential (varied by
source distance). Flat line at zero = Born rule confirmed. Any slope =
discovery.

**Novelty claim:** First test of quantum superposition rule (not just
coherence) in the presence of a controlled gravitational source.

---

## Experiment 2: Gravitational Phase Shift on NV Spin (NV Analog of COW)

### What we are testing

The classic Colella-Overhauser-Werner (COW) experiment showed that neutrons
in a superposition acquire a gravitational phase shift. This is the NV
spin analog: put a single spin in a superposition, let it accumulate phase
from a nearby mass, and read out the phase shift.

**Framework prediction:** The gravitational potential produces a phase
shift on the NV spin coherence:

    delta_phi = (g_source * m_eff * tau) / hbar

where g_source = GM/r^2 from the tungsten mass, m_eff is the effective
gravitational coupling of the NV spin states (this is the key unknown --
it depends on how the spin states couple to gravity, which is a ~meV
zero-point energy difference), and tau is the free evolution time.

The framework additionally predicts that the Born rule is exactly preserved
during this phase accumulation (no decoherence from gravity itself).

### Equipment

Same as Experiment 1, plus:

| Item | Specification | Purpose |
|------|---------------|---------|
| Lock-in amplifier | Stanford SR860 or equivalent | Phase-sensitive detection |
| Function generator | 1-100 kHz sine, <1 ppm stability | Source mass modulation |
| Piezo actuator | Thorlabs PAS009, 9 um travel, 10 kHz BW | Oscillate source mass |

### Measurement protocol

**Ramsey interferometry with gravitational source:**

```
Step 1:  532 nm laser, 3 us            → initialize |0>
Step 2:  MW pi/2 pulse                  → create (|0> + |1>) / sqrt(2)
Step 3:  Free evolution, tau            → gravity accumulates phase
Step 4:  MW pi/2 pulse (phase scanned)  → convert phase to population
Step 5:  532 nm laser, readout          → measure fluorescence
```

Scan the phase of the second pi/2 pulse to trace out a Ramsey fringe.
The gravitational phase shift displaces the fringe pattern.

**Differential measurement:**
- Alternate: 100 shots with mass at r_near, 100 shots with mass at r_far
- The fringe shift between the two positions is the gravitational signal.
- Common-mode rejection of magnetic drift, temperature drift, laser
  fluctuations.

### Expected signal size

This is where honesty is required. The gravitational phase on a spin
is extremely small.

**Gravitational potential at NV from 1 kg at 1 cm:**

    Phi = -GM/r = -6.67e-9 m^2/s^2

**Phase shift on NV spin (optimistic estimate):**

The spin states m_s = 0 and m_s = 1 differ in zero-point energy by the
spin-spin interaction (~2.87 GHz = 1.2e-5 eV). If this energy couples
gravitationally:

    delta_phi = (delta_E * Phi) / (hbar * c^2)
              = (1.2e-5 eV)(6.67e-9 m^2/s^2) / (6.58e-16 eV*s)(9e16 m^2/s^2)
              ~ 1.4e-15 rad

This is far below single-shot sensitivity (~1 rad). After N shots:

    delta_phi_min = 1 / sqrt(N)

To reach 1.4e-15 rad at SNR = 3: N = (3 / 1.4e-15)^2 = 4.6e30 shots.
At 100 kHz, that is 1.5e18 years.

**This experiment is not feasible with a single NV center and a 1 kg mass.**

### What makes it feasible

Two paths to a viable signal:

**Path A -- NV ensemble (10^12 NVs):**
Sensitivity improves by sqrt(N_NV) ~ 10^6. Required integration:
~4.6e18 shots / ensemble, or ~1.5e6 years. Still not feasible.

**Path B -- Larger mass, closer approach, mechanical coupling:**
The direct gravitational phase on a spin is too small. But the mass
produces gravitational acceleration on the *diamond crystal itself*:

    a = GM/r^2 = 6.67e-7 m/s^2 at 1 cm

Over free evolution tau = 1 ms, the diamond moves:

    delta_x = (1/2) a tau^2 = 3.3e-13 m = 0.33 pm

This displacement strains the lattice, and NV centers are excellent
strain sensors (sensitivity ~10^-5 strain / sqrt(Hz) for ensembles).

**Strain-mediated gravitational signal:**

    strain = delta_x / L_diamond

For a 2 mm diamond: strain ~ 1.7e-10.
NV ensemble strain sensitivity: ~10^-10 / sqrt(Hz) (demonstrated).
SNR = 1 in 1 second. SNR = 3 in 9 seconds.

**This is the viable path.** The gravitational signal is detected as a
strain on the diamond, not as a direct spin phase.

### Revised protocol (strain-mediated)

1. Mount diamond on a thin cantilever (100 um thick, 2 mm long).
2. Place 1 kg tungsten at 1 cm from cantilever tip.
3. Modulate source position at 1 kHz using piezo.
4. Use NV ensemble with lock-in detection at the drive frequency.
5. Measure strain amplitude and phase vs source distance.

**Expected signal:**
- Gravitational strain at 1 cm: ~1.7e-10 (oscillating at drive frequency)
- NV strain sensitivity (ensemble, 1 Hz BW): ~10^-10 / sqrt(Hz)
- SNR after 100 s integration: ~17

### Control measurements

1. **Mass retracted:** Signal should vanish.
2. **Magnetic shielding variation:** Add/remove mu-metal. If signal changes,
   there is magnetic contamination from the source mass.
3. **Seismic substitution:** Replace gravitational drive with a calibrated
   acoustic/seismic drive at same frequency. Verifies the detection chain
   independently.
4. **Distance sweep (1 cm, 2 cm, 5 cm):** Signal should scale as 1/r^2.
   This is the key physics check.
5. **Frequency sweep (100 Hz to 10 kHz):** Strain coupling should be
   frequency-independent below the cantilever resonance. Any resonance
   structure is mechanical, not gravitational.

### What constitutes a result

**If strain signal is detected scaling as 1/r^2:**
- NV-center detection of Newtonian gravitational acceleration.
- Analog of the COW experiment using a solid-state spin sensor.
- Framework prediction confirmed: the phase (strain) follows the
  expected potential, and coherence is preserved.

**If coherence degrades in the presence of the mass:**
- Potential evidence for gravity-induced decoherence.
- Contradicts the framework (which predicts exact Born rule preservation).
- Requires careful control for vibration-induced decoherence.

### How the Nature paper looks

**Title:** "Gravitational Acceleration Detected by a Diamond Spin Sensor"

**Key figure:** Strain signal vs 1/r^2 showing Newtonian scaling.
Secondary figure: NV coherence (T2) unchanged with/without mass.

---

## Experiment 3: Retardation Phase Ramp (Finite Propagation Speed)

### What we are testing

General relativity predicts that changes in the gravitational field
propagate at the speed of light. For a mass oscillating at frequency f
near an NV sensor at distance d, the gravitational signal arrives with
a time delay:

    delta_t = d / c

This produces a phase lag in a lock-in measurement:

    phi_lag = 2 * pi * f * d / c

At d = 1 mm, f = 1 kHz: phi_lag = 2.1e-8 rad.

The framework makes an additional prediction beyond smooth GR: the
discrete graph structure produces a **cubic-in-frequency correction**
to the phase ramp:

    phi(f) = 2 pi f d / c + b f^3

where b depends on an effective lattice spacing h:

    b = -A d (2 pi h)^2 / c^3

with A ~ 0.04 to 1.7 (architecture-dependent, computed from the
framework's dispersion relation).

### Equipment

Same as Experiment 2, plus:

| Item | Specification | Purpose |
|------|---------------|---------|
| Piezo actuator (upgraded) | PI P-885.11, 1 kHz - 100 kHz BW | High-frequency source drive |
| Lock-in amplifier (dual) | Zurich HF2LI, DC - 50 MHz | Quadrature detection |
| NV ensemble array | 10^10+ NVs in 2 mm x 2 mm x 0.5 mm diamond | High strain sensitivity |
| Widefield imaging (optional) | sCMOS camera, 1 um resolution | Spatial phase ramp |
| Mu-metal shielding | 3-layer, >60 dB at DC | Magnetic isolation |
| Vibration isolation (upgraded) | Active + passive, <1 nm at 1 kHz | Suppress mechanical coupling |

### Measurement protocol

1. Drive the 1 kg tungsten source at frequency f using the piezo.
2. Lock-in detection of the NV strain signal at frequency f.
3. Record both channels: X (in-phase) and Y (quadrature).
4. The retardation signal appears in the **Y channel**.
5. Sweep f from 100 Hz to 100 kHz.
6. Plot phi(f) = atan2(Y, X) vs f.

### Expected signal (honest numbers)

**GR retardation (the smooth part):**

| Distance d | Drive freq f | Phase lag phi | Delay delta_t |
|-----------|-------------|---------------|---------------|
| 1 mm | 1 kHz | 2.1e-8 rad | 3.3e-12 s |
| 1 mm | 10 kHz | 2.1e-7 rad | 3.3e-12 s |
| 1 mm | 100 kHz | 2.1e-6 rad | 3.3e-12 s |
| 10 mm | 10 kHz | 2.1e-6 rad | 3.3e-11 s |

**Framework lattice correction (the new part):**

| Lattice spacing h | Drive freq f | Fractional correction |
|-------------------|-------------|----------------------|
| Planck (1.6e-35 m) | 1 MHz | 6.7e-74 |
| 1 fm (1e-15 m) | 1 MHz | 2.6e-34 |
| 1 um (1e-6 m) | 1 MHz | 2.6e-16 |

**The lattice correction is undetectable at any reasonable lattice spacing.**
This is stated honestly: the cubic term is interesting theoretically but
unmeasurable. The experiment's value is in detecting the **linear term**
(the GR retardation) itself.

**NV phase sensitivity (state of the art):**
- Single NV: ~10 urad / sqrt(Hz) for strain
- Ensemble (10^10 NVs): ~100 nrad / sqrt(Hz)
- After 10^4 s integration: ~1 nrad = 10^-9 rad

The GR retardation phase of ~2e-7 rad at 10 kHz, 1 mm distance is
**above** the detection threshold for an ensemble measurement with
10^4 s integration (SNR ~ 200).

**However:** The X channel (in-phase gravitational strain) is ~10^-10 strain.
The Y channel (retardation quadrature) is a fraction phi_lag ~ 2e-7 of the
X channel. So:

    Y_signal ~ X_signal * phi_lag ~ 10^-10 * 2e-7 = 2e-17 strain

This is 7 orders of magnitude below the ensemble noise floor.

**Honest verdict: the retardation quadrature is not detectable with
current NV technology at lab-accessible distances and frequencies.**

### What could change this

1. **Cavity-enhanced NV strain sensing:** Emerging techniques coupling NV
   to optical or microwave cavities may improve sensitivity by 10^3-10^4.
2. **Larger source mass or closer approach:** A 100 kg source at 1 mm
   (engineering challenge, not physics) would gain 10^4 in signal.
3. **Higher frequency drive:** At 1 MHz drive, the phase lag is 2e-5 rad,
   but mechanical coupling becomes the dominant systematic.

### Control measurements (if attempting)

1. **Drive off:** Y should be consistent with zero.
2. **Source retracted:** Y should vanish.
3. **Pi phase flip in reference:** Y should change sign.
4. **Static source (no modulation):** Removes any DC or drift contribution.
5. **Known magnetic source at same position:** Calibrates the lock-in
   pipeline. Magnetic signals propagate at c, so a magnetic source at
   close range should also show near-zero retardation (phi_lag ~ 10^-8 rad
   at 1 kHz, 1 mm -- comparable to gravity, serving as a cross-check).
6. **Multi-frequency sweep:** Fit phi(f) = a*f + b*f^3. If b = 0, data
   are consistent with smooth GR. If b is nonzero, extract effective
   lattice spacing h.

### What constitutes a result

**If Y channel is nonzero, scaling as f, surviving all controls:**
- First direct detection of gravitational retardation at lab scales.
- Confirms that gravity propagates at finite speed (GR prediction).
- The framework and GR agree on this prediction.

**If Y channel shows cubic-in-frequency deviation:**
- Evidence for modified dispersion in gravitational sector.
- Extracts effective lattice spacing: h = (c/2pi) * sqrt(|b|*c / (A*d)).
- Would be evidence for discrete spacetime structure.
- Almost certainly an artifact at current sensitivity levels -- require
  extraordinary controls.

**If Y = 0 after exhaustive integration:**
- Sets upper bound on gravitational retardation at lab scales.
- Constrains alternative theories with anomalous propagation speeds.
- Does not falsify GR or the framework (signal may simply be below
  noise floor).

### How the Nature paper looks

**Title:** "Search for Gravitational Field Retardation at Laboratory
Scales Using a Diamond Spin Sensor"

**Key figure:** Phase vs frequency showing upper bound on retardation.
If detected: phase vs frequency with linear fit yielding propagation
speed consistent with c.

---

## Summary Table

| | Experiment 1 | Experiment 2 | Experiment 3 |
|---|---|---|---|
| **What** | Born rule (I_3) in gravity | Gravitational phase on spin | Retardation quadrature |
| **Signal type** | Probability (counting) | Strain (lock-in) | Phase lag (quadrature) |
| **Expected signal** | I_3 = 0 exactly | ~10^-10 strain at 1 cm | ~2e-7 rad phase lag |
| **Detectable?** | Yes | Yes (strain-mediated) | Marginal to No |
| **New equipment** | Tungsten mass + stage | + piezo + lock-in | + high-BW piezo + shielding |
| **Integration time** | Days | Minutes to hours | Weeks (if detectable) |
| **Framework tests** | Born rule structural theorem | Phase = GM/r, coherence | Retardation + dispersion |
| **If null** | Born rule confirmed in gravity | Expected Newtonian scaling | Upper bound on retardation |
| **If signal** | Post-quantum gravity discovery | NV gravitational detection | Lab-scale GR verification |
| **Feasibility** | High | Medium-High | Low |

---

## Recommended Execution Order

1. **Start with Experiment 1.** It requires the least additional equipment,
   produces a publishable result regardless of outcome, and tests the most
   fundamental prediction. A null result (I_3 = 0) is the first Born rule
   test in a gravitational field. A positive result would be a discovery.

2. **Add Experiment 2 hardware (piezo + lock-in) for the strain measurement.**
   This is a natural extension: same diamond, same NV centers, same mass.
   The strain-mediated gravitational detection is achievable with current
   technology and would be noteworthy as a solid-state gravitational sensor
   demonstration.

3. **Attempt Experiment 3 only if Experiment 2 succeeds with high SNR.**
   The retardation measurement requires the gravitational strain detection
   to work first, then pushes for the much smaller quadrature signal.
   Consider this a reach goal for a second-generation setup.

---

## Contact and Attribution

This experiment card is derived from the graph-first discrete spacetime
framework documented at [repository]. The specific predictions tested are:

- **I_3 = 0 (Born rule):** Structural theorem from linearity of the
  path-sum propagator. Numerically verified to |I_3/P| < 10^-14 across
  all tested configurations.

- **Gravitational phase = GM/r:** Standard Newtonian prediction, also
  reproduced by the framework's Poisson-coupled propagator.

- **Retardation phase = 2*pi*f*d/c:** Standard GR prediction, reproduced
  by the framework's causal (retarded) propagator. Lattice correction
  (cubic in frequency) is a framework-specific prediction beyond GR.

The framework makes these predictions as consequences of a single
structure (graph, propagator, growth rule). The experiments test the
predictions on their own terms -- a positive or null result is
informative regardless of the framework's ultimate fate.
