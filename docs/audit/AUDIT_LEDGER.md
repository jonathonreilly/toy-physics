# Audit Ledger

**Generated:** 2026-04-27T04:24:31.659531+00:00
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
| **retained** | 3 |
| _proposed_retained_ | 270 |
| _proposed_promoted_ | 6 |
| bounded | 185 |
| support | 101 |
| open | 11 |
| unknown | 734 |
| ~~audited_decoration~~ | 1 |
| ~~audited_numerical_match~~ | 3 |
| ~~audited_conditional~~ | 287 |

| audit_status | count |
|---|---:|
| `audit_in_progress` | 3 |
| `audited_clean` | 3 |
| `audited_conditional` | 28 |
| `audited_decoration` | 1 |
| `audited_numerical_match` | 3 |
| `unaudited` | 1563 |

| criticality | count |
|---|---:|
| `critical` | 91 |
| `high` | 569 |
| `medium` | 85 |
| `leaf` | 856 |

- **Proposed claims demoted by upstream:** 131
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
| 24 | `planck_parent_source_hidden_character_no_go_note_2026-04-24` | high | 119 | 19.91 | `audited_clean` | **retained** |
| 25 | `native_gauge_closure_note` | critical | 274 | 19.60 | `audited_conditional` | ~~audited_conditional~~ |


## Applied audits

| claim_id | current | audit_status | effective | independence | auditor_family | load-bearing class | decoration parent |
|---|---|---|---|---|---|---|---|
| `graph_first_selector_derivation_note` | _proposed_retained_ | audit_in_progress | _proposed_retained_ | - | - | - | - |
| `graph_first_su3_integration_note` | _proposed_retained_ | audit_in_progress | _proposed_retained_ | - | - | - | - |
| `s3_mass_matrix_no_go_note` | _proposed_retained_ | audit_in_progress | _proposed_retained_ | - | - | - | - |
| `i3_zero_exact_theorem_note` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `planck_finite_response_no_go_note_2026-04-24` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `planck_parent_source_hidden_character_no_go_note_2026-04-24` | _proposed_retained_ | ~~audited_clean~~ | **retained** | cross_family | codex-current | A | - |
| `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `causal_field_canonical_chain_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `complex_action_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | E | - |
| `confinement_string_tension_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `cosmology_single_ratio_inverse_reconstruction_theorem_note_2026-04-25` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `dm_neutrino_schur_suppression_theorem_note_2026-04-15` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `electrostatics_grown_sign_law_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `emergent_lorentz_invariance_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `gravity_clean_derivation_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | E | - |
| `higgs_mass_retention_analysis_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | D | - |
| `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `koide_dimensionless_objection_closure_review_packet_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `koide_pointed_origin_exhaustion_theorem_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `lensing_beta_sweep_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `lensing_deflection_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `lensing_k_sweep_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `linear_response_true_kubo_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `matter_inertial_closure_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `native_gauge_closure_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `neutrino_dirac_z3_support_trichotomy_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `planck_boundary_density_extension_theorem_note_2026-04-24` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `sign_portability_invariant_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `strong_cp_theta_zero_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | E | - |
| `wave_retardation_continuum_limit_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `yt_ew_color_projection_theorem` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | F | - |
| `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | C | - |
| `yt_p1_delta_r_2_loop_extension_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | A | - |
| `yt_p1_delta_r_sm_rge_crosscheck_note_2026-04-18` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | D | - |
| `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | _proposed_retained_ | ~~audited_decoration~~ | ~~audited_decoration~~ | cross_family | codex-current | A | - |
| `bell_inequality_derived_note` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |
| `ckm_down_type_scale_convention_support_note_2026-04-22` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |
| `yt_uv_to_ir_transport_obstruction_theorem_note_2026-04-17` | _proposed_retained_ | ~~audited_numerical_match~~ | ~~audited_numerical_match~~ | cross_family | codex-current | G | - |


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

### `area_law_primitive_edge_entropy_selector_no_go_note_2026-04-25`

