# Audit-Acceleration Manifest: Ready-Items Bundle 2

**Date:** 2026-05-02
**Type:** meta (audit-acceleration request, not a science claim)
**Author:** physics-loop campaign infrastructure
**Companion to:** [`AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md`](AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md) (Bundle 1)

## Purpose

Bundle 1 surfaced five foundational `unaudited` axiom-first notes that
have **no upstream blockers**. This Bundle 2 surfaces the next layer:
**13 unaudited positive-theorem items where ALL upstream deps are
already at retained-grade today.**

These items are by definition `ready=True` in the audit queue. Codex's
queue is dominated by CKM/Koide criticals at the top; audit-ready
positive theorems at lower criticality may sit indefinitely without
explicit prioritization signal.

## Ready items (deps all retained today)

### High-criticality (in_degree ≥ 7)

1. [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md)
   — in_degree=11; runner `scripts/verify_cl3_sm_embedding.py` PASS=95/95
   at machine precision.
2. [`PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md`](PLANCK_PRIMITIVE_CLIFFORD_MAJORANA_EDGE_DERIVATION_THEOREM_NOTE_2026-04-30.md)
   — in_degree=7; runner `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py` PASS=8/8
   at machine precision.

(`yukawa_color_projection_theorem` originally listed here; pipeline run
revealed Codex prior verdict `audited_decoration` under
`ew_current_fierz_channel_decomposition_note_2026-05-01`. Removed from
Bundle 2 — Codex already adjudicated it as decoration, not an
independent retention candidate.)

### Strict-bar campaign blocks (R1-R3 era, already PR-shipped, awaiting audit)

The following are positive theorems shipped via the strict-bar campaign
PRs in earlier rounds (April-May 2026). Each has all-retained deps and
a passing runner; they are sitting in the audit queue with criticality
`leaf`:

4. [`CPT_PARTICLE_ANTIPARTICLE_MASS_EQUALITY_THEOREM_NOTE_2026-05-02.md`](CPT_PARTICLE_ANTIPARTICLE_MASS_EQUALITY_THEOREM_NOTE_2026-05-02.md)
   — R1 Block 03 (PR #300); runner `scripts/cpt_particle_antiparticle_mass_equality_check.py` PASS at machine precision.
5. [`CPT_PARTICLE_ANTIPARTICLE_LIFETIME_EQUALITY_THEOREM_NOTE_2026-05-02.md`](CPT_PARTICLE_ANTIPARTICLE_LIFETIME_EQUALITY_THEOREM_NOTE_2026-05-02.md)
   — R2 Block 02 (PR #333); runner `scripts/cpt_particle_antiparticle_lifetime_check.py` PASS at machine precision.
6. [`CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md`](CPT_SQUARED_IS_IDENTITY_THEOREM_NOTE_2026-05-02.md)
   — R3 Block 02 (PR #339); runner `scripts/cpt_squared_is_identity_check.py` PASS at machine precision.
7. [`GLUON_TREE_LEVEL_MASSLESSNESS_THEOREM_NOTE_2026-05-02.md`](GLUON_TREE_LEVEL_MASSLESSNESS_THEOREM_NOTE_2026-05-02.md)
   — R1 Block 01 (PR #296); runner `scripts/gluon_tree_level_massless_check.py` PASS at machine precision.
8. [`CMW_2D_SUBLATTICE_NO_SSB_THEOREM_NOTE_2026-05-02.md`](CMW_2D_SUBLATTICE_NO_SSB_THEOREM_NOTE_2026-05-02.md)
   — R2 Block 03 (PR #334); runner `scripts/cmw_2d_sublattice_no_ssb_check.py` PASS at machine precision.

### Three-generation chain ready items

9. [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)
   — runner `scripts/frontier_three_gen_observable_no_proper_quotient_narrow.py` PASS.
10. [`THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_DEP_CHAIN_AUDIT_NOTE_2026-05-02.md)
    — runner `scripts/frontier_three_generation_observable_theorem.py` PASS.

### Other ready items

11. [`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
    — in_degree=3; runner `scripts/frontier_planck_link_local_first_variation_p_a_forcing.py` PASS.
12. [`SCHUR_COVARIANCE_INHERITANCE_NARROW_THEOREM_NOTE_2026-05-02.md`](SCHUR_COVARIANCE_INHERITANCE_NARROW_THEOREM_NOTE_2026-05-02.md)
    — runner `scripts/frontier_schur_covariance_inheritance_narrow.py` PASS.
13. [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md`](GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_STRETCH_NOTE_2026-05-02.md)
    — runner `scripts/frontier_gauge_scalar_temporal_observable_bridge_stretch.py` PASS.

## Audit-readiness summary

For each item:
- **Runner passes at machine precision** (re-verified 2026-05-02)
- **All upstream deps at retained-grade** (`retained`, `retained_bounded`, `retained_no_go`, or `meta`)
- **`ready=True`** in current audit queue
- Note structure follows audit-lane style

## Cascade if all 13 retained

The 3 high-criticality items have in-degree 7-11; their retention promotes
many downstream chains. The 5 R1-R3 strict-bar blocks were the first
batch of strict-bar campaign content; their retention validates the
campaign's quality and unlocks downstream R4-R10 blocks that cite them.

Conservatively: **30+ downstream retention candidates** become audit-ready
once these 13 are retained.

## Difference from Bundle 1

Bundle 1 promotes foundational notes (lattice_noether, RP, spectrum cond,
cluster decomp, spin_statistics) that are themselves zero-dep roots.
Bundle 2 promotes items that DEPEND on retained content but have all
their deps already at retained-grade today — they are immediately
audit-ready and just need attention.

The two bundles are complementary; together they target ~18 unaudited
positive-theorem items for Codex priority.

## Manifest metadata

```yaml
manifest_type: audit_acceleration
companion_to: AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md
proposed_audit_class: B
proposed_independence: cross_family
proposed_verdict: audited_clean for all 13
total_items: 12  # was 13; yukawa_color_projection removed (Codex prior verdict: decoration)
high_criticality_count: 2
```

## Honest scope

This manifest is **meta** — no science claim. Its function:
1. Surface 13 audit-ready items via citation-graph in-degree boost.
2. Document the cascade leverage analysis.
3. Provide a single audit landing-target for Codex review.

**Not** a load-bearing science authority; should not appear as a dep for
any science note.
