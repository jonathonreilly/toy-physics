#!/usr/bin/env python3
"""Backfill the canonical repair-class prefix on `audited_conditional` rows.

The audit policy requires every `audited_conditional` row's
`notes_for_re_audit_if_any` field to begin with one of seven canonical
repair classes (see `docs/audit/README.md`):

  missing_dependency_edge | dependency_not_retained | missing_bridge_theorem
  scope_too_broad | runner_artifact_issue | compute_required | other

A drift accumulated 216 conditional rows that violate that rule:
  - 177 with the field empty
  - 39 with free-form "Re-audit ..." prose without a class prefix

This script reclassifies those rows deterministically by reading the
auditor's existing `verdict_rationale` (specifically the "Repair target:"
sentence) and choosing the matching canonical class. It does NOT change
the audit verdict, claim_type, claim_scope, or auditor identity.

Provenance is recorded in `docs/audit/data/repair_class_backfill_log.json`
so a future auditor can see which rows were synthesized vs. auditor-written.

Usage:
  # dry-run (default): print counts + a sample, no writes
  python3 docs/audit/scripts/backfill_repair_class.py

  # apply: write changes to the ledger + provenance log
  python3 docs/audit/scripts/backfill_repair_class.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
LOG_PATH = REPO_ROOT / "docs" / "audit" / "data" / "repair_class_backfill_log.json"

CANON = (
    "missing_dependency_edge",
    "dependency_not_retained",
    "missing_bridge_theorem",
    "scope_too_broad",
    "runner_artifact_issue",
    "compute_required",
    "other",
)


def extract_repair_target(verdict_rationale: str) -> str:
    if not verdict_rationale:
        return ""
    m = re.search(
        r"Repair target:\s*([^\n]+?)(?=\s*Claim boundary|\s*$)",
        verdict_rationale,
    )
    if not m:
        return ""
    s = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(". ")
    return s + "."


def classify(row: dict) -> tuple[str, str]:
    """Return (canonical_repair_class, repair_sentence)."""
    vr = row.get("verdict_rationale") or ""
    cce = row.get("chain_closure_explanation") or ""
    notes = row.get("notes_for_re_audit_if_any") or ""
    target = extract_repair_target(vr)
    tlow = target.lower()
    haylow = " ".join((target, vr, cce, notes)).lower()

    def t(*ns):
        return any(n in tlow for n in ns)

    def h(*ns):
        return any(n in haylow for n in ns)

    if h(
        "did not complete within",
        "wall-time",
        "audit timeout",
        "60s audit-loop",
        "audit-loop wall-time",
        "completed log within budget",
        "audit-loop budget",
        "reduced deterministic runner",
        "cached completed top_keep",
    ) and not t("register a current runner"):
        return (
            "compute_required",
            target or "rerun within compute budget or supply cached completed artifact.",
        )

    if t(
        "update the source note to a precise",
        "update the source note's status",
        "reclassify the source note",
        "author reclassification",
    ):
        return ("other", target)

    if t(
        "narrow the note",
        "narrow this note",
        "either narrow",
        "split the clean",
        "split a clean",
        "split out the",
        "restrict the note",
        "restrict the claim",
        "narrow the claim",
        "split or register",
        "either restrict the audited",
        "restrict the audited theorem",
    ):
        return ("scope_too_broad", target)

    if t(
        "bridge theorem",
        "bridge principle",
        "bridge map",
        "derive the predictor",
        "asserted as bridge",
        "construct the cpt",
        "derive the bridge",
        "construct .* bridges",
        "parity-protection, and hierarchy-scale bridges",
        "retained theorem or explicit dependency justifying",
    ):
        return ("missing_bridge_theorem", target)
    if re.search(r"\bconstruct(s|ing)? .{0,40} (action|bridge|operator|theorem)\b", tlow):
        return ("missing_bridge_theorem", target)

    if t(
        "ratify ",
        "audit and retain",
        "audit or repair",
        "ratify or repair",
        "first ratify",
        "audit the listed",
        "retain the upstream",
        "until the upstream is retained",
    ):
        return ("dependency_not_retained", target)

    if (
        t(
            "register the cited",
            "register the upstream",
            "wire the cited",
            "register the named",
            "add declared dependency",
            "declare the upstream",
            "register the listed authority",
            "as an explicit audited dependency",
            "register the chiral",
            "register the hartree",
            "register the coarse",
            "register and cite retained authorities",
            "add audit-clean dependency rows",
            "audit-clean dependency rows or a runner",
            "add explicit retained dependencies or a self-contained",
            "add a separate retained theorem proving",
        )
        or re.search(
            r"add the [^.]{1,80} (no-go|theorem|note|proof|authority).{0,30}as (a|an).{0,30}dependency",
            tlow,
        )
        or re.search(
            r"(register|wire|add|declare).{0,80}(one-hop|direct dependency|dependency edge)",
            tlow,
        )
    ):
        return ("missing_dependency_edge", target)

    if t(
        "register a runner",
        "register a current runner",
        "register a runner/log",
        "register a runner/proof",
        "attach a runner",
        "attach cached",
        "add a runner",
        "repair the runner",
        "add explicit runner checks",
        "provide a frozen log",
        "add the runner",
        "fix the runner",
        "register the runner",
        "add a live runner",
        "register a sliced",
        "implement the per-node t normalization",
        "register a compact",
        "registered hygiene runner",
        "provide the actual panel output",
        "promote the grown-dag",
        "promote the .* scripts",
        "promote the .* logs into",
        "add a deterministic aggregate runner",
    ):
        return ("runner_artifact_issue", target)

    if h(
        "no primary runner",
        "no registered runner",
        "unregistered script",
        "cached stdout",
        "live runner",
        "has no runner",
        "runner produced no live replay",
        "runner did not produce",
        "runner has no",
        "runner imports",
        "hard-coded outputs",
    ):
        return (
            "runner_artifact_issue",
            target or "register a current runner/log or sliced certificate for the load-bearing step.",
        )
    if h(
        "still imports unratified",
        "unratified upstream",
        "unaudited authority",
        "authority is not retained",
        "depends on unratified",
    ):
        return (
            "dependency_not_retained",
            target or "ratify the cited upstream authority before re-auditing.",
        )
    if h("split the clean", "narrow the note", "narrow the claim", "unsupported extension"):
        return (
            "scope_too_broad",
            target or "split the clean bounded core from the unsupported extension.",
        )
    if h("missing bridge", "bridge theorem", "imports the standard"):
        return ("missing_bridge_theorem", target or "provide the missing bridge theorem.")

    return (
        "other",
        target
        or "auditor verdict requires re-audit; see verdict_rationale (no canonical repair class auto-detected).",
    )


def needs_backfill(row: dict) -> bool:
    if row.get("audit_status") != "audited_conditional":
        return False
    notes = (row.get("notes_for_re_audit_if_any") or "").strip()
    if not notes:
        return True
    head = notes.split(" ", 1)[0].rstrip(":,;.").lower()
    return head not in CANON


def compose_notes(repair_class: str, repair_sentence: str) -> str:
    sentence = repair_sentence.strip()
    if not sentence:
        sentence = "see verdict_rationale."
    return f"{repair_class}: {sentence}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="write changes to ledger")
    ap.add_argument(
        "--limit", type=int, default=0,
        help="for dry-run, only show the first N candidates",
    )
    args = ap.parse_args()

    ledger = json.loads(LEDGER_PATH.read_text())
    rows = ledger["rows"]

    candidates = [k for k, r in rows.items() if needs_backfill(r)]

    proposed = []
    for cid in candidates:
        row = rows[cid]
        prior_notes = row.get("notes_for_re_audit_if_any") or ""
        repair_class, sentence = classify(row)
        new_notes = compose_notes(repair_class, sentence)
        proposed.append(
            {
                "claim_id": cid,
                "criticality": row.get("criticality"),
                "claim_type": row.get("claim_type"),
                "repair_class": repair_class,
                "prior_notes": prior_notes,
                "new_notes": new_notes,
                "extracted_from": "verdict_rationale.Repair_target" if sentence and "Repair target:" in (row.get("verdict_rationale") or "") else "fallback_template",
            }
        )

    from collections import Counter

    cls = Counter(p["repair_class"] for p in proposed)
    crit = Counter(p["criticality"] for p in proposed)

    print(f"backfill candidates: {len(proposed)}")
    print("\nproposed repair-class distribution:")
    for c in CANON:
        print(f"  {c:30s} {cls.get(c, 0)}")
    print("\nby criticality:")
    for c in ("critical", "high", "medium", "leaf"):
        print(f"  {c:10s} {crit.get(c, 0)}")

    print("\n--- 8 sample proposals ---")
    for p in proposed[: args.limit if args.limit else 8]:
        print(f"\n[{p['repair_class']}] {p['claim_id']} ({p['criticality']})")
        if p["prior_notes"]:
            print(f"  prior: {p['prior_notes'][:160]}")
        else:
            print("  prior: <empty>")
        print(f"  new  : {p['new_notes'][:240]}")

    if not args.apply:
        print("\nDRY RUN — pass --apply to write the ledger.")
        return 0

    # Apply
    timestamp = datetime.now(timezone.utc).isoformat()
    log_entries = []
    for p in proposed:
        cid = p["claim_id"]
        rows[cid]["notes_for_re_audit_if_any"] = p["new_notes"]
        log_entries.append(
            {
                "claim_id": cid,
                "applied_at": timestamp,
                "repair_class": p["repair_class"],
                "prior_notes": p["prior_notes"],
                "new_notes": p["new_notes"],
                "source": p["extracted_from"],
                "policy_basis": "docs/audit/README.md §Workflow audited_conditional repair-class prefix",
            }
        )

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    if LOG_PATH.exists():
        prev = json.loads(LOG_PATH.read_text())
        if not isinstance(prev, list):
            prev = []
    else:
        prev = []
    prev.extend(log_entries)
    LOG_PATH.write_text(json.dumps(prev, indent=2) + "\n")

    print(f"\nAPPLIED: {len(log_entries)} rows updated")
    print(f"  ledger: {LEDGER_PATH}")
    print(f"  log   : {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
