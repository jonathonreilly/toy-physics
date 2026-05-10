#!/usr/bin/env python3
"""Re-verify the neutrino_majorana chain audit map synthesis meta note
against the live audit ledger.

This is a navigation-map check, not a physics proof. The synthesis note
makes specific claims about the live ledger:

  - the root (`neutrino_majorana_operator_axiom_first_note`) is present
    and `unaudited`;
  - the transitive-closure size of the upstream chain (including the
    root itself) is `115`;
  - the audit_status distribution matches the table in §"Chain scope";
  - the 12 conditional frontier rows are exactly the set named in
    §"Chain frontier (entry points)" and each carries the repair-class
    string quoted in the synthesis table;
  - the single open-gate frontier row is the one named in the synthesis;
  - no proper-claim interior unaudited row is independently
    `ready=True` in the audit queue;
  - the synthesis itself is `claim_type: meta` with `proposal_allowed: false`;
  - no audit row is promoted by this synthesis.

If any of these drift (e.g. a frontier row's audit_status changes), the
runner FAILs and the synthesis needs a refresh.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
LEDGER = ROOT_DIR / "docs" / "audit" / "data" / "audit_ledger.json"
QUEUE = ROOT_DIR / "docs" / "audit" / "data" / "audit_queue.json"
NOTE = ROOT_DIR / "docs" / "NEUTRINO_MAJORANA_CHAIN_AUDIT_MAP_SYNTHESIS_META_NOTE_2026-05-10.md"

ROOT_CID = "neutrino_majorana_operator_axiom_first_note"

EXPECTED_CHAIN_SIZE = 115

EXPECTED_STATUS_COUNTS = {
    "unaudited": 79,
    "audited_clean": 24,
    "audited_conditional": 12,
}

# Conditional frontier rows + the repair_class prefix that must still be
# in their `notes_for_re_audit_if_any`. The synthesis quotes the full
# auditor strings; this runner checks the structural prefix only so the
# auditor can refine wording without breaking the runner.
EXPECTED_CONDITIONAL_FRONTIER = {
    "axiom_first_cluster_decomposition_theorem_note_2026-04-29": "missing_bridge_theorem",
    "axiom_first_lattice_noether_theorem_note_2026-04-29": "missing_bridge_theorem",
    "observable_principle_from_axiom_note": "missing_bridge_theorem",
    "s3_boundary_link_theorem_note": "missing_bridge_theorem",
    "staggered_fermion_card_2026-04-11": "missing_bridge_theorem",
    "quark_route2_source_domain_bridge_no_go_note_2026-04-28": "missing_dependency_edge",
    "s3_cap_uniqueness_note": "missing_dependency_edge",
    "universal_gr_isotropic_glue_operator_note": "missing_dependency_edge",
    "universal_gr_lorentzian_global_atlas_closure_note": "missing_dependency_edge",
    "universal_gr_tensor_action_blocker_note": "missing_dependency_edge",
    "source_driven_field_recovery_sweep_note": "runner_artifact_issue",
    "physical_hermitian_hamiltonian_and_sme_bridge_note_2026-04-30": "other",
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
    """BFS upstream closure including the start node itself."""
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
    return visited


def main() -> int:
    if not LEDGER.exists():
        print(f"missing ledger: {LEDGER}")
        return 1
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1
    if not QUEUE.exists():
        print(f"missing queue: {QUEUE}")
        return 1

    rows = json.loads(LEDGER.read_text())["rows"]
    note = NOTE.read_text()
    queue_data = json.loads(QUEUE.read_text())
    qmap = {q["claim_id"]: q for q in queue_data.get("queue", [])}

    print("neutrino_majorana chain audit map synthesis check")
    print(f"note: {NOTE.relative_to(ROOT_DIR)}")
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

    # ---- root ----
    r = rows.get(ROOT_CID, {})
    check(
        f"root present: {ROOT_CID}",
        bool(r),
        f"audit_status={r.get('audit_status')!r}",
    )
    check(
        f"root unaudited: {ROOT_CID}",
        r.get("audit_status") == "unaudited",
        f"audit_status={r.get('audit_status')!r}",
    )

    # ---- chain size (includes root) ----
    chain: set[str] = upstream_closure(rows, ROOT_CID)
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
            f"notes_prefix={notes.split(':', 1)[0][:60]!r}",
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
    # all retained-grade. It can be active (audited_conditional) or
    # already resolved (audited_clean open_gate). The root itself is
    # excluded; meta rows are excluded (they don't sit at the audit
    # frontier); fully retained-grade rows are excluded.
    actual_frontier: set[str] = set()
    for cid in chain:
        if cid == ROOT_CID:
            continue
        r = rows.get(cid, {})
        es = r.get("effective_status")
        if es == "meta":
            continue
        # Skip rows whose own audit conclusion is already retained-grade
        # — those are interior to the retained core, not at its boundary.
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
    # attackable. Excludes meta rows (which don't need audit verdicts),
    # the root itself, and the cleanly-audited open_gate frontier
    # (which is at the boundary, not the interior).
    interior_ready = []
    for cid in chain:
        if cid == ROOT_CID:
            continue
        if cid in EXPECTED_OPEN_GATE_FRONTIER:
            continue
        r = rows.get(cid, {})
        if r.get("audit_status") != "unaudited":
            continue
        if r.get("claim_type") == "meta":
            continue
        if r.get("effective_status") == "meta":
            continue
        # If the row appears in the live audit queue and is ready=True,
        # the synthesis claim "no proper-claim interior unaudited row is
        # independently ready" is false.
        q = qmap.get(cid)
        if q is not None and q.get("ready") is True:
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
