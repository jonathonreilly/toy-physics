#!/usr/bin/env python3
"""
PR #230 non-chunk terminal route-exhaustion gate.

The previous non-chunk block proved that no named future same-surface artifact
has appeared after current-surface exhaustion.  This gate turns that result
into a continuation firewall: the non-chunk loop must stop shortcut cycling
until a named same-surface row, certificate, or theorem exists and all aggregate
gates are rerun.

The runner does not load, combine, package, or rerun MC chunks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json"
LOOP_PACK = ROOT / ".claude" / "science" / "physics-loops" / "yt-pr230-osp-oh-retained-closure-20260503"
OPPORTUNITY_QUEUE = LOOP_PACK / "OPPORTUNITY_QUEUE.md"
HANDOFF = LOOP_PACK / "HANDOFF.md"

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "future_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
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

REOPEN_ARTIFACT_KEYS = {
    "canonical_oh_certificate",
    "source_higgs_rows",
    "matched_top_wz_rows",
    "deterministic_response_covariance_certificate",
    "source_coordinate_transport_certificate",
    "wz_mass_response_rows",
    "non_observed_g2_certificate",
    "delta_perp_rows",
    "top_wz_closed_covariance_theorem",
    "stieltjes_moment_certificate",
    "pade_stieltjes_bounds_certificate",
    "contact_subtraction_certificate",
    "polynomial_contact_certificate",
    "schur_kernel_rows",
    "neutral_irreducibility_certificate",
    "neutral_primitive_cone_certificate",
    "certified_physical_readout",
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


def future_presence_from(cert: dict[str, Any]) -> dict[str, bool]:
    presence = cert.get("future_file_presence", {})
    if not isinstance(presence, dict):
        return {}
    return {str(key): bool(value) for key, value in presence.items()}


def work_unit_rows(worklist: dict[str, Any]) -> list[dict[str, Any]]:
    rows = worklist.get("work_units", [])
    return [row for row in rows if isinstance(row, dict)]


def listed_future_paths(worklist: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for unit in work_unit_rows(worklist):
        for rel in unit.get("remaining", []):
            if isinstance(rel, str):
                paths.append(rel)
    return sorted(set(paths))


def present_listed_future_paths(worklist: dict[str, Any]) -> list[str]:
    return sorted(rel for rel in listed_future_paths(worklist) if (ROOT / rel).exists())


def route_frames(future_intake: dict[str, Any]) -> list[dict[str, Any]]:
    rows = future_intake.get("route_frames", [])
    return [row for row in rows if isinstance(row, dict)]


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def main() -> int:
    print("PR #230 non-chunk terminal route-exhaustion gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    parent_failures = [name for name, cert in certs.items() if int(cert.get("fail_count", 0)) != 0]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in certs.items()}

    worklist = certs["worklist"]
    exhaustion = certs["exhaustion"]
    future_intake = certs["future_intake"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    blocked_ids = blocked_unit_ids(worklist)
    closed_ids = closed_unit_ids(worklist)
    worklist_presence = future_presence_from(worklist)
    exhaustion_presence = future_presence_from(exhaustion)
    future_intake_presence = future_presence_from(future_intake)
    future_path_hits = present_listed_future_paths(worklist)
    frames = route_frames(future_intake)
    executable_frames = [frame for frame in frames if frame.get("intake_ready") is True]

    queue_text = text(OPPORTUNITY_QUEUE)
    handoff_text = text(HANDOFF)

    all_work_units_blocked = blocked_ids == EXPECTED_BLOCKED_UNITS and not closed_ids
    future_presence_schema_complete = REOPEN_ARTIFACT_KEYS.issubset(set(worklist_presence))
    future_presence_agrees = (
        bool(worklist_presence)
        and worklist_presence == exhaustion_presence
        and worklist_presence == future_intake_presence
    )
    all_named_future_absent = future_presence_agrees and not any(worklist_presence.values()) and not future_path_hits
    exhaustion_gate_closed = (
        exhaustion.get("current_surface_exhaustion_gate_passed") is True
        and exhaustion.get("proposal_allowed") is False
        and "current PR230 non-chunk route queue exhausted" in statuses["exhaustion"]
    )
    future_intake_closed = (
        future_intake.get("future_artifact_intake_gate_passed") is True
        and future_intake.get("proposal_allowed") is False
        and future_intake.get("dramatic_step_gate", {}).get("passed") is False
        and "future-artifact intake" in statuses["future_intake"]
    )
    no_executable_frame = not executable_frames
    assembly_rejects_current_and_chunk_only = (
        assembly.get("current_evaluation", {}).get("assembly_passed") is False
        and assembly.get("chunk_only_evaluation", {}).get("assembly_passed") is False
        and assembly.get("proposal_allowed") is False
    )
    retained_and_campaign_deny = (
        retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    queue_declares_future_only = (
        "no executable current-surface non-chunk item" in queue_text
        and "future opportunities only" in queue_text
        and "first-action artifact exists" in queue_text
    )
    handoff_lower = " ".join(handoff_text.lower().split())
    handoff_reopen_contract = (
        "stop current-surface non-chunk shortcut cycling" in handoff_lower
        and "reopen only when" in handoff_lower
    )
    chunk_firewall = (
        not any("chunk0" in rel for rel in PARENTS.values())
        and assembly.get("chunk_only_evaluation", {}).get("assembly_passed") is False
    )
    dramatic_step_gate = {
        "passed": False,
        "executable_frames": executable_frames,
        "reason": (
            "The refreshed non-chunk queue contains only future-only rows.  A "
            "new route passes only after a named same-surface row, certificate, "
            "or theorem exists on disk and the aggregate gates are rerun."
        ),
    }
    terminal_route_exhaustion_gate_passed = all(
        [
            not missing_parents,
            not parent_failures,
            not proposal_allowed,
            all_work_units_blocked,
            future_presence_schema_complete,
            all_named_future_absent,
            exhaustion_gate_closed,
            future_intake_closed,
            no_executable_frame,
            assembly_rejects_current_and_chunk_only,
            retained_and_campaign_deny,
            queue_declares_future_only,
            handoff_reopen_contract,
            chunk_firewall,
        ]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("all-nonchunk-work-units-remain-blocked", all_work_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("future-presence-schema-complete", future_presence_schema_complete, f"missing={sorted(REOPEN_ARTIFACT_KEYS.difference(worklist_presence))}")
    report("all-named-future-artifacts-absent", all_named_future_absent, f"present_paths={future_path_hits}")
    report("current-surface-exhaustion-gate-closed", exhaustion_gate_closed, statuses["exhaustion"])
    report("future-artifact-intake-gate-closed", future_intake_closed, statuses["future_intake"])
    report("dramatic-step-gate-has-no-executable-frame", no_executable_frame, f"executable={executable_frames}")
    report("assembly-rejects-current-and-chunk-only", assembly_rejects_current_and_chunk_only, statuses["assembly"])
    report("retained-and-campaign-certificates-deny-proposal", retained_and_campaign_deny, f"retained={statuses['retained_route']} campaign={statuses['campaign']}")
    report("opportunity-queue-declares-future-only", queue_declares_future_only, "queue has no executable current-surface item")
    report("handoff-records-reopen-contract", handoff_reopen_contract, "handoff names stop/reopen rule")
    report("chunk-worker-firewall-held", chunk_firewall, "terminal gate does not consume chunk artifacts")
    report("terminal-route-exhaustion-gate-passed", terminal_route_exhaustion_gate_passed, f"passed={terminal_route_exhaustion_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk terminal route-exhaustion "
            "gate: no current route may continue without a named same-surface "
            "artifact; positive closure still open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current-surface exhaustion gate and future-artifact intake gate "
            "both remain closed, all six non-chunk work units are blocked, the "
            "refreshed opportunity queue is future-only, and no named "
            "same-surface row, certificate, or theorem is present on disk."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "selected_route": {
            "id": "terminal_nonchunk_route_exhaustion",
            "cycle": 11,
            "block": 68,
            "reason": (
                "After current-surface exhaustion and a failed future-artifact "
                "intake, the only honest non-chunk action is to encode the stop "
                "and reopen rule as an executable gate."
            ),
        },
        "terminal_route_exhaustion_gate_passed": terminal_route_exhaustion_gate_passed,
        "dramatic_step_gate": dramatic_step_gate,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "future_file_presence": worklist_presence,
        "present_future_paths": future_path_hits,
        "route_frames": frames,
        "reopen_contract": {
            "requires_named_same_surface_artifact": True,
            "accepted_artifact_keys": sorted(REOPEN_ARTIFACT_KEYS),
            "rerun_required_gates": [
                PARENTS["worklist"],
                PARENTS["exhaustion"],
                PARENTS["future_intake"],
                PARENTS["assembly"],
                PARENTS["retained_route"],
                PARENTS["campaign"],
            ],
        },
        "strict_non_claims": [
            "does not claim retained or proposed-retained top-Yukawa closure",
            "does not load, combine, package, or rerun chunk MC",
            "does not convert queue exhaustion into physical evidence",
            "does not introduce forbidden readout, operator, coupling, target, or unit shortcuts",
            "does not rule out future same-surface rows, certificates, or new theorems",
        ],
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "exact_next_action": (
            "Do not continue current-surface non-chunk shortcut cycling.  Reopen "
            "only after one accepted artifact key in this certificate exists on "
            "disk, then rerun the worklist, exhaustion, future-intake, assembly, "
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
