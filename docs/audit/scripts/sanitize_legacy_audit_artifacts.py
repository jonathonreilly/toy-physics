#!/usr/bin/env python3
"""Remove legacy author-status residue from generated audit artifacts.

This is a deterministic cleanup pass for the scope-aware audit schema. It
removes deprecated ledger keys and rewrites historical audit prose away from
old author-tier vocabulary. It also normalizes legacy decoration-parent ids
that were accidentally stored as note paths. It does not change audit verdicts.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"

DEPRECATED_KEYS = {"current_status", "current_status_raw"}

EXACT_STATUS_VALUE_MAP = {
    "promoted": "retained",
    "proposed_retained": "unaudited",
    "proposed_promoted": "unaudited",
    "proposed_no_go": "unaudited",
    "bounded": "unaudited",
    "support": "unaudited",
    "open": "open_gate",
    "unknown": "unaudited",
}

TEXT_REPLACEMENTS = (
    ("current_status", "source status"),
    ("proposed_retained", "candidate retained-grade"),
    ("proposed_promoted", "candidate promoted-grade"),
    ("proposed_no_go", "candidate no-go"),
    ("proposed-retained", "candidate retained-grade"),
    ("proposed-promoted", "candidate promoted-grade"),
)


def sanitize_string(value: str) -> str:
    mapped = EXACT_STATUS_VALUE_MAP.get(value)
    if mapped is not None:
        return mapped
    out = value
    for old, new in TEXT_REPLACEMENTS:
        out = out.replace(old, new)
    return out


def sanitize_obj(value):
    if isinstance(value, dict):
        return {
            k: sanitize_obj(v)
            for k, v in value.items()
            if k not in DEPRECATED_KEYS
        }
    if isinstance(value, list):
        return [sanitize_obj(v) for v in value]
    if isinstance(value, str):
        return sanitize_string(value)
    return value


def _add_alias(aliases: dict[str, str | None], alias: str, claim_id: str) -> None:
    if not alias:
        return
    previous = aliases.get(alias)
    if previous is None and alias not in aliases:
        aliases[alias] = claim_id
    elif previous != claim_id:
        aliases[alias] = None


def note_path_aliases(note_path: str) -> set[str]:
    normalized = note_path.lstrip("./")
    aliases = {note_path, normalized, f"./{normalized}"}
    basename = Path(normalized).name
    if basename:
        aliases.add(basename)
    return aliases


def canonicalize_decoration_parent_ids(ledger: dict) -> None:
    """Convert legacy decoration parent note paths to canonical claim ids."""
    rows = ledger.get("rows")
    if not isinstance(rows, dict):
        return

    note_to_claim: dict[str, str | None] = {}
    for claim_id, row in rows.items():
        if not isinstance(row, dict):
            continue
        note_path = row.get("note_path")
        if not isinstance(note_path, str):
            continue
        for alias in note_path_aliases(note_path):
            _add_alias(note_to_claim, alias, claim_id)

    for row in rows.values():
        if not isinstance(row, dict):
            continue
        parent = row.get("decoration_parent_claim_id")
        if not isinstance(parent, str) or not parent or parent in rows:
            continue
        normalized = parent.lstrip("./")
        candidates = [parent, normalized, f"./{normalized}", Path(normalized).name]
        for candidate in candidates:
            replacement = note_to_claim.get(candidate)
            if replacement:
                row["decoration_parent_claim_id"] = replacement
                break


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing; run seed_audit_ledger.py first")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    sanitized = sanitize_obj(ledger)
    canonicalize_decoration_parent_ids(sanitized)
    LEDGER_PATH.write_text(json.dumps(sanitized, indent=2, sort_keys=True) + "\n")
    print(f"Sanitized {LEDGER_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
