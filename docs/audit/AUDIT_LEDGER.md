# Audit Ledger

**Generated:** 2026-04-26T22:47:30.238124+00:00  
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
| _proposed_retained_ | 318 |
| _proposed_promoted_ | 8 |
| bounded | 183 |
| support | 96 |
| open | 11 |
| unknown | 985 |

| audit_status | count |
|---|---:|
| `unaudited` | 1601 |

| criticality | count |
|---|---:|
| `critical` | 91 |
| `high` | 569 |
| `medium` | 85 |
| `leaf` | 856 |

- **Proposed claims demoted by upstream:** 125
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
| 1 | `ckm_cp_phase_structural_identity_theorem_note_2026-04-24` | critical | 170 | 33.92 | `unaudited` | unknown |
| 2 | `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24` | critical | 170 | 33.42 | `unaudited` | unknown |
| 3 | `alpha_s_derived_note` | critical | 275 | 32.61 | `unaudited` | unknown |
| 4 | `observable_principle_from_axiom_note` | critical | 276 | 28.61 | `unaudited` | unknown |
| 5 | `ckm_magnitudes_structural_counts_theorem_note_2026-04-25` | critical | 170 | 28.42 | `unaudited` | unknown |
| 6 | `ckm_atlas_axiom_closure_note` | critical | 170 | 25.92 | `unaudited` | unknown |
| 7 | `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24` | critical | 170 | 25.42 | `unaudited` | _proposed_promoted_ |
| 8 | `three_generation_structure_note` | critical | 273 | 25.10 | `unaudited` | unknown |
| 9 | `one_generation_matter_closure_note` | critical | 273 | 24.60 | `unaudited` | unknown |
| 10 | `three_generation_observable_theorem_note` | critical | 273 | 24.60 | `unaudited` | unknown |
| 11 | `ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25` | critical | 170 | 24.42 | `unaudited` | unknown |
| 12 | `graph_first_su3_integration_note` | critical | 275 | 23.11 | `unaudited` | _proposed_retained_ |
| 13 | `yt_ward_identity_derivation_theorem` | critical | 273 | 23.10 | `unaudited` | unknown |
| 14 | `yt_ew_color_projection_theorem` | critical | 276 | 22.61 | `unaudited` | _proposed_retained_ |
| 15 | `anomaly_forces_time_theorem` | critical | 273 | 22.60 | `unaudited` | unknown |
| 16 | `ckm_third_row_magnitudes_theorem_note_2026-04-24` | critical | 170 | 21.92 | `unaudited` | unknown |
| 17 | `minimal_axioms_2026-04-11` | critical | 273 | 21.60 | `unaudited` | unknown |
| 18 | `left_handed_charge_matching_note` | critical | 273 | 21.10 | `unaudited` | unknown |
| 19 | `standard_model_hypercharge_uniqueness_theorem_note_2026-04-24` | critical | 273 | 20.60 | `unaudited` | unknown |
| 20 | `higgs_mass_derived_note` | critical | 276 | 20.11 | `unaudited` | unknown |
| 21 | `physical_lattice_necessity_note` | critical | 273 | 20.10 | `unaudited` | unknown |
| 22 | `ckm_bs_mixing_phase_derivation_theorem_note_2026-04-25` | critical | 170 | 19.92 | `unaudited` | unknown |
| 23 | `ckm_first_row_magnitudes_theorem_note_2026-04-24` | critical | 170 | 19.92 | `unaudited` | unknown |
| 24 | `native_gauge_closure_note` | critical | 274 | 19.60 | `unaudited` | _proposed_retained_ |
| 25 | `ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25` | critical | 170 | 19.42 | `unaudited` | unknown |


## Applied audits

_No audits applied yet._


## Audit findings (full)

