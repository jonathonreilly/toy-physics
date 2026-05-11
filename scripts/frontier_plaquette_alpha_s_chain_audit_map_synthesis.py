#!/usr/bin/env python3
"""Re-verify the plaquette / alpha_s chain audit map synthesis meta note
against the live audit ledger.

This is a navigation-map check, not a physics proof. The synthesis note
makes specific claims about the live ledger:

  - the two roots (`alpha_s_derived_note`, `plaquette_self_consistency_note`)
    are present and `unaudited`;
  - the transitive-closure size of the upstream chain is `44`;
  - the audit_status distribution matches the table in §"Chain scope";
  - the 6 conditional frontier rows are exactly the set named in
    §"Chain frontier (entry points)" and each carries the repair-class
    string quoted in the synthesis table;
  - the synthesis itself is `claim_type: meta` with `proposal_allowed: false`;
  - no audit row is promoted by this synthesis.

If any of these drift (e.g. a frontier row's audit_status changes), the
runner FAILs and the synthesis needs a refresh.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
NOTE = ROOT / "docs" / "PLAQUETTE_ALPHA_S_CHAIN_AUDIT_MAP_SYNTHESIS_META_NOTE_2026-05-10.md"

ROOTS = ("alpha_s_derived_note", "plaquette_self_consistency_note")

EXPECTED_CHAIN_SIZE = 44

EXPECTED_STATUS_COUNTS = {
    "audited_clean": 22,
    "unaudited": 12,
    "audited_conditional": 8,
    "audited_decoration": 2,
}

# Conditional frontier rows + the repair_class prefix that must still be
# in their `notes_for_re_audit_if_any`. The synthesis quotes the full
# auditor strings; this runner checks the structural prefix only so the
# auditor can refine wording without breaking the runner.
EXPECTED_CONDITIONAL_FRONTIER = {
    "g_bare_constraint_vs_convention_theorem_note_2026-05-03": "dependency_not_retained",
    "su3_wigner_intertwiner_block4_block5_theorem_note_2026-05-03": "scope_too_broad",
    "gauge_vacuum_plaquette_spatial_environment_character_measure_theorem_note": "missing_bridge_theorem",
    "gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note": "missing_bridge_theorem",
    "gauge_vacuum_plaquette_local_environment_factorization_theorem_note": "missing_bridge_theorem",
    "gauge_vacuum_plaquette_residual_environment_identification_theorem_note": "missing_bridge_theorem",
}

# Decoration frontier rows + their parent claim_id. These are
# "resolved" frontier — they sit at the boundary but already roll up
# under retained-grade parents and contribute no remaining work.
EXPECTED_DECORATION_FRONTIER = {
    "gauge_vacuum_plaquette_perron_reduction_theorem_note":
        "gauge_vacuum_plaquette_transfer_operator_character_recurrence_note",
    "g_bare_rescaling_freedom_removal_theorem_note_2026-05-03":
        "cl3_color_automorphism_theorem",
}

# Cleanly-audited open_gate frontier rows. These are at the chain
# boundary but the audit lane has explicitly recognized them as named
# open work surfaces (audit_status=audited_clean, effective_status=open_gate).
# Not awaiting forward motion at this row's scope.
EXPECTED_OPEN_GATE_FRONTIER = {
    "staggered_dirac_realization_gate_note_2026-05-03",
}

RETAINED_GRADES = {"retained", "retained_no_go", "retained_bounded", "meta"}


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


def is_retained_grade(es: str | None) -> bool:
    if not es:
        return False
    if es in RETAINED_GRADES:
        return True
    return es.startswith("decoration_under_")


def upstream_closure(rows: dict[str, dict], start_cid: str) -> set[str]:
    visited: set[str] = set()
    queue: deque[str] = deque([start_cid])
    while queue:
        cid = queue.popleft()
        if cid in visited:
            continue
        visited.add(cid)
        for d in rows.get(cid, {}).get("deps", []):
            if d in rows and d not in visited:
                queue.append(d)
    visited.discard(start_cid)
    return visited


def main() -> int:
    if not LEDGER.exists():
        print(f"missing ledger: {LEDGER}")
        return 1
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1

    rows = json.loads(LEDGER.read_text())["rows"]
    note = NOTE.read_text()

    print("plaquette / alpha_s chain audit map synthesis check")
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

    # ---- roots ----
    for cid in ROOTS:
        r = rows.get(cid, {})
        check(
            f"root present: {cid}",
            bool(r),
            f"audit_status={r.get('audit_status')!r}",
        )
        check(
            f"root unaudited: {cid}",
            r.get("audit_status") == "unaudited",
            f"audit_status={r.get('audit_status')!r}",
        )

    # ---- chain size ----
    chain: set[str] = set(ROOTS)
    for root in ROOTS:
        chain |= upstream_closure(rows, root)
    check(
        f"chain transitive-closure size = {EXPECTED_CHAIN_SIZE}",
        len(chain) == EXPECTED_CHAIN_SIZE,
        f"actual={len(chain)}",
    )

    # ---- status distribution ----
    actual_status_counts: dict[str, int] = {}
    for cid in chain:
        s = rows.get(cid, {}).get("audit_status") or "unaudited"
        actual_status_counts[s] = actual_status_counts.get(s, 0) + 1
    for status, expected in EXPECTED_STATUS_COUNTS.items():
        actual = actual_status_counts.get(status, 0)
        check(
            f"chain audit_status[{status}] = {expected}",
            actual == expected,
            f"actual={actual}",
        )

    # ---- decoration frontier ----
    for cid, expected_parent in EXPECTED_DECORATION_FRONTIER.items():
        r = rows.get(cid, {})
        check(
            f"decoration frontier present + audited_decoration: {cid}",
            r.get("audit_status") == "audited_decoration",
            f"audit_status={r.get('audit_status')!r}",
        )
        check(
            f"decoration frontier parent is {expected_parent}",
            r.get("decoration_parent_claim_id") == expected_parent,
            f"actual_parent={r.get('decoration_parent_claim_id')!r}",
        )
        parent_eff = rows.get(expected_parent, {}).get("effective_status")
        check(
            f"decoration frontier parent retained-grade: {expected_parent}",
            is_retained_grade(parent_eff),
            f"parent_effective={parent_eff!r}",
        )

    # ---- conditional frontier ----
    for cid, expected_repair_prefix in EXPECTED_CONDITIONAL_FRONTIER.items():
        r = rows.get(cid, {})
        check(
            f"conditional frontier present: {cid}",
            bool(r),
        )
        check(
            f"conditional frontier audited_conditional: {cid}",
            r.get("audit_status") == "audited_conditional",
            f"audit_status={r.get('audit_status')!r}",
        )
        notes = (r.get("notes_for_re_audit_if_any") or "").strip()
        check(
            f"conditional frontier repair_class={expected_repair_prefix}: {cid}",
            notes.startswith(expected_repair_prefix),
            f"notes_prefix={notes.split(':', 1)[0]!r}",
        )
        # And confirm its deps are all retained-grade — otherwise it
        # is not really a frontier row, it's a deeper-chain row that
        # also has an upstream block.
        bad_deps = [
            d
            for d in r.get("deps", [])
            if not is_retained_grade(rows.get(d, {}).get("effective_status"))
        ]
        check(
            f"conditional frontier has all retained-grade deps: {cid}",
            not bad_deps,
            f"non_retained_deps={bad_deps}",
        )

    # ---- frontier completeness ----
    # A frontier row in this chain is one whose own one-hop deps are
    # all retained-grade. It can be resolved (audited_decoration under
    # retained parent, audited_clean open_gate) or still active
    # (audited_conditional). Roots themselves are excluded; meta rows
    # are excluded (they don't sit at the audit frontier).
    actual_frontier: set[str] = set()
    for cid in chain:
        if cid in ROOTS:
            continue
        r = rows.get(cid, {})
        es = r.get("effective_status")
        if es == "meta":
            continue
        # Skip rows whose own audit conclusion is "retained" without any
        # further frontier-relevant marker — those are interior to the
        # retained core, not at its boundary.
        if r.get("audit_status") == "audited_clean" and es in {
            "retained", "retained_no_go", "retained_bounded"
        }:
            continue
        deps = r.get("deps", [])
        bad = [
            d
            for d in deps
            if not is_retained_grade(rows.get(d, {}).get("effective_status"))
        ]
        if not bad:
            actual_frontier.add(cid)

    expected_frontier = (
        set(EXPECTED_CONDITIONAL_FRONTIER)
        | set(EXPECTED_DECORATION_FRONTIER)
        | set(EXPECTED_OPEN_GATE_FRONTIER)
    )
    extra = actual_frontier - expected_frontier
    missing = expected_frontier - actual_frontier
    check(
        f"chain frontier matches expected ({len(expected_frontier)} rows)",
        not extra and not missing,
        f"extra={sorted(extra)} missing={sorted(missing)}",
    )

    # ---- open-gate frontier rows are audited_clean ----
    for cid in EXPECTED_OPEN_GATE_FRONTIER:
        r = rows.get(cid, {})
        check(
            f"open-gate frontier present + audited_clean: {cid}",
            r.get("audit_status") == "audited_clean",
            f"audit_status={r.get('audit_status')!r}",
        )
        check(
            f"open-gate frontier effective_status=open_gate: {cid}",
            r.get("effective_status") == "open_gate",
            f"effective_status={r.get('effective_status')!r}",
        )

    # ---- interior proper-claim unaudited rows are NOT independently
    # attackable. Excludes meta rows (which don't need audit verdicts)
    # and the cleanly-audited open_gate frontier (which is at the
    # boundary, not the interior).
    interior_ready = []
    for cid in chain:
        if cid in EXPECTED_OPEN_GATE_FRONTIER:
            continue
        r = rows.get(cid, {})
        if r.get("audit_status") != "unaudited":
            continue
        if r.get("claim_type") == "meta":
            continue
        if r.get("effective_status") == "meta":
            continue
        deps = r.get("deps", [])
        bad = [
            d
            for d in deps
            if not is_retained_grade(rows.get(d, {}).get("effective_status"))
        ]
        if not bad:
            interior_ready.append(cid)
    check(
        "no proper-claim interior unaudited row is independently ready",
        not interior_ready,
        f"ready_unaudited={interior_ready}",
    )

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
