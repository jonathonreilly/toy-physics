# Usable Derived Values Index

**Date:** 2026-04-15  
**Purpose:** one place to find the canonical numeric values on `main` that are
actually reused across lanes, together with their claim class and authority.

This is an **atlas helper index**, not a manuscript claim surface.

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
| `alpha_LM` | `0.0906678360173` | derived | same-surface plaquette derivative; exactly `sqrt(alpha_bare * alpha_s(v))` on the retained coupling definitions | hierarchy baseline, taste thresholds, Planck-to-IR running | [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](../../PLAQUETTE_SELF_CONSISTENCY_NOTE.md), [ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `R_conn` | `8/9 = 0.888888888889` | retained support | zero-input structural at leading order + bounded `O(1/N_c^4)` correction | EW color projection, Yukawa color projection, taste weights | [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md) |
| `sqrt(R_conn)` | `sqrt(8/9) = 0.942809041582` | retained support | zero-input structural at leading order + bounded `O(1/N_c^4)` correction propagated through the square root | Yukawa color projection, top/Higgs support lanes | [RCONN_DERIVED_NOTE.md](../../RCONN_DERIVED_NOTE.md), [YUKAWA_COLOR_PROJECTION_THEOREM.md](../../YUKAWA_COLOR_PROJECTION_THEOREM.md) |
| `R_base` | `31/9 = 3.444444444444` | retained support | exact group-theory identity using admitted `3/5` GUT normalization | bounded DM/cosmology cascade base factor; downstream work must not treat this as the full `Omega_DM/Omega_b` value | [R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md](../../R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md) |
| `z_mr` | `3422.913` | retained/admitted structural support | exact `1 + z_mr = Omega_m,0/Omega_r,0` after supplied `Omega_m,0=0.315` and observational `Omega_r,0=9.2e-5` | early-cosmology consistency checks; do not reuse as a native density prediction | [MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../MATTER_RADIATION_EQUALITY_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| `N_eff` | retained count `3`; standard readout `3.046` | retained/admitted structural support | three retained active neutrino flavours plus external standard `0.046` thermal correction | radiation-density consistency checks; do not reuse as a native thermal-history derivation | [N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md](../../N_EFF_FROM_THREE_GENERATIONS_THEOREM_NOTE_2026-04-24.md) |
| `m_TT(2)/m_vec(1)` | `sqrt(3) = 1.732050807569` | retained structural support | exact ratio after combining retained spin-2/spin-1 towers with `Lambda = 3/R^2` | compactness-tower bookkeeping; safe as a structural ratio, not as a physical particle-mass ratio unless the particle interpretation is separately promoted | [GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md](../../GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md) |
| `m_TT(2)` benchmark scale | `2.93e-33 eV/c^2` at `Lambda = 1.105e-52 m^-2` | bounded benchmark | structural formula `sqrt(2) hbar sqrt(Lambda)/c` evaluated after supplying a cosmology benchmark | scale comparator only; do not reuse as a direct graviton-mass prediction without separately promoting the compactness-tower particle interpretation | [GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md](../../GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md) |
| APBC selector factor | `(7/8)^(1/4) = 0.967168210134` | exact / structural | zero-input structural | hierarchy selector and pre/post-selector normalization | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md), [HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md](../../HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md) |
| pre-selector hierarchy baseline `M_Pl * alpha_LM^16` | `254.643210673818 GeV` | derived | same-surface plaquette derivative + framework `M_Pl` | hierarchy support analyses and endpoint comparisons | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) |
| electroweak scale `v` | `246.282818290129 GeV` | derived | same-surface plaquette derivative + framework `M_Pl` | canonical EW scale across the repo | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) |
| `alpha_s(v)` | `0.103303816122` | derived | same-surface plaquette derivative; paired with `alpha_LM` by `alpha_LM^2 = alpha_bare alpha_s(v)` | strong-coupling lane, CKM, confinement, Yukawa/Higgs support | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md), [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](../../PLAQUETTE_SELF_CONSISTENCY_NOTE.md), [ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md) |

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
| `sin^2(theta_W)(M_Z)` | `0.2306` | derived | same-surface plaquette derivative + derived `R_conn` support + running bridge | same-surface EW lane, low-energy comparison | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `1/alpha_EM(M_Z)` | `127.67` | derived | same-surface plaquette derivative + derived `R_conn` support + running bridge | same-surface EW lane, low-energy comparison | [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md) |
| `alpha_s(M_Z)` | `0.1181` | derived | same-surface plaquette derivative + one-decade running bridge | standalone strong-coupling lane, confinement, continuum positioning | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md) |

