# y_t Framework-Seeded Note

## Summary

`scripts/frontier_yt_framework_seeded.py` predicts the top quark mass
from **framework inputs only**, with no observed alpha_s(M_Z) entering
at any point.

## The Bug (in frontier_yt_gauge_crossover_theorem.py)

The old script built g3(M_Pl) by running observed alpha_s(M_Z) = 0.1179
**upward** to M_Pl. This is circular: the observed coupling is used to
derive the prediction.

## The Fix

Start from the **framework** coupling alpha_plaq = 0.092 at the lattice
scale and run **downward** to M_Z.

### Chain

| Step | Value | Source |
|------|-------|--------|
| 1. alpha_plaq | 0.092 | Plaquette with g_bare = 1 (axiom A5) |
| 2. alpha_V | 0.093 | Lepage-Mackenzie conversion |
| 3. alpha_MSbar^latt(M_Pl) | 0.082 | V-to-MSbar (Schroder/Peter) |
| 4. N_taste | 4 | Feshbach taste projection (8 tastes -> 4 sectors) |
| 5. alpha_s^EFT(M_Pl) | 0.0205 | alpha_MSbar^latt / N_taste |
| 6. y_t(M_Pl) | 0.207 | g_s^EFT / sqrt(6) (Ward identity) |
| 7. RGE | 2-loop SM | g_s and y_t co-evolve downward to M_Z |

### Taste Projection

Direct MSbar running from alpha_s = 0.082 at M_Pl hits a Landau pole
(1/alpha = 12.2 is insufficient for 43.9 decades of logarithmic running).

The lattice plaquette sums over all 2^d = 8 staggered taste doublers.
The physical SM has 1 taste per flavor. The Feshbach projection decomposes
the total gauge fluctuations into N_taste = 4 paired sectors. The
single-taste EFT coupling alpha_s^EFT = 0.082/4 = 0.020 is in the
deep perturbative regime and runs cleanly to M_Z.

## Results

| Observable | Framework Prediction | Observed | Deviation |
|-----------|---------------------|----------|-----------|
| alpha_s(M_Z) | 0.238 | 0.1179 | +102% |
| m_t | 150.9 GeV | 173.0 GeV | -12.8% |

## Sensitivity

The prediction is most sensitive to alpha_plaq:
- alpha_plaq = 0.090 -> m_t = 136.5 GeV
- alpha_plaq = 0.092 -> m_t = 150.9 GeV (nominal)
- alpha_plaq = 0.094 -> m_t = 170.1 GeV (-1.7% from observed)

The Higgs quartic lambda(M_Pl) has negligible impact (< 0.01 GeV).

## Circularity Audit

- **NOT used**: alpha_s(M_Z) = 0.1179, any upward running from M_Z
- **Used (non-QCD)**: M_Z, alpha_EM, sin^2(theta_W), quark mass thresholds
- **Verdict**: CLEAN -- alpha_s(M_Z) is a prediction, not an input

## Open Questions

1. The alpha_s(M_Z) prediction (0.238) overshoots by 2x. This may
   indicate the taste projection factor N_taste = 4 needs refinement
   or that additional matching corrections exist at the lattice-to-EFT
   boundary.

2. The m_t prediction (150.9 GeV, -12.8%) is within the ballpark but
   not yet within experimental precision. The sensitivity to alpha_plaq
   suggests that a 2% increase (to 0.094) would give near-perfect
   agreement.

## Script

- **Path**: `scripts/frontier_yt_framework_seeded.py`
- **Dependencies**: numpy, scipy
- **Tests**: 11/11 pass (0 fail)
- **Runtime**: < 1 second
