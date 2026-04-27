#!/usr/bin/env python3
"""Mechanical relabel of source-note Status lines.

Rewrites the `**Status:** ...` line in every claim note from the legacy
author-declared tier vocabulary to the audit-lane's propose / ratify
vocabulary:

  retained        ->  proposed_retained
  promoted        ->  proposed_promoted
  flagship closed ->  proposed_retained   (was flagship-tagged; the audit
                                           lane does not propagate flagship
                                           status, so flagship-closed
                                           collapses to proposed_retained)
  not retained    ->  outside audit-ratified tier
  not promoted    ->  outside audit-ratified tier

Only the `**Status:**` (or `Status:`) line is touched. Body text is left
untouched, because the words "retained", "promoted", and "flagship"
appear throughout normal prose ("the retained CKM atlas", "promoted
quantitative section", etc.) and rewriting those would produce
nonsense.

The script is idempotent: rerunning it on already-relabeled notes is a
no-op.

Usage:
  python3 relabel_status_lines.py --dry-run    # print what would change
  python3 relabel_status_lines.py              # apply changes

After applying, run the full audit pipeline:
  bash docs/audit/scripts/run_pipeline.sh

The pipeline's seed_audit_ledger.py will detect note-hash drift on every
relabeled note and reset audit_status to unaudited (which is correct:
the relabel is a meaningful change to the source surface).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DOCS_DIR = REPO_ROOT / "docs"
SKIP_PREFIXES = ("audit/",)

# Match the entire Status line so we can rewrite only its content.
STATUS_LINE_RE = re.compile(
    r"^(?P<prefix>\s*(?:\*\*Status:?\*\*|Status:)\s*)(?P<rest>.+)$",
    re.IGNORECASE | re.MULTILINE,
)

# Inside a Status line, the legacy vocabulary mapped to new vocabulary.
# Order matters: longer / more specific matches first so we don't double-
# rewrite.
STATUS_REWRITES: list[tuple[re.Pattern[str], str]] = [
    # Negated ratified-tier language should not become
    # "not proposed_retained"; use a canonical negative phrase that does
    # not trip the post-relabel strict lint.
    (re.compile(r"\bnot\s+promoted\s+to\s+flagship\s+core\b", re.IGNORECASE), "outside flagship core"),
    (re.compile(r"\bnot\s+retained\b", re.IGNORECASE), "outside audit-ratified tier"),
    (re.compile(r"\bnot\s+promoted\b", re.IGNORECASE), "outside audit-ratified tier"),
    # "flagship closed package" -> "proposed_retained" (with annotation)
    (re.compile(r"\bflagship\s+closed\b", re.IGNORECASE), "proposed_retained"),
    # "retained" but not already part of "proposed_retained"
    (re.compile(r"(?<!proposed_)\bretained\b", re.IGNORECASE), "proposed_retained"),
    # "promoted" but not already part of "proposed_promoted"
    (re.compile(r"(?<!proposed_)\bpromoted\b", re.IGNORECASE), "proposed_promoted"),
]


def rewrite_status_text(rest: str) -> str:
    """Apply the rewrite rules to the content of a Status line."""
    out = rest
    for pattern, replacement in STATUS_REWRITES:
        out = pattern.sub(replacement, out)
    return out


def rewrite_note(body: str) -> tuple[str, list[tuple[str, str]]]:
    """Rewrite the Status line(s) in a note body.

    Returns the new body and a list of (old_line, new_line) tuples for
    every Status line that changed.
    """
    changes: list[tuple[str, str]] = []

    def replace(m: re.Match[str]) -> str:
        prefix = m.group("prefix")
        rest = m.group("rest")
        new_rest = rewrite_status_text(rest)
        old_full = prefix + rest
        new_full = prefix + new_rest
        if old_full != new_full:
            changes.append((old_full.rstrip(), new_full.rstrip()))
        return new_full

    new_body = STATUS_LINE_RE.sub(replace, body)
    return new_body, changes


def discover_notes() -> list[Path]:
    notes = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        rel = path.relative_to(DOCS_DIR)
        if any(rel.as_posix().startswith(p) for p in SKIP_PREFIXES):
            continue
        notes.append(path)
    return notes


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would change without modifying files.")
    p.add_argument("--quiet", action="store_true",
                   help="Don't print per-file changes (just totals).")
    args = p.parse_args()

    notes = discover_notes()
    n_changed = 0
    n_status_lines_changed = 0
    rewritten_notes: list[Path] = []

    for note_path in notes:
        body = note_path.read_text(encoding="utf-8", errors="replace")
        new_body, changes = rewrite_note(body)
        if not changes:
            continue
        n_changed += 1
        n_status_lines_changed += len(changes)
        rewritten_notes.append(note_path)
        if not args.quiet:
            rel = note_path.relative_to(REPO_ROOT).as_posix()
            for old, new in changes:
                print(f"--- {rel}")
                print(f"-{old}")
                print(f"+{new}")
        if not args.dry_run:
            note_path.write_text(new_body, encoding="utf-8")

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    verb = "would be changed" if args.dry_run else "changed"
    print(f"\n{mode}: {n_changed} note(s) {verb}, "
          f"{n_status_lines_changed} Status line(s) rewritten.")
    if args.dry_run and n_changed:
        print("Re-run without --dry-run to apply.")
    if not args.dry_run and n_changed:
        print("Next: run the full audit pipeline so the ledger picks up")
        print("the new note hashes and re-seeds:")
        print("  bash docs/audit/scripts/run_pipeline.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
