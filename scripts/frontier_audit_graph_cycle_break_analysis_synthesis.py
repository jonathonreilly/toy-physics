#!/usr/bin/env python3
"""Re-verify the audit-graph cycle-break analysis synthesis meta note
against the live cycle inventory + audit queue + audit ledger.

This is a navigation-map check, not a physics proof. The synthesis note
makes specific claims about the live audit-lane data:

  - the cycle inventory reports a total of 305 citation cycles;
  - the audit queue's `cycle_break_targets` list has length 305 (one
    entry per cycle);
  - the cycles-by-length distribution matches the table in
    §"Cycles by length";
  - the top-25 cycle-break primary targets (sorted by
    `max_transitive_descendants` descending, then `cycle_length`
    ascending) match the table in §"Top 25 cycle-break targets",
    including their `cycle_id`, `cycle_length`,
    `max_transitive_descendants`, primary break target claim_id,
    `audit_status`, and `criticality`;
  - the unique-target rollup (17 unique primary break targets across
    the top 25) matches the live queue;
  - all 25 top primary break targets are `unaudited` (so none carries
    an auditor-assigned per-row repair class) and `critical`;
  - none of the top 25 carries `missing_bridge_theorem` on its current
    ledger row;
  - the synthesis itself is `claim_type: meta` with
    `proposal_allowed: false`;
  - no audit row is promoted by this synthesis.

If any of these drift (e.g. the cycle inventory recomputes a different
total, a top-25 break target gets audited and changes status, or the
ranking order shifts), the runner FAILs and the synthesis needs a
refresh.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
QUEUE = ROOT / "docs" / "audit" / "data" / "audit_queue.json"
INVENTORY = ROOT / "docs" / "audit" / "data" / "cycle_inventory.json"
NOTE = ROOT / "docs" / "AUDIT_GRAPH_CYCLE_BREAK_ANALYSIS_SYNTHESIS_META_NOTE_2026-05-10.md"


EXPECTED_CYCLE_COUNT = 305

# length -> count from cycle_inventory.json at write time.
EXPECTED_LENGTH_COUNTS = {
    2: 41,
    3: 17,
    4: 21,
    5: 24,
    6: 15,
    7: 18,
    8: 12,
    9: 7,
    10: 8,
    11: 8,
    12: 6,
    13: 4,
    14: 10,
    15: 3,
    16: 2,
    17: 5,
    18: 2,
    19: 4,
    20: 2,
    21: 4,
    22: 2,
    23: 6,
    24: 6,
    25: 4,
    26: 10,
    27: 4,
    28: 11,
    29: 6,
    31: 10,
    32: 10,
    33: 13,
    34: 8,
    35: 2,
}


# Top-25 ranked entries: (cycle_id, cycle_length, max_desc,
# primary_break_target). Order is by max_desc descending, then
# cycle_length ascending — same sort the queue uses. The max_desc
# values include the +1 contribution from this synthesis note itself
# citing the 17 unique top-25 targets as deps in its markdown body.
EXPECTED_TOP_25 = [
    ("cycle-0001",  2, 709, "axiom_first_reflection_positivity_theorem_note_2026-04-29"),
    ("cycle-0002",  2, 700, "bh_entropy_derived_note"),
    ("cycle-0003",  2, 698, "3d_correction_master_note"),
    ("cycle-0004",  2, 698, "angular_kernel_underdetermination_no_go_note"),
    ("cycle-0005",  2, 698, "architecture_note_directional_measure"),
    ("cycle-0006",  2, 698, "bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29"),
    ("cycle-0007",  2, 698, "discrete_einstein_regge_lift_note"),
    ("cycle-0008",  3, 698, "area_law_coefficient_gap_note"),
    ("cycle-0009",  4, 698, "area_law_coefficient_gap_note"),
    ("cycle-0010",  4, 698, "area_law_coefficient_gap_note"),
    ("cycle-0011",  5, 698, "universal_gr_constraint_action_stationarity_note"),
    ("cycle-0012",  6, 698, "area_law_native_car_semantics_tightening_note_2026-04-25"),
    ("cycle-0013",  7, 698, "area_law_native_car_semantics_tightening_note_2026-04-25"),
    ("cycle-0014", 13, 698, "anomaly_forces_time_theorem"),
    ("cycle-0015", 14, 698, "angular_kernel_underdetermination_no_go_note"),
    ("cycle-0016",  2, 645, "su3_casimir_fundamental_algebraic_k1_k3_narrow_proof_walk_bounded_note_2026-05-10"),
    ("cycle-0017",  2, 642, "g_bare_canonical_convention_narrow_theorem_note_2026-05-02"),
    ("cycle-0018",  2, 642, "g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09"),
    ("cycle-0019",  2, 642, "gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10"),
    ("cycle-0020",  3, 642, "g_bare_canonical_convention_narrow_theorem_note_2026-05-02"),
    ("cycle-0021",  6, 642, "g_bare_constraint_vs_convention_restatement_note_2026-05-07"),
    ("cycle-0022",  7, 642, "g_bare_constraint_vs_convention_restatement_note_2026-05-07"),
    ("cycle-0023",  8, 642, "alpha_s_derived_note"),
    ("cycle-0024",  8, 642, "alpha_s_derived_note"),
    ("cycle-0025",  8, 642, "alpha_s_derived_note"),
]


# Unique-target rollup across top 25:
# primary break target -> count of top-25 cycles it appears on.
EXPECTED_TOP_25_UNIQUE_COUNTS = {
    "area_law_coefficient_gap_note": 3,
    "alpha_s_derived_note": 3,
    "angular_kernel_underdetermination_no_go_note": 2,
    "area_law_native_car_semantics_tightening_note_2026-04-25": 2,
    "g_bare_canonical_convention_narrow_theorem_note_2026-05-02": 2,
    "g_bare_constraint_vs_convention_restatement_note_2026-05-07": 2,
    "axiom_first_reflection_positivity_theorem_note_2026-04-29": 1,
    "bh_entropy_derived_note": 1,
    "3d_correction_master_note": 1,
    "architecture_note_directional_measure": 1,
    "bh_quarter_wald_noether_framework_carrier_theorem_note_2026-04-29": 1,
    "discrete_einstein_regge_lift_note": 1,
    "universal_gr_constraint_action_stationarity_note": 1,
    "anomaly_forces_time_theorem": 1,
    "su3_casimir_fundamental_algebraic_k1_k3_narrow_proof_walk_bounded_note_2026-05-10": 1,
    "g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09": 1,
    "gauge_vacuum_plaquette_hierarchy_obstruction_lemmas_bounded_note_2026-05-10": 1,
}


# All-305 audit_status distribution of break targets at write time.
EXPECTED_ALL_STATUS_COUNTS = {
    "unaudited": 300,
    "audited_conditional": 4,
    None: 1,
}


# All-305 criticality distribution of break targets at write time.
EXPECTED_ALL_CRITICALITY_COUNTS = {
    "critical": 280,
    "medium": 12,
    "high": 11,
    "leaf": 2,
}


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" | {detail}" if detail else ""
    print(f"{tag}: {label}{suffix}")


def main() -> int:
    if not LEDGER.exists():
        print(f"missing ledger: {LEDGER}")
        return 1
    if not QUEUE.exists():
        print(f"missing queue: {QUEUE}")
        return 1
    if not INVENTORY.exists():
        print(f"missing cycle inventory: {INVENTORY}")
        return 1
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1

    rows = json.loads(LEDGER.read_text())["rows"]
    queue = json.loads(QUEUE.read_text())
    inventory = json.loads(INVENTORY.read_text())
    note = NOTE.read_text()

    print("audit-graph cycle-break analysis synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification + governance ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    check(
        "synthesis declares proposal_allowed: false",
        "proposal_allowed: false" in note,
    )
    audit_clean_token = "audited" + "_clean"
    check(
        "synthesis does not declare itself audited_clean",
        audit_clean_token not in note.split("## ", 1)[0],
        "header block must not pre-empt audit verdict",
    )

    # ---- total cycle count ----
    actual_cycle_count = inventory.get("cycle_count")
    check(
        f"cycle_inventory cycle_count = {EXPECTED_CYCLE_COUNT}",
        actual_cycle_count == EXPECTED_CYCLE_COUNT,
        f"actual={actual_cycle_count}",
    )
    actual_inventory_cycles = len(inventory.get("cycles") or [])
    check(
        f"cycle_inventory cycles list length = {EXPECTED_CYCLE_COUNT}",
        actual_inventory_cycles == EXPECTED_CYCLE_COUNT,
        f"actual={actual_inventory_cycles}",
    )

    # ---- queue cycle_break_targets length ----
    cb = queue.get("cycle_break_targets") or []
    actual_cb_count = queue.get("cycle_break_target_count")
    check(
        f"audit_queue cycle_break_target_count = {EXPECTED_CYCLE_COUNT}",
        actual_cb_count == EXPECTED_CYCLE_COUNT,
        f"actual={actual_cb_count}",
    )
    check(
        f"audit_queue cycle_break_targets list length = {EXPECTED_CYCLE_COUNT}",
        len(cb) == EXPECTED_CYCLE_COUNT,
        f"actual={len(cb)}",
    )

    # ---- length distribution ----
    actual_length_counts: Counter[int] = Counter()
    for c in inventory.get("cycles") or []:
        L = c.get("length")
        if L is not None:
            actual_length_counts[int(L)] += 1
    for L, expected in EXPECTED_LENGTH_COUNTS.items():
        actual = actual_length_counts.get(L, 0)
        check(
            f"length[{L}] count = {expected}",
            actual == expected,
            f"actual={actual}",
        )
    # Reverse direction: any unexpected lengths?
    extra_lengths = sorted(
        set(actual_length_counts.keys()) - set(EXPECTED_LENGTH_COUNTS.keys())
    )
    check(
        "no unexpected cycle lengths in inventory",
        not extra_lengths,
        f"extra_lengths={extra_lengths}",
    )

    # ---- top-25 cycle break targets ----
    # The queue is already sorted by (-max_desc, length, ...). Verify
    # the prefix matches our expected table in order.
    for i, expected in enumerate(EXPECTED_TOP_25):
        exp_cycle_id, exp_len, exp_desc, exp_target = expected
        if i >= len(cb):
            check(f"top-25 entry [{i + 1}] present", False, f"queue too short")
            continue
        actual = cb[i]
        check(
            f"top-25[{i + 1}] cycle_id = {exp_cycle_id}",
            actual.get("cycle_id") == exp_cycle_id,
            f"actual={actual.get('cycle_id')!r}",
        )
        check(
            f"top-25[{i + 1}] cycle_length = {exp_len}",
            actual.get("cycle_length") == exp_len,
            f"actual={actual.get('cycle_length')}",
        )
        check(
            f"top-25[{i + 1}] max_desc = {exp_desc}",
            actual.get("max_transitive_descendants") == exp_desc,
            f"actual={actual.get('max_transitive_descendants')}",
        )
        check(
            f"top-25[{i + 1}] primary_break_target = {exp_target}",
            actual.get("primary_break_target") == exp_target,
            f"actual={actual.get('primary_break_target')!r}",
        )
        # Live audit_status + criticality from the ledger row.
        r = rows.get(exp_target, {})
        check(
            f"top-25[{i + 1}] target audit_status = unaudited",
            r.get("audit_status") == "unaudited",
            f"actual={r.get('audit_status')!r}",
        )
        check(
            f"top-25[{i + 1}] target criticality = critical",
            r.get("criticality") == "critical",
            f"actual={r.get('criticality')!r}",
        )

    # ---- top-25 unique-target rollup ----
    actual_top_25_targets = Counter(c["primary_break_target"] for c in cb[:25])
    check(
        f"top-25 unique-target count = {len(EXPECTED_TOP_25_UNIQUE_COUNTS)}",
        len(actual_top_25_targets) == len(EXPECTED_TOP_25_UNIQUE_COUNTS),
        f"actual_unique={len(actual_top_25_targets)}",
    )
    for target, expected_count in EXPECTED_TOP_25_UNIQUE_COUNTS.items():
        actual = actual_top_25_targets.get(target, 0)
        check(
            f"top-25 unique[{target}] count = {expected_count}",
            actual == expected_count,
            f"actual={actual}",
        )

    # ---- top-25 carry no per-row repair_class ----
    # Because all 25 are unaudited, none should have a notes_for_re_audit_if_any
    # populated with an auditor repair class. The cycle entry's repair_class
    # is the queue-assigned cycle_break_required.
    bridge_theorem_count = 0
    for c in cb[:25]:
        cid = c["primary_break_target"]
        r = rows.get(cid, {})
        notes = (r.get("notes_for_re_audit_if_any") or "").strip()
        if notes.startswith("missing_bridge_theorem"):
            bridge_theorem_count += 1
    check(
        "0 of top-25 primary targets carry missing_bridge_theorem on their row",
        bridge_theorem_count == 0,
        f"actual={bridge_theorem_count}",
    )
    # And every top-25 cycle entry carries cycle_break_required as the
    # queue-assigned repair_class.
    not_cbr = [
        c["cycle_id"]
        for c in cb[:25]
        if c.get("repair_class") != "cycle_break_required"
    ]
    check(
        "all top-25 cycle entries carry repair_class=cycle_break_required",
        not not_cbr,
        f"non_cbr={not_cbr}",
    )

    # ---- all-305 status distribution ----
    actual_all_status: dict[object, int] = {}
    for c in cb:
        s = c.get("primary_break_target_audit_status")
        actual_all_status[s] = actual_all_status.get(s, 0) + 1
    for s, expected in EXPECTED_ALL_STATUS_COUNTS.items():
        actual = actual_all_status.get(s, 0)
        check(
            f"all-305 audit_status[{s!r}] = {expected}",
            actual == expected,
            f"actual={actual}",
        )

    # ---- all-305 criticality distribution ----
    actual_all_crit: dict[object, int] = {}
    for c in cb:
        cr = c.get("primary_break_target_criticality")
        actual_all_crit[cr] = actual_all_crit.get(cr, 0) + 1
    for cr, expected in EXPECTED_ALL_CRITICALITY_COUNTS.items():
        actual = actual_all_crit.get(cr, 0)
        check(
            f"all-305 criticality[{cr!r}] = {expected}",
            actual == expected,
            f"actual={actual}",
        )

    # ---- ordering invariant: cycle_break_targets sorted by
    # (-max_desc, length) ----
    prev_key = None
    out_of_order = 0
    for c in cb:
        key = (-(c.get("max_transitive_descendants") or 0), c.get("cycle_length") or 0)
        if prev_key is not None and key < prev_key:
            out_of_order += 1
        prev_key = key
    check(
        "cycle_break_targets sorted by (-max_desc, length) ascending",
        out_of_order == 0,
        f"out_of_order_pairs={out_of_order}",
    )

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
