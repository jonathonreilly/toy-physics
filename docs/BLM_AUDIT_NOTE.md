# BLM Audit: Generic vs Staggered-Specific Optimal Scale

**Date:** 2026-04-13
**Script:** `scripts/frontier_blm_audit.py`
**Reconciles:** `frontier_yt_blm_threshold.py` (generic 5/6) vs `frontier_blm_scale.py` (staggered-specific)

## The Discrepancy

Two calculations in this project use different BLM (Brodsky-Lepage-Mackenzie) scales:

| Calculation | BLM factor | Source | alpha_V(q*) |
|---|---|---|---|
| `frontier_yt_blm_threshold.py` | 5/6 = 0.833 (generic continuum V-scheme) | Continuum quark self-energy | ~0.088 |
| `frontier_blm_scale.py` | I_log/I_stag (staggered-specific lattice integrals) | Staggered fermion self-energy on L^4 lattice | ~0.084 |

## Key Finding

The staggered-specific BLM ratio is **I_log/I_stag = 1.972**, which is **136.6% larger** than the generic continuum factor 5/6 = 0.833. These are fundamentally different quantities:

- **Generic 5/6:** V-scheme to MSbar conversion for the continuum static potential
- **Staggered I_log/I_stag:** BLM optimal scale for the lattice staggered fermion self-energy

The lattice integral has a much larger logarithmic moment because the `sin^2(k)` dispersion relation and the compact Brillouin zone produce UV structure absent in the continuum.

## Lattice Integrals (L -> infinity, Richardson extrapolation)

| Quantity | Value |
|---|---|
| I_stag(4) | 0.619733 |
| I_log(4) | 1.222021 |
| Sigma_1 = 4 I_stag | 2.4789 |
| I_log / I_stag | 1.9718 |
| q\*a | 2.680 (q\* ~ 0.85 pi/a) |

## Sign Convention

Both files give the **same** alpha_V(q\*) despite using opposite sign conventions. The signs cancel:

- `frontier_blm_scale.py`: ln(q\*^2 a^2) = -ratio, denominator has (1 - ...)
- Lepage-Mackenzie standard: ln(q\*^2 a^2) = +ratio, denominator has (1 + ...)
- Both yield alpha_V(q\*) = alpha_plaq / (1 + alpha_plaq beta_0 ratio / 4pi)

## Correct alpha_V(q*)

**alpha_V(q\*) = 0.0836** from the staggered-specific BLM prescription.

This is 5.3% smaller than the generic-5/6 value (0.0882), and **further** from the value needed for v = 246 GeV.

## Hierarchy Formula Impact

| alpha_V | Z_chi | N_eff | v (GeV) | v / 246 |
|---|---|---|---|---|
| 0.0836 (staggered BLM) | 0.978 | 11.48 | 9.05 | 0.037 |
| 0.0882 (generic 5/6) | 0.977 | 11.45 | 8.18 | 0.033 |
| 0.092 (bare plaquette) | 0.976 | 11.43 | 7.54 | 0.031 |

The alpha_V needed for v = 246 GeV is **negative** (-0.080), meaning 1-loop Z_chi > 1 is required. No positive coupling achieves v = 246 within the current hierarchy formula structure.

## Verdict

1. The staggered-specific BLM scale is substantially different from the generic 5/6 factor (2.4x larger logarithmic moment).
2. Both calculations agree to within 5% on alpha_V(q\*) because the BLM correction is a modest ~10% shift on alpha_plaq regardless of which ratio is used.
3. Neither alpha_V value produces v = 246 GeV. The hierarchy formula requires additional physics beyond the 1-loop BLM scale-setting to generate the electroweak scale.
