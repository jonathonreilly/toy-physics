#!/usr/bin/env python3
"""
PR #230 non-chunk future-artifact intake gate.

Cycle 8 closed the current non-chunk shortcut queue.  This cycle-9 gate checks
whether any named strict future same-surface row, certificate, or theorem has
arrived since that closeout.  If none has arrived, the dramatic-step gate does
not pass and the non-chunk loop has no executable current-surface route.

The runner does not load, combine, package, or rerun MC chunks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json"

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
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

ROUTE_FRAME_LABELS = {
    "canonical_oh_source_higgs": "source-Higgs / canonical-Higgs row intake",
    "same_source_wz_response": "same-source W/Z response row intake",
    "scalar_lsz_model_fv_ir": "scalar-LSZ certificate intake",
    "schur_scalar_denominator_rows": "Schur kernel-row intake",
    "neutral_scalar_rank_one": "neutral irreducibility certificate intake",
    "matching_running": "downstream matching bridge intake",
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


def future_presence_from(worklist: dict[str, Any]) -> dict[str, bool]:
    presence = worklist.get("future_file_presence", {})
    if not isinstance(presence, dict):
        return {}
    return {str(key): bool(value) for key, value in presence.items()}


def blocked_unit_ids(worklist: dict[str, Any]) -> set[str]:
    ids = worklist.get("blocked_work_unit_ids", [])
    if not isinstance(ids, list):
        return set()
    return {str(item) for item in ids}


def closed_unit_ids(worklist: dict[str, Any]) -> set[str]:
    ids = worklist.get("closed_work_unit_ids", [])
    if not isinstance(ids, list):
        return set()
    return {str(item) for item in ids}


def work_unit_rows(worklist: dict[str, Any]) -> list[dict[str, Any]]:
    rows = worklist.get("work_units", [])
    return [row for row in rows if isinstance(row, dict)]


def missing_or_present_future_files(worklist: dict[str, Any]) -> tuple[list[str], list[str]]:
    missing_schema: list[str] = []
    present_paths: list[str] = []
    for unit in work_unit_rows(worklist):
        for rel in unit.get("remaining", []):
            if not isinstance(rel, str):
                missing_schema.append(str(rel))
                continue
            if (ROOT / rel).exists():
                present_paths.append(rel)
    return sorted(missing_schema), sorted(present_paths)


def route_frames(worklist: dict[str, Any], presence: dict[str, bool]) -> list[dict[str, Any]]:
    frames: list[dict[str, Any]] = []
    for unit in work_unit_rows(worklist):
        unit_id = str(unit.get("id", ""))
        remaining = [rel for rel in unit.get("remaining", []) if isinstance(rel, str)]
        present = [rel for rel in remaining if (ROOT / rel).exists()]
        frames.append(
            {
                "id": unit_id,
                "label": ROUTE_FRAME_LABELS.get(unit_id, unit_id),
                "current_state": str(unit.get("current_state", "")),
                "intake_ready": bool(present),
                "present_future_paths": present,
                "remaining_future_paths": remaining,
            }
        )
    # Preserve top-level future_file_presence as an independent schema guard.
    extra_present = sorted(key for key, value in presence.items() if value)
    if extra_present:
        frames.append(
            {
                "id": "top_level_future_presence",
                "label": "top-level future-file presence",
                "current_state": "present",
                "intake_ready": True,
                "present_future_paths": extra_present,
                "remaining_future_paths": [],
            }
        )
    return frames


def main() -> int:
    print("PR #230 non-chunk future-artifact intake gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    parent_failures = [name for name, cert in certs.items() if int(cert.get("fail_count", 0)) != 0]
    statuses = {name: status(cert) for name, cert in certs.items()}

    worklist = certs["worklist"]
    exhaustion = certs["exhaustion"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    blocked_ids = blocked_unit_ids(worklist)
    closed_ids = closed_unit_ids(worklist)
    future_presence = future_presence_from(worklist)
    exhaustion_presence = future_presence_from(exhaustion)
    schema_gaps, present_future_paths = missing_or_present_future_files(worklist)
    frames = route_frames(worklist, future_presence)
    executable_frames = [frame for frame in frames if frame["intake_ready"]]

    all_work_units_blocked = blocked_ids == EXPECTED_BLOCKED_UNITS and not closed_ids
    future_presence_agrees = future_presence == exhaustion_presence and future_presence
    top_level_future_absent = future_presence_agrees and not any(future_presence.values())
    future_paths_absent = not schema_gaps and not present_future_paths
    exhaustion_gate_closed = (
        "current PR230 non-chunk route queue exhausted" in statuses["exhaustion"]
        and exhaustion.get("current_surface_exhaustion_gate_passed") is True
        and exhaustion.get("proposal_allowed") is False
    )
    assembly_blocks_current_and_chunk_only = (
        assembly.get("current_evaluation", {}).get("assembly_passed") is False
        and assembly.get("chunk_only_evaluation", {}).get("assembly_passed") is False
        and assembly.get("proposal_allowed") is False
    )
    retained_and_campaign_deny = (
        retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    dramatic_step_passed = bool(executable_frames)
    future_artifact_intake_gate_passed = all(
        [
            not missing_parents,
            not proposal_allowed,
            not parent_failures,
            all_work_units_blocked,
            top_level_future_absent,
            future_paths_absent,
            exhaustion_gate_closed,
            assembly_blocks_current_and_chunk_only,
            retained_and_campaign_deny,
            not dramatic_step_passed,
        ]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("worklist-units-remain-blocked", all_work_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("future-presence-schema-agrees", future_presence_agrees, f"keys={sorted(future_presence)}")
    report("top-level-future-files-absent", top_level_future_absent, f"present={[key for key, value in future_presence.items() if value]}")
    report("listed-future-paths-absent", future_paths_absent, f"present={present_future_paths} schema_gaps={schema_gaps}")
    report("cycle-8-exhaustion-gate-closed", exhaustion_gate_closed, statuses["exhaustion"])
    report("assembly-still-rejects-current-and-chunk-only", assembly_blocks_current_and_chunk_only, statuses["assembly"])
    report("retained-and-campaign-certificates-deny-proposal", retained_and_campaign_deny, f"retained={statuses['retained_route']} campaign={statuses['campaign']}")
    report("dramatic-step-gate-has-no-executable-route", not dramatic_step_passed, f"executable={executable_frames}")
    report("future-artifact-intake-gate-passed", future_artifact_intake_gate_passed, f"passed={future_artifact_intake_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk future-artifact intake "
            "finds no executable current route; positive closure still open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The cycle-8 exhaustion gate remains closed, every non-chunk work "
            "unit is still blocked, and no named strict future row or "
            "certificate path exists on disk.  No route crosses the "
            "dramatic-step intake threshold on the current surface."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "selected_route": {
            "id": "strict_future_artifact_intake",
            "cycle": 9,
            "block": 67,
            "reason": (
                "After current-surface non-chunk exhaustion, the only honest "
                "next route is to test whether a named future same-surface "
                "artifact has appeared.  None has."
            ),
        },
        "dramatic_step_gate": {
            "passed": dramatic_step_passed,
            "executable_frames": executable_frames,
            "reason": (
                "A future row/certificate intake route passes only if at least "
                "one named strict same-surface artifact is present for review."
            ),
        },
        "future_artifact_intake_gate_passed": future_artifact_intake_gate_passed,
        "future_file_presence": future_presence,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "route_frames": frames,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not load, combine, package, or rerun chunk MC",
            "does not introduce external target selectors or coupling shortcuts",
            "does not turn a missing future artifact into branch-local evidence",
        ],
        "exact_next_action": (
            "Stop current-surface non-chunk shortcut cycling.  Reopen this "
            "non-chunk loop only when a named strict same-surface row, "
            "certificate, or theorem is supplied, then rerun the worklist, "
            "assembly, retained-route, and campaign gates before any proposal."
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
