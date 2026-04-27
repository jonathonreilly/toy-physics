# Audit Ledger

**Generated:** 2026-04-27T03:21:25.721281+00:00
**Source of truth:** `data/audit_ledger.json`
**Schema:** see [README.md](README.md), [FRESH_LOOK_REQUIREMENTS.md](FRESH_LOOK_REQUIREMENTS.md), and [ALGEBRAIC_DECORATION_POLICY.md](ALGEBRAIC_DECORATION_POLICY.md).

This file is auto-generated. Do not edit by hand. Apply audits via `scripts/apply_audit.py`, then re-run `scripts/compute_effective_status.py` and `scripts/render_audit_ledger.py`.

## Reading rule

- **Bold** = audit-ratified (`retained`, `promoted`).
- _Italic_ = author-proposed but not yet audit-ratified (`proposed_retained`, `proposed_promoted`).
- ~~Strikethrough~~ = audit returned a failure verdict.
- Plain = `support`, `bounded`, `open`, or `unknown`.

Publication-facing tables MUST read `effective_status`, not `current_status`.

## Summary

| effective_status | count |
|---|---:|
| **retained** | 2 |
| _proposed_retained_ | 294 |
| _proposed_promoted_ | 6 |
| bounded | 185 |
| support | 101 |
| open | 11 |
| unknown | 739 |
| ~~audited_decoration~~ | 1 |
| ~~audited_numerical_match~~ | 2 |
| ~~audited_conditional~~ | 260 |

| audit_status | count |
|---|---:|
| `audit_in_progress` | 3 |
| `audited_clean` | 2 |
| `audited_conditional` | 9 |
| `audited_decoration` | 1 |
| `audited_numerical_match` | 2 |
| `unaudited` | 1584 |

| criticality | count |
|---|---:|
| `critical` | 91 |
| `high` | 569 |
| `medium` | 85 |
| `leaf` | 856 |

- **Proposed claims demoted by upstream:** 128
- **Citation cycles detected:** 283

### Runner classification (static heuristic)

- runners classified: 679
- runners with (C) first-principles compute hits: 410
- runners with (D) external comparator hits: 173
- decoration candidates (no C, no D): 71

## Top 25 by load-bearing score (topology only)

Criticality and load-bearing score are computed from the citation graph alone. The audit lane intentionally does not use author-declared flagship status — that would let unratified framing drive audit cost on upstream support claims.

| # | claim_id | criticality | desc | score | audit_status | effective |
|---:|---|---|---:|---:|---|---|
| 1 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | 170 | 33.92 | `unaudited` | ~~audited_conditional~~ |
| 2 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | critical | 170 | 33.42 | `unaudited` | ~~audited_conditional~~ |
| 3 | `alpha_s_derived_note` | critical | 275 | 32.61 | `unaudited` | unknown |
| 4 | `observable_principle_from_axiom_note` | critical | 276 | 28.61 | `unaudited` | unknown |
| 5 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | critical | 170 | 28.42 | `unaudited` | ~~audited_conditional~~ |
| 6 | `ckm_atlas_axiom_closure_note` | critical | 170 | 25.92 | `unaudited` | ~~audited_conditional~~ |
| 7 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | critical | 170 | 25.42 | `unaudited` | _proposed_promoted_ |
| 8 | `three_generation_structure_note` | critical | 273 | 25.10 | `unaudited` | ~~audited_conditional~~ |
| 9 | `one_generation_matter_closure_note` | critical | 273 | 24.60 | `unaudited` | ~~audited_conditional~~ |
| 10 | `three_generation_observable_theorem_note` | critical | 273 | 24.60 | `unaudited` | ~~audited_conditional~~ |
| 11 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | critical | 170 | 24.42 | `unaudited` | ~~audited_conditional~~ |
| 12 | `graph_first_su3_integration_note` | critical | 275 | 23.11 | `audit_in_progress` | _proposed_retained_ |
| 13 | `yt_ward_identity_derivation_theorem` | critical | 273 | 23.10 | `unaudited` | ~~audited_conditional~~ |
| 14 | `yt_ew_color_projection_theorem` | critical | 276 | 22.61 | `audited_conditional` | ~~audited_conditional~~ |
| 15 | `anomaly_forces_time_theorem` | critical | 273 | 22.60 | `unaudited` | ~~audited_conditional~~ |
| 16 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | critical | 170 | 21.92 | `unaudited` | unknown |
| 17 | `minimal_axioms_2026-04-11` | critical | 273 | 21.60 | `unaudited` | ~~audited_conditional~~ |
| 18 | `left_handed_charge_matching_note` | critical | 273 | 21.10 | `unaudited` | ~~audited_conditional~~ |
| 19 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | critical | 273 | 20.60 | `unaudited` | ~~audited_conditional~~ |
| 20 | `higgs_mass_derived_note` | critical | 276 | 20.11 | `unaudited` | unknown |
| 21 | `physical_lattice_necessity_note` | critical | 273 | 20.10 | `unaudited` | ~~audited_conditional~~ |
| 22 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | critical | 170 | 19.92 | `unaudited` | ~~audited_conditional~~ |
| 23 | `ckm_first_row_magnitudes_theorem_note_2026-04-24` | critical | 170 | 19.92 | `unaudited` | unknown |
| 24 | `native_gauge_closure_note` | critical | 274 | 19.60 | `audited_conditional` | ~~audited_conditional~~ |
| 25 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | critical | 170 | 19.42 | `unaudited` | ~~audited_conditional~~ |


