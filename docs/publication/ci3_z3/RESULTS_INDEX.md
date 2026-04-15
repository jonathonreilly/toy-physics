# Results Index

This maps manuscript sections to the primary note+runner artifacts on this
branch.

For the claim-by-claim derivation/validation pairing, use
[DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md).

For the repo-wide capture across remote branches and branch-local workstreams,
use [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) and
[REMOTE_BRANCH_AUDIT_2026-04-14.md](./REMOTE_BRANCH_AUDIT_2026-04-14.md).

For the reviewer-facing prediction/observation rows, use
[QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md).

## Main-text core

| Section | Note | Runner |
|---|---|---|
| Framework / claim surface | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | n/a |
| Weak-field gravity (`Poisson` / Newton chain) | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | [frontier_self_consistent_field_equation.py](../../../scripts/frontier_self_consistent_field_equation.py), [frontier_poisson_exhaustive_uniqueness.py](../../../scripts/frontier_poisson_exhaustive_uniqueness.py), [frontier_newton_derived.py](../../../scripts/frontier_newton_derived.py) |
| Weak-field gravity corollaries (WEP / time dilation) | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) |
| Restricted strong-field gravity closure on the star-supported finite-rank class | [RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](../../RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md), [OH_STATIC_CONSTRAINT_LIFT_NOTE.md](../../OH_STATIC_CONSTRAINT_LIFT_NOTE.md), [OH_SCHUR_BOUNDARY_ACTION_NOTE.md](../../OH_SCHUR_BOUNDARY_ACTION_NOTE.md), [STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md](../../STAR_SUPPORTED_BRIDGE_CLASS_NOTE.md) | [frontier_oh_static_constraint_lift.py](../../../scripts/frontier_oh_static_constraint_lift.py), [frontier_oh_schur_boundary_action.py](../../../scripts/frontier_oh_schur_boundary_action.py), [frontier_star_supported_bridge_class.py](../../../scripts/frontier_star_supported_bridge_class.py) |
| Universal GR discrete global closure on `PL S^3 x R` | [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](../../UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md), [UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md](../../UNIVERSAL_GR_LORENTZIAN_SIGNATURE_EXTENSION_NOTE.md) | [frontier_universal_gr_discrete_global_closure.py](../../../scripts/frontier_universal_gr_discrete_global_closure.py), [frontier_universal_gr_lorentzian_global_atlas_closure.py](../../../scripts/frontier_universal_gr_lorentzian_global_atlas_closure.py), [frontier_universal_gr_lorentzian_signature_extension.py](../../../scripts/frontier_universal_gr_lorentzian_signature_extension.py) |
| UV-finite partition-density bridge to discrete GR | [UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md](../../UNIVERSAL_QG_UV_FINITE_PARTITION_NOTE.md) | [frontier_universal_qg_uv_finite_partition.py](../../../scripts/frontier_universal_qg_uv_finite_partition.py) |
| Canonical geometric refinement net for the discrete QG bridge | [UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md](../../UNIVERSAL_QG_CANONICAL_REFINEMENT_NET_NOTE.md) | [frontier_universal_qg_canonical_refinement_net.py](../../../scripts/frontier_universal_qg_canonical_refinement_net.py) |
| Inverse-limit Gaussian cylinder closure for the discrete QG bridge | [UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md](../../UNIVERSAL_QG_INVERSE_LIMIT_CLOSURE_NOTE.md) | [frontier_universal_qg_inverse_limit_closure.py](../../../scripts/frontier_universal_qg_inverse_limit_closure.py) |
| Abstract Gaussian / Cameron-Martin completion for the discrete QG bridge | [UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md](../../UNIVERSAL_QG_ABSTRACT_GAUSSIAN_COMPLETION_NOTE.md) | [frontier_universal_qg_abstract_gaussian_completion.py](../../../scripts/frontier_universal_qg_abstract_gaussian_completion.py) |
| Project-native PL field realization for the discrete QG bridge | [UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_FIELD_INTERFACE_NOTE.md) | [frontier_universal_qg_pl_field_interface.py](../../../scripts/frontier_universal_qg_pl_field_interface.py) |
| Project-native PL weak/Dirichlet-form closure for the discrete QG bridge | [UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md](../../UNIVERSAL_QG_PL_WEAK_FORM_NOTE.md) | [frontier_universal_qg_pl_weak_form.py](../../../scripts/frontier_universal_qg_pl_weak_form.py) |
| Project-native PL `H^1`-type Sobolev interface for the discrete QG bridge | [UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md](../../UNIVERSAL_QG_PL_SOBOLEV_INTERFACE_NOTE.md) | [frontier_universal_qg_pl_sobolev_interface.py](../../../scripts/frontier_universal_qg_pl_sobolev_interface.py) |
| Native gauge algebra | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) | [frontier_non_abelian_gauge.py](../../../scripts/frontier_non_abelian_gauge.py) |
| Graph-first structural `SU(3)` | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| Left-handed charge matching on selected-axis surface | [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](../../LEFT_HANDED_CHARGE_MATCHING_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| Time / `3+1` closure | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) |
| Electroweak hierarchy / `v` scale | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](../../OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | [frontier_hierarchy_observable_principle_from_axiom.py](../../../scripts/frontier_hierarchy_observable_principle_from_axiom.py) |
| `S^3` compactification / topology closure | [S3_GENERAL_R_DERIVATION_NOTE.md](../../S3_GENERAL_R_DERIVATION_NOTE.md), [S3_CAP_UNIQUENESS_NOTE.md](../../S3_CAP_UNIQUENESS_NOTE.md) | [frontier_s3_boundary_link_theorem.py](../../../scripts/frontier_s3_boundary_link_theorem.py), [frontier_s3_cap_uniqueness.py](../../../scripts/frontier_s3_cap_uniqueness.py), [frontier_s3_general_r.py](../../../scripts/frontier_s3_general_r.py) |
| One-generation matter closure | [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](../../ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | [frontier_right_handed_sector.py](../../../scripts/frontier_right_handed_sector.py), [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) |
| Three-generation matter structure | [THREE_GENERATION_STRUCTURE_NOTE.md](../../THREE_GENERATION_STRUCTURE_NOTE.md) | [frontier_generation_fermi_point.py](../../../scripts/frontier_generation_fermi_point.py), [frontier_generation_rooting_undefined.py](../../../scripts/frontier_generation_rooting_undefined.py), [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) |
| Exact `I_3 = 0` | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) | [frontier_born_rule_derived.py](../../../scripts/frontier_born_rule_derived.py) (historical filename) |
| Exact CPT | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) | [frontier_cpt_exact.py](../../../scripts/frontier_cpt_exact.py) (even periodic lattices only) |

