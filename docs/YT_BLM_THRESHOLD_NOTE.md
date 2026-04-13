# BLM Optimal Scale & Taste-Doubler Threshold Correction

**Script:** `scripts/frontier_yt_blm_threshold.py`
**PStack:** `yt-blm-threshold`
**Status:** BOUNDED -- 6/9 pass, 3 honest FAILs (see below)

## Problem

The framework gives alpha_s(M_Pl) = 0.084 (V-scheme: 0.092) from the
lattice plaquette.  The SM perturbative value at M_Pl obtained by running
alpha_s(M_Z) = 0.1179 upward with 2-loop RGE is alpha_s(M_Pl) ~ 0.010.
This is roughly an 8x mismatch.  Can BLM scale-setting and/or
taste-doubler threshold corrections resolve it?

## Two Mechanisms Investigated

### 1. BLM Optimal Scale (Brodsky-Lepage-Mackenzie)

The V-scheme coupling and MSbar coupling at the same scale differ by:

    alpha_MSbar(mu) = alpha_V(mu) / [1 + alpha_V * b_0 * (5/6) / (2*pi)]

At M_Pl with b_0(n_f=6) = 7:

    shift factor = 1.085
    alpha_MSbar = 0.092 / 1.085 = 0.0848

**Result:** ~9% correction.  Real but far too small to bridge the gap.

### 2. Taste-Doubler Threshold Correction

The staggered lattice has 2^3 = 8 taste copies per quark.  With 3
generations: n_f = 24 Dirac fermions above the taste-splitting scale.

- b_0(n_f=24) = (33 - 48)/3 = **-5** (asymptotic freedom LOST)
- b_0(n_f=6)  = (33 - 12)/3 = +7 (AF restored below threshold)

Integrating out 18 taste doublers at mass M_taste:

    1/alpha^(6)(M_Pl) = 1/alpha^(24)(M_Pl) + (18*T_F)/(3*pi) * ln(M_taste^2/M_Pl^2)

**Scan results:**

| M_taste / M_Pl | alpha^(6)(M_Pl) | Change from 0.098 |
|:-:|:-:|:-:|
| 0.5  | 0.113 | +15% (wrong direction) |
| 1.0  | 0.098 | 0% (continuous) |
| pi   | 0.081 | -17% |
| 10   | 0.068 | -30% |
| 100  | 0.053 | -46% |
| 1000 | 0.043 | -56% |

To reach alpha_s = 0.019 requires M_taste ~ 4 x 10^9 * M_Pl (unnatural).
To reach alpha_s = 0.010 requires an even larger hierarchy.

## Key Findings

### Finding 1: Threshold correction is ~20% with natural taste masses

With M_taste ~ O(M_Pl) to O(pi * M_Pl), the taste decoupling shifts
alpha_s by at most 20-30%.  This does not close the order-of-magnitude gap.

### Finding 2: Landau pole blocks perturbative running

ALL couplings alpha_s ~ 0.01-0.13 at M_Pl hit a Landau pole when running
down to M_Z with the perturbative 1-loop beta function.  The SM running
works because it starts from M_Z (where alpha_s = 0.1179 is large enough)
and runs UP.  Running DOWN from M_Pl requires passing through the Landau
pole region near Lambda_QCD ~ 200 MeV.

This confirms the gauge crossover blocker identified in
`frontier_yt_gauge_crossover.py`: no perturbative mechanism connects the
framework coupling at M_Pl to the SM coupling at M_Z.

### Finding 3: No self-consistent solution exists

There is no value of M_taste/M_Pl for which the threshold correction
plus perturbative running reproduces alpha_s(M_Z) = 0.1179.  The scan
over M_taste/M_Pl from 0.1 to 10^6 shows alpha_s(M_Z) saturates at
the Landau pole value for all choices.

## Honest Assessment

The BLM + threshold approach is **necessary but insufficient**:

- BLM scheme conversion: 9% effect (correct, systematic)
- Taste threshold: 20-30% with natural masses (correct, systematic)
- Combined: reduces the gap from ~8x to ~5-6x
- Remaining gap: requires non-perturbative crossover mechanism

## Failing Tests (by design -- these are honest physics results)

1. `threshold_M_taste_natural`: FAIL -- required M_taste for full gap
   closure is 10^{-9} * M_Pl, far from natural O(M_Pl).
2. `required_x_natural`: FAIL -- same conclusion from combined pipeline.
3. `self_consistent_x_found`: FAIL -- no M_taste produces correct
   alpha_s(M_Z) through perturbative running.

## Implications

The taste decoupling threshold is a REAL physical effect that must be
included in any matching calculation.  However, the gauge crossover
from the framework coupling at M_Pl to the SM coupling regime at low
energies requires a non-perturbative mechanism beyond simple threshold
matching.  The most likely candidate is a condensate-driven phase
transition in the gauge sector around Lambda_QCD.
