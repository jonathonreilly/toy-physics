# Quantitative Summary Table

**Date:** 2026-04-15
**Purpose:** reviewer-facing summary of the current quantitative lanes plus the
remaining bounded companions

| Quantity / lane | Predicted / framework result | Observed / comparator | Error / comparison | Status | Qualifier | Primary authority |
|---|---|---|---|---|---|---|
| `alpha_s(M_Z)` | `0.1181` | `0.1179` | `+0.14%` | retained / derived | one computed plaquette input, all else derived | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) |
| `SU(3)` string tension `\sqrt{\sigma}` | `465 MeV` | `440 ± 20 MeV` | `+5.6%` | retained structural / bounded quantitative | `T = 0` confinement is structural on the graph-first `SU(3)` gauge sector; the numeric `\sqrt{\sigma}` row is bounded through retained `\alpha_s` plus the low-energy EFT bridge and screening correction | [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) |
| `sin^2(theta_W)(M_Z)` | `0.2306` | `0.2312` | `-0.26%` | retained / derived | standalone EW lane; one computed plaquette input, all else derived | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `1/alpha_EM(M_Z)` | `127.67` | `127.95` | `-0.22%` | retained / derived | standalone EW lane; one computed plaquette input, all else derived | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_1(v)` | `0.4644` | `0.4640` | `+0.08%` | retained / derived | standalone EW lane; one computed plaquette input, all else derived | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_2(v)` | `0.6480` | `0.6463` | `+0.26%` | retained / derived | standalone EW lane; one computed plaquette input, all else derived | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `y_t(v)` | `0.9176` | `~0.917` | `+0.06%` | bounded / derived | zero SM imports; bounded by `~3%` QFP/RGE-surrogate systematic | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_t(pole)` 2-loop | `172.57 GeV` | `172.69 GeV` | `-0.07%` | bounded / derived | inherits the `~3%` QFP/RGE-surrogate bound from the `y_t` lane | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_t(pole)` 3-loop | `173.10 GeV` | `172.69 GeV` | `+0.24%` | bounded / derived | inherits the `~3%` QFP/RGE-surrogate bound from the `y_t` lane | [YT_COLOR_PROJECTION_CORRECTION_NOTE.md](../../YT_COLOR_PROJECTION_CORRECTION_NOTE.md) |
| `m_H` 2-loop | `119.8 GeV` | `125.25 GeV` | `-4.4%` | bounded | corrected-input 2-loop support route | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) |
| `m_H` framework-side 3-loop | `125.3 GeV` | `125.25 GeV` | `+0.0%` | bounded | direct framework-native 3-loop computation; remaining bound is inherited from the `~3%` bounded `y_t` lane | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) |
| Vacuum stability | qualitatively favorable | SM metastability comparator | qualitative prediction | bounded | inherits the bounded Yukawa / Higgs status on the current route | [HIGGS_VACUUM_PROMOTED_NOTE.md](../../HIGGS_VACUUM_PROMOTED_NOTE.md) |
| Dark matter ratio `R` | `5.48` | `5.47` | near-match | bounded | bounded companion lane | [DM_RELIC_PAPER_NOTE.md](../../DM_RELIC_PAPER_NOTE.md) |
| CKM atlas/axiom closure package | `|V_us|=0.22727`, `|V_cb|=0.04217`, `|V_ub|=0.003913`, `\delta=65.905^\circ`, `J=3.331 x 10^-5` | PDG magnitudes plus coherent angle package `\delta=65.5^\circ`, `J_{recon}=3.304 x 10^-5` | `+1.32%`, `-0.06%`, `-0.69%`, `+0.62%`, `+0.82%` | closed / derived | atlas/axiom package with canonical CMT `\alpha_s(v)` as the quantitative coupling input and no quark-mass or fitted CKM observables in the derivation; exact atlas counts + exact `1/6` projector + exact tensor slot + Schur cascade | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |

## Reading rule

- retained rows are safe standalone quantitative lanes on `main`
- bounded rows remain package-captured, but must carry their explicit
  qualifiers
