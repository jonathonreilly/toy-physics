#!/usr/bin/env python3
"""Seed the audit ledger from the citation graph.

For every node in citation_graph.json, ensure an audit ledger row exists
with audit_status=unaudited as the default. If a row already exists,
preserve its audit fields but update graph metadata and dependencies. The
audit-owned `claim_type` drives retained/no-go/bounded classification. If
the source note's hash has changed since the last
audit, reset audit_status to unaudited and archive the prior verdict in
previous_audits. Terminal failed rows whose source notes moved to
archive_unlanded/ are preserved as negative-result history even though
they are no longer active graph nodes.

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
    # Non-claim planning/session/status artifacts identified during
    # unknown-row triage.
    "docs/EXPERIMENT_BACKMATCH_QUERY_PACK_NOTE.md",
    "docs/GRAPH_DIRAC_REQUIREMENTS_2026-04-10.md",
    "docs/GRAVITY_DESIGN_BLUEPRINT.md",
    "docs/KOIDE_A1_CLOSURE_RECOMMENDATION_2026-04-22.md",
    "docs/KOIDE_CLOSURE_ATLAS_ISSUES_FLAGGED.md",
    "docs/PHYSICS_CRITIC_TRACKER.md",
    "docs/PHYSICS_FIRST_ATTACK_PLAN.md",
    "docs/PHYSICS_QA_TRACKER.md",
    "docs/REOPENED_LANE_CHECKLIST.md",
    "docs/REPO_SUBMISSION_CONSOLIDATION_PLAN_2026-04-12.md",
    "docs/SCALING_TARGETS.md",
    "docs/SESSION_SUMMARY_*.md",
    "docs/SESSION_SYNTHESIS_*.md",
    "docs/WRITING_VOICE_GUIDE_2026-04-25.md",
    "docs/YT_RETENTION_LANDING_READINESS_2026-04-18.md",
    "docs/YT_RETENTION_MASTER_MANIFEST_2026-04-18.md",
    ".claude/**",
)

# Exact source paths that must remain in the ledger even if they match a
# broad infrastructure pattern.
NEVER_GATE_SOURCE_PATHS = {
    "docs/ai_methodology/raw/prompts_session_ebae4639_jonreilly.md",
}

# Top-level campaign/infrastructure notes that are intentionally kept as
# ledger metadata instead of dropped from the graph or treated as claims.
META_SOURCE_PATTERNS = (
    "docs/AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_*.md",
    "docs/PHYSICAL_LATTICE_NECESSITY_DEP_DECLARATION_AUDIT_NOTE_*.md",
    "docs/SCALAR_SELECTOR_FULL_STACK_RECOVERY_NOTE_*.md",
)

CLAIM_TYPES = {
    "positive_theorem",
    "bounded_theorem",
    "no_go",
    "open_gate",
    "decoration",
    "meta",
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
    "claim_type": None,
    "claim_scope": None,
    "claim_type_provenance": None,
    "claim_type_last_reviewed": None,
    "notes_for_re_audit_if_any": None,
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

    if prior is not None:
        audit_status = prior.get("audit_status")
        if audit_status and audit_status != "unaudited":
            return False
        # This cleanup targets unknown infra rows; keep rows that already
        # contribute to a different effective-status bucket.
        effective_status = prior.get("effective_status")
        if effective_status and effective_status != "unknown":
            return False

    return True


def should_preserve_archived_failed_row(row: dict) -> bool:
    """Keep terminal failed audit rows for archived notes out of docs/."""
    if row.get("audit_status") != "audited_failed":
        return False
    note_path = row.get("note_path") or ""
    if not note_path.startswith("archive_unlanded/"):
        return False
    return (REPO_ROOT / note_path).exists()


def default_claim_type_for(node: dict) -> tuple[str, str]:
    """Return a provisional claim type for legacy rows.

    The auditor owns the final value. This backfill exists so the new
    propagation rule is total over old ledger rows before their next audit.
    """
    path = node.get("path") or ""
    if any(fnmatchcase(path, pattern) for pattern in META_SOURCE_PATTERNS):
        return "meta", "backfilled_from_path"

    hint = node.get("claim_type_author_hint") or node.get("claim_type_seed_hint")
    if hint in CLAIM_TYPES:
        provenance = "author_hint" if node.get("claim_type_author_hint") else "migration_hint"
        return hint, provenance

    if path.startswith(("docs/repo/", "docs/work_history/", "docs/lanes/", "docs/publication/")):
        return "meta", "backfilled_from_path"

    return "positive_theorem", "default_positive_theorem"


def backfill_scope(row: dict) -> str | None:
    if row.get("audit_status") in {None, "unaudited", "audit_in_progress"}:
        return None
    return (
        "Legacy audit row backfilled during scope-aware classification migration; "
        "re-audit may narrow this scope."
    )


def needs_critical_type_reaudit(row: dict, prior: dict | None) -> bool:
    if prior is None:
        return False
    if prior.get("claim_type") in CLAIM_TYPES:
        return False
    if prior.get("audit_status") in {None, "unaudited", "audit_in_progress"}:
        return False
    return (prior.get("criticality") or row.get("criticality")) == "critical"


def apply_claim_type_defaults(row: dict, node: dict, prior: dict | None) -> None:
    row.pop("current_status", None)
    row.pop("current_status_raw", None)
    row["claim_type_author_hint_raw"] = node.get("claim_type_author_hint_raw")
    row["claim_type_author_hint"] = node.get("claim_type_author_hint")

    audited_type = row.get("claim_type")
    provenance = row.get("claim_type_provenance")
    if audited_type in CLAIM_TYPES and provenance == "audited":
        return

    if row.get("audit_status") == "audited_decoration" and audited_type != "decoration":
        row["claim_type"] = "decoration"
        row["claim_type_provenance"] = "backfilled_pending_reaudit"
        row["claim_scope"] = row.get("claim_scope") or backfill_scope(row)
        return

    if audited_type not in CLAIM_TYPES:
        claim_type, inferred_provenance = default_claim_type_for(node)
        row["claim_type"] = claim_type
        row["claim_type_provenance"] = inferred_provenance
        if needs_critical_type_reaudit(row, prior):
            row["claim_type_provenance"] = "backfilled_pending_reaudit"
        if not row.get("claim_scope"):
            row["claim_scope"] = backfill_scope(row)
    elif provenance in {None, "author_hint", "backfilled", "backfilled_from_status", "backfilled_from_path", "migration_hint", "default_positive_theorem"}:
        claim_type, inferred_provenance = default_claim_type_for(node)
        row["claim_type"] = claim_type
        row["claim_type_provenance"] = inferred_provenance


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
    archived_failed_rows = {
        cid: dict(row)
        for cid, row in existing_rows.items()
        if cid not in graph["nodes"] and should_preserve_archived_failed_row(row)
    }

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
                "claim_type_author_hint_raw": node.get("claim_type_author_hint_raw"),
                "claim_type_author_hint": node.get("claim_type_author_hint"),
                "runner_path": node["runner_path"],
                "deps": deps,
                "note_hash": node["note_hash"],
                "previous_audits": [],
            }
            for k, v in EMPTY_AUDIT.items():
                row[k] = v if not isinstance(v, (list, dict)) else (list(v) if isinstance(v, list) else dict(v))
            apply_claim_type_defaults(row, node, prior)
            seeded += 1
        else:
            row = dict(prior)
            row["claim_id"] = cid
            row["note_path"] = node["path"]
            row["title"] = node["title"]
            row["claim_type_author_hint_raw"] = node.get("claim_type_author_hint_raw")
            row["claim_type_author_hint"] = node.get("claim_type_author_hint")
            row["runner_path"] = node["runner_path"]
            row["deps"] = deps
            if prior.get("note_hash") != node["note_hash"] and prior.get("audit_status") in {None, "unaudited"}:
                row["note_hash"] = node["note_hash"]
                preserved += 1
            elif prior.get("note_hash") != node["note_hash"]:
                row = archive_prior_audit(row)
                row["note_hash"] = node["note_hash"]
                re_audit_required += 1
            else:
                preserved += 1
            apply_claim_type_defaults(row, node, prior)
        out_rows[cid] = row

    for cid, row in archived_failed_rows.items():
        row.pop("current_status", None)
        row.pop("current_status_raw", None)
        if row.get("claim_type") not in CLAIM_TYPES:
            row["claim_type"] = "no_go"
            row["claim_type_provenance"] = "backfilled_from_archived_failed"
            row["claim_scope"] = row.get("claim_scope") or backfill_scope(row)
        out_rows[cid] = row

    # Drop ledger rows whose source note no longer exists, plus rows
    # intentionally gated out as non-claim infrastructure.
    dropped = [
        cid
        for cid in existing_rows
        if cid not in included_cids and cid not in archived_failed_rows
    ]
    missing = [
        cid
        for cid in existing_rows
        if cid not in graph["nodes"] and cid not in archived_failed_rows
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "stats": {
            "row_count": len(out_rows),
            "seeded_new": seeded,
            "preserved_existing": preserved,
            "preserved_archived_failed": len(archived_failed_rows),
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
    print(f"  preserved archived failed: {s['preserved_archived_failed']}")
    print(f"  re-audit required (hash changed): {s['re_audit_required']}")
    print(f"  dropped (note removed): {s['dropped_missing_notes']}")
    print(f"  dropped (gated source): {s['dropped_gated_sources']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
