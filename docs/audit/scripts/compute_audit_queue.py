#!/usr/bin/env python3
"""Produce the next-up audit queue.

Reads the ledger and writes a sorted list of claims awaiting audit. The
queue is the input that an auditor (Codex GPT-5.5 by default) pulls from.

Sorting key (descending priority):
  1. criticality (critical -> high -> medium -> leaf)
  2. all deps already at retained-grade ('ready')
     ahead of those waiting on an upstream audit
  3. transitive_descendants
  4. load_bearing_score

Each queue entry includes everything the auditor needs to construct the
prompt via AUDIT_AGENT_PROMPT_TEMPLATE.md without further repo access.

Writes:
  - data/audit_queue.json: full queue, machine-readable
  - AUDIT_QUEUE.md: top-50 human-readable view
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
QUEUE_JSON = DATA_DIR / "audit_queue.json"
QUEUE_MD = REPO_ROOT / "docs" / "audit" / "AUDIT_QUEUE.md"

CRITICALITY_RANK = {"critical": 3, "high": 2, "medium": 1, "leaf": 0}

# Effective statuses considered stable inputs for an auditor.
READY_DEP_STATUSES = {
    "retained",
    "retained_no_go",
    "retained_bounded",
    "meta",
}


def dep_ready(status: str | None) -> bool:
    if status in READY_DEP_STATUSES:
        return True
    return bool(status and status.startswith("decoration_under_"))


def is_ready(row: dict, rows: dict[str, dict]) -> bool:
    for d in row.get("deps", []):
        d_eff = rows.get(d, {}).get("effective_status") or "unknown"
        if not dep_ready(d_eff):
            return False
    return True


def needs_audit(row: dict) -> tuple[bool, str]:
    if row.get("claim_type") == "meta":
        return False, "metadata"
    audit_status = row.get("audit_status", "unaudited")
    if audit_status in {"unaudited", "audit_in_progress"}:
        return True, audit_status
    if row.get("claim_type_provenance") == "backfilled_pending_reaudit":
        return True, "claim_type_backfill_reaudit"
    return False, "not_pending"


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    pending: list[dict] = []
    for cid, row in rows.items():
        include, queue_reason = needs_audit(row)
        if not include:
            continue
        a = row.get("audit_status", "unaudited")
        criticality = row.get("criticality") or "leaf"
        ready = is_ready(row, rows)
        entry = {
            "claim_id": cid,
            "note_path": row.get("note_path"),
            "claim_type": row.get("claim_type"),
            "claim_scope": row.get("claim_scope"),
            "claim_type_provenance": row.get("claim_type_provenance"),
            "audit_status": a,
            "effective_status": row.get("effective_status"),
            "queue_reason": queue_reason,
            "criticality": criticality,
            "criticality_rank": CRITICALITY_RANK.get(criticality, 0),
            "transitive_descendants": row.get("transitive_descendants", 0),
            "direct_in_degree": row.get("direct_in_degree", 0),
            "load_bearing_score": row.get("load_bearing_score", 0.0),
            "runner_path": row.get("runner_path"),
            "deps": list(row.get("deps", [])),
            "ready": ready,
            "blocker": row.get("blocker"),
            "cross_confirmation_status": (row.get("cross_confirmation") or {}).get("status"),
            "audit_independence_required": (
                "fresh_context_or_stronger_with_cross_confirmation"
                if criticality == "critical"
                else "fresh_context_or_stronger"
                if criticality == "high"
                else "any_non_self"
            ),
        }
        pending.append(entry)

    pending.sort(
        key=lambda e: (
            -e["criticality_rank"],
            0 if e["ready"] else 1,
            -e["transitive_descendants"],
            -e["load_bearing_score"],
        )
    )

    queue = {
        "total_pending": len(pending),
        "ready_count": sum(1 for e in pending if e["ready"]),
        "by_criticality": {
            c: sum(1 for e in pending if e["criticality"] == c)
            for c in ("critical", "high", "medium", "leaf")
        },
        "queue": pending,
    }
    QUEUE_JSON.write_text(json.dumps(queue, indent=2, sort_keys=True) + "\n")

    # Top-50 human view.
    top = pending[:50]
    md_lines = [
        "# Audit Queue",
        "",
        f"**Total pending:** {queue['total_pending']}",
        f"**Ready (all deps already at retained-grade or metadata tiers):** {queue['ready_count']}",
        "",
        "By criticality:",
    ]
    for c in ("critical", "high", "medium", "leaf"):
        md_lines.append(f"- `{c}`: {queue['by_criticality'][c]}")
    md_lines.append("")
    md_lines.append(
        "Auditor (Codex GPT-5.5 by default) should pull from the top of "
        "this list. Critical claims require cross-confirmation by a "
        "second independent clean-room auditor before `audited_clean` lands."
    )
    md_lines.append("")
    md_lines.append("## Top 50")
    md_lines.append("")
    md_lines.append(
        "| # | claim_id | claim_type | reason | criticality | desc | score | ready | indep required | runner |"
    )
    md_lines.append("|---:|---|---|---|---|---:|---:|:---:|---|---|")
    for i, e in enumerate(top, 1):
        md_lines.append(
            f"| {i} | `{e['claim_id']}` | {e.get('claim_type') or '-'} | "
            f"{e['queue_reason']} | {e['criticality']} | "
            f"{e['transitive_descendants']} | "
            f"{e['load_bearing_score']:.2f} | "
            f"{'Y' if e['ready'] else ''} | "
            f"{e['audit_independence_required']} | "
            f"{'`' + e['runner_path'] + '`' if e['runner_path'] else '-'} |"
        )
    md_lines.append("")
    md_lines.append("Full queue lives in `data/audit_queue.json`.")
    QUEUE_MD.write_text("\n".join(md_lines) + "\n")

    print(f"Wrote {QUEUE_JSON.relative_to(REPO_ROOT)}")
    print(f"Wrote {QUEUE_MD.relative_to(REPO_ROOT)}")
    print(f"  total pending: {queue['total_pending']}")
    print(f"  ready: {queue['ready_count']}")
    print(f"  by criticality: {queue['by_criticality']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
