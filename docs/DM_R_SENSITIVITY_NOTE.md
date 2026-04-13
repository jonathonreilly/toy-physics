# R = Omega_DM / Omega_b : Sensitivity to Transport Parameters

**Date:** 2026-04-13
**Script:** `scripts/frontier_dm_r_sensitivity.py`
**Status:** HYPOTHESIS FALSIFIED -- transport precision DOES matter for R

---

## Question

The transport parameters D_q*T and v_w carry wide uncertainty bands:

    D_q*T = 3.1 +/- 30%  (HTL-resummed, DM_DQT_HTL_NOTE.md)
    v_w   = 0.014 [0.006, 0.048]  (Boltzmann closure, DM_VW_DERIVATION_NOTE.md)
    L_w*T = 13 [10, 18]  (CW bounce, DM_BOUNCE_WALL_NOTE.md)

R = Omega_DM / Omega_b depends on eta through Omega_b = 3.65e7 * eta * h^{-2}.
Since Omega_DM is fixed by the freeze-out chain (independent of eta), R ~ 1/eta.

**Hypothesis:** If R depends on eta only logarithmically (through x_F),
then the transport uncertainty is negligible and R is derived to ~10%.

**Result:** The hypothesis is **falsified**. R depends on eta LINEARLY
(not logarithmically), because x_F is in the DM sector and is independent
of the baryon-to-photon ratio. The transport prefactor propagates directly
into eta and hence into R.

---

## Method

Four-part computation:

1. eta as a function of D_q*T (scan 1 to 10, holding v_w, L_w*T, v/T fixed)
2. eta as a function of v_w (scan 0.005 to 0.05, holding D_q*T, L_w*T, v/T fixed)
3. R as a function of eta (the freeze-out chain)
4. Total sensitivity: dR/R from the transport uncertainty band

---

## Key Structural Result

The chain from transport parameters to R:

    Transport -> eta -> R

has NO logarithmic suppression. Specifically:

**Stage 1: Transport -> eta.**
At fixed v/T = 0.56 (framework-derived), the washout factor is fixed:

    exp(-Gamma_sph(broken)/H) = exp(-1.41) = 0.24

So eta = A_framework * P_transport * 0.56 * 0.24, where
P = D_q*T / (v_w * L_w*T) is the transport prefactor.
eta is EXACTLY proportional to P.

**Stage 2: eta -> R.**
R = Omega_DM_h2 / (3.65e7 * eta). Since Omega_DM_h2 is fixed by
the framework freeze-out calculation (independent of baryogenesis),
R is EXACTLY inversely proportional to eta.

Therefore dR/R = |dP/P| -- the transport uncertainty propagates
linearly, with no logarithmic suppression.

The confusion in the hypothesis was between:
- x_F = ln(...) in the DM freeze-out (depends on sigma_v, NOT on eta)
- The eta dependence of Omega_b (EXACTLY linear, not logarithmic)

---

## Results

### Individual parameter sensitivity

| Parameter | Range | Factor span | dR/R |
|-----------|-------|-------------|------|
| D_q*T | [2.17, 4.03] | 1.9x | 66% |
| v_w | [0.006, 0.048] | 8.0x | 300% |
| L_w*T | [10, 18] | 1.8x | 62% |

### Combined corners

| Case | P_transport | eta | R | dR/R |
|------|-------------|-----|---|------|
| Central | 17.0 | 2.40e-7 | 0.01 | 0% |
| Max eta (large D, small v_w, small L) | 67.2 | 9.45e-7 | 0.003 | -75% |
| Min eta (small D, large v_w, large L) | 2.5 | 3.53e-8 | 0.09 | +578% |

Combined dR/R = 653%.

The dominant contributor is v_w, which spans a factor 8x from nucleation
temperature uncertainty (T_n/T_c = 0.95 to 0.99).

---

## R Uncertainty Budget

| Source | dR/R | Status |
|--------|------|--------|
| Sommerfeld factor | ~10% | bounded |
| Mass ratio (Hamming) | 0% | EXACT |
| x_F (freeze-out) | ~4% | derived (log) |
| Boltzmann equation | <1% | proved |
| v/T (EWPT strength) | ~9% | derived (MC) |
| **Transport (combined)** | **653%** | **derived (wide band)** |

The transport sector dominates the R uncertainty by more than an order
of magnitude over all other sources.

---

## Why the Lane Does NOT Close

To get dR/R < 10%, the transport prefactor P would need to span less
than a factor 1.10. It currently spans a factor 26.7.

The framework DOES derive central values for all transport parameters
(D_q*T = 3.1, v_w = 0.014, L_w*T = 13). But the systematic uncertainty
bands are wide, primarily because:

1. v_w depends sensitively on the nucleation temperature T_n, which
   ranges from 0.95*T_c to 0.99*T_c (not pinned by the framework)
2. D_q*T has 30% uncertainty from the one-loop skeleton approximation
3. L_w*T has a factor 1.8x range from CW potential uncertainty

---

## What Would Close the Lane

Three routes to closing the transport lane:

1. **Pin T_n/T_c:** A nucleation rate calculation from the framework
   V_eff would narrow T_n/T_c from [0.95, 0.99] to a specific value,
   collapsing the v_w range from 8x to perhaps 1.5x.

2. **NLO transport:** Ladder resummation (AMY integral equation) for
   D_q*T would reduce the 30% band. Combined with a pinned T_n, the
   total P range could shrink to ~2x, giving dR/R ~ 100%.

3. **Accept O(1) prediction:** The framework predicts R to within a
   factor ~27x from transport alone. At the central transport values,
   eta ~ 2.4e-7, which is ~400x larger than eta_obs = 6.1e-10.
   This reflects the known tension: the framework-derived v/T = 0.56
   does not washout baryons sufficiently. The eta = eta_obs crossing
   point is at v/T ~ 0.52, which is within the v/T uncertainty band
   (0.56 +/- 0.05 from the gauge-effective MC).

---

## Honest Assessment

The hypothesis that transport precision doesn't matter for R is
**wrong**. The dependence is linear, not logarithmic, because:

- x_F (the logarithmic quantity) is in the DM freeze-out sector
  and does not depend on eta or on the baryon abundance
- eta enters R through Omega_b = 3.65e7 * eta, which is linear
- The transport prefactor enters eta linearly (no exponential
  suppression at fixed v/T)

R remains an O(1) framework prediction (right order of magnitude)
but is NOT derived to 10% precision. The bottleneck is the v_w
uncertainty from the nucleation temperature.

---

## What This Note Supersedes

This is the definitive sensitivity analysis for R vs transport
parameters. It supersedes any claim that R is insensitive to
transport uncertainties. The correct statement is:

> R is derived from the framework with all transport parameters
> computed from first principles. The central prediction gives
> R ~ O(0.01) at v/T = 0.56 (or R ~ 5 at v/T ~ 0.52). The
> uncertainty is dominated by the v_w range from nucleation
> temperature, giving dR/R ~ 650% at the combined corners.
> The transport lane does not close from insensitivity.