## Applied audits

| claim_id | current | audit_status | effective | independence | auditor_family | load-bearing class | decoration parent |
|---|---|---|---|---|---|---|---|
| `graph_first_selector_derivation_note` | _proposed_retained_ | audit_in_progress | _proposed_retained_ | - | - | - | - |
| `graph_first_su3_integration_note` | _proposed_retained_ | audit_in_progress | _proposed_retained_ | - | - | - | - |
| `s3_mass_matrix_no_go_note` | _proposed_retained_ | audit_in_progress | _proposed_retained_ | - | - | - | - |
| `i3_zero_exact_theorem_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `planck_parent_source_hidden_character_no_go_note_2026-04-24` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `confinement_string_tension_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `dm_neutrino_schur_suppression_theorem_note_2026-04-15` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `gravity_clean_derivation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | E | - |
| `linear_response_true_kubo_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `native_gauge_closure_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `neutrino_dirac_z3_support_trichotomy_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `strong_cp_theta_zero_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | E | - |
| `wave_retardation_continuum_limit_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `yt_ew_color_projection_theorem` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | F | - |
| `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | _proposed_retained_ | ~~audited_decoration~~ | ~~audited_decoration~~ | cross_family | codex-current | A | - |
| `bell_inequality_derived_note` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |
| `ckm_down_type_scale_convention_support_note_2026-04-22` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |


## Audit findings (full)

### `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24`

- **Note:** [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](../../docs/ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_decoration~~
- **effective_status:** ~~audited_decoration~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** By the retained definitions, alpha_LM^2 = (alpha_bare / u_0)^2 = alpha_bare^2 / u_0^2 = alpha_bare * (alpha_bare / u_0^2) = alpha_bare * alpha_s(v).  _(class `A`)_
- **chain closes:** True — The identity follows exactly from the coupling definitions stated in the source note, but it is only an algebraic restatement of the accepted coupling chain and has no independent comparator or physical observable.
- **rationale:** Issue: The load-bearing step is exact algebra from the definitions alpha_LM = alpha_bare/u_0 and alpha_s(v) = alpha_bare/u_0^2, but the row presents this bookkeeping corollary as a separate proposed-retained theorem and registers no parent dependency or primary runner. Why this blocks: A definition-level geometric-mean identity adds no independent observable, comparator, falsifiability, or new physical bridge beyond the upstream plaquette/coupling surface, so it should not inflate the retained claim surface as a standalone theorem. Repair target: Box this identity under the retained plaquette/coupling-chain parent, or re-promote only if it is shown to be genuine compression used load-bearing by downstream claims with an explicit parent dependency. Claim boundary until fixed: It is safe to state the exact identity as a bookkeeping corollary of the accepted coupling definitions and to use it to avoid double-counting alpha_LM and alpha_s(v) as independent knobs.
- **open / conditional deps cited:**
  - `accepted_plaquette_coupling_chain_parent_not_registered`
- **auditor confidence:** high

### `bell_inequality_derived_note`

- **Note:** [`BELL_INEQUALITY_DERIVED_NOTE.md`](../../docs/BELL_INEQUALITY_DERIVED_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_numerical_match~~
- **effective_status:** ~~audited_numerical_match~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** For the hard-coded two-species tensor product Hamiltonian H=H1⊗I+I⊗H1+G V(i,j)|i><i|⊗|j><j|, selected small-lattice/large-G points give Horodecki CHSH values above 2 while G=0 gives |S|=2.000.  _(class `G`)_
- **chain closes:** False — The runner reproduces CHSH violations for selected model parameters, but the physical tensor species, D5 Poisson coupling, and large-G/continuum scale selection are not derived or registered as one-hop retained inputs.
- **rationale:** Issue: the runner cleanly computes CHSH>2 for the specified two-species staggered-lattice Hamiltonian, but the retained claim is load-bearing on selected small lattices and large chosen G values, plus unregistered assumptions that two distinguishable retained species supply the bipartition and that the diagonal periodic-Poisson density coupling is the relevant gravitational interaction. Why this blocks: G=0 is a good null control, but the violations are parameter-surface results, not a derived physical Bell prediction; in 3D the runner itself shows no violation at G=1000 and violation only at G=2000/5000, while the note states that the physical interpretation of these couplings and the continuum limit are not established. Repair target: register the Hilbert/two-species matter theorem and D5 Poisson-coupling authority as one-hop dependencies, derive the physical normalization of G and its continuum scaling, and add a runner that tests a fixed derived coupling/continuum-refinement family rather than sweeping to violation. Claim boundary until fixed: it is safe to claim a reproducible model-surface CHSH violation for the listed finite lattices and selected couplings, with explicit Cl(3) taste-operator checks and G=0 null controls; it is not yet an audited retained framework-native or physical gravitational Bell-violation theorem.
- **open / conditional deps cited:**
  - `SINGLE_AXIOM_HILBERT_NOTE_not_registered_one_hop`
  - `retained_multi_species_matter_content_not_registered_one_hop`
  - `D5_periodic_Poisson_coupling_not_registered_one_hop`
  - `physical_G_normalization_and_continuum_limit_not_derived`
- **auditor confidence:** high

### `ckm_down_type_scale_convention_support_note_2026-04-22`

- **Note:** [`CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md`](../../docs/CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_numerical_match~~
- **effective_status:** ~~audited_numerical_match~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The bounded lane's current live support uses threshold-local because R_pred matches R_thresh at +0.20% but is +15.0% above R_common; the scale split is exactly the transport factor.  _(class `G`)_
- **chain closes:** False — The runner verifies a coherent numerical relation among PDG scale conventions, but the threshold-local comparator and the 5/6 bridge are explicitly not derived by this note.
- **rationale:** Issue: The load-bearing support comes from choosing the threshold-local mass-ratio comparator, where the framework prediction is +0.20%, while the common-scale comparator gives a +15% mismatch; the note explicitly says the 5/6 bridge and the natural scale convention remain open. Why this blocks: A proposed-retained support claim cannot be ratified as structural closure when the sharp evidence depends on a selected comparator scale plus PDG running inputs, and no one-hop dependencies for alpha_s(v), CKM atlas, the 5/6 bridge, or the down-type lane are registered. Repair target: Derive the 5/6 bridge and a framework-natural scale-convention theorem, register those as clean dependencies, and keep the runner's exact transport identity separate from PDG comparator checks. Claim boundary until fixed: It is safe to claim that the threshold-local and common-scale comparisons differ by the QCD transport factor and that the threshold-local comparison gives a sub-percent numerical support check; it is not a retained theorem-grade down-type mass-ratio closure.
- **open / conditional deps cited:**
  - `DOWN_TYPE_MASS_RATIO_CKM_DUAL_NOTE.md`
  - `CKM_FIVE_SIXTHS_BRIDGE_SUPPORT_NOTE.md`
  - `ALPHA_S_DERIVED_NOTE.md`
  - `CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`
  - `PDG_2024_mass_and_alpha_s_inputs`
- **auditor confidence:** high

### `confinement_string_tension_note`

- **Note:** [`CONFINEMENT_STRING_TENSION_NOTE.md`](../../docs/CONFINEMENT_STRING_TENSION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The framework's graph-first SU(3) gauge sector is SU(3) Yang-Mills at beta = 6.0, SU(3) YM confines at T = 0, and the string tension follows from the framework alpha_s(M_Z) = 0.1181 through standard lattice/EFT inputs.  _(class `B`)_
- **chain closes:** False — The note and runner combine unregistered upstream framework claims with external lattice-QCD and EFT inputs; the runner checks consistency after setting those premises rather than deriving the physical bridge from the allowed audit packet.
- **rationale:** Issue: The failed step is claiming retained confinement/string-tension closure from graph-first SU(3), alpha_s(M_Z), Wilson confinement, Sommer-scale lattice inputs, and quark-screening corrections while none of those load-bearing authorities are registered one-hop dependencies for this row; several runner PASS lines are hard-coded `True` physical premises or external comparator checks. Why this blocks: The current packet demonstrates a bounded consistency story, not a derivation that the framework gauge sector is the relevant SU(3) YM theory with a computed string tension; the numerical match depends on imported lattice/EFT constants and a screening factor. Repair target: Register clean dependencies for graph-first SU(3), g_bare/beta normalization, the alpha_s lane, and the lattice/EFT string-tension bridge, and replace hard-coded True checks with a runner that computes only the bridge quantities from declared inputs while labeling external comparators separately. Claim boundary until fixed: It is safe to say that, conditional on the framework gauge sector being SU(3) YM at beta = 6.0 and on the standard lattice/EFT bridge, the numbers are consistent with confinement and a 435-484 MeV string-tension range; it is not audit-retained as a zero-parameter confinement theorem.
- **open / conditional deps cited:**
  - `GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`
  - `scripts/canonical_plaquette_surface.py`
  - `standard_lattice_qcd_sommer_and_string_tension_inputs`
- **auditor confidence:** high

### `dm_neutrino_schur_suppression_theorem_note_2026-04-15`

- **Note:** [`DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`](../../docs/DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Assume the retained weak-axis local Higgs family, exact selector potential, direct Gamma_1 bridge, and bosonic-normalization theorem selecting j = g_weak/sqrt(2); then y_nu^eff = j^2 / 32 = g_weak^2 / 64.  _(class `B`)_
- **chain closes:** False — The runner verifies the local Schur complement algebra for the specified matrices, but the retained conclusion imports unregistered assumptions about the weak-axis local lane, Gamma_1 bridge, bosonic normalization, and DM staircase mapping.
- **rationale:** Issue: The exact Schur identity is proved for the chosen local block, but the theorem's retained claim depends on unregistered upstream inputs: the retained weak-axis Higgs family, the direct post-EWSB Gamma_1 bridge, the bosonic-normalization result j = g_weak/sqrt(2), and the staircase conversion from y_eff to k_eff. Why this blocks: Without those dependencies in the audit packet and clean in the ledger, the result is conditional algebra on selected inputs rather than an independently retained local neutrino suppression theorem. Repair target: Register clean dependency notes for the selector curvature, Gamma_1 bridge, bosonic normalization, and DM staircase relation, and make the runner read or compute those declared inputs while separating the exact Schur complement theorem from the downstream k_eff comparison. Claim boundary until fixed: It is safe to claim that for the specified projectors and block M(m,j), the Schur return gives j^2/m and therefore gives g_weak^2/64 if m = 32 and j = g_weak/sqrt(2); it is not audit-retained as a closed DM denominator result.
- **open / conditional deps cited:**
  - `weak_axis_local_higgs_family_dependency_not_registered`
  - `gamma_1_direct_bridge_dependency_not_registered`
  - `bosonic_normalization_dependency_not_registered`
  - `dm_staircase_relation_dependency_not_registered`
- **auditor confidence:** high

### `gravity_clean_derivation_note`

- **Note:** [`GRAVITY_CLEAN_DERIVATION_NOTE.md`](../../docs/GRAVITY_CLEAN_DERIVATION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Self-consistency is imposed as L^{-1}=G_0; since G_0=(-Delta_lat)^{-1}, the field operator is set to L=G_0^{-1}=-Delta_lat, yielding the Poisson equation and then Newton's 1/r^2 law.  _(class `E`)_
- **chain closes:** False — The decisive closure condition L^{-1}=G_0, the source law rho=|psi|^2 as mass density, and the test-mass/action response are physical premises in the note, not derived or registered one-hop retained inputs; no primary runner is registered for the claim.
- **rationale:** Issue: the note advertises a zero-free-parameter derivation of Newton gravity from Cl(3) on Z^3, but the load-bearing step is the imposed physical closure condition L^{-1}=G_0, followed by unregistered identifications of rho=|psi|^2 as gravitational mass density and test-mass response via S=L(1-phi). Why this blocks: the algebra L=G_0^{-1} is valid once the closure condition is granted, and the Z^3 Green-function asymptotic is standard mathematics, but the audit packet does not derive or register the physical law that the gravitational field operator must have the same Green function as the propagator, nor the source/readout/mass-coupling maps needed to turn the Poisson equation into F=G_N M_1 M_2/r^2; the ledger also has no registered runner despite the note naming a command. Repair target: register a primary gravity-clean runner and one-hop retained theorems deriving the self-consistency condition, the Born/mass-density source map, the weak-field action/test-mass response, and the lattice Green-function normalization/asymptotic with controlled finite-lattice checks. Claim boundary until fixed: it is safe to claim a conditional weak-field chain: if the framework imposes L^{-1}=G_0 and the stated source/response maps, then the Z^3 Laplacian Green function gives a Newtonian 1/r potential and inverse-square force in lattice units; it is not yet an audited retained derivation of Newton gravity from the single axiom alone.
- **open / conditional deps cited:**
  - `self_consistency_L_inverse_equals_G0_theorem_not_registered`
  - `rho_equals_abs_psi_squared_mass_density_bridge_not_registered`
  - `weak_field_action_test_mass_response_not_registered`
  - `lattice_green_function_normalization_runner_not_registered`
  - `scripts/frontier_gravity_clean_derivation.py_not_registered_primary_runner`
- **auditor confidence:** high

### `i3_zero_exact_theorem_note`

- **Note:** [`I3_ZERO_EXACT_THEOREM_NOTE.md`](../../docs/I3_ZERO_EXACT_THEOREM_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Given linear amplitude composition and quadratic probability P=|A|^2, the inclusion-exclusion expression I_3=|A+B+C|^2-|A+B|^2-|A+C|^2-|B+C|^2+|A|^2+|B|^2+|C|^2 cancels identically.  _(class `A`)_
- **chain closes:** True — The source note is explicitly scoped to the Hilbert/Born surface, and the algebraic cancellation follows for arbitrary complex amplitudes without additional lattice assumptions.
- **rationale:** The retained claim is the scoped exact theorem that I_3 vanishes once amplitudes add linearly and probabilities are quadratic, not a freestanding derivation of the Born rule. The runner verifies the identity for arbitrary complex amplitudes, higher Sorkin orders under the Born rule, a non-Born control, and concrete 1D/3D lattice propagator cross-checks, with 6 computed passes and no failures. Residual boundary: this audit ratifies the Hilbert-surface no-third-order-interference theorem only; it does not promote any claim that P=|A|^2 itself has been derived from the lattice axioms alone.
- **auditor confidence:** high

### `linear_response_true_kubo_note`

- **Note:** [`LINEAR_RESPONSE_TRUE_KUBO_NOTE.md`](../../docs/LINEAR_RESPONSE_TRUE_KUBO_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The first-order recurrence gives d(cz)/ds = (1/T) sum_j (z_j - cz_free) 2 Re[A_j* B_j], and the note asserts that this derivative matches measured finite-difference responses across 44 families with r=0.9716 overall, r=0.9995 off-scaffold, and 42/44 sign agreement.  _(class `A`)_
- **chain closes:** False — The algebraic first-order recurrence can be read from the note, but the empirical 44-family finite-difference comparison is not reproducible from registered audit evidence because the ledger has no primary runner or runner output for this claim.
- **rationale:** Issue: the source note gives a plausible first-order derivative recurrence for the specified propagator and field, but the retained claim rests on a 44-family empirical finite-difference comparison and sign-agreement battery for which the audit packet has no registered primary runner, deterministic output, or ledger-recognized log. The note names scripts/linear_response_true_kubo.py and a log, but the ledger/queue runner_path is null, so those artifacts are not available as the registered primary evidence for this audit. Why this blocks the claim: Nature-grade retention requires the stated r=0.9716 overall, r=0.9995 off-scaffold, 42/44 sign agreement, and edge-case corrections to be reproducible from registered evidence; the analytic recurrence alone does not verify that the implementation computed the same derivative, used the claimed 44 families, compared against the finite-difference battery correctly, or supports the broad compact-principle interpretation. Repair target: register scripts/linear_response_true_kubo.py as the claim's primary runner, include or regenerate the deterministic 44-family dataset/log, and make the runner independently check both the recurrence derivative and the finite-difference comparison with exact thresholds for the reported correlations, sign counts, scaffold exclusions, and residual sign cases. Claim boundary until fixed: it is safe to claim a conditional first-order response formula for the specified propagator/field, subject to the derivation assumptions in the note; the 44-family correlation/sign-agreement result is unratified numerical support, not a retained physical theorem or retained compact-principle explanation.
- **open / conditional deps cited:**
  - `runner_not_registered_for_linear_response_true_kubo_note`
  - `logs/2026-04-07-linear-response-true-kubo.txt_not_registered_primary_output`
- **auditor confidence:** high

### `native_gauge_closure_note`

- **Note:** [`NATIVE_GAUGE_CLOSURE_NOTE.md`](../../docs/NATIVE_GAUGE_CLOSURE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Use this note as the publication-facing claim boundary for the CI(3) / Z^3 gauge lane on main: exact native Cl(3) / SU(2) algebra, derived graph-first weak-axis selector, and structural graph-first su(3) closure.  _(class `B`)_
- **chain closes:** False — The note aggregates SU(2), graph-first selector, and SU(3) integration results, but the audit row has no one-hop dependencies and no registered primary runner, so the claimed publication boundary does not close from the allowed audit packet.
- **rationale:** Issue: The failed step is treating this boundary note as retained authority for exact native SU(2), the derived graph-first selector, and structural SU(3) closure while the row supplies no one-hop dependency notes and no primary runner; the note only names scripts/results rather than making them auditable inputs. Why this blocks: A retained publication-facing gauge-lane boundary cannot be ratified from a summary note whose load-bearing algebra and computations are outside the allowed packet, especially when the SU(3) integration result is itself awaiting critical cross-confirmation. Repair target: Register the SU(2), selector, and SU(3) integration notes as explicit dependencies with clean effective statuses, attach a primary runner or split this boundary into separate auditable claims, and rerun the audit after the dependency graph exposes the proof chain. Claim boundary until fixed: It is safe to use this note as a bounded map of intended gauge-lane claims and to say the listed components have supporting scripts, but not to treat the combined gauge-structure backbone as audit-retained.
- **open / conditional deps cited:**
  - `scripts/frontier_non_abelian_gauge.py`
  - `scripts/frontier_graph_first_selector_derivation.py`
  - `scripts/frontier_graph_first_su3_integration.py`
- **auditor confidence:** high

### `neutrino_dirac_z3_support_trichotomy_note`

- **Note:** [`NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md`](../../docs/NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Assume the retained three-generation matter structure, the retained reduction of neutrino mass to the Dirac lane, and a single Higgs doublet with definite generation Z_3 charge q_H; then the allowed support of Y_nu is exactly one of three permutation patterns.  _(class `B`)_
- **chain closes:** False — The runner verifies the Z_3 support trichotomy once the left/right generation charges and single-Higgs q_H condition are supplied, but those retained atlas inputs are not registered as one-hop dependencies for this row.
- **rationale:** Issue: The exact support classification depends on unregistered upstream inputs: one-generation matter closure, three-generation matter structure, reduction to the Dirac neutrino lane, and the explicit single-Higgs definite-Z_3-charge condition. Why this blocks: The matrix-support trichotomy is valid algebra after those charges are supplied, but the audit packet does not establish the charges, the Dirac-lane reduction, or the Higgs charge bridge as clean retained dependencies, so the proposed-retained lane cannot close from this row alone. Repair target: Register clean dependency notes for the generation charges and Dirac-lane reduction, and either derive or keep explicitly bounded the single-Higgs q_H assumption; make the runner read those declared charges rather than hard-coding them as retained. Claim boundary until fixed: It is safe to claim the conditional theorem that given q_L=(0,+1,-1), q_R=(0,-1,+1), and one definite q_H, Y_nu support reduces from nine entries to one of three three-entry permutation patterns.
- **open / conditional deps cited:**
  - `one_generation_matter_closure_dependency_not_registered`
  - `three_generation_matter_structure_dependency_not_registered`
  - `neutrino_dirac_lane_reduction_dependency_not_registered`
  - `single_higgs_z3_charge_condition_not_derived`
- **auditor confidence:** high

### `planck_parent_source_hidden_character_no_go_note_2026-04-24`

- **Note:** [`PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md`](../../docs/PLANCK_PARENT_SOURCE_HIDDEN_CHARACTER_NO_GO_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Because C(c_cell, delta)=c_cell is constant on the affine hidden-character fiber while p_Schur(c_cell, delta)=c_cell+delta varies, p_Schur=p_event holds iff delta=0 and no carrier-only function can recover the Schur scalar on that fiber.  _(class `A`)_
- **chain closes:** True — The source note and runner prove the bounded no-go by an explicit two-point affine-fiber counterexample: identical carrier data produce different Schur scalars, so carrier commutation alone cannot force scalar equality.
- **rationale:** The claim is scoped as a negative no-go for the unconstrained carrier-only parent-source scalar route, not as a positive Planck coefficient derivation. The load-bearing hidden-character fiber is explicit in the source note and the runner verifies the kernel, two-parent counterexample, carrier-only non-recoverability, equivalence of scalar equality to delta=0, and normalization sensitivity. Residual boundary: this clean audit does not rule out a future no-hidden-character law or a direct gravitational carrier-identification theorem; it only closes the carrier-only route without such an extra law.
- **auditor confidence:** high

### `strong_cp_theta_zero_note`

- **Note:** [`STRONG_CP_THETA_ZERO_NOTE.md`](../../docs/STRONG_CP_THETA_ZERO_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note sets the retained action class to S_ret = S_Wilson + psi_bar(D[U]+m)psi with no bare θ slot, so θ_bare = 0 by the retained action-surface definition and arg det(M_u M_d)=0 on an explicit positive-mass surface gives θ_eff = 0.  _(class `E`)_
- **chain closes:** False — The runner verifies many consistency checks on the θ-free Wilson-plus-staggered scalar-mass surface, but the absence of a CP-odd F tilde F/θ operator and the positive real quark-mass surface are selected as retained action-class premises rather than derived from registered one-hop authorities.
- **rationale:** Issue: the decisive step is not a computed strong-CP cancellation but the retained-action-surface selection: the runner/support text takes 'no bare θ slot' and θ_bare = 0 from the action-class definition, and it uses an explicit positive real quark-mass surface for arg det(M_u M_d)=0. Why this blocks: the 13 theorem and 30 retained-surface compute passes show internal consistency of that restricted θ-free Wilson-plus-staggered scalar-mass surface, but they do not derive from the provided audit packet that the physical Cl(3)/Z^3 action forbids an allowed CP-odd F tilde F term, fixes the real-mass orientation, or dynamically selects θ=0 rather than merely evaluating the θ-free surface; the sampled topological positivity check also demonstrates the triangle-inequality minimum, not a derivation of the missing action-slot theorem. Repair target: add a retained operator-basis/action-surface theorem deriving from Cl(3)/Z^3 primitives and canonical normalization that no gauge-invariant CP-odd θ term is an admissible slot, register the positive real quark-mass orientation/arg-det theorem as a dependency, and update the runner so it constructs the allowed action basis and fails if an F tilde F term or complex mass phase is admitted. Claim boundary until fixed: it is safe to claim that on the explicitly θ-free Wilson-plus-staggered scalar-mass surface, the implemented determinant, axial-grid, effective-action, and sampled positive-weight checks find no generated strong-sector phase; it is not yet an audited retained solution of strong CP beyond that selected action surface.
- **open / conditional deps cited:**
  - `retained_action_surface_no_theta_slot_theorem_not_registered`
  - `positive_real_quark_mass_orientation_theorem_not_registered`
  - `theta_free_surface_selection_not_dynamical_theta_minimization`
- **auditor confidence:** high

### `wave_retardation_continuum_limit_note`

- **Note:** [`WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md`](../../docs/WAVE_RETARDATION_CONTINUUM_LIMIT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note's bottom-line refinement table asserts that rel_MI = 28.81% -> 9.53% -> 43.40%, rel_MN = 25.60% -> 1.26% -> 31.24%, rel_MIeq = 74.11% -> 29.44% -> 23.16%, while dM drifts only 14% monotonically, so the magnitude is comparator-dominated rather than continuum-stable.  _(class `C`)_
- **chain closes:** False — The stated negative follows from the refinement/comparator numerics only if the unregistered harness and logs are accepted; the ledger provides no primary runner or runner output, and the exact discrete static comparator remains explicitly unresolved.
- **rationale:** Issue: the retained negative is load-bearing on a numerical H-refinement and three-comparator sweep, but the audit ledger registers no primary runner or runner output for wave_retardation_continuum_limit_note, and the note itself says the correct exact discrete static comparator is still the bottleneck. Why this blocks: without a registered deterministic computation, a hostile auditor cannot verify the rel_MI, rel_MN, rel_MIeq, rel_IeqN, dM-drift, integer-rounding, or corrected-radial-distance numbers; and without the exact static comparator theorem/solve, the broad statement about a continuum retardation magnitude is limited to the particular tested comparators. Repair target: register scripts/wave_retardation_continuum_limit.py as the primary runner, include deterministic output for the H=0.50/0.35/0.25 battery, make the runner assert the reported tables and corrected dN geometry, and add either a direct discrete static solve or an analytic discrete Green-function comparator for the implemented lattice operator. Claim boundary until fixed: it is safe to say that the source note reports a conditional negative for the tested cached-static, equilibrated-static, and imposed-Newton comparators, and that the reported tables would downgrade the Lane 6/8b magnitude if reproduced; it is not yet an audited retained continuum theorem about retardation magnitude, while fixed-H M != I existence and the separate dM stability observation remain only conditional on the unregistered computation.
- **open / conditional deps cited:**
  - `runner_not_registered_for_wave_retardation_continuum_limit_note`
  - `logs/2026-04-07-wave-retardation-continuum-limit.txt_not_registered_primary_output`
  - `exact_discrete_static_comparator_not_derived`
- **auditor confidence:** high

### `yt_ew_color_projection_theorem`

- **Note:** [`YT_EW_COLOR_PROJECTION_THEOREM.md`](../../docs/YT_EW_COLOR_PROJECTION_THEOREM.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The physical EW coupling (matched to the continuum where the SU(3) and EW sectors are factored) should use the connected color trace N_c(N_c^2-1)/N_c^2 = (N_c^2-1)/N_c.  _(class `F`)_
- **chain closes:** False — The source note gives the Fierz identity and shows CMT is color-blind, but it does not derive the physical lattice-to-continuum EW-current matching rule that selects the connected trace as the coupling readout.
- **rationale:** Issue: The failed step is the assertion that the physical EW coupling extraction should replace the total color trace N_c by the connected color trace N_c(N_c^2-1)/N_c^2; no one-hop retained theorem or registered runner derives that matching/readout rule, and the source note's R_conn input is stated as leading-order 1/N_c with O(1/N_c^4) corrections. Why this blocks: A proposed_retained universal 9/8 correction to physical EW couplings cannot follow from an asserted normalization convention or from a leading-order corrected quantity; the exact Fierz and CMT algebra leave the connected-trace value and the physical readout selection as independent premises. Repair target: Add a retained theorem deriving the lattice-to-continuum EW current matching from Cl(3)/Z^3 primitives, register the R_conn authority as a one-hop dependency if it remains load-bearing, and provide a runner that computes the connected two-vertex observable/matching factor rather than applying 8/9. Claim boundary until fixed: It is safe to claim that CMT alone cannot produce 9/8, that 8/9 is a motivated connected-color-trace/large-N_c matching ansatz with controlled corrections, and that applying it improves the quoted g_1 and g_2 numerics.
- **open / conditional deps cited:**
  - `RCONN_DERIVED_NOTE.md`
- **auditor confidence:** high
