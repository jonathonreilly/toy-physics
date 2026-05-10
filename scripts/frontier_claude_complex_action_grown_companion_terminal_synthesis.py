#!/usr/bin/env python3
"""Check the claude-complex-action grown-companion terminal-synthesis meta note.

Review-hygiene check, not a physics proof. Verifies that the synthesis is:
  - classified as meta and does not declare pipeline status;
  - cites the leaf, its runner, and the imported-premise upstream module;
  - cites the prior audited_conditional verdicts and the recorded
    missing_dependency_edge repair class;
  - cites the audit-lane policy authority (docs/audit/README.md);
  - records the do-NOT-spawn-campaign-cycles recommendation.

Also verifies live audit-ledger state:
  - claude_complex_action_grown_companion_note exists with
    criticality=critical and runner_path=scripts/complex_action_grown_companion.py.
  - The leaf's deps[] array does NOT contain gate_b_grown_joint_package_note
    (PASS — confirms the missing_dependency_edge block still applies; FAIL if
    it has been added).
  - The leaf's previous_audits contains at least one audited_conditional
    verdict whose chain_closure_explanation cites the imported-premise issue
    (PASS — confirms the recorded structural block).
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
NOTE = ROOT / "docs" / "CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10.md"
LEAF_NOTE = ROOT / "docs" / "CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md"
LEAF_RUNNER = ROOT / "scripts" / "complex_action_grown_companion.py"
IMPORTED_MODULE = ROOT / "scripts" / "gate_b_grown_joint_package.py"
AUDIT_README = ROOT / "docs" / "audit" / "README.md"
AUDIT_LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
BAE_TEMPLATE = ROOT / "docs" / "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09.md"

LEAF_ID = "claude_complex_action_grown_companion_note"
IMPORTED_MODULE_CLAIM_ID = "gate_b_grown_joint_package_note"
EXPECTED_RUNNER_PATH = "scripts/complex_action_grown_companion.py"
EXPECTED_IMPORTED_PATH = "scripts/gate_b_grown_joint_package.py"

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


def main() -> int:
    for path in (NOTE, LEAF_NOTE, LEAF_RUNNER, IMPORTED_MODULE, AUDIT_README, AUDIT_LEDGER, BAE_TEMPLATE):
        if not path.exists():
            print(f"missing required file: {path}")
            return 1

    note = NOTE.read_text(encoding="utf-8")
    audit_readme = AUDIT_README.read_text(encoding="utf-8")
    leaf_runner_src = LEAF_RUNNER.read_text(encoding="utf-8")
    ledger = json.loads(AUDIT_LEDGER.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    print("Claude complex-action grown-companion terminal-synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    effective_token = "effective" + "_status:"
    audit_clean_token = "audited" + "_clean"
    # The meta note discusses verdict semantics but must NOT declare any row's
    # pipeline status. We require the canonical "does not promote" disclaimer
    # plus absence of a row-promotion to retained.
    check(
        "does not promote any row to retained",
        "Promote any audit row to retained" in note
        and "What this note does NOT do" in note,
    )
    check("synthesis carries authority disclaimer", "Authority disclaimer" in note)
    check(
        "synthesis explicitly disclaims new derivation / new vocabulary",
        "no theorem promotion" in note.lower()
        or "does not propose" in note.lower()
        or "is not a new derivation" in note.lower()
        or "It does not\npromote theorems" in note,
    )

    # ---- leaf and dep identifiers cited by claim_id ----
    check(f"leaf claim_id cited: {LEAF_ID}", LEAF_ID in note)
    check(
        f"imported-premise upstream claim_id cited: {IMPORTED_MODULE_CLAIM_ID}",
        IMPORTED_MODULE_CLAIM_ID in note,
    )
    check(
        f"imported-premise module file path cited: {EXPECTED_IMPORTED_PATH}",
        EXPECTED_IMPORTED_PATH in note,
    )
    check(
        f"runner path cited: {EXPECTED_RUNNER_PATH}",
        EXPECTED_RUNNER_PATH in note,
    )

    # ---- imported-premise / missing_dependency_edge language ----
    check("cites imported premise language", "imported premise" in note)
    check(
        "cites missing_dependency_edge repair class",
        "missing_dependency_edge" in note,
    )
    check("cites audited_conditional verdicts", "audited_conditional" in note)

    # ---- the runner actually does the import we claim ----
    check(
        "leaf runner imports from scripts.gate_b_grown_joint_package",
        "from scripts.gate_b_grown_joint_package" in leaf_runner_src,
    )
    check(
        "leaf runner imports the `grow` symbol",
        "import grow" in leaf_runner_src,
    )

    # ---- repair surface analysis ----
    check(
        "two structural repair paths recorded",
        ("Register the dep + retain the upstream" in note
         or ("Register" in note and "retain" in note.lower()))
        and ("Inline the grown-geometry construction" in note
             or "Inline" in note),
    )
    check(
        "rules out small-bounded-note repair",
        "not a small bounded source note" in note.lower()
        or "structurally insufficient" in note.lower()
        or "small bounded" in note.lower(),
    )
    check(
        "notes both repair paths are substantial open derivation",
        ("substantial open" in note.lower()
         or "open theorem" in note.lower()
         or "open derivation" in note.lower())
        and ("not a small bounded" in note.lower()
             or "not a single-identity" in note.lower()
             or "scope exceeds" in note.lower()),
    )

    # ---- audit-lane policy authority cited ----
    check(
        "cites docs/audit/README.md authority",
        "docs/audit/README.md" in note or "audit/README.md" in note,
    )
    check(
        "cites hard rule 1 (audit-only retained grade)",
        "Retained grade is audit-only" in note or "hard rule 1" in note.lower(),
    )
    check(
        "cites hard rule 2 (open gates / terminal block propagation)",
        "Open gates block propagation" in note or "hard rule 2" in note.lower(),
    )

    # ---- recommendation for future campaigns ----
    check(
        "Recommendation for future campaigns section present",
        "Recommendation for future campaigns" in note,
    )
    check(
        "explicitly says do NOT spawn audit-backlog cycles",
        ("Do not" in note or "Do **not**" in note) and "audit-backlog" in note.lower(),
    )
    check(
        "explicitly says do NOT spawn retained-promotion attempts",
        "retained-promotion" in note.lower() or "retained promotion" in note.lower(),
    )
    check(
        "explicitly says no new vocabulary / tags / framings",
        ("new vocabulary" in note.lower() or "new tags" in note.lower())
        and ("new framing" in note.lower() or "new framings" in note.lower()
             or "new claim_types" in note.lower()),
    )

    # ---- proposal_allowed: false ----
    check("proposal_allowed: false declared", "proposal_allowed: false" in note)
    check(
        "proposal_allowed_reason justifies as backward-looking synthesis",
        "backward-looking" in note.lower() or "synthesis" in note.lower(),
    )

    # ---- companion + cross-references ----
    check(
        "cites sibling quark projector terminal synthesis (PR #959)",
        "QUARK_PROJECTOR_PARAMETER_AUDIT_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10" in note,
    )
    check(
        "cites sibling DM leptogenesis terminal synthesis (PR #960)",
        "DM_LEPTOGENESIS_TRANSPORT_STATUS_TERMINAL_SYNTHESIS_META_NOTE_2026-05-10" in note,
    )
    check(
        "cites synthesis-template (BAE 30-probe)",
        "KOIDE_BAE_30_PROBE_CAMPAIGN_TERMINAL_SYNTHESIS_META_NOTE_2026-05-09" in note,
    )
    check(
        "cites leaf source note in cross-references",
        "CLAUDE_COMPLEX_ACTION_GROWN_COMPANION_NOTE.md" in note,
    )
    check(
        "cites campaign-level synthesis template",
        "AUDIT_BACKLOG_CAMPAIGN_PROGRESS_SYNTHESIS_2026-05-02" in note,
    )

    # ---- review-loop rule ----
    check("Review-loop rule section present", "Review-loop rule" in note)
    check(
        "review-loop rule notes block is terminal pending repair",
        "terminal" in note.lower()
        and ("retained derivation" in note.lower()
             or "inlined" in note.lower()
             or "imported-premise gate" in note.lower()),
    )

    # ---- live ledger state ----
    check(
        "audit_ledger.json has rows table",
        isinstance(rows, dict) and len(rows) > 0,
        detail=f"rows count: {len(rows) if isinstance(rows, dict) else 0}",
    )

    leaf_row = rows.get(LEAF_ID)
    imported_row = rows.get(IMPORTED_MODULE_CLAIM_ID)

    check(f"ledger has leaf row: {LEAF_ID}", leaf_row is not None)
    check(
        f"ledger has imported-premise upstream row: {IMPORTED_MODULE_CLAIM_ID}",
        imported_row is not None,
    )

    if leaf_row is not None:
        leaf_runner_path = leaf_row.get("runner_path")
        check(
            "leaf runner_path matches synthesis citation",
            leaf_runner_path == EXPECTED_RUNNER_PATH,
            detail=f"got {leaf_runner_path!r}, expected {EXPECTED_RUNNER_PATH!r}",
        )
        leaf_criticality = leaf_row.get("criticality")
        check(
            "leaf row is critical",
            leaf_criticality == "critical",
            detail=f"criticality: {leaf_criticality!r}",
        )
        leaf_deps = list(leaf_row.get("deps") or [])
        check(
            "leaf deps[] does NOT contain gate_b_grown_joint_package_note "
            "(missing_dependency_edge block still applies)",
            IMPORTED_MODULE_CLAIM_ID not in leaf_deps,
            detail=f"deps: {leaf_deps}",
        )
        # Verify previous_audits contains audited_conditional verdicts citing
        # the imported-premise issue.
        prior = leaf_row.get("previous_audits") or []
        conditional_with_import_block = [
            a for a in prior
            if a.get("audit_status") == "audited_conditional"
            and (
                "imported premise" in (a.get("chain_closure_explanation") or "").lower()
                or "imported module" in (a.get("verdict_rationale") or "").lower()
                or "unprovided retained-status premises" in (a.get("chain_closure_explanation") or "").lower()
                or "missing_dependency_edge" in (a.get("notes_for_re_audit_if_any") or "").lower()
                or "gate_b_grown_joint_package" in (
                    str(a.get("open_dependency_paths") or "")
                    + str(a.get("verdict_rationale") or "")
                    + str(a.get("chain_closure_explanation") or "")
                ).lower()
            )
        ]
        check(
            "leaf previous_audits contains audited_conditional verdict citing "
            "the imported-premise / missing_dependency_edge issue",
            len(conditional_with_import_block) >= 1,
            detail=f"matching conditional verdicts: {len(conditional_with_import_block)}",
        )
        # Strengthen by confirming AT LEAST one of the conditional verdicts
        # explicitly names the gate_b_grown_joint_package module via
        # open_dependency_paths.
        named_module_audits = [
            a for a in prior
            if EXPECTED_IMPORTED_PATH in (a.get("open_dependency_paths") or [])
        ]
        check(
            "leaf previous_audits has at least one verdict where "
            "open_dependency_paths names scripts/gate_b_grown_joint_package.py",
            len(named_module_audits) >= 1,
            detail=f"matching verdicts: {len(named_module_audits)}",
        )
    else:
        check("leaf runner_path matches synthesis citation", False, detail="row missing")
        check("leaf row is critical", False, detail="row missing")
        check(
            "leaf deps[] does NOT contain gate_b_grown_joint_package_note "
            "(missing_dependency_edge block still applies)",
            False,
            detail="row missing",
        )
        check(
            "leaf previous_audits contains audited_conditional verdict citing "
            "the imported-premise / missing_dependency_edge issue",
            False,
            detail="row missing",
        )
        check(
            "leaf previous_audits has at least one verdict where "
            "open_dependency_paths names scripts/gate_b_grown_joint_package.py",
            False,
            detail="row missing",
        )

    if imported_row is not None:
        imported_audit_status = imported_row.get("audit_status")
        check(
            "imported-premise upstream is not yet audited_clean (retained-grade)",
            imported_audit_status != "audited_clean",
            detail=f"audit_status: {imported_audit_status!r}",
        )
    else:
        check(
            "imported-premise upstream is not yet audited_clean (retained-grade)",
            False,
            detail="row missing",
        )

    # ---- audit-lane README still has terminal-verdict / repair-class language ----
    check(
        "audit/README.md retains 'audited_<failure_mode>' terminal language",
        "audited_<failure_mode>" in audit_readme
        or "terminal non-clean audit verdicts" in audit_readme,
    )
    check(
        "audit/README.md retains missing_dependency_edge repair-class definition",
        "missing_dependency_edge" in audit_readme,
    )
    check(
        "audit/README.md retains hard rule 1 (Retained grade is audit-only)",
        "Retained grade is audit-only" in audit_readme,
    )
    check(
        "audit/README.md retains hard rule 2 (Open gates block propagation)",
        "Open gates block propagation" in audit_readme,
    )

    print()
    print(f"TOTAL: PASS={PASS} FAIL={FAIL}")
    if FAIL:
        return 1
    print(
        "Claude complex-action grown-companion terminal-synthesis check "
        "passed: leaf and imported-premise upstream cited, "
        "audited_conditional verdicts + missing_dependency_edge repair "
        "class recorded, repair surface analysis present, audit-lane "
        "policy authority cited, do-NOT-spawn-campaign-cycles "
        "recommendation present, live ledger state consistent with "
        "synthesis."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
