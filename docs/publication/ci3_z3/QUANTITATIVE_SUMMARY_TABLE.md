# Quantitative Summary Table

**Date:** 2026-04-15
**Purpose:** reviewer-facing summary of the current quantitative lanes plus the
remaining bounded companions

Use [repo/CONTROLLED_VOCABULARY.md](../../repo/CONTROLLED_VOCABULARY.md) for
the repo-wide status taxonomy.

In this table:

- `Claim-strength status` says what kind of quantitative row this is
- `Qualifier` carries the bridge / import / caveat language
- publication-capture placement lives in [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)

| Quantity / lane | Predicted / framework result | Observed / comparator | Error / comparison | Claim-strength status | Qualifier | Primary authority |
|---|---|---|---|---|---|---|
| `alpha_s(M_Z)` | `0.1181` | `0.1179` | `+0.14%` | derived | canonical same-surface plaquette chain for `alpha_s(v)` plus the retained one-decade running bridge to `M_Z` | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) |
| `SU(3)` string tension `\sqrt{\sigma}` | `465 MeV` | `440 ± 20 MeV` | `+5.6%` | bounded companion | `T = 0` confinement is structural on the graph-first `SU(3)` gauge sector; the numeric `\sqrt{\sigma}` row is bounded through retained `\alpha_s` plus the low-energy EFT bridge and screening correction | [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) |
| `sin^2(theta_W)(M_Z)` | `0.2306` | `0.2312` | `-0.26%` | derived | standalone EW lane; bare geometry + same-surface plaquette chain + derived `R_conn` support + retained running bridge | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `1/alpha_EM(M_Z)` | `127.67` | `127.95` | `-0.22%` | derived | standalone EW lane; derived `g_1(v), g_2(v)` package after color projection plus the retained running bridge | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_1(v)` | `0.4644` | `0.4640` | `+0.08%` | derived | standalone EW lane; bare geometry + same-surface plaquette chain + derived `R_conn = 8/9 + O(1/N_c^4)` support | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_2(v)` | `0.6480` | `0.6463` | `+0.26%` | derived | standalone EW lane; bare geometry + same-surface plaquette chain + derived `R_conn = 8/9 + O(1/N_c^4)` support | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `y_t(v)` | `0.9176` | `~0.917` | `+0.06%` | derived | zero SM imports on the framework-side readout; the exact lattice-scale Ward theorem `y_t(M_Pl) / g_s(M_Pl) = 1/sqrt(6)` is retained, and the current primary precision caveat is standard lattice 1-loop matching plus standard SM RGE truncation; the older Schur-bridge budget remains an independent cross-check | [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md), [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](../../YT_ZERO_IMPORT_AUTHORITY_NOTE.md), [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](../../YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md) |
| `m_t(pole)` 2-loop | `172.57 GeV` | `172.69 GeV` | `-0.07%` | derived | inherits the retained exact lattice-scale Ward theorem and the current standard-method residual budget of the `y_t(v)` lane | [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](../../YT_ZERO_IMPORT_AUTHORITY_NOTE.md), [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](../../YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md) |
| `m_t(pole)` 3-loop | `173.10 GeV` | `172.69 GeV` | `+0.24%` | derived | inherits the retained exact lattice-scale Ward theorem and the current standard-method residual budget of the `y_t(v)` lane | [YT_ZERO_IMPORT_AUTHORITY_NOTE.md](../../YT_ZERO_IMPORT_AUTHORITY_NOTE.md), [YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md](../../YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md) |
| `m_H` 2-loop | `119.8 GeV` | `125.25 GeV` | `-4.4%` | derived | corrected-input 2-loop support route; inherits the current YT-lane residual budget on the accepted package route | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md) |
| `m_H` framework-side 3-loop | `125.1 GeV` | `125.25 GeV` | `-0.1%` | derived | direct framework-native 3-loop computation exists, and the remaining quantitative limitation is inherited from the current YT lane rather than a separate Higgs-native closure gap | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md), [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md) |
| Vacuum stability | qualitatively favorable | SM metastability comparator | qualitative prediction | derived | qualitative vacuum readout on the same route; inherits the current Yukawa/Higgs precision caveat rather than a separate closure failure | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md) |
| Taste-scalar pair | `124.91 GeV` | no confirmed observation | near-Higgs search surface | bounded companion | exact taste-block fermion-CW isotropy plus bounded gauge-only split; scalar-only thermal-cubic estimate gives `v_c/T_c = 0.3079` | [TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md](../../TASTE_SCALAR_ISOTROPY_THEOREM_NOTE.md) |
| DM transport / PMNS gate status | exact one-flavor branch `0.1888`; reduced-surface PMNS support branch `1.0` | asymmetry target `1.0` | mixed | open flagship gate | exact transport chain plus source-side closeout to the `2`-real `Z_3` doublet-block law and PMNS constructive-chamber / CP-blindness support stack | [DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md](../../DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md) |
| CKM algebraic atlas/axiom closure package | `|V_us|=0.22727`, `|V_cb|=0.04217`, `|V_ub|=0.003913`, `\delta=65.905^\circ`, `J=3.331 x 10^-5` | PDG magnitudes plus coherent angle package `\delta=65.5^\circ`, `J_{recon}=3.304 x 10^-5` | `+1.32%`, `-0.06%`, `-0.69%`, `+0.62%`, `+0.82%` | promoted quantitative package | atlas/axiom package with canonical CMT `\alpha_s(v)` as the quantitative coupling input and no quark-mass or fitted CKM observables in the derivation; exact atlas counts + exact `1/6` projector + exact tensor slot + Schur cascade on the canonical tensor/projector surface | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| down-type CKM-dual mass-ratio lane | `m_d/m_s = 0.05165`, `m_s/m_b = 0.02239`, `m_d/m_b = 0.001156` | threshold-local self-scale comparators `0.05000`, `0.02234`, `0.001117` | `+3.3%`, `+0.2%`, `+3.5%`; common-scale `m_s(m_b)/m_b(m_b)` stays `+15.0%` away | bounded secondary lane | promoted CKM closure plus GST and bounded `5/6` bridge support; no observed masses as derivation inputs, with threshold-local self-scale comparison supported but theorem-grade scale closure still open | [DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md](../../DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md) |

## Reading rule

- `derived` rows are safe current-main quantitative values, but their bridge /
  import caveats still live in the qualifier column
- `bounded companion` and `bounded secondary lane` rows remain package-captured
  and must carry their explicit qualifiers
- `open flagship gate` rows are live status rows, not closed quantitative
  predictions
