# Quantitative Summary Table

**Date:** 2026-04-15
**Purpose:** reviewer-facing summary of the current quantitative lanes plus the
remaining bounded companions

| Quantity / lane | Predicted / framework result | Observed / comparator | Error / comparison | Status | Qualifier | Primary authority |
|---|---|---|---|---|---|---|
| `alpha_s(M_Z)` | `0.1181` | `0.1179` | `+0.14%` | retained / derived | one computed plaquette input, all else derived | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) |
| `sin^2(theta_W)(M_Z)` | `0.2306` | `0.2312` | `-0.26%` | retained / derived | standalone EW lane; one computed plaquette input, all else derived | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `1/alpha_EM(M_Z)` | `127.67` | `127.95` | `-0.22%` | retained / derived | standalone EW lane; one computed plaquette input, all else derived | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_1(v)` | `0.4644` | `0.4640` | `+0.08%` | retained / derived | standalone EW lane; one computed plaquette input, all else derived | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_2(v)` | `0.6480` | `0.6463` | `+0.26%` | retained / derived | standalone EW lane; one computed plaquette input, all else derived | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `y_t(v)` | `0.9176` | `~0.917` | `+0.06%` | bounded / derived | zero SM imports; bounded by `~3%` QFP/RGE-surrogate systematic | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_t(pole)` 2-loop | `172.57 GeV` | `172.69 GeV` | `-0.07%` | bounded / derived | inherits the `~3%` QFP/RGE-surrogate bound from the `y_t` lane | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_t(pole)` 3-loop | `173.10 GeV` | `172.69 GeV` | `+0.24%` | bounded / derived | inherits the `~3%` QFP/RGE-surrogate bound from the `y_t` lane | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_H` 2-loop | `119.8 GeV` | `125.25 GeV` | `-4.4%` | bounded | Higgs mechanism derived; exact low-energy mass still not closed | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) |
| `m_H` calibrated 3-loop estimate | `129.7 GeV` | `125.25 GeV` | `+3.5%` | bounded | uses a calibrated 3-loop fit, not a framework-native from-scratch implementation | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) |
| Vacuum stability | absolutely stable | SM metastability comparator | qualitative prediction | bounded | inherits the bounded Higgs / Yukawa status on the current route | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) |
| Dark matter ratio `R` | `5.48` | `5.47` | near-match | bounded | bounded companion lane | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md) |
| CKM magnitudes | strong bounded package | PDG values | mixed but strong | bounded | bounded flavor package | [CKM_MASS_BASIS_NNI_NOTE.md](../../CKM_MASS_BASIS_NNI_NOTE.md) |

## Reading rule

- retained rows are safe standalone quantitative lanes on `main`
- bounded rows remain package-captured, but must carry their explicit
  qualifiers
