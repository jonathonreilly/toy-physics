# Audit Ledger

**Generated:** 2026-04-27T02:52:12.457844+00:00
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
| _proposed_retained_ | 306 |
| _proposed_promoted_ | 6 |
| bounded | 185 |
| support | 101 |
| open | 11 |
| unknown | 744 |
| ~~audited_decoration~~ | 1 |
| ~~audited_numerical_match~~ | 1 |
| ~~audited_conditional~~ | 246 |

| audit_status | count |
|---|---:|
| `audit_in_progress` | 3 |
| `audited_conditional` | 4 |
| `audited_decoration` | 1 |
| `audited_numerical_match` | 1 |
| `unaudited` | 1592 |

| criticality | count |
|---|---:|
| `critical` | 91 |
| `high` | 569 |
| `medium` | 85 |
| `leaf` | 856 |

- **Proposed claims demoted by upstream:** 124
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
| `confinement_string_tension_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `dm_neutrino_schur_suppression_theorem_note_2026-04-15` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `native_gauge_closure_note` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | B | - |
| `yt_ew_color_projection_theorem` | _proposed_retained_ | ~~audited_conditional~~ | ~~audited_conditional~~ | cross_family | codex-current | F | - |
| `alpha_lm_geometric_mean_identity_theorem_note_2026-04-24` | _proposed_retained_ | ~~audited_decoration~~ | ~~audited_decoration~~ | cross_family | codex-current | A | - |
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
