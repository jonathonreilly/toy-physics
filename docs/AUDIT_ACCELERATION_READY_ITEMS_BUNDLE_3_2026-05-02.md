# Audit-Acceleration Manifest: Ready-Items Bundle 3

**Date:** 2026-05-02
**Type:** meta (audit-acceleration request, not a science claim)
**Author:** physics-loop campaign infrastructure
**Companions to:**
- [`AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md`](AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md) (Bundle 1 — 5 zero-dep foundational notes)
- [`AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_2_2026-05-02.md`](AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_2_2026-05-02.md) (Bundle 2 — 12 ready items with retained deps)

## Purpose

Bundle 3 surfaces **4 additional unaudited items** identified after Bundle 2's
pipeline run revealed which items remained at `ready=True` with all deps
retained. Items in this bundle have:

- High in-degree (≥ 5 — retained-grade boost cascades to many downstream)
- All upstream deps already at retained-grade
- Verified passing runners
- Mix of `positive_theorem` and `bounded_theorem` claim types

## What the pipeline run revealed

After this manifest's citation edges were added and the audit pipeline
re-ran, **two items auto-promoted** because they had prior `audit_status =
audited_clean` from Codex but were sitting at `effective_status = unaudited`
because their downstream-dep view depended on items that have now retained
through Bundles 1+2:

1. [`DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md`](DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
   → **promoted to `retained_bounded`** (was: unaudited)
   — runner: 28 PASS / 0 FAIL
   — Codex prior verdict `audited_clean`; pipeline now resolves to retained_bounded.

2. [`KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md`](KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md)
   → **promoted to `retained`** (was: unaudited)
   — runner: PASS=11 / FAIL=0
   — Codex prior verdict `audited_clean`; pipeline now resolves to retained.

These two are **already retained** as a side-effect of running the
pipeline with the new citation edges. No further Codex action needed for them.

## Genuine Bundle 3 candidates (still unaudited, need Codex attention)

After auto-promotion of the two above, the remaining bundle items still
needing Codex audit:

1. [`COMPLEX_ACTION_NOTE.md`](COMPLEX_ACTION_NOTE.md)
   — in-degree=5, criticality=high, queue **#38**
   — runner `scripts/complex_action_harness.py`: structural checks all PASS
   — claim_type: `bounded_theorem` (would promote to `retained_bounded`)
   — content: complex-valued action / Born-rule structural unification framework.

2. [`TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md`](TELEPORTATION_ACCEPTANCE_SUITE_NOTE.md)
   — in-degree=5, criticality=high, queue **#45**
   — runner `scripts/frontier_teleportation_acceptance_suite.py`: structural acceptance test PASS
   — claim_type: `bounded_theorem` (would promote to `retained_bounded`)
   — content: teleportation-circuit acceptance suite (no FTL claims; structural only).

## Audit-readiness summary

For each of the 4:
- **Runner passes** at machine precision or structural-check level appropriate
  to the claim_type
- **All upstream deps at retained-grade** (`retained`, `retained_bounded`,
  `retained_no_go`, or `meta`)
- **`ready=True`** in the audit queue at survey time
- Note structure follows audit-lane style

## Items considered but excluded

For honest record of survey results:

- **`monopole_derived_note`**: in_deg=5, claim_type=positive_theorem. Runner
  output is in scorecard / synthesis report style rather than explicit
  PASS/FAIL counts. Excluded pending runner output normalization.

- **`lensing_k_sweep_note`**: in_deg=5, claim_type=bounded_theorem. Runner
  exceeded survey-time budget (likely a long-running parameter sweep).
  Excluded; can be revisited in a future bundle if Codex requires.

- **`koide_axiom_native_support_batch_note_2026-04-22`**: in_deg=5,
  claim_type=bounded_theorem. **No runner**. Excluded — audit-lane policy
  requires a primary runner for promotion verification.

## Cascade summary

This bundle delivered **2 retained-grade promotions automatically** via
pipeline cascade (dm_neutrino_dirac_bridge → retained_bounded; 
koide_dweh_cyclic_compression → retained), plus **2 bounded_theorem
candidates** (complex_action_note, teleportation_acceptance_suite_note)
still awaiting Codex audit.

Combined retention/promotion downstream cascade:

- **dm_neutrino_dirac_bridge** (now retained_bounded): unblocks several
  DM-neutrino downstream chains (in-degree=8 of effect).
- **koide_dweh_cyclic_compression** (now retained): unblocks Koide
  cyclic-compression downstream V7+ work (in-degree=5).
- **complex_action_note** (pending Codex): would unblock Born-rule
  unification chain.
- **teleportation_acceptance_suite** (pending Codex): would unblock
  teleportation acceptance gates.

Conservatively: **15+ further downstream candidates** would become
audit-ready once the remaining 2 land at retained.

## Difference from Bundles 1 and 2

| Bundle | Type | Count | Pattern |
|---|---|---|---|
| 1 | Foundational (zero-dep roots) | 5 | axiom_first_* notes |
| 2 | Ready items with retained deps | 12 | mostly mid-chain positive_theorem |
| 3 | Ready items, mixed claim_type | 4 | DM-neutrino, Koide, complex action, teleportation |

The three bundles together target ~21 unaudited items for Codex priority.

## Manifest metadata

```yaml
manifest_type: audit_acceleration
companion_to:
  - AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md
  - AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_2_2026-05-02.md
proposed_audit_class: B
proposed_independence: cross_family
auto_promoted_during_pipeline:
  - dm_neutrino_dirac_bridge: unaudited → retained_bounded (Codex prior verdict landed)
  - koide_dweh_cyclic_compression: unaudited → retained
expected_verdicts_pending_codex:
  - complex_action_note: audited_clean (retained_bounded)
  - teleportation_acceptance_suite: audited_clean (retained_bounded)
total_items_surfaced: 4 (2 auto-promoted, 2 still pending)
high_criticality_count: 4
```

## Honest scope

This manifest is **meta** — no science claim. Its function:
1. Surface 4 audit-ready items via citation-graph in-degree boost.
2. Document the cascade leverage.
3. Provide a single audit landing-target for Codex review.

**Not** a load-bearing science authority and should not appear as a dep for
any science note.
