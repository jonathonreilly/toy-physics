# Canonical Harness Index

**Date:** 2026-04-15
**Purpose:** current rerun map for the actual `main` package

This file replaces the retired toy / staggered harness index as the default
runner map for the current publication-facing framework.

Start with:

- [CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md](CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md)
- [publication/ci3_z3/PUBLICATION_MATRIX.md](publication/ci3_z3/PUBLICATION_MATRIX.md)
- [publication/ci3_z3/DERIVATION_VALIDATION_MAP.md](publication/ci3_z3/DERIVATION_VALIDATION_MAP.md)

## Retained Core Runners

| Package row | Primary note | Primary runner(s) |
|---|---|---|
| weak-field gravity | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | `frontier_self_consistent_field_equation.py`, `frontier_poisson_exhaustive_uniqueness.py`, `frontier_newton_derived.py` |
| weak-field WEP / time dilation | [BROAD_GRAVITY_DERIVATION_NOTE.md](BROAD_GRAVITY_DERIVATION_NOTE.md) | `frontier_broad_gravity.py` |
| restricted strong-field closure | [RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md](RESTRICTED_STRONG_FIELD_CLOSURE_NOTE.md) | `frontier_oh_static_constraint_lift.py`, `frontier_oh_schur_boundary_action.py`, `frontier_star_supported_bridge_class.py` |
| full discrete `3+1` GR on the project route | [UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md) | `frontier_universal_gr_discrete_global_closure.py`, `frontier_universal_gr_lorentzian_global_atlas_closure.py`, `frontier_universal_gr_lorentzian_signature_extension.py` |
| exact native `SU(2)` | [BOUNDED_NATIVE_GAUGE_NOTE.md](BOUNDED_NATIVE_GAUGE_NOTE.md) | `frontier_non_abelian_gauge.py` |
| graph-first structural `SU(3)` | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | `frontier_graph_first_su3_integration.py` |
| anomaly-forced `3+1` | [ANOMALY_FORCES_TIME_THEOREM.md](ANOMALY_FORCES_TIME_THEOREM.md) | `frontier_anomaly_forces_time.py` |
| electroweak hierarchy / `v` | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | `frontier_hierarchy_observable_principle_from_axiom.py` |
| one-generation matter closure | [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](ONE_GENERATION_MATTER_CLOSURE_NOTE.md) | `frontier_right_handed_sector.py`, `frontier_anomaly_forces_time.py` |
| three-generation matter structure | [THREE_GENERATION_STRUCTURE_NOTE.md](THREE_GENERATION_STRUCTURE_NOTE.md) | `frontier_generation_fermi_point.py`, `frontier_generation_rooting_undefined.py`, `frontier_generation_axiom_boundary.py` |
| exact `I_3 = 0` | [I3_ZERO_EXACT_THEOREM_NOTE.md](I3_ZERO_EXACT_THEOREM_NOTE.md) | `frontier_born_rule_derived.py` |
| exact CPT | [CPT_EXACT_NOTE.md](CPT_EXACT_NOTE.md) | `frontier_cpt_exact.py` |

## Current Bounded EW / `y_t` / Higgs Package

| Package row | Primary note | Primary runner(s) |
|---|---|---|
| retained hierarchy / `v` support for the low-energy package | [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md) | `frontier_hierarchy_observable_principle_from_axiom.py` |
| zero-input `y_t` authority | [YT_ZERO_IMPORT_CLOSURE_NOTE.md](YT_ZERO_IMPORT_CLOSURE_NOTE.md) | `frontier_yt_2loop_chain.py` |
| boundary endpoint theorem | [YT_BOUNDARY_THEOREM.md](YT_BOUNDARY_THEOREM.md) | `frontier_yt_boundary_consistency.py` |
| EFT bridge theorem | [YT_EFT_BRIDGE_THEOREM.md](YT_EFT_BRIDGE_THEOREM.md) | `frontier_yt_eft_bridge.py` |
| zero-input `alpha_s(M_Z)` support | [ALPHA_S_DERIVED_NOTE.md](ALPHA_S_DERIVED_NOTE.md) | `frontier_alpha_s_determination.py`, `frontier_yt_2loop_chain.py` |
| vertex-power support theorem | [YT_VERTEX_POWER_DERIVATION.md](YT_VERTEX_POWER_DERIVATION.md) | `frontier_vertex_power.py` |
| import-allowed top-mass companion | [YT_GAUGE_CROSSOVER_THEOREM.md](YT_GAUGE_CROSSOVER_THEOREM.md) | `frontier_yt_gauge_crossover_theorem.py` |
| Higgs bounded authority stack | [HIGGS_MASS_DERIVED_NOTE.md](HIGGS_MASS_DERIVED_NOTE.md), [HIGGS_MECHANISM_NOTE.md](HIGGS_MECHANISM_NOTE.md), [HIGGS_FROM_LATTICE_NOTE.md](HIGGS_FROM_LATTICE_NOTE.md) | `frontier_higgs_mass_derived.py` |

## Other Bounded Companion Packages

| Package row | Primary note | Primary runner(s) |
|---|---|---|
| DM ratio / relic companions | [DM_RELIC_PAPER_NOTE.md](DM_RELIC_PAPER_NOTE.md) | `frontier_dm_relic_paper.py` |
| CKM magnitude package | [CKM_MASS_BASIS_NNI_NOTE.md](CKM_MASS_BASIS_NNI_NOTE.md) | `frontier_ckm_mass_basis_nni.py`, `frontier_ckm_from_z3.py` |
| Jarlskog companion | [JARLSKOG_PHASE_BOUND_NOTE.md](JARLSKOG_PHASE_BOUND_NOTE.md) | `frontier_jarlskog_derived.py` |
| cosmology companions | [OMEGA_LAMBDA_DERIVATION_NOTE.md](OMEGA_LAMBDA_DERIVATION_NOTE.md) | `frontier_omega_lambda_derivation.py`, `frontier_primordial_spectrum.py`, `frontier_dark_energy_eos.py`, `frontier_cosmological_constant.py` |

## Historical Rule

Older route-history or pre-package harnesses may still be useful for archaeology
or debugging, but they are not the default current rerun map. The publication
package wins over older harness inventories.
