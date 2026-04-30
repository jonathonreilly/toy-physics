#!/usr/bin/env python3
"""Seed the audit ledger from the citation graph.

For every node in citation_graph.json, ensure an audit ledger row exists
with audit_status=unaudited as the default. If a row already exists,
preserve its audit fields but update the dependency list and current_status
from the graph. If the source note's hash has changed since the last
audit, reset audit_status to unaudited and archive the prior verdict in
previous_audits.

Writes docs/audit/data/audit_ledger.json.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from fnmatch import fnmatchcase
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
GRAPH_PATH = DATA_DIR / "citation_graph.json"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"

# Source paths that are documentation or agent infrastructure, not
# auditable claim notes. These are candidates for exclusion; rows are
# only dropped when the safety checks below confirm they are unaudited
# unknowns.
EXCLUDED_SOURCE_PATTERNS = (
    "docs/ai_methodology/*.md",
    "docs/ai_methodology/raw/**",
    "docs/ai_methodology/skills/**",
    "docs/lanes/**",
    "docs/publication/**",
    "docs/repo/**",
    "docs/work_history/**",
    "docs/ARCHITECTURE_OPTIONS.md",
    "docs/BRANCH_SUMMARY_DISTRACTED_NAPIER.md",
    "docs/BREAKTHROUGH_DIRECTION_MEMO_2026-04-10.md",
    "docs/CLAUDE_BRANCH_RETAINABILITY_NOTE.md",
    "docs/INTEREST_MAP.md",
    "docs/LITERATURE_POSITIONING_NOTE.md",
    "docs/MOONSHOT_DIAMOND_SENSOR_BRAINSTORM_NOTE.md",
    "docs/MOONSHOT_DIAMOND_SENSOR_TECH_NOTE.md",
    "docs/MOONSHOT_FAILURE_AUDIT_NOTE.md",
    "docs/MOONSHOT_FRONTIER_BRAINSTORM_NOTE.md",
    "docs/MOONSHOT_FRONTIER_BRAINSTORM_V2_NOTE.md",
    "docs/MOONSHOT_FRONTIER_PORTFOLIO_NOTE.md",
    "docs/MOONSHOT_HONEST_REVIEW_2026-04-09.md",
    "docs/MOONSHOT_MECHANISM_NEXT_NOTE.md",
    "docs/MOONSHOT_SCIENCE_NEXT_NOTE.md",
    "docs/MOONSHOT_SELF_GRAVITY_BRAINSTORM_NOTE.md",
    "docs/MOONSHOT_TOP20_FRONTIERS.md",
    "docs/NATURE_DISCOVERY_DIRECTIONS_2026-04-11.md",
    "docs/NATURE_RANKED_DIRECTIONS_2026-04-11.md",
    "docs/NEXT_CHUNK_RECOMMENDATION.md",
    "docs/PAPER_OUTLINE_2026-04-12.md",
    ".claude/**",
)

# Exact source paths that must remain in the ledger even if they match a
# broad infrastructure pattern. This protects rows that already have a
# real audit verdict or a retained/proposed tier.
NEVER_GATE_SOURCE_PATHS = {
    "docs/ai_methodology/raw/prompts_session_ebae4639_jonreilly.md",
}

PROTECTED_CURRENT_STATUSES = {
    "retained",
    "promoted",
    "proposed_retained",
    "proposed_promoted",
}

# Default empty audit fields applied to a freshly seeded row.
EMPTY_AUDIT = {
    "audit_status": "unaudited",
    "audit_date": None,
    "auditor": None,
    "auditor_family": None,
    "independence": None,
    "load_bearing_step": None,
    "load_bearing_step_class": None,
    "chain_closes": None,
    "chain_closure_explanation": None,
    "verdict_rationale": None,
    "open_dependency_paths": [],
    "decoration_parent_claim_id": None,
    "auditor_confidence": None,
    "runner_check_breakdown": {"A": 0, "B": 0, "C": 0, "D": 0, "total_pass": 0},
    "blocker": None,
}

# Audit fields that are preserved across re-seeds when the note hash is
# unchanged. If the hash changes, these are archived and reset.
AUDIT_FIELDS = list(EMPTY_AUDIT.keys())


def is_excluded_source_path(path: str) -> bool:
    return any(fnmatchcase(path, pattern) for pattern in EXCLUDED_SOURCE_PATTERNS)


def should_gate_node(node: dict, prior: dict | None) -> bool:
    """Return True when a graph node should not become a ledger row."""
    path = node["path"]
    if not is_excluded_source_path(path):
        return False
    if path in NEVER_GATE_SOURCE_PATHS:
        return False

    current_statuses = {node.get("current_status")}
    if prior is not None:
        current_statuses.add(prior.get("current_status"))
    if current_statuses & PROTECTED_CURRENT_STATUSES:
        return False

    if prior is not None:
        audit_status = prior.get("audit_status")
        if audit_status and audit_status != "unaudited":
            return False
        # This cleanup targets unknown infra rows; keep rows that already
        # contribute to a different effective-status bucket.
        effective_status = prior.get("effective_status")
        if effective_status and effective_status != "unknown":
            return False

    return node.get("current_status") == "unknown"


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def archive_prior_audit(row: dict) -> dict:
    """Snapshot the audit fields into previous_audits and return the cleared row."""
    prior = {k: row.get(k) for k in AUDIT_FIELDS}
    prior["archived_at"] = datetime.now(timezone.utc).isoformat()
    prior["archived_for_note_hash"] = row.get("note_hash")
    history = list(row.get("previous_audits", []))
    history.append(prior)
    new_row = dict(row)
    new_row["previous_audits"] = history
    for k, v in EMPTY_AUDIT.items():
        new_row[k] = v if not isinstance(v, (list, dict)) else (list(v) if isinstance(v, list) else dict(v))
    return new_row


def seed() -> dict:
    graph = load_json(GRAPH_PATH, None)
    if graph is None:
        raise SystemExit(
            "citation_graph.json missing; run build_citation_graph.py first"
        )

    existing = load_json(LEDGER_PATH, {"rows": {}})
    existing_rows: dict[str, dict] = existing.get("rows", {})

    out_rows: dict[str, dict] = {}
    seeded = 0
    preserved = 0
    re_audit_required = 0

    included_cids = {
        cid
        for cid, node in graph["nodes"].items()
        if not should_gate_node(node, existing_rows.get(cid))
    }
    gated = [cid for cid in graph["nodes"] if cid not in included_cids]

    for cid, node in graph["nodes"].items():
        if cid not in included_cids:
            continue

        deps = [dep for dep in node["deps"] if dep in included_cids]
        prior = existing_rows.get(cid)
        if prior is None:
            row = {
                "claim_id": cid,
                "note_path": node["path"],
                "title": node["title"],
                "current_status": node["current_status"],
                "current_status_raw": node["current_status_raw"],
                "runner_path": node["runner_path"],
                "deps": deps,
                "note_hash": node["note_hash"],
                "previous_audits": [],
            }
            for k, v in EMPTY_AUDIT.items():
                row[k] = v if not isinstance(v, (list, dict)) else (list(v) if isinstance(v, list) else dict(v))
            seeded += 1
        else:
            row = dict(prior)
            row["claim_id"] = cid
            row["note_path"] = node["path"]
            row["title"] = node["title"]
            row["current_status"] = node["current_status"]
            row["current_status_raw"] = node["current_status_raw"]
            row["runner_path"] = node["runner_path"]
            row["deps"] = deps
            if prior.get("note_hash") != node["note_hash"]:
                row = archive_prior_audit(row)
                row["note_hash"] = node["note_hash"]
                re_audit_required += 1
            else:
                preserved += 1
        out_rows[cid] = row

    # Drop ledger rows whose source note no longer exists, plus rows
    # intentionally gated out as non-claim infrastructure.
    dropped = [cid for cid in existing_rows if cid not in included_cids]
    missing = [cid for cid in existing_rows if cid not in graph["nodes"]]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "stats": {
            "row_count": len(out_rows),
            "seeded_new": seeded,
            "preserved_existing": preserved,
            "re_audit_required": re_audit_required,
            "dropped_missing_notes": len(missing),
            "dropped_gated_sources": len(gated),
            "dropped_total": len(dropped),
        },
        "rows": out_rows,
    }


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ledger = seed()
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    s = ledger["stats"]
    print(f"Wrote {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"  rows: {s['row_count']}")
    print(f"  newly seeded: {s['seeded_new']}")
    print(f"  preserved (audit kept): {s['preserved_existing']}")
    print(f"  re-audit required (hash changed): {s['re_audit_required']}")
    print(f"  dropped (note removed): {s['dropped_missing_notes']}")
    print(f"  dropped (gated source): {s['dropped_gated_sources']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
