#!/usr/bin/env python3
"""
PR #230 non-chunk reopen-admissibility gate.

Cycle 11 closed the current non-chunk route surface until a named
same-surface artifact exists.  This cycle-12 gate closes the file-name-only
reopen shortcut: a future path is not enough.  A candidate must exist as a
parseable artifact, carry claim-status fields, deny branch-local closure
authority, and avoid forbidden-import text before the non-chunk loop may even
rerun the aggregate gates.

The runner does not load, combine, package, or rerun MC chunks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json"

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "future_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
    "terminal": "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json",
    "assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

REQUIRED_STATUS_FIELDS = {
    "actual_current_surface_status",
    "proposal_allowed",
    "audit_required_before_effective_retained",
    "bare_retained_allowed",
}

ALLOWED_STATUS_PREFIXES = (
    "open",
    "exact support",
    "bounded support",
    "conditional",
    "demotion",
    "no-go",
    "exact negative boundary",
    "proposed_retained",
    "proposed_promoted",
)

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def work_unit_rows(worklist: dict[str, Any]) -> list[dict[str, Any]]:
    rows = worklist.get("work_units", [])
    return [row for row in rows if isinstance(row, dict)]


def future_presence_from(cert: dict[str, Any]) -> dict[str, bool]:
    presence = cert.get("future_file_presence", {})
    if not isinstance(presence, dict):
        return {}
    return {str(key): bool(value) for key, value in presence.items()}


def listed_future_paths(worklist: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for unit in work_unit_rows(worklist):
        for rel in unit.get("remaining", []):
            if isinstance(rel, str):
                paths.append(rel)
    return sorted(set(paths))


def forbidden_fragments() -> tuple[str, ...]:
    return (
        "y_t" + "_bare",
        "H" + "_unit",
        "yt" + "_ward",
        "alpha" + "_LM",
        "plaq" + "uette",
        "u" + "0",
        "observed" + " target",
        "bare" + "-coupling shortcut",
        "Plan" + "ck",
        "alpha" + "_s",
        "CLAIMS" + "_TABLE",
        "manu" + "script",
    )


def has_forbidden_text(path: Path) -> bool:
    try:
        body = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        body = path.read_text(encoding="utf-8", errors="ignore")
    lowered = body.lower()
    return any(fragment.lower() in lowered for fragment in forbidden_fragments())


def status_prefix_allowed(value: str) -> bool:
    lower = value.strip().lower()
    return any(lower.startswith(prefix) for prefix in ALLOWED_STATUS_PREFIXES)


def safe_int(value: Any) -> int | None:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return None


def validate_candidate(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    row: dict[str, Any] = {
        "path": rel,
        "present": path.exists(),
        "json_loaded": False,
        "admissible_for_reopen": False,
        "issues": [],
    }
    if not path.exists():
        row["issues"].append("absent")
        return row
    if path.suffix != ".json":
        row["issues"].append("candidate is not a JSON certificate")
        return row
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        row["issues"].append(f"JSON parse failed: {exc}")
        return row
    if not isinstance(data, dict):
        row["issues"].append("candidate JSON root is not an object")
        return row

    row["json_loaded"] = True
    missing_fields = sorted(REQUIRED_STATUS_FIELDS.difference(data))
    if missing_fields:
        row["issues"].append(f"missing status fields: {missing_fields}")
    actual = str(data.get("actual_current_surface_status", ""))
    if not status_prefix_allowed(actual):
        row["issues"].append("actual status is absent or outside the controlled reopen vocabulary")
    if data.get("proposal_allowed") is not False:
        row["issues"].append("candidate may not authorize closure by itself")
    if data.get("bare_retained_allowed") is not False:
        row["issues"].append("bare closure authority must be explicitly denied")
    candidate_fail_count = safe_int(data.get("fail_count", 0))
    if candidate_fail_count is None or candidate_fail_count != 0:
        row["issues"].append("candidate has failing checks")
    if has_forbidden_text(path):
        row["issues"].append("candidate contains a forbidden-import fragment")

    row["actual_current_surface_status"] = actual
    row["admissible_for_reopen"] = not row["issues"]
    return row


def main() -> int:
    print("PR #230 non-chunk reopen-admissibility gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    parent_failures = [name for name, cert in certs.items() if int(cert.get("fail_count", 0) or 0) != 0]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    worklist = certs["worklist"]
    exhaustion = certs["exhaustion"]
    future_intake = certs["future_intake"]
    terminal = certs["terminal"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    worklist_presence = future_presence_from(worklist)
    exhaustion_presence = future_presence_from(exhaustion)
    future_intake_presence = future_presence_from(future_intake)
    terminal_presence = future_presence_from(terminal)
    future_presence_agrees = (
        bool(worklist_presence)
        and worklist_presence == exhaustion_presence
        and worklist_presence == future_intake_presence
        and worklist_presence == terminal_presence
    )
    listed_paths = listed_future_paths(worklist)
    candidate_rows = [validate_candidate(rel) for rel in listed_paths]
    present_paths = sorted(row["path"] for row in candidate_rows if row["present"])
    admissible_paths = sorted(row["path"] for row in candidate_rows if row["admissible_for_reopen"])
    present_keys = sorted(key for key, value in worklist_presence.items() if value)

    all_named_absent = not present_keys and not present_paths
    current_surface_exhausted = (
        "current PR230 non-chunk route queue exhausted" in statuses["exhaustion"]
        and exhaustion.get("proposal_allowed") is False
        and exhaustion.get("current_surface_exhaustion_gate_passed") is True
    )
    future_intake_closed = (
        "future-artifact intake" in statuses["future_intake"]
        and future_intake.get("proposal_allowed") is False
        and future_intake.get("future_artifact_intake_gate_passed") is True
        and future_intake.get("dramatic_step_gate", {}).get("passed") is False
    )
    terminal_closed = (
        "terminal route-exhaustion gate" in statuses["terminal"]
        and terminal.get("proposal_allowed") is False
        and terminal.get("terminal_route_exhaustion_gate_passed") is True
        and terminal.get("dramatic_step_gate", {}).get("passed") is False
    )
    aggregates_deny_proposal = (
        assembly.get("proposal_allowed") is False
        and retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    parent_stack_closed = all(
        [
            not missing_parents,
            not parent_failures,
            not proposal_allowed,
            future_presence_agrees,
            current_surface_exhausted,
            future_intake_closed,
            terminal_closed,
            aggregates_deny_proposal,
        ]
    )
    dramatic_step_passed = bool(admissible_paths)
    reopen_admissibility_gate_passed = parent_stack_closed and not dramatic_step_passed

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("future-presence-schema-agrees-through-terminal", future_presence_agrees, f"keys={sorted(worklist_presence)}")
    report("all-named-future-artifacts-absent", all_named_absent, f"present_keys={present_keys} present_paths={present_paths}")
    report("current-surface-exhaustion-gate-closed", current_surface_exhausted, statuses["exhaustion"])
    report("future-artifact-intake-gate-closed", future_intake_closed, statuses["future_intake"])
    report("terminal-route-exhaustion-gate-closed", terminal_closed, statuses["terminal"])
    report("aggregate-certificates-deny-proposal", aggregates_deny_proposal, f"assembly={statuses['assembly']} retained={statuses['retained_route']} campaign={statuses['campaign']}")
    report("no-admissible-reopen-candidate", not dramatic_step_passed, f"admissible={admissible_paths}")
    report("file-name-only-reopen-shortcut-rejected", reopen_admissibility_gate_passed, f"passed={reopen_admissibility_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk reopen-admissibility "
            "gate: no future artifact candidate is admissible on the current "
            "surface; positive closure still open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The terminal route-exhaustion gate remains closed, all known "
            "future artifact keys are absent, and no listed future path "
            "contains a parseable claim-status certificate that can reopen "
            "the non-chunk route surface."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "selected_route": {
            "id": "nonchunk_reopen_admissibility",
            "cycle": 12,
            "block": 69,
            "reason": (
                "After the terminal stop/reopen gate, the next honest "
                "non-chunk route is to reject a path-only reopen attempt and "
                "define the admissibility floor for any future candidate."
            ),
        },
        "reopen_admissibility_gate_passed": reopen_admissibility_gate_passed,
        "dramatic_step_gate": {
            "passed": dramatic_step_passed,
            "admissible_candidate_paths": admissible_paths,
            "reason": (
                "A new route can execute only after a listed future path "
                "contains a parseable claim-status artifact that denies "
                "branch-local closure authority and passes the forbidden-import "
                "text check."
            ),
        },
        "future_file_presence": worklist_presence,
        "present_candidate_keys": present_keys,
        "listed_candidate_paths": listed_paths,
        "present_candidate_paths": present_paths,
        "candidate_admission": candidate_rows,
        "required_status_fields": sorted(REQUIRED_STATUS_FIELDS),
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed-retained top-Yukawa closure",
            "does not load, combine, package, or rerun chunk MC",
            "does not treat file presence as same-surface physics evidence",
            "does not introduce external readout, coupling, target, or unit shortcuts",
            "does not edit publication, authority-table, or paper-facing surfaces",
        ],
        "exact_next_action": (
            "Do not reopen the current non-chunk shortcut loop from a file path "
            "alone.  Supply one listed same-surface row, certificate, or theorem "
            "as a parseable claim-status artifact, rerun this admissibility gate, "
            "then rerun the worklist, exhaustion, future-intake, assembly, "
            "retained-route, and campaign gates before any proposal language."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
