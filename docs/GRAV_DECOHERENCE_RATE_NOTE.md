# Gravitational Decoherence Rate for the Diamond NV Experiment

**Date:** 2026-04-12
**Script:** `scripts/frontier_grav_decoherence_rate.py`
**Depends on:** `frontier_gravitational_entanglement.py`, `frontier_accessible_prediction.py`, `frontier_diamond_nv_lattice_correction.py`

---

## Summary

This note gives the **specific gravitational decoherence rate** that the
discrete-graph framework predicts for a BMV-class diamond NV experiment.
The goal is to hand an experimentalist a concrete number.

---

## Key Results

### 1. Gravitational Decoherence Rate

For a 10 pg diamond microsphere in a 1 um superposition:

| Level | Formula | Rate (Hz) | tau (s) |
|-------|---------|-----------|---------|
| Penrose-Diosi (point) | Gm^2 / (hbar dx) | 63.3 | 0.016 |
| Gaussian wavepacket | (Gm^2)/(sqrt(pi) sigma hbar) [1 - exp(-dx^2/(4 sigma^2))] | 45.1 | 0.022 |
| + self-consistent | x [1 + c_1 r_S/sigma] | 45.1 | 0.022 |
| Physical (+ geometry) | with sphere overlap | 52.6 | 0.019 |

The self-consistent correction (r_S/sigma ~ 10^-35) is negligible. The
geometry factor for finite-size diamond spheres modifies the rate by ~17%.

### 2. Entanglement Phase (the Signal)

| Configuration | delta_x | Phi_ent (rad) | Detectable? |
|--------------|---------|---------------|-------------|
| Conservative NV | 1 um | 6.3e-3 | Marginal |
| Original BMV | 250 um | 12.4 | YES |

The BMV experiment succeeds when Phi_ent >> 1. The original BMV parameters
(delta_x = 250 um, d = 200 um) give Phi = 12 rad, which is strongly detectable.

### 3. The Decoherence Problem

For delta_x = 1 um: gamma_grav = 53 Hz, but the experiment needs gamma_total < 0.5 Hz.
The gravitational decoherence itself kills the coherence before entanglement accumulates.

For delta_x = 250 um (original BMV): gamma_grav = 0.25 Hz < 0.5 Hz. This works because
the larger superposition accumulates entanglement faster than it decoheres.

**The key ratio:** Phi_ent / (gamma_grav * T) must exceed ~1. The original BMV
parameters satisfy this.

### 4. Lattice Correction

The discrete lattice modifies the decoherence rate by:

    delta_gamma / gamma ~ (l_Planck / delta_x)^2 ~ 10^{-58}

This is undetectable for any sub-atomic lattice spacing. The lattice correction
is NOT the point of the experiment.

### 5. Born Rule Connection

If the propagator has a nonlinear perturbation beta != 1:

    delta_gamma / gamma ~ (beta - 1)

Current bounds from Eot-Wash: |beta - 1| < 10^{-5}, so the decoherence rate
is constrained to be within 10^{-5} of the linear prediction. The framework
predicts beta = 1 exactly.

This links the decoherence measurement to the Born rule test (Experiment 1
from the NV card): both measure the same propagator linearity.

---

## What the Experimentalist Should Know

1. **The gravitational decoherence rate is gamma = 52.6 Hz** for m = 10 pg,
   delta_x = 1 um, sigma = 0.5 um. This is the Gaussian-smeared Penrose-Diosi
   result with a sphere geometry correction.

2. **Use the original BMV parameters** (delta_x = 250 um) to ensure the
   entanglement phase dominates over decoherence.

3. **The framework predicts the same decoherence rate as standard
   gravitational decoherence models** to all accessible precision.
   The lattice correction is 10^{-58} -- not the experiment's target.

4. **The unique framework prediction is qualitative:** gravity mediates
   entanglement (quantum gravity), and the Born rule holds exactly during
   the process (I_3 = 0). Both can be tested with the NV setup.

5. **If a decoherence rate different from the Penrose-Diosi prediction
   is measured,** it constrains the Born rule parameter beta through
   delta_gamma/gamma ~ (beta - 1).

---

## Parameters Used

| Parameter | Value | Source |
|-----------|-------|--------|
| m (mass) | 10^{-14} kg (10 pg) | BMV proposal |
| d (separation) | 200 um | BMV proposal |
| delta_x (superposition) | 1 um / 250 um | Conservative / BMV |
| sigma (wavepacket) | 0.5 um | Ground state of optical trap |
| R (sphere radius) | 0.88 um | From m and rho_diamond = 3500 kg/m^3 |
| T (interaction time) | 2 s | BMV proposal |
| c_1 (self-consistent coeff) | 0.5 | From 1D lattice iteration |
| l_Planck | 1.616e-35 m | Fundamental |

---

## Formulas

**Penrose-Diosi:**
gamma_PD = G m^2 / (hbar delta_x)

**Gaussian wavepacket (framework Level 1):**
gamma_gauss = G m^2 / (sqrt(pi) sigma hbar) * [1 - exp(-delta_x^2 / (4 sigma^2))]

**Self-consistent correction (framework Level 2):**
gamma_SC = gamma_gauss * [1 + c_1 * r_S / sigma]
where r_S = 2Gm/c^2

**Sphere geometry (framework Level 3):**
gamma_phys = gamma_PD * f(delta_x, R) * [1 + c_1 * r_S / sigma]
where f is the Diosi sphere overlap factor

**Lattice correction:**
gamma_lat = gamma_phys * [1 + alpha_lat * (l_P / delta_x)^2]

**Born rule modification:**
gamma(beta) = gamma_phys * [1 + (beta - 1) + O((beta - 1)^2)]
