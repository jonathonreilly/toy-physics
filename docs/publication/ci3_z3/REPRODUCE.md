# Reproduce Guide

Run these from the repo root on the current `main`.

This file is the quickest route to validating the active package. For claim
boundaries, pair it with [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md).
For domain routing, pair it with [SCIENCE_MAP.md](./SCIENCE_MAP.md).

## Fastest Validation Paths

Choose the slice that matches what you are trying to check.

### Retained backbone

```bash
python3 scripts/frontier_self_consistent_field_equation.py
python3 scripts/frontier_poisson_exhaustive_uniqueness.py
python3 scripts/frontier_newton_derived.py
python3 scripts/frontier_universal_gr_discrete_global_closure.py
python3 scripts/frontier_universal_qg_canonical_textbook_continuum_gr_closure.py
python3 scripts/frontier_non_abelian_gauge.py
python3 scripts/frontier_graph_first_su3_integration.py
python3 scripts/frontier_anomaly_forces_time.py
python3 scripts/frontier_three_generation_observable_theorem.py
python3 scripts/frontier_strong_cp_theta_zero.py
```

### Quantitative package

```bash
python3 scripts/frontier_hierarchy_observable_principle_from_axiom.py
python3 scripts/frontier_complete_prediction_chain.py
python3 scripts/frontier_yt_ward_identity_derivation.py
python3 scripts/frontier_yt_p1_bz_quadrature_full_staggered_pt.py
python3 scripts/frontier_higgs_mass_full_3loop.py
python3 scripts/frontier_ckm_atlas_axiom_closure.py
```

### Flagship/open and package-support lanes

```bash
python3 scripts/frontier_dm_leptogenesis_transport_status.py
python3 scripts/frontier_dm_abcc_retained_measurement_closure_2026_04_21.py
python3 scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py
python3 scripts/frontier_koide_reviewer_stress_test.py
python3 scripts/frontier_koide_lane_regression.py
python3 scripts/frontier_planck_scale_program_audit.py
```

## How To Read The Output

- use the note paired with each runner as the claim boundary
- use [DERIVATION_VALIDATION_MAP.md](./DERIVATION_VALIDATION_MAP.md) to see
  which derivation note and release artifact each runner supports
- use [RESULTS_INDEX.md](./RESULTS_INDEX.md) when you want the canonical
  note/runner path for a specific lane
- do not elevate bounded or support lanes from raw stdout alone

Historical runner-name caveats:

- `frontier_born_rule_derived.py` supports the retained `I_3 = 0` theorem, not
  a standalone full Born-rule derivation
- `frontier_cpt_exact.py` is an exact theorem runner on even periodic lattices
  only
- `frontier_newton_derived.py` supports the retained weak-field Newton/Poisson
  claim, not the full gravity/QG chain
- `frontier_anomaly_forces_time.py` mixes computed checks with labeled
  assertions; use the theorem note as the safe claim boundary

## Logs and Release Artifacts

- archive raw stdout logs per runner under `logs/` or `outputs/`
- archive retained logs under `logs/retained/`
- store figure-prep data under `outputs/figures/`
- keep the release status ledger aligned with the package labels:
  `retained`, `bounded`, or `open`

Before release:

- pin the exact commit hash
- confirm that the manuscript, claims table, inputs/qualifiers note, and
  non-claims note agree on the released package boundary

## Archival Freeze

The existing freeze note is an archival selective freeze, not the current
package authority surface:

- [REPRODUCIBILITY_FREEZE_2026-04-14.md](./REPRODUCIBILITY_FREEZE_2026-04-14.md)

Use it for provenance only.
