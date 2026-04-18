# Usable Derived Values Index

**Date:** 2026-04-15  
**Purpose:** one place to find the canonical numeric values on `main` that are
actually reused across lanes, together with their claim class and authority.

This is an **atlas helper index**, not a manuscript claim surface.

Use [repo/CONTROLLED_VOCABULARY.md](../../repo/CONTROLLED_VOCABULARY.md) for
the repo-wide status taxonomy.

Use this file when the question is:

- what exact or retained numeric value should downstream work reuse?
- is that value zero-input structural, one-computed-input derived, or bounded?
- which note/runner is the current authority on `main`?

## Reading rule

- `exact / structural` means the quantity is fixed on the theorem surface
  without an external phenomenology bridge
- `derived` means the quantity is numerically reusable on the current package
  surface and should be treated as canonical on `main`
- `retained support` means the value is itself a reusable support object on the
  retained surface
- `bounded companion` means the number is useful, but downstream reuse must
  carry its bounded qualifier explicitly
- `same-surface evaluated / derived` means numerically evaluated on the
  retained framework surface rather than imported from experiment or chosen as
  a free parameter

## A. Core reusable numbers

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| plaquette `<P>` | `0.5934` | same-surface evaluated / derived | current canonical package value; exact bridge-support stack now includes the accepted Wilson gauge-source temporal-completion theorem, the exact distinct-shell theorem, the exact mixed repeated-plaquette audit and first nonlinear `beta_eff` coefficient, an exact implicit reduction-law existence/uniqueness theorem on the finite Wilson evaluation surface, an exact nonperturbative susceptibility-flow theorem for that reduction, an exact connected plaquette-hierarchy theorem, an exact obstruction to the naive constant-lift law, an exact obstruction to any finite-order connected-hierarchy truncation, an exact compact spectral generating object for that hierarchy, an exact transfer-operator / character-recurrence realization, an exact Perron-state reduction theorem, an exact source-sector matrix-element factorization theorem, an exact local/environment factorization theorem, an exact residual-environment identification theorem, an exact spatial-environment character-measure theorem showing that the remaining operator is the explicit boundary class function `C_(Z_6^env)`, an exact spatial-environment structural transfer theorem, an exact spatial-environment tensor-transfer theorem fixing the remaining class to explicit Wilson-coefficient / `SU(3)`-intertwiner data, and an exact Perron/Jacobi underdetermination theorem showing that the exact local Wilson marked-link factor and the exact normalized mixed-kernel local compression are explicit, while the remaining open object is the explicit `beta = 6` tensor-transfer Perron / boundary data generating the boundary character data of `Z_6^env`; repo-wide numeric migration is therefore still not justified | tadpole improvement, coupling map, hierarchy baseline | [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](../../PLAQUETTE_SELF_CONSISTENCY_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md), [GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md](../../GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_DISTINCT_SHELL_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_DISTINCT_SHELL_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md), [GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md) |
| `u_0 = <P>^{1/4}` | `0.877681381199` | derived | same-surface plaquette derivative | coupling map, hierarchy, EW, Yukawa | [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](../../PLAQUETTE_SELF_CONSISTENCY_NOTE.md) |
| `alpha_LM` | `0.0906678360173` | derived | same-surface plaquette derivative | hierarchy baseline, taste thresholds, Planck-to-IR running | [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](../../PLAQUETTE_SELF_CONSISTENCY_NOTE.md) |
| `R_conn` | `8/9 = 0.888888888889` | retained support | zero-input structural at leading order + bounded `O(1/N_c^4)` correction | EW color projection, Yukawa color projection, taste weights | [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md) |
| `sqrt(R_conn)` | `sqrt(8/9) = 0.942809041582` | retained support | zero-input structural at leading order + bounded `O(1/N_c^4)` correction propagated through the square root | Yukawa color projection, top/Higgs support lanes | [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md), [YUKAWA_COLOR_PROJECTION_THEOREM.md](../../YUKAWA_COLOR_PROJECTION_THEOREM.md) |
| APBC selector factor | `(7/8)^(1/4) = 0.967168210134` | exact / structural | zero-input structural | hierarchy selector and pre/post-selector normalization | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md), [HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md](../../HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md) |
| pre-selector hierarchy baseline `M_Pl * alpha_LM^16` | `254.643210673818 GeV` | derived | same-surface plaquette derivative + framework `M_Pl` | hierarchy support analyses and endpoint comparisons | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) |
| electroweak scale `v` | `246.282818290129 GeV` | derived | same-surface plaquette derivative + framework `M_Pl` | canonical EW scale across the repo | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) |
| `alpha_s(v)` | `0.103303816122` | derived | same-surface plaquette derivative | strong-coupling lane, CKM, confinement, Yukawa/Higgs support | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md), [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](../../PLAQUETTE_SELF_CONSISTENCY_NOTE.md) |

## B. Retained EW normalization package

Analytic plaquette support on `main`:

- [GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md)
- [GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md](../../GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_REDUCTION_EXISTENCE_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SUSCEPTIBILITY_FLOW_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_INFINITE_HIERARCHY_OBSTRUCTION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SPECTRAL_MEASURE_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_FRAMEWORK_POINT_UNDERDETERMINATION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_TRANSFER_OPERATOR_CHARACTER_RECURRENCE_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_PERRON_REDUCTION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_SOURCE_SECTOR_MATRIX_ELEMENT_FACTORIZATION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_LOCAL_ENVIRONMENT_FACTORIZATION_THEOREM_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_PERRON_JACOBI_UNDERDETERMINATION_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_MIXED_CUMULANT_AUDIT_NOTE.md)
- [GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md](../../GAUGE_VACUUM_PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION_NOTE.md)
- [SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md](../../SCALAR_3PLUS1_TEMPORAL_RATIO_NOTE.md)