## Main text vs SI split

- Nature main text:
  - framework statement
  - weak-field gravity through the Poisson / Newton chain
  - weak-field WEP and time dilation as compact corollaries on that same
    gravity surface
  - restricted strong-field gravity closure on the current star-supported
    finite-rank class as an Extended Data / SI theorem, not the flagship
    gravity headline
  - direct-universal discrete global closure on `PL S^3 x R` as the
    capstone discrete `3+1` gravity theorem
  - UV-finite partition-density bridge whose mean/stationary sector is that
    same discrete `3+1` gravity family
  - canonical geometric barycentric-dyadic refinement net for that same
    discrete partition-density and stationary-section family
  - inverse-limit Gaussian cylinder closure for that same canonical discrete
    QG family
  - exact native `SU(2)`
  - graph-first structural `SU(3)`
  - selected-axis left-handed charge matching as a corollary
  - `3+1` closure
  - electroweak hierarchy / `v` scale
  - retained `S^3` compactification / topology closure
  - full-framework one-generation closure
  - three-generation matter structure
  - exact `I_3 = 0` and CPT as compact supporting theorems
- SI / arXiv:
  - bounded weak-field GR companions beyond Newton / Poisson / WEP / time-dilation
  - continuum / unrestricted GR beyond the project's discrete route
  - derivation chains
  - bounded phenomenology
  - three live-gate notes and negative results

## Figure sources

- Use [FIGURE_PLAN.md](./FIGURE_PLAN.md) as the canonical figure inventory.
- No manuscript figure should be sourced from a note or runner that is not also
  represented in [CLAIMS_TABLE.md](./CLAIMS_TABLE.md).
- No manuscript section should rely on a claim that is missing from
  [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md).

## Bounded and frozen-out surfaces

- The observation-facing quantitative portfolio is catalogued in
  [PUBLICATION_MATRIX.md](./PUBLICATION_MATRIX.md) and summarized in
  [QUANTITATIVE_SUMMARY_TABLE.md](./QUANTITATIVE_SUMMARY_TABLE.md).
- Important excluded workstreams are catalogued in
  [FROZEN_OUT_REGISTRY.md](./FROZEN_OUT_REGISTRY.md).
