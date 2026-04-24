# Manuscript Claims Surface

Use [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) alongside
this file. This is the short public surface for what the paper may claim. It
is intentionally not the full package ledger.

For broader inventory and companion lanes, use:

- [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md)
- [FULL_CLAIM_LEDGER.md](./FULL_CLAIM_LEDGER.md)
- [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md)

## Status Legend

- `retained`: safe as a core paper claim on the current package surface
- `retained companion`: exact or structural companion that belongs in Extended
  Data, theorem boxes, or discussion rather than as a headline claim
- `promoted quantitative`: quantitative row the package is prepared to present
  explicitly
- `flagship closed package`: major package-level closeout on the manuscript
  surface
- `open flagship lane`: scientifically central lane still open
- `bounded companion`: useful package result kept outside the manuscript core

## External Inputs

The current manuscript conditions phenomenology on:

- `T_CMB = 2.7255 K`
- `H_0 = 67.4 km/s/Mpc`

The accepted package statement is `Cl(3)` on `Z^3` as the physical theory.
The electroweak scale is not treated as an external input on the manuscript
surface.

## Manuscript-Core Claims

| Claim | Status | Placement | Authority | Primary runner |
|---|---|---|---|---|
| `Cl(3)` on `Z^3` is the working physical theory | retained | main text | [ARXIV_DRAFT.md](./ARXIV_DRAFT.md), [MINIMAL_AXIOMS_2026-04-11.md](../../MINIMAL_AXIOMS_2026-04-11.md) | n/a |
| Weak-field gravity from the Poisson self-consistency / Newton chain on `Z^3` | retained | main text | [SELF_CONSISTENCY_FORCES_POISSON_NOTE.md](../../SELF_CONSISTENCY_FORCES_POISSON_NOTE.md), [POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md](../../POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md), [NEWTON_LAW_DERIVED_NOTE.md](../../NEWTON_LAW_DERIVED_NOTE.md) | [frontier_self_consistent_field_equation.py](../../../scripts/frontier_self_consistent_field_equation.py), [frontier_poisson_exhaustive_uniqueness.py](../../../scripts/frontier_poisson_exhaustive_uniqueness.py), [frontier_newton_derived.py](../../../scripts/frontier_newton_derived.py) |
| Full discrete `3+1` GR on the project route | retained | main text / theorem box | [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](../../UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md) | [frontier_universal_gr_discrete_global_closure.py](../../../scripts/frontier_universal_gr_discrete_global_closure.py) |
| Chosen continuum/QG identification chain on the project route | retained companion | Extended Data / theorem box | [UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md](../../UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md), [GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md](./GRAVITY_PUBLICATION_PACKAGE_SUMMARY_2026-04-15.md) | [frontier_universal_qg_canonical_textbook_continuum_gr_closure.py](../../../scripts/frontier_universal_qg_canonical_textbook_continuum_gr_closure.py) |
| Exact native `SU(2)` and graph-first structural `SU(3)` on the accepted package surface | retained | main text | [NATIVE_GAUGE_CLOSURE_NOTE.md](../../NATIVE_GAUGE_CLOSURE_NOTE.md), [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_non_abelian_gauge.py](../../../scripts/frontier_non_abelian_gauge.py), [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| Anomaly-forced `3+1`, one-generation matter closure, SM hypercharge uniqueness/electric-charge quantization, `SU(2)` Witten global-anomaly cancellation, B-L anomaly freedom as a gaugeable option, and retained three-generation matter structure | retained | main text | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md), [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](../../ONE_GENERATION_MATTER_CLOSURE_NOTE.md), [STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md](../../STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md), [SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md](../../SU2_WITTEN_Z2_ANOMALY_THEOREM_NOTE_2026-04-24.md), [BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md](../../BMINUSL_ANOMALY_FREEDOM_THEOREM_NOTE_2026-04-24.md), [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md), [PHYSICAL_LATTICE_NECESSITY_NOTE.md](../../PHYSICAL_LATTICE_NECESSITY_NOTE.md) | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py), [frontier_sm_hypercharge_uniqueness.py](../../../scripts/frontier_sm_hypercharge_uniqueness.py), [frontier_su2_witten_z2_anomaly.py](../../../scripts/frontier_su2_witten_z2_anomaly.py), [frontier_bminusl_anomaly_freedom.py](../../../scripts/frontier_bminusl_anomaly_freedom.py), [frontier_three_generation_observable_theorem.py](../../../scripts/frontier_three_generation_observable_theorem.py) |
| Strong CP closure on the retained action surface at `theta_eff = 0` | retained | main text / theorem box | [STRONG_CP_THETA_ZERO_NOTE.md](../../STRONG_CP_THETA_ZERO_NOTE.md) | [frontier_strong_cp_theta_zero.py](../../../scripts/frontier_strong_cp_theta_zero.py) |
| Electroweak hierarchy row `v = 246.282818290129 GeV` on the accepted package surface | promoted quantitative | quantitative section | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md), [PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md](../../PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) |
| `alpha_s(M_Z)`, the `alpha_LM` geometric-mean identity, electroweak normalization, and retained YT/top transport package | promoted quantitative + retained support | quantitative section / Extended Data | [ALPHA_S_DERIVED_NOTE.md](../../ALPHA_S_DERIVED_NOTE.md), [ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md), [YT_EW_COLOR_PROJECTION_THEOREM.md](../../YT_EW_COLOR_PROJECTION_THEOREM.md), [YT_WARD_IDENTITY_DERIVATION_THEOREM.md](../../YT_WARD_IDENTITY_DERIVATION_THEOREM.md) | [frontier_complete_prediction_chain.py](../../../scripts/frontier_complete_prediction_chain.py), [frontier_alpha_lm_geometric_mean_identity.py](../../../scripts/frontier_alpha_lm_geometric_mean_identity.py), [frontier_yt_ward_identity_derivation.py](../../../scripts/frontier_yt_ward_identity_derivation.py) |
| CKM atlas/axiom package on the canonical tensor/projector surface, including the standalone CP-phase identity `cos^2(delta_CKM)=1/6` | promoted quantitative | quantitative section / theorem box | [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](../../CKM_ATLAS_AXIOM_CLOSURE_NOTE.md), [CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md](../../CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) | [frontier_ckm_atlas_axiom_closure.py](../../../scripts/frontier_ckm_atlas_axiom_closure.py), [frontier_ckm_cp_phase_structural_identity.py](../../../scripts/frontier_ckm_cp_phase_structural_identity.py), [frontier_ckm_no_import_audit.py](../../../scripts/frontier_ckm_no_import_audit.py) |
| Dark-matter exact-target PMNS package on the manuscript surface | flagship closed package | dedicated manuscript package section | [DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md](../../DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md), [DM_ABCC_RETAINED_MEASUREMENT_CLOSURE_THEOREM_NOTE_2026-04-21.md](../../DM_ABCC_RETAINED_MEASUREMENT_CLOSURE_THEOREM_NOTE_2026-04-21.md), [DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md](../../DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md) | [frontier_dm_leptogenesis_transport_status.py](../../../scripts/frontier_dm_leptogenesis_transport_status.py), [frontier_dm_abcc_retained_measurement_closure_2026_04_21.py](../../../scripts/frontier_dm_abcc_retained_measurement_closure_2026_04_21.py), [frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py](../../../scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py) |