- **Note:** [`AREA_LAW_PRIMITIVE_EDGE_ENTROPY_SELECTOR_NO_GO_NOTE_2026-04-25.md`](../../docs/AREA_LAW_PRIMITIVE_EDGE_ENTROPY_SELECTOR_NO_GO_NOTE_2026-04-25.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Within the finite primitive-edge class with H_cell=C^16, rho=I_16/16, rank(P_A)=4, locality/additivity, and standard von Neumann or binary entropy, none of the canonical entropy constructions gives the coefficient 1/4, and a gapped edge needs an extra Schmidt-spectrum selector.  _(class `A`)_
- **chain closes:** False — The runner verifies the finite-cell entropy arithmetic and the tunable gapped-edge counterexample, but the primitive cell, Planck Target 2 entropy requirement, and claimed exhaustiveness of the allowed finite primitive-edge entropy class are not registered one-hop dependencies. The no-go therefore closes for the supplied standard entropy constructions, not as a retained framework-wide Target 2 obstruction.
- **rationale:** Issue: the note correctly separates the primitive trace 4/16 from several standard von Neumann/binary entropy values, but it relies on unregistered authority for the source-free C^16 primitive cell, the rank-four boundary projector, the Planck Target 2 entanglement-entropy interpretation, and the claim that the listed finite-cell entropy constructions exhaust the canonical primitive-edge class. Why this blocks: the runner proves the arithmetic for the listed constructions and shows a same-gap two-level edge can be tuned through entropy 1/4, but it does not derive the physical entropy carrier, prove that no other retained entropy/readout functional is allowed, or register the finite-boundary density/action-side 1/4 authority it is distinguishing from entanglement entropy. Repair target: register the Planck conditional packet, finite-boundary density extension/primitive trace theorem, Target 2 entropy-carrier definition, and any allowed entropy functional class as dependencies; add an exhaustion theorem or runner proving that every retained primitive-edge entropy candidate reduces to the checked cases unless a named selector is supplied. Claim boundary until fixed: it is safe to claim a conditional no-go: for the stated C^16/rank-4 primitive data and standard entropy choices, the canonical entropies are log16, log4, log2, H(1/4), or 1/2, not 1/4, and hitting 1/4 in a gapped edge requires an additional Schmidt-spectrum selector; it is not yet an audited retained proof that Target 2 cannot be closed by any CL3 primitive-edge entropy construction.
- **open / conditional deps cited:**
  - `Planck_conditional_packet_primitive_trace_c_cell_equals_1_over_4_not_registered`
  - `finite_boundary_density_extension_theorem_not_registered_or_audited_conditional`
  - `source_free_C16_primitive_cell_and_rank_four_projector_authority_not_registered`
  - `Planck_Target_2_entanglement_entropy_carrier_definition_not_registered`
  - `canonical_primitive_edge_entropy_functional_class_exhaustiveness_not_registered`
  - `gapped_edge_Schmidt_spectrum_selector_open`
  - `operational_primitive_boundary_entropy_theorem_open`
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

### `causal_field_canonical_chain_note`

- **Note:** [`CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md`](../../docs/CAUSAL_FIELD_CANONICAL_CHAIN_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The package elevates the Shapiro phase lag and related causal-field observables as the canonical lab bridge while acknowledging that matched static cone/exposure proxies can reproduce the retained phase and escape effects and that c remains a free parameter.  _(class `B`)_
- **chain closes:** False — The note depends on multiple artifact notes/logs and lab-bridge claims that are not registered as one-hop dependencies, has no primary runner, and explicitly lacks a unique causal discriminator or absolute lab transfer/noise budget.
- **rationale:** Issue: the note is a proposed_retained causal-field package summary, but its numerical hierarchy and lab-facing Shapiro bridge rely on unregistered artifact scripts/logs/notes, and the source itself says the Shapiro phase and trapping escape are not uniquely causal because matched static proxies can reproduce them. Why this blocks: a retained canonical lab bridge cannot rest on a free cone speed c, missing transfer/noise/systematics budgets, no registered primary runner, and no one-hop retained support for the listed Shapiro, gravitomagnetic, escape, boundary-law, or diamond/NV bridge artifacts; the causal interpretation is underdetermined by the observable. Repair target: register the primary runners and logs for each retained observable, register the bridge notes as one-hop dependencies with their current statuses, derive or externally fix the field speed c, and add a discriminator runner comparing causal cone predictions against best matched static proxies plus a lab transfer/noise budget. Claim boundary until fixed: it is safe to treat this as a conditional inventory saying the causal-cone model naturally produces the listed phase/escape/gravitomagnetic signatures and that Shapiro phase is a shape-sensitive observable; it is not yet an audited retained causal-field lab prediction or unique causal discriminator.
- **open / conditional deps cited:**
  - `SHAPIRO_DELAY_NOTE.md_not_registered_one_hop`
  - `SHAPIRO_STATIC_DISCRIMINATOR_NOTE.md_not_registered_one_hop`
  - `GRAVITOMAGNETIC_NOTE.md_not_registered_one_hop`
  - `CAUSAL_ESCAPE_WINDOW_NOTE.md_not_registered_one_hop`
  - `diamond_NV_lab_bridge_notes_not_registered_one_hop`
  - `causal_field_primary_runner_not_registered`
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

### `complex_action_note`

- **Note:** [`COMPLEX_ACTION_NOTE.md`](../../docs/COMPLEX_ACTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note introduces the ansatz S=L(1-f)+i gamma L f, so exp(i k S)=exp(i k L(1-f)) exp(-k gamma L f), and uses a free gamma sweep to interpolate between Newtonian deflection and absorption-biased centroid shifts.  _(class `E`)_
- **chain closes:** False — The complex-action form and gamma parameter are imposed rather than derived, the claimed horizon interpretation is not tied to black-hole observables, and the audit ledger has no registered runner/output for the numerical tables.
- **rationale:** Issue: the load-bearing step is an introduced complex-action ansatz with a free gamma parameter, not a retained derivation of a horizon term from Cl(3)/Z^3 or from the gravity chain; the registered audit packet also has no primary runner/output even though the note names a script and log. Why this blocks: Born preservation follows structurally from linearity once the kernel is accepted, and the tabulated centroid/escape behavior may be a valid model sweep, but a free imaginary coupling cannot support the retained claim that gravity and horizons are unified, nor can an absorption-biased AWAY centroid shift be identified with horizon physics without photon-sphere/Schwarzschild/Hawking or causal-horizon tests. Repair target: register scripts/complex_action_harness.py as the primary runner with deterministic output, derive gamma or the imaginary action term from retained primitives, run resolution/geometry checks around the exceptional point, and add horizon-specific observables rather than centroid-shift proxies. Claim boundary until fixed: it is safe to claim a conditional one-parameter complex-kernel model where gamma=0 reduces to the real-action propagator, linearity keeps I3 near machine zero, and positive gamma produces absorption-biased escape/centroid behavior in the listed setup; it is not yet an audited retained gravity-horizon unification theorem.
- **open / conditional deps cited:**
  - `complex_action_imaginary_term_derivation_not_registered`
  - `gamma_selection_theorem_not_registered`
  - `scripts/complex_action_harness.py_not_registered_primary_runner`
  - `logs/2026-04-05-complex-action-harness.txt_not_registered_primary_output`
  - `horizon_observable_bridge_not_derived`
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

### `cosmology_single_ratio_inverse_reconstruction_theorem_note_2026-04-25`

- **Note:** [`COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md`](../../docs/COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the retained/admitted flat-FRW w_Lambda=-1 surface, the four inverse reconstructions L_H(a), L_q, L_mL, and L_acc must agree and equal (H_inf/H_0)^2.  _(class `A`)_
- **chain closes:** False — The inverse formulas close as exact algebra once the flat-FRW matter+radiation+Lambda surface and L=(H_inf/H_0)^2 bridge are assumed, but those authorities are not registered as one-hop dependencies for this audit row. The runner reads and status-checks those notes directly, so the retained/admitted surface is imported rather than supplied by the constrained audit packet.
- **rationale:** Issue: the theorem's exact inverse identities are algebraically correct on a flat matter+radiation+Lambda FRW surface with w_Lambda=-1 and L=Omega_Lambda,0=(H_inf/H_0)^2, but the audit row registers no one-hop dependencies for the FRW forward theorem, matter-bridge theorem, dark-energy EOS corollary, or cosmological-constant/spectral-gap identity that define that surface. Why this blocks: the result is not an unconditional retained theorem from the source note alone; the runner's authority-status PASSes read external notes and publication wiring files outside the ledger dependency packet, and the note itself says the matter-content bridge and numerical ratio remain open. Repair target: register the FRW kinematic reduction, Omega_Lambda matter bridge, dark-energy EOS, and spectral-gap authority notes as one-hop dependencies, audit or demote their statuses explicitly, and make the runner validate the inverse identities only after loading the registered authority set and its allowed status. Claim boundary until fixed: it is safe to claim a conditional algebraic certificate: given the stated flat-FRW w_Lambda=-1 surface, fixed R, nonnegative M,L, and the L=(H_inf/H_0)^2 bridge, each listed observable reconstructs the same L and cross-consistency can falsify that surface; it is not yet an audited retained cosmology closure or independent derivation of H_inf/H_0, Omega_Lambda, Omega_m, or the matter bridge.
- **open / conditional deps cited:**
  - `COSMOLOGY_FRW_KINEMATIC_REDUCTION_THEOREM_NOTE_2026-04-24.md_not_registered_one_hop_dependency`
  - `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md_not_registered_one_hop_dependency`
  - `DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md_not_registered_one_hop_dependency`
  - `flat_FRW_wLambda_minus_one_surface_is_admitted_not_independently_audited_here`
  - `matter_content_bridge_and_numerical_H_inf_over_H0_remain_open`
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

### `electrostatics_grown_sign_law_note`

- **Note:** [`ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md`](../../docs/ELECTROSTATICS_GROWN_SIGN_LAW_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the fixed retained grown row drift=0.2, restore=0.7, the tabulated single-source, neutral-pair, like-pair, dipole, and double-charge cases have the expected sign response and a +1 to +2 charge exponent of 1.000.  _(class `C`)_
- **chain closes:** False — The claim is a narrow numerical grown-geometry compute, but the ledger has no registered runner/output and the artifact paths in the note are absolute external paths rather than audit-registered evidence.
- **rationale:** Issue: the retained sign-law companion rests on frozen numerical results for one fixed grown geometry row, but the audit ledger registers no primary runner or output, and the note's artifact links are absolute local paths outside the audit packet. Why this blocks: a hostile auditor cannot reproduce the printed delta_z signs, neutral cancellation, dipole partial cancellation, or +1/+2 linearity threshold from registered evidence; moreover the note explicitly limits the result to fixed-field, no graph update, one source layer, and one final-layer centroid on a single grown row. Repair target: register scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py as the claim runner with deterministic output and explicit PASS thresholds for sign, cancellation, and charge-linearity; either keep the note scoped to the single grown row or add sweeps over grown-geometry parameters, graph update, source layers, and detector definitions. Claim boundary until fixed: it is safe to say the source note reports a conditional fixed-row sign-law transfer check with neutral cancellation and approximate charge linearity; it is not yet an audited retained grown-geometry theorem or geometry-generic electrostatics result.
- **open / conditional deps cited:**
  - `scripts/ELECTROSTATICS_GROWN_SIGN_LAW.py_not_registered_primary_runner`
  - `logs/2026-04-05-electrostatics-grown-sign-law.txt_not_registered_primary_output`
  - `grown_geometry_parameter_sweep_not_performed`
  - `graph_update_case_not_tested`
- **auditor confidence:** high

### `emergent_lorentz_invariance_note`

- **Note:** [`EMERGENT_LORENTZ_INVARIANCE_NOTE.md`](../../docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** On the retained hierarchy surface a ~ 1/M_Planck, the dimension-6 cubic-lattice correction is suppressed by (E/M_Planck)^2, so Lorentz invariance is emergent to all currently accessible precision.  _(class `B`)_
- **chain closes:** False — The runner verifies the staggered/bosonic dispersion expansion and cubic-harmonic angular structure, but the broad emergent-observable conclusion relies on CPT exactness, parity protection, and a ~ 1/M_Planck as imported bridges. Those bridges are not registered as one-hop dependencies for this claim and are asserted in the runner rather than derived or read from audited inputs.
- **rationale:** Issue: the source note's structural dispersion and cubic-harmonic checks are reproduced by the registered runner, but the retained conclusion that Lorentz invariance holds to all accessible precision depends on unregistered bridge premises: exact CPT, exact/tree-level parity protection against odd-dimension LV, and the hierarchy-scale identification a ~ 1/M_Planck. Why this blocks: without ledger one-hop dependencies and a runner that constructs or verifies those bridges, a hostile auditor cannot distinguish a theorem from a calculation performed on an assumed symmetry/scale surface; the runner's CPT, P, and hierarchy checks are hard-coded assertions downstream of the contested inputs. Repair target: register the CPT_EXACT_NOTE, a parity/operator-basis theorem forbidding dimension-5 LV on the relevant action surface, and the hierarchy theorem fixing the physical lattice spacing as dependencies, then update the runner to read/verify those inputs and fail if any bridge is absent or conditional. Claim boundary until fixed: it is safe to claim the conditional lattice result that the implemented Z^3 staggered and Laplacian dispersions have leading O(a^2 p^4) cubic-harmonic anisotropy and exact cubic isotropy at leading order; the Planck-suppressed observable-Lorentz-invariance theorem remains conditional on the unregistered symmetry and scale bridges.
- **open / conditional deps cited:**
  - `CPT_EXACT_NOTE.md_not_registered_one_hop_dependency`
  - `parity_operator_basis_dimension5_LV_no_go_theorem_not_registered`
  - `hierarchy_scale_a_equals_planck_length_theorem_not_registered`
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

### `higgs_mass_retention_analysis_note_2026-04-18`

- **Note:** [`HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](../../docs/HIGGS_MASS_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The retained band m_H = 125.04 GeV +/- 3.17 GeV is obtained by propagating the inherited YT through-2-loop Delta_R uncertainty with A_MH=2.67 and combining it in quadrature with loop-transport, classicality-BC, and threshold-matching retention gaps.  _(class `D`)_
- **chain closes:** False — The runner reproduces the stated budget arithmetic and an RGE sensitivity probe, but it consumes many unregistered inherited authorities as constants and uses a local 2-loop RGE replica while the note's central claim is the canonical 3-loop route. The audit packet therefore does not independently close the retained Higgs-band derivation or the observed-mass comparator claim.
- **rationale:** Issue: the Higgs retention band is a propagated budget built from inherited YT Delta_R bands, canonical Higgs authority centrals, hierarchy/canonical-surface constants, loop-geometric assumptions, quadrature independence, and the observed Higgs comparator, but none of these authorities are registered as one-hop dependencies for this row. Why this blocks: the runner can verify arithmetic after those inputs are supplied, but it does not derive the YT +/-0.70% band, the 125.1/119.8 GeV Higgs authority centrals, the 3-loop canonical RGE route, the loop-tail/geometric-gap model, the lambda(M_Pl)=0 classicality correction, or the independence assumptions behind the 3.17 GeV quadrature band; moreover its local compute_mh probe is documented as a 2-loop replica, not the canonical 3-loop runner that the note cites as authority. Repair target: register the YT Delta_R stack, canonical Higgs 3-loop runner/output, 2-loop authority, canonical plaquette/hierarchy constants, loop-geometric bound, classicality-BC theorem, threshold-matching source, and observed-mass comparator as dependencies; update the primary runner to call or reproduce the canonical 3-loop implementation and assert the 3.17 GeV band from registered outputs with explicit covariance/quadrature assumptions. Claim boundary until fixed: it is safe to claim a conditional retention-budget calculation: given the supplied inherited inputs and quadrature model, the script reproduces m_H about 125.04 GeV with a roughly 3.17 GeV 1-sigma budget and includes the observed 125.25 GeV value; it is not yet an audited retained first-principles Higgs-mass precision theorem or an independent validation of the YT/Higgs authority chain.
- **open / conditional deps cited:**
  - `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `HIGGS_MASS_DERIVED_NOTE.md_not_registered_one_hop_dependency`
  - `HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md_not_registered_one_hop_dependency`
  - `scripts/frontier_higgs_mass_full_3loop.py_not_registered_dependency_output`
  - `quadrature_independence_model_for_retention_gaps_not_registered`
  - `observed_higgs_mass_comparator_not_registered`
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

### `koide_a1_radian_bridge_irreducibility_audit_note_2026-04-24`

- **Note:** [`KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md`](../../docs/KOIDE_A1_RADIAN_BRIDGE_IRREDUCIBILITY_AUDIT_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Retained periodic phase sources give only q*pi phases, while the Brannen selected-line target is the pure rational 2/9 used as a radian, so a Type-B rational-to-radian observable law remains primitive.  _(class `A`)_
- **chain closes:** False — The runner verifies the rational-pi versus pure-rational arithmetic and several finite-Wilson/A1 no-go probes, but the audit packet does not register the authority that this list exhausts retained phase sources or that the selected-line Koide/Brannen target is the required observable. Thus the no-go is valid for the supplied source taxonomy, not closed as a retained framework-wide irreducibility theorem.
- **rationale:** Issue: the no-go rests on an unregistered taxonomy asserting that all retained periodic phase sources are Type-A q*pi objects, while the Koide/Brannen selected-line delta target is a Type-B pure rational 2/9 to be read as radians; the note also imports branch-local no-go probes and Type-B witnesses without one-hop dependency registration. Why this blocks: the runner proves exact arithmetic for the listed examples and the mathematical separation q*pi in Q only at zero, but it does not prove the retained source list is exhaustive, that no allowed retained observable law can set a period-1-rad convention, or that the selected-line Brannen target is the physical readout. Repair target: register the retained phase-source classification, Brannen selected-line parameterization, April 24 Koide packet, APS/ABSS eta and other 2/9 witness authorities, plus the fractional-topology no-go probes as dependencies; add an exhaustive theorem or runner showing every retained phase/readout source factors through q*pi unless a named new primitive is added. Claim boundary until fixed: it is safe to claim conditional no-go support: for the listed finite lattice/APBC/BZ/Z3/C9/Wilson/Berry phase sources, phases are q*pi and cannot equal nonzero 2/9 radians, and the listed rational witnesses do not by themselves supply a unit map; it is not yet an audited retained proof that all possible CL3 retained routes to the Koide A1 radian bridge are irreducible.
- **open / conditional deps cited:**
  - `retained_periodic_phase_source_exhaustiveness_theorem_not_registered`
  - `Type_A_Type_B_phase_vs_rational_taxonomy_not_registered`
  - `Brannen_selected_line_delta_target_not_registered`
  - `period_1_rad_vs_2pi_rad_observable_convention_law_not_registered`
  - `KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md_not_registered_and_audited_conditional`
  - `APS_ABSS_eta_2_over_9_authority_not_registered`
  - `SU3_Casimir_hypercharge_charge_product_2_over_9_witness_authorities_not_registered`
  - `fractional_topology_no_go_probe_bundle_not_registered`
  - `equivariant_index_A1_no_go_authority_not_registered`
  - `minimal_heat_kernel_multitrace_no_go_authority_not_registered`
- **auditor confidence:** high

### `koide_dimensionless_objection_closure_review_packet_2026-04-24`

- **Note:** [`KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md`](../../docs/KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The packet's safe retained-support statement is that KOIDE_DIMENSIONLESS_RETAINED_CLOSURE=FALSE because traceless Z backgrounds and ambient/spectator endpoint sources remain counterdomains unless extra source-domain and boundary laws are derived.  _(class `A`)_
- **chain closes:** False — The runner verifies the algebraic countermodels and conditional Q/delta closures, but the retained source carrier, Z label, APS eta value, selected-line endpoint law, and based endpoint section are imported premises rather than registered one-hop dependencies. The primary runner also does not emit every expected closeout line in the note, so the support packet is not fully closed by the registered runner output.
- **rationale:** Issue: the packet correctly avoids claiming full dimensionless Koide closure, but its proposed-retained support/no-go status relies on unregistered authorities for the normalized two-channel source-response carrier, retained central/projected commutant source grammar with Z, the April 25 background-zero/Z-erasure and onsite-source-domain results, the APS eta_APS=2/9 value, and the physical selected-line/based-endpoint boundary setup. Why this blocks: the primary runner proves rational counterexamples inside a supplied model, not that the supplied model is the retained physical source domain or that no retained boundary law elsewhere selects the closing quotient; it also omits several expected closeout declarations from the note, including the onsite-source-domain conditional and residual source-domain line. Repair target: register the source-response, onsite-source-domain, Q/delta split no-go, pointed-origin/endpoint, APS eta, and hostile-review guard authorities as one-hop dependencies; make the primary runner or registered runner bundle assert every expected closeout line and fail if any residual authority is missing. Claim boundary until fixed: it is safe to claim conditional support/no-go evidence: within the supplied two-channel source-response and endpoint-source toy algebra, z=0 gives Q=2/3, traceless Z and ambient endpoint sources give exact counterdomains, selected-line plus based endpoint would give delta=2/9, and full retained closure remains unestablished; it is not yet an audited retained proof of the physical dimensionless Koide obstruction or of all listed residual boundaries.
- **open / conditional deps cited:**
  - `retained_two_channel_source_response_carrier_not_registered`
  - `central_projected_commutant_Z_source_grammar_not_registered`
  - `april_25_background_zero_Z_erasure_criterion_theorem_not_registered`
  - `april_25_onsite_source_domain_synthesis_not_registered`
  - `APS_eta_APS_equals_2_over_9_authority_not_registered`
  - `selected_line_local_boundary_source_law_not_registered`
  - `based_endpoint_section_theorem_not_registered`
  - `scripts/frontier_koide_q_delta_readout_retention_split_no_go.py_not_registered_runner_dependency`
  - `scripts/frontier_koide_pointed_origin_exhaustion_theorem.py_not_registered_runner_dependency`
  - `scripts/frontier_koide_hostile_review_guard.py_not_registered_runner_dependency`
  - `scripts/frontier_koide_q_onsite_source_domain_no_go_synthesis.py_not_registered_runner_dependency`
- **auditor confidence:** high

### `koide_pointed_origin_exhaustion_theorem_note_2026-04-24`

- **Note:** [`KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md`](../../docs/KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Within the residual dimensionless Koide atlas, unpointed retained tests are invariant along the Q source-translation, CP1 selected-line, and endpoint-torsor fibres while the open charged-lepton readouts change, so origin-free retained data do not force the closing representative.  _(class `A`)_
- **chain closes:** False — The runner proves exact algebraic/torsor countermodels inside the supplied residual atlas, but that atlas, its three fibres, the eta_APS readout, and the claim that these are the retained unpointed tests are not registered as one-hop dependencies. The theorem therefore closes conditionally inside the modeled atlas, not as an audited retained exhaustion theorem for the full Koide lane.
- **rationale:** Issue: the no-go/exhaustion theorem assumes a residual Koide atlas with exactly three unpointed freedoms: Q source-origin translation, CP1 selected-line source choice, and endpoint torsor translation, but the audit row registers no one-hop authority that this atlas is complete or retained. Why this blocks: the runner proves that polynomial invariants, scalar equivariant marks, and torsor-invariant data cannot choose the pointed representative in the supplied model, but it does not derive that the physical charged-lepton readout is restricted to that model or that no retained source/boundary law already selects the needed origin. Repair target: register the residual Koide atlas, source-response carrier, CP1/selected-line primitive, endpoint torsor, eta_APS readout, April 24 Koide packet, and background-zero/Z-erasure authorities as dependencies; add an exhaustion theorem showing these fibres are complete for retained unpointed data. Claim boundary until fixed: it is safe to claim conditional necessity inside the stated atlas: a pointed origin law would close Q=2/3 and delta=2/9, while unpointed invariant data admit countermodels; it is not yet an audited retained proof that all CL3 Koide dimensionless closure routes require exactly those physical source/boundary-origin laws.
- **open / conditional deps cited:**
  - `residual_dimensionless_Koide_atlas_not_registered`
  - `Q_source_response_background_translation_fibre_not_registered`
  - `CP1_selected_line_rank_two_primitive_not_registered`
  - `endpoint_torsor_readout_model_not_registered`
  - `eta_APS_Z3_1_2_equals_2_over_9_authority_not_registered`
  - `KOIDE_DIMENSIONLESS_OBJECTION_CLOSURE_REVIEW_PACKET_2026-04-24.md_not_registered_and_audited_conditional`
  - `background_zero_Z_erasure_criterion_authority_not_registered`
  - `selected_line_local_boundary_source_law_not_registered`
  - `based_endpoint_section_theorem_not_registered`
  - `retained_physical_source_boundary_origin_law_open`
- **auditor confidence:** high

### `lensing_beta_sweep_note`

- **Note:** [`LENSING_BETA_SWEEP_NOTE.md`](../../docs/LENSING_BETA_SWEEP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note asserts that beta=5 at H=0.5 is an isolated near-1/b coarse-grid spike because beta=7 and beta=10 leave it and the beta=5 refinement at H=0.35 flips sign with slope -0.7930.  _(class `C`)_
- **chain closes:** False — The falsification depends on numerical sweep/refinement tables, but the ledger has no registered primary runner or output and the note gives only absolute local artifact paths.
- **rationale:** Issue: the proposed_retained negative rests on a beta sweep and H-refinement numerical battery, but the audit ledger registers no primary runner/output, and the source note's artifacts are absolute local paths outside the audit packet. Why this blocks: a hostile auditor cannot reproduce the key beta=5 coarse slope, the beta=7/10 sign/shape departures, or the H=0.35 sign flip/slope -0.7930 from registered evidence; the result is also scoped to Fam1 b={3,4,5,6} and does not register the adjoint-kernel authority it uses for interpretation. Repair target: register scripts/lensing_beta_sweep.py and the deterministic log as primary evidence, add explicit PASS thresholds for slopes/sign patterns/shape spread, extend or explicitly bound the beta-neighborhood and H-refinement checks, and register the adjoint-kernel note if it remains interpretive support. Claim boundary until fixed: it is safe to say the source note reports a conditional numerical negative that the beta=5 coarse-grid near-1/b point did not survive nearby beta checks or one H=0.35 refinement; it is not yet an audited retained closure of the narrow-beam/ray-optics rescue.
- **open / conditional deps cited:**
  - `scripts/lensing_beta_sweep.py_not_registered_primary_runner`
  - `logs/2026-04-08-lensing-beta-sweep.txt_not_registered_primary_output`
  - `LENSING_ADJOINT_KERNEL_NOTE.md_not_registered_one_hop`
  - `multi_family_or_broader_H_refinement_not_registered`
- **auditor confidence:** high

### `lensing_deflection_note`

- **Note:** [`LENSING_DEFLECTION_NOTE.md`](../../docs/LENSING_DEFLECTION_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** At H=0.25 on b in {3,4,5,6}, kubo_true(b) follows a clean power law with slope about -1.43 and R^2 = 0.998, so the retained gravity-side result is a non-standard power law rather than Newton/Einstein 1/b lensing.  _(class `C`)_
- **chain closes:** False — The claim rests on numerical lensing sweeps, fine single-b runs, and combined log-log fits, but the ledger registers no primary runner or runner output. The quoted slopes, R^2 values, H-refinement drift, and b=3 reference match cannot be reproduced from the audit packet.
- **rationale:** Issue: the retained partial positive depends on a numerical Lane L/L+ sweep -- H=0.25 fine b in {3,4,5,6}, kubo_true slope -1.4335, dM slope -1.5162, R^2 near 0.998/0.995, and a b=3 match to the Lane-alpha reference -- but the ledger runner_path is null even though the note names multiple scripts and logs. Why this blocks: without a registered deterministic runner and output, a hostile auditor cannot verify the grown-DAG setup, b/H sampling, OOM workaround, fit subset choices, Kubo/finite-difference agreement, reference-point comparison, or the downgrade from 1/b to a steeper non-standard exponent. Repair target: register the primary lensing-deflection runner or a deterministic L+ aggregate runner, include the fine-single outputs and combined-analysis log as primary outputs, and make the runner assert the per-b table, slope/R^2 fits, H-drift table, b=3 reference agreement, and the failure of the -1 exponent under explicit thresholds. Claim boundary until fixed: it is safe to say the source note reports a conditional non-standard power-law signal in the tested Fam1 lensing harness and downgrades the old 1/b headline; it is not yet an audited retained gravity-side functional-form theorem or continuum-stable lensing prediction.
- **open / conditional deps cited:**
  - `scripts/lensing_deflection_sweep.py_not_registered_primary_runner`
  - `scripts/lensing_deflection_fine_single.py_not_registered_primary_runner`
  - `scripts/lensing_deflection_lane_lplus.py_not_registered_primary_runner`
  - `logs/2026-04-07-lensing-deflection-sweep.txt_not_registered_primary_output`
  - `logs/2026-04-07-lensing-fine-asymptotic.txt_not_registered_primary_output`
  - `logs/2026-04-07-lensing-deflection-lane-lplus.txt_not_registered_primary_output`
- **auditor confidence:** high

### `lensing_k_sweep_note`

- **Note:** [`LENSING_K_SWEEP_NOTE.md`](../../docs/LENSING_K_SWEEP_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note asserts that the mean lensing slope varies from +0.58 to about -1.43 across k*H values, with sign flips at k*H=0.5 and 5.0, so the earlier -1.40 slope at k*H=2.5 is configuration-specific rather than a geometric invariant.  _(class `C`)_
- **chain closes:** False — The diagnostic depends on numerical k-sweep tables and an eikonal comparison, but the ledger has no registered primary runner/output and no one-hop dependency for the eikonal/mechanism interpretation.
- **rationale:** Issue: the proposed_retained diagnostic rests on a numerical k-sweep over one Fam1 setup with three seeds per k*H value, but the audit ledger registers no primary runner/output for scripts/lensing_k_sweep.py or its log. Why this blocks: a hostile auditor cannot reproduce the reported slope range, sign flips, R^2 ranges, seed spread, or eikonal-gap oscillation from registered evidence; additionally, the inference that the correction is a wave-interference mechanism is stronger than the table alone unless supported by registered kernel/mode analysis. Repair target: register the k-sweep runner and deterministic output with PASS thresholds for slopes/signs/seed spread, register the eikonal baseline and adjoint-kernel/mode analysis used to infer mechanism, and extend or explicitly bound family/H/b-range coverage. Claim boundary until fixed: it is safe to say the source note reports a conditional numerical diagnostic that the reference k*H=2.5 slope is not invariant within the tested sweep; it is not yet an audited retained theorem that lensing is a k-dependent wave-interference phenomenon.
- **open / conditional deps cited:**
  - `scripts/lensing_k_sweep.py_not_registered_primary_runner`
  - `logs/2026-04-09-lensing-k-sweep.txt_not_registered_primary_output`
  - `eikonal_baseline_not_registered_one_hop`
  - `kernel_or_mode_interference_analysis_not_registered`
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

### `matter_inertial_closure_note`

- **Note:** [`MATTER_INERTIAL_CLOSURE_NOTE.md`](../../docs/MATTER_INERTIAL_CLOSURE_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Gaussian packets under the same uniform linear force give Newton-linear delta_z(g) per packet but equivalence-principle slopes differing by 123% across packets, so generator-invariant inertial mass fails at the persistent-object level.  _(class `C`)_
- **chain closes:** False — The retained negative depends on numerical packet-propagator measurements, but the audit ledger registers no primary runner or runner output for this claim. The source note's quoted slopes, R^2 values, spread ratios, and family-portability numbers are therefore not reproducible from the audit packet.
- **rationale:** Issue: the source note reports a concrete numerical negative for Gaussian-packet matter closure, but the load-bearing values -- slopes -73.5, -7.05, -18.3; R^2 > 0.96; 123% slope spread; persistence ratios; and Fam1/2/3 portability -- are backed only by an artifact chain named in the note, while the ledger runner_path is null. Why this blocks: a Nature-grade audit cannot verify that the same grown-DAG propagator, packet definitions, force coupling, baseline subtraction, and slope fits produced the quoted failure; the qualitative 'fields but no matter' conclusion depends on those exact computations rather than on an analytic theorem in the note. Repair target: register scripts/matter_inertial_closure.py as the primary runner, preserve or regenerate logs/2026-04-07-matter-inertial-closure.txt, and make the runner assert the null response, per-packet R^2 thresholds, slope table, 123% equivalence failure metric, persistence ratios, and Fam1/2/3 portability thresholds deterministically. Claim boundary until fixed: it is safe to say that the source note reports a conditional negative for the specific Gaussian-packet plus uniform-linear-force closure attempt; it is not yet an audited retained theorem that the grown-DAG propagator lacks generator-invariant inertial mass, and it does not exclude other persistent-object definitions or modified actions.
- **open / conditional deps cited:**
  - `scripts/matter_inertial_closure.py_not_registered_primary_runner`
  - `logs/2026-04-07-matter-inertial-closure.txt_not_registered_primary_output`
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

### `planck_boundary_density_extension_theorem_note_2026-04-24`

- **Note:** [`PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md`](../../docs/PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Any local additive rule agreeing with c_cell = 1/4 on one primitive face must give N_A(P) = n * c_cell = c_cell * A(P) / a^2 on every finite boundary patch tiled by n primitive faces.  _(class `A`)_
- **chain closes:** False — The finite-union additivity proof closes as algebra once locality, additivity, cubic orientation symmetry, and c_cell = 1/4 are assumed. The proposed Planck-lane conclusion still depends on the unregistered primitive-coefficient authority and the explicitly open gravitational carrier premise.
- **rationale:** Issue: the runner verifies the finite-patch additive extension, but the source note is explicitly a support theorem inside a conditional Planck packet: it assumes c_cell = 1/4 and states that the primitive boundary/worldtube count has not yet been derived as the microscopic carrier of gravitational boundary/action density. Why this blocks: the algebra N_A(P)=n c_cell and the conditional a/l_P=1 normalization are valid only after those premises are granted; with no ledger one-hop dependency for the primitive coefficient and no retained carrier-identification theorem, the result cannot be promoted as a closed Planck-boundary density derivation. Repair target: register the primitive c_cell=1/4 theorem as a dependency, add a retained carrier-identification theorem deriving that the one-step boundary/worldtube count is the gravitational boundary/action carrier, and make the runner fail unless those inputs are present and retained. Claim boundary until fixed: it is safe to claim the exact finite-face extension: given locality, additivity, cubic-frame orientation symmetry, and primitive c_cell=1/4, every finite face-union patch has density c_cell/a^2, and if the gravitational carrier premise is later derived this extension preserves the conditional a/l_P=1 normalization.
- **open / conditional deps cited:**
  - `primitive_c_cell_equals_one_fourth_theorem_not_registered`
  - `gravitational_boundary_action_carrier_identification_theorem_open`
- **auditor confidence:** high

### `planck_finite_response_no_go_note_2026-04-24`

- **Note:** [`PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md`](../../docs/PLANCK_FINITE_RESPONSE_NO_GO_NOTE_2026-04-24.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_clean~~
- **effective_status:** **retained**  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The signed-permutation finite frame B_4 has min_{g != I} ||g-I||_F = 2 and therefore zero infinitesimal tangent, while linearized metric/coframe response requires nonzero Sym^2(R^4) directions of dimension 10.  _(class `A`)_
- **chain closes:** True — The note is scoped to a finite-automorphism-only no-go, and the source plus runner give an exact group-theoretic identity-gap/tangent-dimension obstruction. The retained parent-source hidden-character no-go is already audited clean and is cited only as an independent remaining-route boundary, not as a missing premise for this finite-response no-go.
- **rationale:** The claim is a bounded negative theorem about the finite-automorphism-only Planck route, not a positive Planck-scale derivation. The runner explicitly enumerates B_4, verifies |B_4|=384, proves the nearest nonidentity element is Frobenius distance 2, checks the empty infinitesimal neighborhood, contrasts zero finite-group tangent with the 10-dimensional symmetric metric-response space, and confirms the finite-dimensional trace obstruction for canonical commutators. Residual boundary: this clean audit only closes the finite automorphism route; it does not derive the gravitational carrier identification or rule out realified/canonical response surfaces.
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

### `sign_portability_invariant_note`

- **Note:** [`SIGN_PORTABILITY_INVARIANT_NOTE.md`](../../docs/SIGN_PORTABILITY_INVARIANT_NOTE.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The note infers a portable signed-control fixed point across retained sign-law basins from exact zero-source/neutral cancellation, plus-minus antisymmetry, and weak-field exponents near 1.0 in multiple family notes and a comparison runner.  _(class `B`)_
- **chain closes:** False — The synthesis depends on multiple family notes, a comparison script/log, and a holdout package, but the ledger lists no one-hop dependencies and no registered primary runner/output for this claim.
- **rationale:** Issue: the proposed_retained portability invariant is a cross-family comparison, but the audit packet provides no registered one-hop family notes and no primary runner/output for SIGN_PORTABILITY_INVARIANT_COMPARE.py. Why this blocks: a hostile auditor cannot verify that the named families are themselves retained, that their exact controls and weak-field exponents use compatible protocols, or that the claimed signed-control fixed point is independent of basin width/seed selectivity rather than a summary label imposed after filtering passing rows. Repair target: register the comparison runner/log, add the family and holdout notes as one-hop dependencies with their current audit statuses, and make the runner assert common thresholds for zero-source cancellation, neutral same-point cancellation, antisymmetry, unit-slope tolerance, and basin/seed exclusions. Claim boundary until fixed: it is safe to say the source note proposes a conditional comparison invariant across reported sign-law families; it is not yet an audited retained portability theorem or independent order parameter.
- **open / conditional deps cited:**
  - `scripts/SIGN_PORTABILITY_INVARIANT_COMPARE.py_not_registered_primary_runner`
  - `logs/2026-04-06-sign-portability-invariant.txt_not_registered_primary_output`
  - `retained_sign_family_notes_not_registered_one_hop`
  - `fifth_family_holdout_notes_not_registered_one_hop`
  - `common_threshold_protocol_not_registered`
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

### `yt_p1_bz_quadrature_full_staggered_pt_note_2026-04-18`

- **Note:** [`YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md`](../../docs/YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The full Kawamoto-Smit staggered-PT 4D BZ quadrature with MSbar subtraction yields Delta_R = -3.77% +/- 0.45% and moves Delta_R from literature-cited status to framework-native retained status with sub-half-percent precision.  _(class `C`)_
- **chain closes:** False — The runner recomputes the N=32/48/64 quadrature and assembles the stated number, but the registered audit row has no one-hop dependencies for the retained Feynman rules, canonical surface, MSbar subtraction, taste normalizations, prior brackets, or 5% systematic model. Those premises are imported or hard-coded rather than closed inside the audit packet.
- **rationale:** Issue: the retained-status upgrade from a full staggered-PT quadrature rests on unregistered upstream authorities and physical-normalization choices: the Ward identity, Rep-A/Rep-B three-channel formula, H_unit Feynman rules, Delta_1/Delta_2/Delta_3 ranges, prior schematic and master Delta_R notes, canonical plaquette constants, MSbar subtraction prescription, N_TASTE normalization, and the asserted 5% full-PT systematic are all used but the ledger row lists no one-hop dependencies. Why this blocks: the runner verifies the quadrature arithmetic once those rules and constants are supplied, but it does not derive the Kawamoto-Smit/taste-normalized integrands from retained CL3 primitives, prove the continuum-subtraction prescription, justify the n_f=6 matching surface, or substantiate the 5% systematic/covariance model; it also compares to prior/literature brackets that are absent from the audit packet. Repair target: register the cited notes and canonical-surface script as one-hop dependencies, add or cite a retained theorem deriving the full staggered Feynman rules, MSbar subtraction, taste averaging, and systematic budget, and update the runner to fail if those dependencies or uncertainty inputs change rather than hard-coding them. Claim boundary until fixed: it is safe to claim a reproducible conditional quadrature calculation which, given the supplied staggered-PT rules, canonical constants, and 5% per-channel systematic, produces I_v_scalar=3.902, I_v_gauge=0, I_SE_gluonic=2.323, I_SE_fermion=0.996, and Delta_R=-3.769% +/-0.452%; it is not yet an audited retained first-principles framework-native precision theorem.
- **open / conditional deps cited:**
  - `YT_P1_BZ_QUADRATURE_NUMERICAL_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md_not_registered_one_hop_dependency`
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_H_UNIT_RENORMALIZATION_FRAMEWORK_NATIVE_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `scripts/canonical_plaquette_surface.py_not_registered_one_hop_dependency`
  - `MSbar_continuum_subtraction_and_N_TASTE_normalization_theorem_not_registered`
  - `five_percent_full_PT_systematic_model_not_registered`
- **auditor confidence:** high

### `yt_p1_delta_r_2_loop_extension_note_2026-04-18`

- **Note:** [`YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md`](../../docs/YT_P1_DELTA_R_2_LOOP_EXTENSION_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** Applying the retained loop-geometric bound r_R=0.22126 to the retained 1-loop central Delta_R=-3.27% and assuming same-sign bound saturation gives Delta_R^{through-2-loop}=Delta_R^{1-loop}(1+r_R)=-3.99% with P1 in [3.3%, 4.7%].  _(class `A`)_
- **chain closes:** False — The runner verifies the algebra of the color-tensor enumeration and envelope propagation, but the 1-loop central, loop-geometric bound, canonical constants, P3 analogy, m_t comparator, and same-sign/bound-saturation interpretation are imported without registered one-hop dependencies. The eight 2-loop BZ integrals are explicitly open, so the through-2-loop central is an assumed envelope scenario rather than a derived 2-loop correction.
- **rationale:** Issue: the proposed-retained 2-loop extension turns an inherited 1-loop central and inherited loop-geometric bound into a retained through-2-loop central by assuming the unknown 2-loop term saturates the bound and has the same sign, while all eight 2-loop BZ integrals remain open and the row registers no one-hop dependencies for the 1-loop master, loop-geometric theorem, canonical surface, P3 color-template notes, or observed m_t comparator. Why this blocks: the runner confirms exact Casimir arithmetic and envelope propagation after those inputs are supplied, but it does not compute any J_X integral, derive the 2-loop sign, justify saturation as a central estimate, or reconcile authority between the older literature-cited -3.27% base and the later full-staggered -3.77% canonical cross-reference. Repair target: register and audit the 1-loop master, full-staggered 1-loop update, loop-geometric bound, Rep-A/Rep-B, Delta_i notes, P3 color-factor templates, canonical constants, and comparator sources; either compute the eight J_X BZ integrals with a runner or demote the -3.99% value to a named envelope scenario with no retained central status. Claim boundary until fixed: it is safe to claim a conditional structural envelope: given Delta_R^{1-loop}=-3.27085% and r_R=0.221264, the 2-loop magnitude is bounded by 0.7237%, the geometric tail by 0.9294%, the bound-saturated same-sign scenario gives -3.9946%, and the broad m_t lane contains 172.69 GeV; it is not yet an audited retained 2-loop Delta_R computation or first-principles P1 precision closure.
- **open / conditional deps cited:**
  - `YT_P1_DELTA_R_MASTER_ASSEMBLY_THEOREM_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P1_LOOP_GEOMETRIC_BOUND_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_1_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_2_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_DELTA_3_BZ_COMPUTATION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_and_audited_conditional`
  - `YT_P1_BZ_QUADRATURE_2_LOOP_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_P3_MSBAR_TO_POLE_K3_COLOR_FACTOR_RETENTION_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `scripts/canonical_plaquette_surface.py_not_registered_one_hop_dependency`
  - `eight_two_loop_BZ_integrals_J_FF_J_FA_J_AA_J_Fl_J_Al_J_ll_J_FFh_J_Fh_open`
  - `same_sign_bound_saturation_central_assumption_not_derived`
  - `observed_m_t_PDG_comparator_not_registered`
- **auditor confidence:** high

### `yt_p1_delta_r_sm_rge_crosscheck_note_2026-04-18`

- **Note:** [`YT_P1_DELTA_R_SM_RGE_CROSSCHECK_NOTE_2026-04-18.md`](../../docs/YT_P1_DELTA_R_SM_RGE_CROSSCHECK_NOTE_2026-04-18.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_conditional~~
- **effective_status:** ~~audited_conditional~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The backward 2-loop SM RGE gives y_t/g_s(M_Pl)=0.78510, whose naive comparison to Ward*(1+Delta_R)=0.3949 fails by +95.6%, and the note classifies this as consistent only after invoking an orthogonal v-scale matching decomposition M = sqrt(8/9)*F_yt*sqrt(u_0).  _(class `D`)_
- **chain closes:** False — The runner verifies the SM-RGE integration and several arithmetic checks, but the consistency verdict depends on unregistered Ward, Delta_R, v-boundary, color-projection, CMT, P2 matching, and QFP-envelope authorities. The runner also tests the older -3.27% Delta_R central, while the note says the canonical retained central has been superseded to -3.77% +/- 0.45%.
- **rationale:** Issue: the registered runner is a valid deterministic SM-RGE arithmetic check, but the retained cross-validation conclusion is conditional on a large set of unregistered authorities and on the interpretive claim that the 95.6% direct-comparison gap is orthogonal to the M_Pl scheme-conversion Delta_R rather than a failed comparator. Why this blocks: from the audit packet alone, a hostile auditor can verify that backward SM RGE gives y_t/g_s(M_Pl)=0.78510 and that it does not equal Ward*(1+Delta_R)=0.3949; the packet cannot independently validate the v-scale color projection, CMT endpoint, P2 M decomposition, QFP envelope, Delta_i inputs, or the orthogonality theorem that turns that failed direct comparison into support for Delta_R. Repair target: register the Ward, Delta_i/Delta_R, zero-import boundary, P2 v-matching, QFP-envelope, color-projection, CMT endpoint, and canonical -3.77% BZ-quadrature authorities as one-hop dependencies, and update the runner to consume their outputs, test both -3.27% and canonical -3.77% surfaces explicitly, and assert a derived factorization theorem explaining why the direct M_Pl ratio comparison is not the relevant observable. Claim boundary until fixed: it is safe to claim a conditional numerical cross-check: given the framework primary-chain v-boundaries and accepted v-scale matching factorization, the SM 2-loop backward integration is reproducible and does not by itself falsify the chosen Delta_R scheme-conversion interpretation; it is not an audited retained independent validation of Delta_R or of the full lattice-to-SM translation.
- **open / conditional deps cited:**
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md_not_registered_one_hop_dependency`
  - `YT_P1_REP_A_REP_B_CANCELLATION_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_P1_BZ_QUADRATURE_FULL_STAGGERED_PT_NOTE_2026-04-18.md_not_registered_one_hop_dependency`
  - `YT_ZERO_IMPORT_CHAIN_NOTE.md_not_registered_one_hop_dependency`
  - `YT_P2_V_MATCHING_THEOREM_NOTE_2026-04-17.md_not_registered_one_hop_dependency`
  - `YT_QFP_INSENSITIVITY_SUPPORT_NOTE.md_not_registered_one_hop_dependency`
  - `color_projection_and_CMT_endpoint_factorization_theorem_not_registered`
- **auditor confidence:** high

### `yt_uv_to_ir_transport_obstruction_theorem_note_2026-04-17`

- **Note:** [`YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md`](../../docs/YT_UV_TO_IR_TRANSPORT_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)
- **current_status:** _proposed_retained_
- **audit_status:** ~~audited_numerical_match~~
- **effective_status:** ~~audited_numerical_match~~  (reason: `self`)
- **auditor:** `codex-audit-loop`  (codex-current; independence=cross_family)
- **load-bearing step:** The packaged residuals (P1, P2, P3) = (1.92%, 0.50%, 0.30%) are combined in quadrature as sigma_YT = sqrt(P1^2 + P2^2 + P3^2) ~= 1.95% to define the retained master envelope on the Ward ratio.  _(class `G`)_
- **chain closes:** False — The runner reproduces the arithmetic of the packaged envelope and the qualitative P1/P2/P3 partition, but the residual centrals are imported, heuristic, or hard-coded rather than derived from registered one-hop authorities. The source note also states that the per-primitive central values and transport primitives remain open downstream work.
- **rationale:** Issue: the master obstruction's quantitative retention rests on the packaged residual inputs P1=1.92%, P2=0.50%, and P3=0.30%; P2 and P3 are heuristic/hard-coded tails, P1 is a selected single-channel packaged magnitude, and the note itself says the per-primitive centrals are not derived from first principles on the retained canonical surface. Why this blocks: the runner verifies the quadrature arithmetic and broad scale partition after those numbers are supplied, but it does not derive the P1 lattice-to-MSbar correction, the P2 UV-to-IR transport residual, the P3 K-series tail, or the independence/correlation assumptions needed for the envelope; the current output also gives sigma_YT=2.010% and Delta m_t=3.47 GeV while the text rounds this as ~1.95% and ~3.4 GeV. Repair target: register the Ward, color-projection, plaquette/canonical-surface, P1/P2/P3 residual, and comparator authorities as one-hop dependencies; replace the hard-coded residuals with runner computations or cited retained outputs, and make the runner assert the current rounded envelope and m_t uncertainty from those inputs with explicit correlation rules. Claim boundary until fixed: it is safe to claim an organizational obstruction that a direct Ward-identity promotion to y_t(v) or m_t(pole) requires separate UV matching, transport, and pole-conversion inputs, and that the supplied packaged numbers arithmetically give about a 2.01% Ward-ratio envelope; it is not an audited retained theorem-grade quantitative envelope or first-principles YT transport result.
- **open / conditional deps cited:**
  - `YT_WARD_IDENTITY_DERIVATION_THEOREM.md_not_registered_one_hop_dependency`
  - `YT_EW_COLOR_PROJECTION_THEOREM.md_not_registered_one_hop_dependency`
  - `PLAQUETTE_SELF_CONSISTENCY_NOTE.md_not_registered_one_hop_dependency`
  - `P1_lattice_to_MSbar_residual_theorem_not_registered`
  - `P2_UV_to_IR_transport_residual_theorem_open_or_not_registered`
  - `P3_K_series_tail_residual_theorem_open_or_not_registered`
- **auditor confidence:** high
