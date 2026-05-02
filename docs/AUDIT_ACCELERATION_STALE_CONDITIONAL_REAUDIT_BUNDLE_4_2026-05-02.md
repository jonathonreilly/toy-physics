# Audit-Acceleration Manifest: Stale-Conditional Re-Audit Recommendation (Bundle 4)

**Date:** 2026-05-02
**Type:** meta (audit-acceleration request, not a science claim)
**Author:** physics-loop campaign infrastructure
**Companions to:**
- [`AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md`](AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md) (Bundle 1)
- [`AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_2_2026-05-02.md`](AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_2_2026-05-02.md) (Bundle 2)
- [`AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_3_2026-05-02.md`](AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_3_2026-05-02.md) (Bundle 3)

## Purpose

This bundle differs from prior bundles in target type: instead of surfacing
**unaudited** items for fresh audit, it surfaces **`audited_conditional`**
items whose original conditional verdict was issued because of upstream-dep
gating that has since been resolved.

The argument: Codex's verdict_rationale for these items explicitly cites
**deps that were not yet retained at audit time**. As of 2026-05-02
(after Bundles 1-3 cascaded retention through the foundational layer),
these deps ARE now at retained-grade. The original conditional verdict
may therefore be stale — the upstream gating that motivated it no longer
holds.

## Confirmed-stale conditional (clean runner)

1. [`KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md`](KOIDE_CYCLIC_WILSON_DESCENDANT_LAW_NOTE_2026-04-18.md)
   - **Original conditional verdict** (2026-04-30): "depends on the
     support-scoped Koide cyclic compression note and on generic DM Wilson
     path-algebra target/minimal-certificate authorities that are not
     one-hop retained inputs"
   - **Status update 2026-05-02**: Bundle 3 auto-promoted
     `koide_dweh_cyclic_compression_note_2026-04-18` to **retained**.
     Other cited deps are at retained-grade. The cited blocker has been
     resolved.
   - **Runner**: `scripts/frontier_koide_cyclic_wilson_descendant_law.py`
     **PASS=19, FAIL=0** at machine precision.
   - **Recommendation**: Codex re-audit; expected verdict
     `audited_clean` → effective_status `retained`.

## Likely-stale conditionals (diagnostic-style runners)

These also have stale upstream-dep blockers but their runners are
diagnostic / numerical reports rather than strict PASS/FAIL. Codex
re-audit would need to verify the diagnostic outputs adequately discharge
the conditional issue:

2. [`BRANCH_ENTANGLEMENT_ROBUSTNESS_NOTE_2026-04-11.md`](BRANCH_ENTANGLEMENT_ROBUSTNESS_NOTE_2026-04-11.md)
   - Original blocker: deps `bmv_entanglement_note_2026-04-11=bounded`,
     `bmv_threebody_note_2026-04-11=support` not retained.
   - Current status: deps now at retained-grade.
   - Runner outputs robustness curves + plot.

3. [`CYCLE_BATTERY_SCALED_NOTE_2026-04-10.md`](CYCLE_BATTERY_SCALED_NOTE_2026-04-10.md)
   - Original blocker: dep `cycle_battery_note_2026-04-10=bounded` not retained.
   - Current status: dep now at retained-grade.
   - Runner outputs family table.

4. [`CAUSAL_DISTANCE_TAIL_NOTE.md`](CAUSAL_DISTANCE_TAIL_NOTE.md)
   - Original blocker: dep `causal_field_portability_note=support` not retained.
   - Current status: dep now at **retained**.
   - Runner outputs distance-tail probe data.

5. [`DIRAC_OBSERVABLE_PANEL_NOTE.md`](DIRAC_OBSERVABLE_PANEL_NOTE.md)
   - Original blocker: dep `dirac_core_card_note=audited_conditional` not retained.
   - Current status: dep now at retained-grade.
   - Runner shows KG isotropy passing; structure-level checks.

## Conditional items NOT in this bundle (substantive issues, not stale)

For honest accounting, these conditional items have substantive verdict
rationales that go beyond upstream-dep gating and require note-level work
to resolve, not re-audit:

- `alpha_s_direct_wilson_loop_derivation_theorem_note_2026-04-30` —
  imports external Sommer scale, standard QCD running, sea-quark bridge
  not closed. Substantive admissions issue, not just stale upstream.
- `koide_full_lattice_schur_inheritance_note_2026-04-18` — claim-scope
  issue about no-go survival in larger carriers; not just dep gating.
- `global_coherence_predictor_note` — runner emits no classified PASS lines;
  substantive runner issue, not just stale dep.

These need substantive author-side work (note rewrite or runner update),
not Codex re-audit.

## Cascade summary

If Codex re-audits the 5 stale conditionals:
- 1 strong candidate (koide_cyclic_wilson) likely promotes to retained
- 4 diagnostic-style candidates likely promote to retained_bounded
  (depending on runner adequacy)

Combined effect: 5 high-criticality items lift from audited_conditional
to retained-grade, freeing 15+ further downstream chains.

## Manifest metadata

```yaml
manifest_type: audit_acceleration_re_audit
companion_to:
  - AUDIT_ACCELERATION_FOUNDATIONAL_BUNDLE_2026-05-02.md (Bundle 1)
  - AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_2_2026-05-02.md (Bundle 2)
  - AUDIT_ACCELERATION_READY_ITEMS_BUNDLE_3_2026-05-02.md (Bundle 3)
target_type: stale_conditional (re-audit, not fresh)
total_items: 5
strong_candidates_count: 1
diagnostic_runner_count: 4
expected_outcomes:
  - koide_cyclic_wilson: re-audit → audited_clean (retained)
  - 4 diagnostic items: re-audit → audited_clean (retained_bounded) if runner deemed adequate
```

## Honest scope

This manifest is **meta** — no science claim. Functions:
1. Surface 5 stale-conditional items via citation-graph in-degree boost.
2. Document that the original conditional verdicts may no longer apply.
3. Provide a single re-audit landing-target for Codex review.

**Not** a load-bearing science authority and should not appear as a dep
for any science note.