## Open Flagship Lane

| Lane | Status | Current boundary | Main authority | Primary runner |
|---|---|---|---|---|
| Charged-lepton Koide (`Q = 2/3`, `delta = 2/9`) | open flagship lane | strong support package, but the physical/source-law bridge behind `Q` and the physical Brannen-phase bridge behind `delta` remain open; pointed-origin exhaustion now proves origin-free retained data cannot select the closing representative; the separate overall lepton scale `v_0` also remains open | [KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md](../../KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md), [CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md](../../CHARGED_LEPTON_KOIDE_REVIEW_PACKET_2026-04-18.md), [KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md](../../KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM_NOTE_2026-04-24.md) | [frontier_koide_lane_regression.py](../../../scripts/frontier_koide_lane_regression.py), [frontier_koide_reviewer_stress_test.py](../../../scripts/frontier_koide_reviewer_stress_test.py), [frontier_koide_pointed_origin_exhaustion_theorem.py](../../../scripts/frontier_koide_pointed_origin_exhaustion_theorem.py) |

## Bounded Companion Surface

These rows are in the public package, but they are not manuscript-core claims.

| Lane | Status | Authority |
|---|---|---|
| Higgs / vacuum package | bounded companion | [HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md](../../HIGGS_VACUUM_EXPLICIT_SYSTEMATIC_NOTE.md), [HIGGS_MASS_DERIVED_NOTE.md](../../HIGGS_MASS_DERIVED_NOTE.md) |
| Quark mass-ratio support stack | bounded companion | [QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md](../../QUARK_MASS_RATIO_REVIEW_PACKET_2026-04-18.md) |
| Curated neutrino retained boundary/support packet | bounded companion | [NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md](../../NEUTRINO_RETAINED_STATUS_NOTE_2026-04-16.md), [NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md](../../NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md) |
| Cosmology structural identities and bounded numerics | bounded companion | [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](../../COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md), [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) |
| Proton lifetime, neutron EDM continuation, monopole mass, gravitational decoherence, BH entropy companion, GW echo null result | bounded companion | [PREDICTION_SURFACE_2026-04-15.md](./PREDICTION_SURFACE_2026-04-15.md), [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) |

## Rule

No manuscript-facing claim is ready unless it is present in both:

- this file
- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