## C. Closed flavor package values

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| `lambda^2` | `0.0516519080611` | derived | `alpha_s(v)/2` on promoted CKM atlas/axiom package | CKM downstream comparisons and summary tables | [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `A^2` | `2/3` | derived | exact weak-pair/color count on promoted CKM atlas/axiom package | CKM downstream comparisons and summary tables | [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| atlas-leading `|V_ud|_0` | `0.973824` | derived support | first-row atlas-leading unitarity completion `sqrt(1-alpha_s(v)/2-alpha_s(v)^3/72)`; finite-`lambda` standard-matrix readout guarded separately | CKM downstream comparisons and summary tables | [CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md) |
| atlas-leading `|V_us|_0` | `0.22727` | derived support | promoted CKM atlas/axiom package; `sqrt(alpha_s(v)/2)`; finite-`lambda` standard-matrix readout guarded separately | CKM downstream comparisons and summary tables | [CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md), [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md), [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| atlas-leading `|V_cd|_0` | `0.22727` | derived support | promoted CKM atlas/axiom package; `sqrt(alpha_s(v)/2)`; finite-`lambda` standard-matrix readout guarded separately | CKM downstream comparisons and summary tables | [CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md](../../CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md) |
| atlas-leading `|V_cs|_0` | `0.97292` | derived support | second-row atlas-leading unitarity completion `sqrt(1-alpha_s(v)/2-alpha_s(v)^2/6)`; direct hadronic extraction not used as input | CKM downstream comparisons and summary tables | [CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md](../../CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md) |
| `|V_cb|` | `0.04217` | derived | promoted CKM atlas/axiom package; `alpha_s(v)/sqrt(6)` | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md), [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| atlas-leading `|V_ub|_0` | `0.003913` | derived support | promoted CKM atlas/axiom package; `alpha_s(v)^(3/2)/(6 sqrt(2))`; finite-`lambda` standard-matrix readout guarded separately | CKM downstream comparisons and summary tables | [CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md), [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md), [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md), [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| atlas-leading `|V_td|_0` | `0.008750` | derived support | promoted CKM atlas/axiom package; `sqrt(5/72) alpha_s(v)^(3/2)`; finite-`lambda` standard-matrix readout guarded separately | CKM downstream comparisons and summary tables | [CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md) |
| atlas-leading `|V_ts|_0` | `0.04217` | derived support | promoted CKM atlas/axiom package; `alpha_s(v)/sqrt(6)`; finite-`lambda` standard-matrix readout guarded separately | CKM downstream comparisons and summary tables | [CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md) |
| atlas `|V_ts|/|V_cb|` | `1` | exact / structural | Thales-pinned `alpha_s`-independent ratio; cancellation of the common `A^2 lambda^4` factor on the atlas-leading third row | CKM ratio comparators and atlas-geometry tests | [CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md) |
| atlas `|V_td|/|V_ub|` | `sqrt(5)` | exact / structural | Thales-pinned `alpha_s`-independent ratio; cancellation of the common `A^2 lambda^6` factor leaves `R_t/R_b = sqrt(5)` at the atlas point | CKM ratio comparators and atlas-geometry tests | [CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md) |
| atlas `|V_td V_cb|^2 / |V_ts V_ub|^2` | `5` | exact / structural | Thales-pinned `alpha_s`-independent cross-row ratio; common `alpha_s^5` factor cancels between the two CKM products | CKM cross-row comparators and atlas-geometry tests | [CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md) |
| atlas `R_b^2` | `1/6 = rho` | exact / structural | Thales corollary `R_b^2 = rho^2 + eta^2 = rho` at the atlas point | CKM triangle geometry and ratio bookkeeping | [CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md), [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md](../../CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| atlas `R_t^2 / R_b^2` | `5` | exact / structural | Thales-pinned ratio `(1-rho)/rho = 5` at the atlas point; geometric source of `|V_td|^2/|V_ub|^2` and the cross-row product identity | CKM triangle geometry and ratio bookkeeping | [CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md), [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md](../../CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| atlas-leading `|V_tb|_0` | `0.99907` | derived support | third-row atlas-leading unitarity completion `sqrt(1-alpha_s(v)^2/6-5 alpha_s(v)^3/72)` | CKM downstream comparisons and summary tables | [CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md](../../CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md) |
| `delta_CKM` | `65.905157 deg` | derived | promoted CKM atlas/axiom package | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md), [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| atlas `alpha_0` | `90 deg` | exact / structural | rescaled CKM atlas triangle only; not the exact finite-`lambda` barred unitarity-triangle angle | CKM atlas geometry, Jarlskog-area bookkeeping, comparator discipline | [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md](../../CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| NLO `gamma_bar` | `65.905157 deg` | derived support | protected through the NLO barred-apex multiplicative map; not claimed beyond the `O(lambda^4)` remainder | CKM barred-triangle geometry and angle comparators | [CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md](../../CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) |
| NLO `rho_bar`, `eta_bar` | `0.16236`, `0.36305` | derived support | `(4-alpha_s(v))/24`, `sqrt(5)(4-alpha_s(v))/24` on the NLO barred-apex map | CKM barred-triangle geometry and angle comparators | [CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md](../../CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md) |
| NLO `sin(2 beta_bar)/sin(2 beta_0)` | `0.979339` | derived support | `1-alpha_s(v)/(n_quark-1)=1-alpha_s(v)/5` on the retained CKM NLO surface; not claimed beyond the `O(alpha_s^2)` remainder | CKM barred-triangle ratio bookkeeping and `sin(2 beta)` comparators | [CKM_SIN_2_BETA_BAR_NLO_N_QUARK_RATIO_THEOREM_NOTE_2026-04-25.md](../../CKM_SIN_2_BETA_BAR_NLO_N_QUARK_RATIO_THEOREM_NOTE_2026-04-25.md) |
| NLO `R_t_bar^2` | `0.833444` | derived support | `(80+alpha_s(v)^2)/96` on the retained protected-`gamma_bar` surface | CKM barred-triangle side-length bookkeeping and geometry comparators | [CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md](../../CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md) |
| NLO barred-triangle defect `rho_bar lambda^2` | `0.008386` | derived support | exact `1-(R_b_bar^2+R_t_bar^2)=rho_bar lambda^2=alpha_s(v)(4-alpha_s(v))/48` on the retained protected-`gamma_bar` surface | CKM barred-triangle consistency checks and joint-fit bookkeeping | [CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md](../../CKM_BARRED_TRIANGLE_PYTHAGOREAN_RHO_LAMBDA_SUM_RULE_THEOREM_NOTE_2026-04-25.md) |
| atlas-leading `beta_s` | `0.019250 rad` | derived support | `alpha_s(v) sqrt(5)/12` from retained `lambda^2` and `eta`; leading non-trivial Wolfenstein order only | B_s mixing comparator and CKM CP bookkeeping | [CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md](../../CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md) |
| atlas-leading `phi_s(B_s)` | `-0.038499 rad` | derived support | `-alpha_s(v) sqrt(5)/6`; no fitted CKM or B-mixing input, not an all-orders BSM-inclusive mixing theorem | B_s mixing comparator and CKM CP bookkeeping | [CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md](../../CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md) |
| atlas-leading `sin(2 beta_s)_LO / sin(2 beta_d)` | `0.0516519` | derived support | Thales-mediated cancellation gives `lambda^2=alpha_s(v)/2`; exact-sine correction remains guarded | B_d/B_s CP-ratio comparator and CKM CP bookkeeping | [CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md) |
| atlas-leading `phi_s / sin(2 beta_d)` | `-0.0516519` | derived support | Thales-mediated cancellation gives `-lambda^2=-alpha_s(v)/2`; leading-Wolfenstein ratio only | B_d/B_s CP-ratio comparator and CKM CP bookkeeping | [CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md](../../CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md) |
| atlas-leading `sin(2 beta_d) sin(2 beta_s)` | `0.0286955` | derived support | CP-product identity `5 alpha_s(v)/18`; leading-Wolfenstein / atlas-LO only | B_d/B_s CP-product comparator and alpha_s cross-sector consistency checks | [CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md](../../CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md) |
| CP-product `alpha_s(v)` estimator | `0.098 +/- 0.056` | comparator | `(18/5) sin(2 beta_d) sin(2 beta_s)` using the PDG/LHCb 2024 baseline; not a replacement for the canonical plaquette/CMT value | CKM CP cross-sector consistency check against canonical `alpha_s(v)=0.103303816122` | [CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md](../../CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md) |
| atlas `R_t^2` | `5/6` | exact / structural | Pythagorean companion to retained `R_b^2=1/6` on the atlas triangle | CKM triangle geometry and B_s phase support | [CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md](../../CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md), [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md](../../CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| atlas `J_0` area factor | `alpha_s(v)^3 sqrt(5)/72 = 3.4237 x 10^-5` | derived support | rescaled atlas/Wolfenstein area factor; finite-`lambda` exact standard-matrix `J` remains the parent atlas readout | CKM area bookkeeping and CP-phase support only | [CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md](../../CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md), [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| kaon epsilon_K CKM factors | `(+2J_0, -J_0, -(5 alpha_s(v)^2/18)J_0)` = `(+6.85e-5, -3.42e-5, -1.01e-7)` using atlas `J_0` | derived support | atlas-leading factorization of the SM epsilon_K CKM-imaginary bracket; absolute epsilon_K inputs remain external | kaon CP bookkeeping, Jarlskog reuse, epsilon_K comparator discipline | [CKM_KAON_EPSILON_K_JARLSKOG_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md](../../CKM_KAON_EPSILON_K_JARLSKOG_DECOMPOSITION_THEOREM_NOTE_2026-04-25.md) |
| exact standard-matrix `J` | `3.331 x 10^-5` | derived | promoted CKM atlas/axiom package with finite-`lambda` cosine factors | CKM downstream comparisons and summary tables | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md), [WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md](../../WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md), [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |

## D. Useful YT/Higgs downstream values

These are usable, but only with their qualifiers attached.

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| `y_t(v)` | `0.9176` | retained | retained YT/top transport lane: exact lattice-scale `1/sqrt(6)` Ward theorem plus the retained UV-to-IR transport obstruction / full-staggered-PT quadrature stack | YT/top/Higgs reuse is safe on the current retained YT transport surface, with the explicit transport uncertainty carried when precision matters | [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md), [YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](../../YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md) |
| `m_t(pole)` 2-loop | `172.57 GeV` | retained | retained YT/top transport lane with explicit canonical `±6.50 GeV` envelope and through-2-loop structural / bound-constrained continuation | top-mass reuse is safe on the retained 2-loop canonical transport surface, with the explicit continuation band carried when precision matters | [YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](../../YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md), [YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md](../../YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md) |
| `m_t(pole)` 3-loop | `173.10 GeV` | derived | older 3-loop continuation remains a derived cross-check against the retained 2-loop canonical transport lane | top-mass reuse is safe only as a derived cross-check; the retained YT authority remains the 2-loop canonical transport package | [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md](../../YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md) |
| `m_H` framework-side 3-loop | `125.1 GeV` | derived | derived Higgs route with an explicit retention-decomposed budget `125.04 ± 3.17 GeV` on the accepted package route | Higgs/vacuum reuse is safe with the retention-analysis budget carried explicitly when precision matters | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md), [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md), [HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md](../../HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md) |
| `sqrt(sigma)` | `465 MeV` | bounded companion | retained `alpha_s` + EFT bridge | bounded confinement phenomenology only | [CONFINEMENT_STRING_TENSION_NOTE.md](../../CONFINEMENT_STRING_TENSION_NOTE.md) |

## E. Neutrino Bounded Observable Values

These are reusable as retained-package inequality bounds, not as positive
point predictions for the full neutrino lane.

| Quantity | Canonical value on `main` | Claim class | Import class | Safe reuse | Authority |
|---|---:|---|---|---|---|
| retained atmospheric light scale `m_3` | `50.58 meV` | retained support | retained atmospheric-scale package | upper/lower endpoint for retained neutrino-observable bounds | [DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md](../../DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md), [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md) |
| `Σm_ν` strict floor | `> 50.58 meV` | bounded companion | retained `m_3` + retained normal ordering | cosmology falsification floor; not a point prediction for the mass sum | [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md) |
| tritium endpoint `m_β` ceiling | `≤ 50.58 meV` | bounded companion | retained `m_3` + retained normal ordering + PMNS unitarity | beta-decay endpoint ceiling; not a point prediction for `m_β` | [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md) |
| Majorana effective mass `m_ββ` ceiling | `≤ 50.58 meV` | bounded companion | retained `m_3` + retained normal ordering + triangle inequality | `0νββ` ceiling only; not a positive Majorana signal claim | [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md) |

## Rule for downstream work

Before reusing a number elsewhere in the repo:

1. take it from this file or from the authority linked here
2. carry its claim class with it
3. if it is bounded, keep the qualifier in the target note or table
4. do not copy older route-history values when a canonical value exists here
