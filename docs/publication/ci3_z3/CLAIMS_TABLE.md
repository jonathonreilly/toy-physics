# Claims Table

Use [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) alongside
this table. This file says what the paper may claim. The derivation /
validation map says how each claim is evidenced and released.

## Retained core

| Claim | Status | Placement | Authority | Primary runner |
|---|---|---|---|---|
| `Cl(3)` on `Z^3` is the working physical theory | retained framework statement | main text | [Publication state](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | n/a |
| weak-field gravity from the Poisson / Newton chain on `Z^3` | retained | main text | [Publication state](../../CI3_Z3_PUBLICATION_STATE_2026-04-12.md) | [frontier_self_consistent_field_equation.py](../../../scripts/frontier_self_consistent_field_equation.py), [frontier_poisson_exhaustive_uniqueness.py](../../../scripts/frontier_poisson_exhaustive_uniqueness.py), [frontier_newton_derived.py](../../../scripts/frontier_newton_derived.py) |
| weak-field WEP from the derived lattice action | retained corollary | main text or Extended Data corollary | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) |
| weak-field gravitational time dilation on the retained Poisson/Newton surface | retained corollary | main text or Extended Data corollary | [BROAD_GRAVITY_DERIVATION_NOTE.md](../../BROAD_GRAVITY_DERIVATION_NOTE.md), [GRAVITY_CLEAN_DERIVATION_NOTE.md](../../GRAVITY_CLEAN_DERIVATION_NOTE.md) | [frontier_broad_gravity.py](../../../scripts/frontier_broad_gravity.py) |
| exact native `SU(2)` from cubic `Cl(3)` | retained | main text | [BOUNDED_NATIVE_GAUGE_NOTE.md](../../BOUNDED_NATIVE_GAUGE_NOTE.md) | [frontier_non_abelian_gauge.py](../../../scripts/frontier_non_abelian_gauge.py) |
| graph-first structural `SU(3)` closure | retained | main text | [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](../../GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| left-handed `+1/3` / `-1` charge matching on the selected-axis surface | retained corollary | main text or SI corollary | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_graph_first_su3_integration.py](../../../scripts/frontier_graph_first_su3_integration.py) |
| anomaly-forced `3+1` closure | retained | main text | [ANOMALY_FORCES_TIME_THEOREM.md](../../ANOMALY_FORCES_TIME_THEOREM.md) | [frontier_anomaly_forces_time.py](../../../scripts/frontier_anomaly_forces_time.py) |
| retained `S^3` compactification / topology closure | retained | main text or SI theorem box | [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_GENERAL_R_DERIVATION_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_GENERAL_R_DERIVATION_NOTE.md), [/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_CAP_UNIQUENESS_NOTE.md](/Users/jonreilly/Projects/Physics/.claude/worktrees/youthful-neumann/docs/S3_CAP_UNIQUENESS_NOTE.md) | [frontier_s3_boundary_link_theorem.py](../../../scripts/frontier_s3_boundary_link_theorem.py), [frontier_s3_cap_uniqueness.py](../../../scripts/frontier_s3_cap_uniqueness.py), [frontier_s3_general_r.py](../../../scripts/frontier_s3_general_r.py) |
| full-framework one-generation matter closure | retained | main text | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_right_handed_sector.py](../../../scripts/frontier_right_handed_sector.py) |
| three-generation matter structure in the framework | retained | main text | [GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md](../../GAUGE_MATTER_CLOSURE_GATES_2026-04-12.md) | [frontier_generation_fermi_point.py](../../../scripts/frontier_generation_fermi_point.py), [frontier_generation_rooting_undefined.py](../../../scripts/frontier_generation_rooting_undefined.py), [frontier_generation_axiom_boundary.py](../../../scripts/frontier_generation_axiom_boundary.py) |
| exact `I_3 = 0` / no third-order interference on the Hilbert surface | retained exact companion | main text or Extended Data | [I3_ZERO_EXACT_THEOREM_NOTE.md](../../I3_ZERO_EXACT_THEOREM_NOTE.md) | [frontier_born_rule_derived.py](../../../scripts/frontier_born_rule_derived.py) |
| exact CPT on the free staggered lattice | retained exact companion | main text or Extended Data | [CPT_EXACT_NOTE.md](../../CPT_EXACT_NOTE.md) | [frontier_cpt_exact.py](../../../scripts/frontier_cpt_exact.py) |
| single-axiom Hilbert/locality reduction | SI framing only | SI / framing box | [SINGLE_AXIOM_HILBERT_NOTE.md](../../SINGLE_AXIOM_HILBERT_NOTE.md), [SINGLE_AXIOM_INFORMATION_NOTE.md](../../SINGLE_AXIOM_INFORMATION_NOTE.md) | [frontier_single_axiom_hilbert.py](../../../scripts/frontier_single_axiom_hilbert.py), [frontier_single_axiom_information.py](../../../scripts/frontier_single_axiom_information.py) |

## Bounded companions

These lanes are intentionally kept out of the retained publication surface. They
remain authority-tracked on `review-active` until they are either promoted
cleanly or closed.

| Claim | Status | Placement | Authority |
|---|---|---|---|
| weak-field GR-signature companions beyond Newton/Poisson/WEP/time-dilation | bounded | arXiv / SI only | `review-active` bounded gravity notes |
| direct lattice DM contact enhancement and bounded relic chain | bounded | arXiv / SI only | `review-active` bounded DM notes |
| renormalized `y_t` bridge | bounded | arXiv / SI only | `review-active` bounded `y_t` notes |
| CKM / Higgs `Z_3` route | bounded | arXiv / SI only | `review-active` bounded CKM notes |
| cosmology windows (`w=-1`, graviton mass, `Omega_Lambda`, `n_s`) | bounded / conditional | arXiv companion only | `review-active` bounded cosmology notes |
| Higgs / Coleman-Weinberg mass lane | bounded | arXiv companion only | `claude/youthful-neumann` Higgs derivation note + runner |
| proton lifetime | bounded sharp prediction | arXiv companion only | `claude/youthful-neumann` proton lifetime note + runner |
| Lorentz-violation cubic fingerprint | bounded sharp prediction | arXiv companion only | `claude/youthful-neumann` Lorentz-violation note + runner |
| BH entropy / RT ratio | bounded companion | arXiv companion only | `claude/youthful-neumann` BH entropy note + runner |
| gravitational decoherence | bounded companion | arXiv companion only | `claude/youthful-neumann` grav-decoherence note + runner |
| magnetic monopole mass | bounded companion | arXiv companion only | `claude/youthful-neumann` monopole note + runner |
| GW echo timing | bounded / off-scope companion | later companion paper only | `claude/youthful-neumann` GW echo note + runner |

## Open paper gates

1. DM relic mapping
2. renormalized `y_t` matching
3. CKM / quantitative flavor closure

## Packaging rule

No manuscript claim is ready until it appears in both:

- this table
- [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md)
