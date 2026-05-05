#!/usr/bin/env python3
"""
PR #230 non-chunk cycle-14 route-selector gate.

Cycle 13 closed the last current-branch W/Z covariance-theorem import
shortcut.  This gate checks the selector state after that closure: no
non-chunk route family may be selected on the current surface until a named
same-surface row, certificate, or theorem exists as a parseable claim-status
artifact and the aggregate gates are rerun.

The runner does not load, combine, package, or rerun MC chunks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_nonchunk_cycle14_route_selector_gate_2026-05-05.json"
LOOP_PACK = ROOT / ".claude" / "science" / "physics-loops" / "yt-pr230-osp-oh-retained-closure-20260503"
OPPORTUNITY_QUEUE = LOOP_PACK / "OPPORTUNITY_QUEUE.md"

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "route_family": "outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json",
    "exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "future_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
    "terminal": "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json",
    "reopen": "outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_BLOCKED_UNITS = {
    "canonical_oh_source_higgs",
    "same_source_wz_response",
    "scalar_lsz_model_fv_ir",
    "schur_scalar_denominator_rows",
    "neutral_scalar_rank_one",
    "matching_running",
}

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


def list_field(cert: dict[str, Any], key: str) -> list[Any]:
    value = cert.get(key, [])
    return value if isinstance(value, list) else []


def dict_field(cert: dict[str, Any], key: str) -> dict[str, Any]:
    value = cert.get(key, {})
    return value if isinstance(value, dict) else {}


def route_rows(route_family: dict[str, Any]) -> list[dict[str, Any]]:
    return [row for row in list_field(route_family, "route_families_audited") if isinstance(row, dict)]


def future_presence(cert: dict[str, Any]) -> dict[str, bool]:
    raw = dict_field(cert, "future_file_presence")
    return {str(key): bool(value) for key, value in raw.items()}


def queue_text() -> str:
    if not OPPORTUNITY_QUEUE.exists():
        return ""
    return OPPORTUNITY_QUEUE.read_text(encoding="utf-8")


def main() -> int:
    print("PR #230 non-chunk cycle-14 route-selector gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    parent_failures = [name for name, cert in certs.items() if int(cert.get("fail_count", 0) or 0) != 0]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    worklist = certs["worklist"]
    route_family = certs["route_family"]
    exhaustion = certs["exhaustion"]
    future_intake = certs["future_intake"]
    terminal = certs["terminal"]
    reopen = certs["reopen"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    blocked_ids = {str(item) for item in list_field(worklist, "blocked_work_unit_ids")}
    closed_ids = {str(item) for item in list_field(worklist, "closed_work_unit_ids")}
    rows = route_rows(route_family)
    row_executable_ids = sorted(str(row.get("id")) for row in rows if row.get("can_execute_now") is True)
    reported_executable_ids = [str(item) for item in list_field(route_family, "executable_route_ids")]
    selected_route = dict_field(route_family, "selected_route")
    ranked_future_route = dict_field(route_family, "ranked_future_route")
    presence = future_presence(worklist)
    queue = queue_text()

    all_work_units_blocked = blocked_ids == EXPECTED_BLOCKED_UNITS and not closed_ids
    no_future_artifact_present = bool(presence) and not any(presence.values())
    route_family_selector_closed = (
        "non-chunk route-family import audit" in statuses["route_family"]
        and "no executable current-surface route" in statuses["route_family"]
        and route_family.get("proposal_allowed") is False
        and selected_route.get("id") == "no_current_surface_nonchunk_route"
        and not row_executable_ids
        and not reported_executable_ids
    )
    ranked_future_is_wz_only = (
        ranked_future_route.get("id") == "same_source_wz_response"
        and ranked_future_route.get("can_execute_now") is False
        and "covariance-theorem import audit" in str(ranked_future_route.get("current_disposition", ""))
    )
    exhaustion_closed = (
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
    reopen_closed = (
        "reopen-admissibility gate" in statuses["reopen"]
        and reopen.get("proposal_allowed") is False
        and reopen.get("reopen_admissibility_gate_passed") is True
        and reopen.get("dramatic_step_gate", {}).get("passed") is False
    )
    retained_and_campaign_deny = (
        retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    queue_lower = " ".join(queue.lower().split())
    queue_records_cycle14 = (
        "cycle-14 update" in queue_lower
        and "no executable current-surface non-chunk route" in queue_lower
        and "parseable claim-status artifact" in queue_lower
    )
    dramatic_step_gate = {
        "passed": False,
        "selected_current_route": selected_route,
        "ranked_future_route": ranked_future_route,
        "reason": (
            "The route-family selector has no executable current-surface "
            "non-chunk row after the cycle-13 covariance-theorem import "
            "no-go.  The next route is future-only until a listed "
            "same-surface artifact exists and the reopen/aggregate gates pass."
        ),
    }
    route_selector_gate_passed = all(
        [
            not missing_parents,
            not parent_failures,
            not proposal_allowed,
            all_work_units_blocked,
            no_future_artifact_present,
            route_family_selector_closed,
            ranked_future_is_wz_only,
            exhaustion_closed,
            future_intake_closed,
            terminal_closed,
            reopen_closed,
            retained_and_campaign_deny,
            queue_records_cycle14,
        ]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("all-worklist-units-remain-blocked", all_work_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("all-listed-future-artifacts-absent", no_future_artifact_present, f"present={[key for key, value in presence.items() if value]}")
    report("route-family-selector-closed", route_family_selector_closed, selected_route.get("id", ""))
    report("wz-is-ranked-future-route-not-current-selection", ranked_future_is_wz_only, ranked_future_route.get("id", ""))
    report("current-surface-exhaustion-gate-closed", exhaustion_closed, statuses["exhaustion"])
    report("future-artifact-intake-gate-closed", future_intake_closed, statuses["future_intake"])
    report("terminal-route-exhaustion-gate-closed", terminal_closed, statuses["terminal"])
    report("reopen-admissibility-gate-closed", reopen_closed, statuses["reopen"])
    report("retained-and-campaign-deny-proposal", retained_and_campaign_deny, f"retained={statuses['retained_route']} campaign={statuses['campaign']}")
    report("opportunity-queue-records-cycle14-selector", queue_records_cycle14, "cycle-14 selector state recorded")
    report("route-selector-gate-passed", route_selector_gate_passed, f"passed={route_selector_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk cycle-14 route-selector "
            "gate: no executable current-surface non-chunk route remains after "
            "the W/Z covariance-theorem import no-go; positive closure still open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The route-family audit selects no current route, all six worklist "
            "units remain blocked, all listed future artifacts are absent, and "
            "the exhaustion, intake, terminal, and reopen-admissibility gates "
            "all remain closed."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "selected_route": selected_route,
        "ranked_future_route": ranked_future_route,
        "route_selector_gate_passed": route_selector_gate_passed,
        "dramatic_step_gate": dramatic_step_gate,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "executable_route_ids": reported_executable_ids,
        "future_file_presence": presence,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed-retained top-Yukawa closure",
            "does not load, combine, package, or rerun chunk MC",
            "does not convert route exhaustion into positive physics evidence",
            "does not introduce forbidden readout, operator, coupling, target, or unit shortcuts",
            "does not edit publication, authority-table, or paper-facing surfaces",
        ],
        "exact_next_action": (
            "Stop current-surface non-chunk shortcut cycling.  Reopen only when "
            "a listed same-surface row, certificate, or theorem exists as a "
            "parseable claim-status artifact; then rerun reopen-admissibility, "
            "worklist, current-surface exhaustion, future-artifact intake, "
            "assembly, retained-route, and campaign gates before any proposal "
            "language or route selection."
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
