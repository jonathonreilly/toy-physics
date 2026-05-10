#!/usr/bin/env python3
"""Re-verify the observable_principle_from_axiom chain audit map synthesis
meta note against the live audit ledger.

This is a navigation-map check, not a physics proof. The synthesis note
makes specific claims about the live ledger:

  - the root (`observable_principle_from_axiom_note`) is present with
    `audit_status = audited_conditional` and `effective_status =
    audited_conditional`;
  - the transitive-closure size of the upstream chain is `1` (the root
    has empty `deps`, so the chain is the root itself);
  - the audit_status distribution matches the table in §"Chain scope";
  - the chain frontier (excluding the root) is empty;
  - the root carries `notes_for_re_audit_if_any` starting with the
    `missing_bridge_theorem` repair-class prefix;
  - the synthesis itself is `claim_type: meta` with `proposal_allowed:
    false`;
  - no audit row is promoted by this synthesis.

If any of these drift (e.g. the root's audit_status changes, or a new
upstream dep is added so the chain grows), the runner FAILs and the
synthesis needs a refresh.
"""

from __future__ import annotations

import json
from collections import deque
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
LEDGER = ROOT_DIR / "docs" / "audit" / "data" / "audit_ledger.json"
QUEUE = ROOT_DIR / "docs" / "audit" / "data" / "audit_queue.json"
NOTE = (
    ROOT_DIR
    / "docs"
    / "OBSERVABLE_PRINCIPLE_FROM_AXIOM_CHAIN_AUDIT_MAP_SYNTHESIS_META_NOTE_2026-05-10.md"
)

ROOT_CID = "observable_principle_from_axiom_note"

EXPECTED_CHAIN_SIZE = 1

EXPECTED_STATUS_COUNTS = {
    "audited_conditional": 1,
}

EXPECTED_REPAIR_CLASS_PREFIX = "missing_bridge_theorem"

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

    print("observable_principle_from_axiom chain audit map synthesis check")
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

    # ---- root present + audited_conditional ----
    r = rows.get(ROOT_CID, {})
    check(
        f"root present: {ROOT_CID}",
        bool(r),
        f"audit_status={r.get('audit_status')!r}",
    )
    check(
        f"root audited_conditional: {ROOT_CID}",
        r.get("audit_status") == "audited_conditional",
        f"audit_status={r.get('audit_status')!r}",
    )
    check(
        f"root effective_status audited_conditional: {ROOT_CID}",
        r.get("effective_status") == "audited_conditional",
        f"effective_status={r.get('effective_status')!r}",
    )
    check(
        f"root criticality critical: {ROOT_CID}",
        r.get("criticality") == "critical",
        f"criticality={r.get('criticality')!r}",
    )

    # ---- chain size ----
    upstream = upstream_closure(rows, ROOT_CID)
    chain: set[str] = upstream | {ROOT_CID}
    check(
        f"chain transitive-closure size = {EXPECTED_CHAIN_SIZE}",
        len(chain) == EXPECTED_CHAIN_SIZE,
        f"actual={len(chain)} chain={sorted(chain)}",
    )
    check(
        "root has empty deps (no upstream rows)",
        r.get("deps") == [],
        f"deps={r.get('deps')!r}",
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
    # Also check that no other audit_status values appear in the chain
    extra_statuses = {
        s: c
        for s, c in actual_status_counts.items()
        if s not in EXPECTED_STATUS_COUNTS
    }
    check(
        "chain contains no unexpected audit_status values",
        not extra_statuses,
        f"extra={extra_statuses}",
    )

    # ---- root repair class ----
    notes_for_re_audit = (r.get("notes_for_re_audit_if_any") or "").strip()
    check(
        f"root carries repair_class prefix: {EXPECTED_REPAIR_CLASS_PREFIX}",
        notes_for_re_audit.startswith(EXPECTED_REPAIR_CLASS_PREFIX),
        f"notes_prefix={notes_for_re_audit.split(':', 1)[0]!r}",
    )

    # ---- frontier ----
    # A frontier row in this chain is one whose own one-hop deps are
    # all retained-grade. Roots themselves are excluded; meta rows are
    # excluded (they don't sit at the audit frontier).
    actual_frontier: set[str] = set()
    for cid in chain:
        if cid == ROOT_CID:
            continue
        row = rows.get(cid, {})
        es = row.get("effective_status")
        if es == "meta":
            continue
        if row.get("audit_status") == "audited_clean" and es in {
            "retained", "retained_no_go", "retained_bounded"
        }:
            continue
        deps = row.get("deps", [])
        bad = [
            d
            for d in deps
            if not is_retained_grade(rows.get(d, {}).get("effective_status"))
        ]
        if not bad:
            actual_frontier.add(cid)
    check(
        "chain frontier is empty (root excluded; chain has size 1)",
        not actual_frontier,
        f"actual_frontier={sorted(actual_frontier)}",
    )

    # ---- interior proper-claim unaudited rows are NOT independently
    # attackable. Vacuous given chain size 1, but checked for symmetry
    # with the sibling plaquette / alpha_s chain map synthesis runner.
    interior_ready = []
    for cid in chain:
        if cid == ROOT_CID:
            continue
        row = rows.get(cid, {})
        if row.get("audit_status") != "unaudited":
            continue
        if row.get("claim_type") == "meta":
            continue
        if row.get("effective_status") == "meta":
            continue
        deps = row.get("deps", [])
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

    # ---- audit queue cross-check: root must not be in the queue (it
    # has a terminal-audit conditional verdict, not a pending row) ----
    if QUEUE.exists():
        queue_data = json.loads(QUEUE.read_text())
        queue_entries = queue_data.get("queue", [])
        root_in_queue = any(
            e.get("claim_id") == ROOT_CID for e in queue_entries
        )
        check(
            f"root not in audit queue: {ROOT_CID}",
            not root_in_queue,
            "root has terminal_audit verdict; should not be re-queued",
        )

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
