# Derivation / Validation Map

This file is the evidence contract for the publication package.

Every paper-facing claim must have:

1. one derivation authority note that defines the safe theorem boundary
2. one validation path, usually one or more runners with expected pass output
3. one manuscript placement decision
4. one release artifact path for logs, tables, or figure inputs

If a claim does not have both a derivation path and a validation path here, it
is not ready for the manuscript.

## Retained backbone

| Claim | Manuscript placement | Derivation authority | Validation path | Release artifact |
|---|---|---|---|---|
| `Cl(3)` on `Z^3` is the physical theory | main text framework sentence | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | framework-level audit only; no numeric runner required | framework statement pinned in release README |
| Weak-field gravity through the Poisson / Newton chain | main text | [CI3_Z3_PUBLICATION_STATE_2026-04-12.md](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md), [SELF_CONSISTENCY_FORCES_POISSON_NOTE.md](../../SELF_CONSISTENCY_FORCES_POISSON_NOTE.md), [POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md](../../POISSON_EXHAUSTIVE_UNIQUENESS_NOTE.md), [NEWTON_LAW_DERIVED_NOTE.md](../../NEWTON_LAW_DERIVED_NOTE.md) | [frontier_self_consistent_field_equation.py](../../../scripts/frontier_self_consistent_field_equation.py), [frontier_poisson_exhaustive_uniqueness.py](../../../scripts/frontier_poisson_exhaustive_uniqueness.py), [frontier_newton_derived.py](../../../scripts/frontier_newton_derived.py) | `logs/retained/gravity_*` plus figure inputs for the gravity chain |
| Weak-field WEP from the derived lattice action | main text or Extended Data corollary | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) | `logs/retained/gravity_wep_*` |
| Weak-field gravitational time dilation on the retained Poisson/Newton surface | main text or Extended Data corollary | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) | `logs/retained/gravity_time_dilation_*` |
| Exact native `SU(2)` from cubic `Cl(3)` | main text | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) | [frontier_non_abelian_gauge.py](../../../scripts/frontier_non_abelian_gauge.py) | `logs/retained/su2_*` |
| Graph-first structural `SU(3)` | main text | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) | `logs/retained/su3_*` |
| Left-handed `+1/3` / `-1` charge matching | main text or SI corollary | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) | `logs/retained/charge_matching_*` |
| Anomaly-forced `3+1` closure | main text | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) | `logs/retained/time_*` |
| Retained `S^3` compactification / topology closure | main text or SI theorem box | [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_GENERAL_R_DERIVATION_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_GENERAL_R_DERIVATION_NOTE.md), [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_CAP_UNIQUENESS_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_CAP_UNIQUENESS_NOTE.md) | [frontier_s3_boundary_link_theorem.py](../../../scripts/frontier_s3_boundary_link_theorem.py), [frontier_s3_cap_uniqueness.py](../../../scripts/frontier_s3_cap_uniqueness.py), [frontier_s3_general_r.py](../../../scripts/frontier_s3_general_r.py) | `logs/retained/s3_*` |
| Full-framework one-generation matter closure | main text | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_right_handed_sector.py](../../../scripts/frontier_right_handed_sector.py) | `logs/retained/one_generation_*` |
| Three-generation matter structure | main text | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_generation_fermi_point.py](../../../scripts/frontier_generation_fermi_point.py), [frontier_generation_rooting_undefined.py](../../../scripts/frontier_generation_rooting_undefined.py), [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) | `logs/retained/generation_*` |
| Exact `I_3 = 0` / no third-order interference | main text support or Extended Data | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) | [frontier_born_rule_derived.py](../../../scripts/frontier_born_rule_derived.py) | `logs/retained/i3_zero_*` |
| Exact CPT on the free staggered lattice | main text support or Extended Data | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) | [frontier_cpt_exact.py](../../../scripts/frontier_cpt_exact.py) | `logs/retained/cpt_*` |
| Single-axiom Hilbert/locality reduction | SI framing only | [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md), [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md) | [frontier_single_axiom_hilbert.py](../../../scripts/frontier_single_axiom_hilbert.py), [frontier_single_axiom_information.py](../../../scripts/frontier_single_axiom_information.py) | `logs/si/single_axiom_*` |

## Live gates and strongest current evidence

These lanes are not promoted, but they still need the same structure.

| Gate | Strongest current derivation note | Strongest current validation path | Current status | Promotion blocker |
|---|---|---|---|---|
| DM relic mapping | bounded `DM_*` authority on `review-active`; Stosszahlansatz and graph-native notes are strongest sub-results | `frontier_dm_stosszahlansatz.py`, `frontier_dm_k_independence.py`, `frontier_dm_graph_native.py` | bounded/open | graph-to-relic bridge, normalization, and cancellation steps still outrun the paper bar |
| Renormalized `y_t` matching | bounded `YT_*` authority on `review-active`; `Cl(3)` RG preservation is exact | `frontier_yt_cl3_preservation.py`, `frontier_yt_matching_coefficient.py`, `frontier_yt_full_closure.py` | bounded/open | continuum running, Planck-scale coupling chain, and matching are still bounded |
| CKM / quantitative flavor closure | bounded `CKM_*` authority on `review-active` | current `CKM_*` runners on `review-active` and `youthful-neumann` | bounded/open | Higgs `Z_3` universality and ab initio coefficient closure still open |

## Release rule

Before submission freeze:

- archive one stdout log per retained runner under `logs/retained/`
- archive one short pass-summary table keyed by the claim names above
- store figure-prep data under `outputs/figures/`
- pin the release commit in the root README and the manuscript code/data sections

If a claim needs caveats to stay safe, those caveats belong in the derivation
authority note, not only in the manuscript prose.