Those notes now provide a sharp analytic support candidate
`P_cand(6) = 0.593530679977098`, but the canonical reusable plaquette value
remains `<P> = 0.5934` because the naive constant-lift law is ruled out and,
although the onset theorem
`beta_eff(beta) = beta + beta^5 / 26244 + O(beta^6)` is now exact, the final
physical-vacuum reduction at `beta = 6` is still an open nonperturbative
`beta`-dependent theorem rather than a closed exact route.

The exact implicit finite-surface reduction law is now also closed:

`P_L(beta) = P_1plaq(beta_eff,L(beta))`

with a unique analytic and strictly increasing `beta_eff,L`. Applying that to
the canonical same-surface plaquette gives the unique implicit support value

`beta_eff^can = 9.326167920875534`,

but that is not yet the same thing as an explicit analytic closure of
`P(6)`.

The exact nonperturbative transport law is now also closed:

`beta_eff,L'(beta) = chi_L(beta) / chi_1plaq(beta_eff,L(beta))`

and equivalently

`beta_eff,L(beta) = P_1plaq^(-1)(integral_0^beta chi_L(s) ds)`.

So the remaining open object is no longer just an abstract spectral measure.
The transfer-operator / character-recurrence theorem and Perron-state
reduction theorem made the operator route explicit; the new source-sector
matrix-element factorization theorem now closes the exact structural
`beta = 6` source-sector matrix law
`T_src(6) = exp(3 J) D_6 exp(3 J)`, while the linked runner audits that law
only on a generic positive diagonal witness rather than an explicit Wilson
`D_6` evaluation.
The updated local/environment factorization theorem then shows that the
normalized mixed-kernel contribution is already exactly the local Wilson
marked-link factor, the residual-environment identification theorem isolates
the compressed unmarked spatial environment, and the spatial-environment
character-measure theorem realizes that remaining operator as the boundary
class function `C_(Z_6^env)`, the spatial-environment structural transfer
theorem realizes those boundary character data as boundary amplitudes of one
positive spatial transfer law, and the spatial-environment tensor-transfer
theorem fixes the remaining local matrix-element class to explicit Wilson
coefficients and `SU(3)` intertwiners, with its runner only a truncated
support packet over an audited tensor-transfer word rather than a full
`beta = 6` Perron solve. So the remaining open object is
specifically the explicit `beta = 6` tensor-transfer Perron / boundary data
generating the boundary character data of `Z_6^env`, equivalently the Perron eigenvector / moments of the factorized operator
`exp(3 J) D_6^loc C_(Z_6^env) exp(3 J)`.

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| `g_1(v)` | `0.4644` | derived | same-surface plaquette derivative + derived `R_conn` support | EW normalization, Higgs/top support | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `g_2(v)` | `0.6480` | derived | same-surface plaquette derivative + derived `R_conn` support | EW normalization, Higgs/top support | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `sin^2(theta_W)(M_Z)` | `0.2306` | derived | same-surface plaquette derivative + derived `R_conn` support + running bridge | reviewer-facing EW lane, low-energy comparison | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `1/alpha_EM(M_Z)` | `127.67` | derived | same-surface plaquette derivative + derived `R_conn` support + running bridge | reviewer-facing EW lane, low-energy comparison | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `alpha_s(M_Z)` | `0.1181` | derived | same-surface plaquette derivative + one-decade running bridge | standalone strong-coupling lane, confinement, continuum positioning | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) |

## C. Closed flavor package values

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| `|V_us|` | `0.22727` | derived | promoted CKM atlas/axiom package | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `|V_cb|` | `0.04217` | derived | promoted CKM atlas/axiom package | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `|V_ub|` | `0.003913` | derived | promoted CKM atlas/axiom package | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `delta_CKM` | `65.905157 deg` | derived | promoted CKM atlas/axiom package | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `J` | `3.331 x 10^-5` | derived | promoted CKM atlas/axiom package | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |

## D. Useful YT/Higgs downstream values

These are usable, but only with their qualifiers attached.

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| `y_t(v)` | `0.9176` | retained | retained YT/top transport lane: exact lattice-scale `1/sqrt(6)` Ward theorem plus the retained UV-to-IR transport obstruction / full-staggered-PT quadrature stack | YT/top/Higgs reuse is safe on the current retained YT transport surface, with the explicit transport uncertainty carried when precision matters | [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md), [YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](../../YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md) |
| `m_t(pole)` 2-loop | `172.57 GeV` | retained | retained YT/top transport lane with explicit canonical `±6.50 GeV` envelope and through-2-loop structural / bound-constrained continuation | top-mass reuse is safe on the retained 2-loop canonical transport surface, with the explicit continuation band carried when precision matters | [YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](../../YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md), [YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md](../../YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md) |
| `m_t(pole)` 3-loop | `173.10 GeV` | derived | older 3-loop continuation remains a derived cross-check against the retained 2-loop canonical transport lane | top-mass reuse is safe only as a derived cross-check; the retained YT authority remains the 2-loop canonical transport package | [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md) |
| `m_H` framework-side 3-loop | `125.1 GeV` | derived | derived Higgs route with an explicit retention-decomposed budget `125.04 ± 3.17 GeV` on the accepted package route | Higgs/vacuum reuse is safe with the retention-analysis budget carried explicitly when precision matters | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md), [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md) |
| `sqrt(sigma)` | `465 MeV` | bounded companion | retained `alpha_s` + EFT bridge | bounded confinement phenomenology only | [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) |

## Rule for downstream work

Before reusing a number elsewhere in the repo:

1. take it from this file or from the authority linked here
2. carry its claim class with it
3. if it is bounded, keep the qualifier in the target note or table
4. do not copy older route-history values when a canonical value exists here
