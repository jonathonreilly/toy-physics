# v from RG-Improved Coleman-Weinberg EWSB

**Status**: BOUNDED -- mechanism works, numerical value off by ~13 decades
**Script**: `scripts/frontier_v_rg_improved.py`
**Date**: 2026-04-13

## Summary

We derive the electroweak VEV v by finding the energy scale where the
RG-running Coleman-Weinberg effective potential triggers EWSB, using
the framework's UV boundary conditions at M_Pl.

**Result**: The CW mechanism IS triggered at mu_cross ~ 10^16 GeV.
The top Yukawa overtakes the gauge contribution to B(mu) at 3 decades
below M_Pl. However, v_CW ~ 4 x 10^15 GeV, which is 13 decades above
the measured v = 246 GeV.

## Framework Boundary Conditions at M_Pl

| Parameter | Value | Source |
|-----------|-------|--------|
| alpha_s(M_Pl) | 0.082 | Plaquette matching |
| sin^2(theta_W) | 3/8 | Cl(3) GUT normalisation |
| y_t(M_Pl) | g_s/sqrt(6) = 0.414 | Lattice relation |
| alpha_2(M_Pl) | 0.082 | Gauge unification |
| lambda(M_Pl) | ~0 | CW dimensional transmutation |

## Physics: Coleman-Weinberg EWSB via RG Running

The CW effective potential parameter B(mu) controls whether EWSB occurs:

    B(mu) = (1/64pi^2) [3g_2^4/8 + 3(g_2^2+g'^2)^2/16 - 3y_t^4]

- B > 0: gauge bosons dominate, no EWSB
- B < 0: top quark dominates, CW triggers EWSB

At M_Pl with unified couplings (alpha_GUT = 0.082):
- Gauge: g_2 = g_s ~ 1.015, giving large gauge^4 contribution
- Top: y_t = 0.414, giving smaller top^4 contribution
- B(M_Pl) = +1.30 x 10^-3 > 0 (gauge dominates)

Running downward:
- y_t GROWS toward its IR fixed point (~1 at M_Z)
- g_2 SHRINKS (SU(2) asymptotic freedom, though slower than SU(3))
- At mu_cross ~ 10^16 GeV: y_t^4 overtakes gauge^4, B changes sign

## Results

### Crossover Scale (2-loop)

    mu_cross = 1.27 x 10^16 GeV  (log10 = 16.10)

At the crossing:
- alpha_1 = 0.060, alpha_2 = 0.117, alpha_3 = 0.209
- y_t = 0.842
- All couplings perturbative

### B(mu) Profile

| log10(mu/GeV) | B(mu) | Dominant |
|----------------|-------|----------|
| 19 (M_Pl) | +1.30e-3 | GAUGE |
| 17 | +1.19e-3 | GAUGE |
| 16.1 (crossing) | 0 | -- |
| 15 | -2.36e-2 | TOP |

### CW VEV Estimate

Leading order: v ~ mu_cross ~ 10^16 GeV
Self-consistency (lambda = -2B): v ~ 4.0 x 10^15 GeV

### Error Budget

| Source | Uncertainty |
|--------|-------------|
| 1-loop vs 2-loop | 0.16 decades |
| alpha_s +/- 10% | ~0.9 decades (15.65 to 16.52) |
| Threshold corrections | potentially O(several) decades |
| Higher-order CW | O(1) in log(v) |

### alpha_s Sensitivity

| alpha_s(M_Pl) | mu_cross (GeV) | log10 |
|---------------|----------------|-------|
| 0.075 | 4.50e+15 | 15.65 |
| 0.078 | 7.18e+15 | 15.86 |
| 0.082 | 1.27e+16 | 16.10 |
| 0.086 | 2.10e+16 | 16.32 |
| 0.090 | 3.33e+16 | 16.52 |

## Honest Assessment

### What Works

1. The CW mechanism IS triggered: B(mu) changes sign from positive
   (gauge-dominated at M_Pl) to negative (top-dominated) purely through
   RG running.

2. No parameter tuning: the framework's UV boundary conditions
   (alpha_s, sin^2(theta_W), y_t relation) determine everything.

3. The naive CW formula v ~ M_Pl * exp(-8pi^2/(3y_t^2)) gives v ~ 0
   (the exponential suppression is exp(-153), essentially zero).
   The RG improvement -- where y_t grows toward its IR fixed point --
   rescues the mechanism and produces a finite crossover.

4. The crossover occurs in the perturbative regime (alpha_3 ~ 0.2).

### What Does Not Work

1. v_CW ~ 10^15-16 GeV instead of 246 GeV. The CW crossover occurs
   at the GUT scale, not the EW scale.

2. This is actually a well-known result: minimal CW EWSB with SM-only
   running produces a transition near the GUT scale. Getting v ~ 246 GeV
   requires either:
   - New particles at intermediate scales (threshold corrections)
   - Additional scalar fields (extended Higgs sector)
   - Strong dynamics (technicolor-like)
   - The actual framework mechanism may differ from minimal CW

3. The 13-decade gap IS the hierarchy problem restated: why is v/M_Pl
   so small? The CW mechanism replaces the tuned negative m^2 with a
   dynamical crossover, but in the minimal SM the crossover happens
   too close to M_Pl.

## Significance

The calculation establishes that:
1. The framework's UV boundary conditions DO trigger EWSB via the CW mechanism
2. A hierarchy IS generated (v << M_Pl by 3+ decades)
3. The mechanism is perturbatively controlled at the crossover
4. The remaining gap (13 decades) quantifies what threshold corrections
   or new physics must provide

This replaces the ad hoc negative m^2 parameter with a dynamical mechanism,
even though the full hierarchy requires additional input beyond minimal SM running.

## Scenario Comparison

| Scenario | alpha_2(M_Pl) | B(M_Pl) | mu_cross | Issue |
|----------|---------------|---------|----------|-------|
| A (SM running) | 0.020 | < 0 | none | Gauge too weak, no crossover |
| B (unification) | 0.082 | > 0 | 10^16 GeV | Crossover at GUT scale |
| Needed for v=246 | -- | -- | ~10^2 GeV | Requires new thresholds |
