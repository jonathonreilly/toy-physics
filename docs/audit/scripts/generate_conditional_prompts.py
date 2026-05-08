#!/usr/bin/env python3
"""Append per-row physics-loop prompts for the auditor-written
audited_conditional cohort to docs/audit/MISSING_DERIVATION_PROMPTS.md.

The existing prompts file covers:
  audited_renaming | audited_failed | audited_numerical_match | open_gate

The audited_conditional cohort was missing — the autonomous
science_fix_loop.py had no queue for it. This script extends coverage
to the three auditor-written conditional repair classes whose verdicts
contain a concrete repair target:

  audited_conditional_runner_artifact_issue   (12 auditor-written rows)
  audited_conditional_scope_too_broad         (6 auditor-written rows)
  audited_conditional_missing_bridge_theorem  (58 auditor-written rows)

Synthesized backfilled rows (from backfill_repair_class.py) are
intentionally excluded — their repair-class prefix was inferred from
boilerplate verdict_rationale, not stated by an independent auditor.
Those rows need re-audit, not autonomous derivation work.

Usage:
  # idempotent: rewrites the three conditional sections at the file end
  python3 docs/audit/scripts/generate_conditional_prompts.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
LOG = REPO_ROOT / "docs" / "audit" / "data" / "repair_class_backfill_log.json"
PROMPTS = REPO_ROOT / "docs" / "audit" / "MISSING_DERIVATION_PROMPTS.md"

CONDITIONAL_SECTIONS = [
    (
        "audited_conditional_runner_artifact_issue",
        "Auditor judged the load-bearing step blocked by a runner, log, classifier, threshold, import, or pass/fail accounting problem. To close: repair the runner per the auditor's repair_target sentence and rerun, or replace the runner with a self-contained certificate.",
    ),
    (
        "audited_conditional_scope_too_broad",
        "Auditor judged that a clean bounded core exists inside a claim whose current scope includes an unclosed extension. To close: split the clean bounded core out as its own retained-grade claim and demote the extension to bounded or open scope.",
    ),
    (
        "audited_conditional_missing_bridge_theorem",
        "Auditor judged that the chain needs a new theorem for a physical carrier, readout, unit map, boundary condition, sector choice, normalization, or observable bridge. To close: derive the missing bridge from retained primitives so the audited claim no longer asserts it.",
    ),
]


def load_synthesized_ids() -> set[str]:
    if not LOG.exists():
        return set()
    log = json.loads(LOG.read_text())
    return {entry["claim_id"] for entry in log}


def collect_rows(rows: dict[str, dict], synthesized: set[str]) -> dict[str, list[dict]]:
    by_class: dict[str, list[dict]] = {h: [] for h, _ in CONDITIONAL_SECTIONS}
    map_class = {
        "runner_artifact_issue": "audited_conditional_runner_artifact_issue",
        "scope_too_broad": "audited_conditional_scope_too_broad",
        "missing_bridge_theorem": "audited_conditional_missing_bridge_theorem",
    }
    for cid, row in rows.items():
        if row.get("audit_status") != "audited_conditional":
            continue
        if cid in synthesized:
            continue
        notes = (row.get("notes_for_re_audit_if_any") or "").strip().lower()
        for prefix, section in map_class.items():
            if notes.startswith(prefix):
                by_class[section].append({"cid": cid, "row": row})
                break
    for section in by_class:
        by_class[section].sort(
            key=lambda r: -(r["row"].get("transitive_descendants") or 0)
        )
    return by_class


def render_prompt(cid: str, row: dict) -> str:
    note_path = row.get("note_path") or ""
    descendants = row.get("transitive_descendants") or 0
    cls = row.get("load_bearing_step_class") or "?"
    audit_status = row.get("audit_status") or ""
    claim_type = row.get("claim_type") or ""
    claim_scope = (row.get("claim_scope") or "").strip()
    rationale = (row.get("verdict_rationale") or "").strip()
    load_bearing = (row.get("load_bearing_step") or "").strip()
    notes = (row.get("notes_for_re_audit_if_any") or "").strip()

    block = []
    block.append(f"### `{cid}`")
    block.append("")
    block.append(
        f"**Note:** [{note_path}]({note_path})  |  **Descendants:** {descendants}  |  **Class:** {cls}"
    )
    block.append("")
    block.append("```")
    block.append(f"Use the physics-loop skill to close the conditional audit on {note_path}.")
    block.append("")
    block.append("Current audit state:")
    block.append(f"- audit_status: {audit_status}")
    block.append(f"- claim_type: {claim_type}")
    block.append(f"- load_bearing_step_class: {cls}")
    block.append(f"- claim_scope: {claim_scope}")
    block.append("")
    block.append("Auditor's verdict_rationale:")
    block.append(rationale)
    block.append("")
    block.append("Auditor-quoted load-bearing step:")
    block.append(load_bearing)
    block.append("")
    block.append("Auditor's repair target (canonical class + action):")
    block.append(notes)
    block.append("")
    block.append(
        "Goal: close the chain so a re-audit of this same note can land"
    )
    block.append(
        "audited_clean at retained-grade. Use the physics-loop skill to iterate."
    )
    block.append(
        "Do not over-prescribe approach — explore the framework, let the skill"
    )
    block.append("drive.")
    block.append("```")
    block.append("")
    return "\n".join(block)


def render_section(title: str, description: str, rows: list[dict]) -> str:
    parts = []
    parts.append(f"## {title}")
    parts.append("")
    parts.append(description)
    parts.append("")
    parts.append(f"_{len(rows)} rows in this category._")
    parts.append("")
    parts.append("")
    for r in rows:
        parts.append(render_prompt(r["cid"], r["row"]))
        parts.append("")
    return "\n".join(parts)


def replace_or_append_sections(prompts_text: str, new_sections_text: str) -> str:
    """Replace the conditional sections if present; otherwise append."""
    marker_first = "## audited_conditional_runner_artifact_issue"
    if marker_first in prompts_text:
        idx = prompts_text.find(marker_first)
        return prompts_text[:idx].rstrip() + "\n\n" + new_sections_text.lstrip()
    return prompts_text.rstrip() + "\n\n" + new_sections_text.lstrip()


def main() -> int:
    ledger = json.loads(LEDGER.read_text())
    rows = ledger["rows"]
    synthesized = load_synthesized_ids()

    by_class = collect_rows(rows, synthesized)

    section_texts = []
    for header, description in CONDITIONAL_SECTIONS:
        section_texts.append(render_section(header, description, by_class[header]))
    new_blob = "\n".join(section_texts).rstrip() + "\n"

    prompts_text = PROMPTS.read_text()
    updated = replace_or_append_sections(prompts_text, new_blob)
    PROMPTS.write_text(updated)

    print("generate_conditional_prompts: wrote", PROMPTS)
    for header, _ in CONDITIONAL_SECTIONS:
        print(f"  {header}: {len(by_class[header])} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
