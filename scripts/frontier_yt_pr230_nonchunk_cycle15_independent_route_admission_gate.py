#!/usr/bin/env python3
"""
PR #230 non-chunk cycle-15 independent-route admission gate.

Cycle 14 closed current-surface route selection.  This gate tests the only
remaining continuation clause inside the non-chunk scope: whether an
independent route can be admitted without a new same-surface artifact.  The
answer is no on the current branch.  The runner records a stuck-fanout
synthesis over the orthogonal route frames and leaves the reopen contract
unchanged.

The runner does not load, combine, package, or rerun MC chunks.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_nonchunk_cycle15_independent_route_admission_gate_2026-05-05.json"
)
LOOP_PACK = (
    ROOT
    / ".claude"
    / "science"
    / "physics-loops"
    / "yt-pr230-osp-oh-retained-closure-20260503"
)
OPPORTUNITY_QUEUE = LOOP_PACK / "OPPORTUNITY_QUEUE.md"
HANDOFF = LOOP_PACK / "HANDOFF.md"

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "route_family": "outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json",
    "exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "future_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
    "terminal": "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json",
    "reopen": "outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json",
    "cycle14_selector": "outputs/yt_pr230_nonchunk_cycle14_route_selector_gate_2026-05-05.json",
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


def future_presence(cert: dict[str, Any]) -> dict[str, bool]:
    raw = dict_field(cert, "future_file_presence")
    return {str(key): bool(value) for key, value in raw.items()}


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def present_keys(presence: dict[str, bool], keys: list[str]) -> list[str]:
    return sorted(key for key in keys if presence.get(key) is True)


def missing_keys(presence: dict[str, bool], keys: list[str]) -> list[str]:
    return sorted(key for key in keys if presence.get(key) is not True)


def fanout_frames(presence: dict[str, bool]) -> list[dict[str, Any]]:
    rows = [
        {
            "id": "same_source_wz_response",
            "attack_frame": "new rows or a same-surface joint covariance theorem",
            "minimum_reopen_keys": [
                "matched_top_wz_rows",
                "top_wz_closed_covariance_theorem",
                "source_coordinate_transport_certificate",
                "wz_mass_response_rows",
                "non_observed_g2_certificate",
                "delta_perp_rows",
            ],
            "load_bearing_wall": (
                "No matched top/W rows, closed covariance theorem, source-transport "
                "certificate, W/Z rows, independent coupling certificate, or "
                "orthogonal-correction rows are present."
            ),
        },
        {
            "id": "canonical_oh_source_higgs",
            "attack_frame": "same-surface canonical Higgs certificate plus source-Higgs rows",
            "minimum_reopen_keys": [
                "canonical_oh_certificate",
                "source_higgs_rows",
            ],
            "load_bearing_wall": (
                "The current primitives do not supply the same-surface identity "
                "and normalization certificate, and no production rows are present."
            ),
        },
        {
            "id": "scalar_lsz_model_fv_ir",
            "attack_frame": "strict scalar-LSZ moment, bound, or contact certificate",
            "minimum_reopen_keys": [
                "stieltjes_moment_certificate",
                "pade_stieltjes_bounds_certificate",
                "contact_subtraction_certificate",
                "polynomial_contact_certificate",
            ],
            "load_bearing_wall": (
                "Finite-shell and contact shortcuts are already blocked; no strict "
                "moment, bound, contact, threshold, or FV/IR certificate is present."
            ),
        },
        {
            "id": "schur_scalar_denominator_rows",
            "attack_frame": "same-surface Schur kernel partition rows",
            "minimum_reopen_keys": ["schur_kernel_rows"],
            "load_bearing_wall": (
                "The compressed denominator bootstrap is non-unique, and no genuine "
                "A/B/C kernel-row certificate is present."
            ),
        },
        {
            "id": "neutral_scalar_rank_one",
            "attack_frame": "neutral-sector primitive-cone or irreducibility theorem",
            "minimum_reopen_keys": [
                "neutral_irreducibility_certificate",
                "neutral_primitive_cone_certificate",
            ],
            "load_bearing_wall": (
                "Source-only and conditional Perron-style premises do not force "
                "irreducibility, and no same-surface neutral certificate is present."
            ),
        },
        {
            "id": "matching_running",
            "attack_frame": "downstream bridge after certified physical readout",
            "minimum_reopen_keys": ["certified_physical_readout"],
            "load_bearing_wall": (
                "This route is downstream only; it cannot execute before a certified "
                "physical readout exists."
            ),
        },
    ]
    for row in rows:
        keys = list(row["minimum_reopen_keys"])
        row["present_reopen_keys"] = present_keys(presence, keys)
        row["missing_reopen_keys"] = missing_keys(presence, keys)
        row["admitted_now"] = False
        row["current_disposition"] = "future-only; no admissible current-surface first action"
    return rows


def main() -> int:
    print("PR #230 non-chunk cycle-15 independent-route admission gate")
    print("=" * 72)

    certs = {name: load(rel) for name, rel in PARENTS.items()}
    statuses = {name: status(cert) for name, cert in certs.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    parent_failures = [
        name for name, cert in certs.items() if int(cert.get("fail_count", 0) or 0) != 0
    ]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    worklist = certs["worklist"]
    route_family = certs["route_family"]
    exhaustion = certs["exhaustion"]
    future_intake = certs["future_intake"]
    terminal = certs["terminal"]
    reopen = certs["reopen"]
    cycle14 = certs["cycle14_selector"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    blocked_ids = {str(item) for item in list_field(worklist, "blocked_work_unit_ids")}
    closed_ids = {str(item) for item in list_field(worklist, "closed_work_unit_ids")}
    route_executable_ids = [str(item) for item in list_field(route_family, "executable_route_ids")]
    selected_route = dict_field(route_family, "selected_route")
    reopen_candidates = [
        str(item) for item in list_field(dict_field(reopen, "dramatic_step_gate"), "admissible_candidate_paths")
    ]

    worklist_presence = future_presence(worklist)
    cycle14_presence = future_presence(cycle14)
    terminal_presence = future_presence(terminal)
    presence_sources = {
        "worklist": worklist_presence,
        "cycle14_selector": cycle14_presence,
        "terminal": terminal_presence,
    }
    future_presence_keys = sorted(
        {key for source in presence_sources.values() for key in source}
    )
    all_future_absent = bool(worklist_presence) and not any(worklist_presence.values())
    future_presence_agrees = (
        bool(worklist_presence)
        and all(
            source.get(key) is not True
            for source in presence_sources.values()
            for key in future_presence_keys
        )
    )
    frames = fanout_frames(worklist_presence)
    admitted_frames = [row["id"] for row in frames if row["admitted_now"]]

    queue_body = " ".join(text(OPPORTUNITY_QUEUE).lower().split())
    handoff_body = " ".join(text(HANDOFF).lower().split())

    all_work_units_blocked = blocked_ids == EXPECTED_BLOCKED_UNITS and not closed_ids
    route_family_closed = (
        route_family.get("proposal_allowed") is False
        and selected_route.get("id") == "no_current_surface_nonchunk_route"
        and not route_executable_ids
        and "no executable current-surface route" in statuses["route_family"]
    )
    previous_selector_closed = (
        cycle14.get("proposal_allowed") is False
        and cycle14.get("route_selector_gate_passed") is True
        and cycle14.get("dramatic_step_gate", {}).get("passed") is False
    )
    terminal_and_reopen_closed = (
        terminal.get("proposal_allowed") is False
        and terminal.get("terminal_route_exhaustion_gate_passed") is True
        and terminal.get("dramatic_step_gate", {}).get("passed") is False
        and reopen.get("proposal_allowed") is False
        and reopen.get("reopen_admissibility_gate_passed") is True
        and reopen.get("dramatic_step_gate", {}).get("passed") is False
        and not reopen_candidates
    )
    intake_and_exhaustion_closed = (
        exhaustion.get("proposal_allowed") is False
        and exhaustion.get("current_surface_exhaustion_gate_passed") is True
        and future_intake.get("proposal_allowed") is False
        and future_intake.get("future_artifact_intake_gate_passed") is True
        and future_intake.get("dramatic_step_gate", {}).get("passed") is False
    )
    aggregates_deny = (
        assembly.get("proposal_allowed") is False
        and retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    fanout_complete = len(frames) >= 5 and not admitted_frames
    queue_records_cycle15 = (
        "cycle-15 update" in queue_body
        and "no independent current-surface route is admitted" in queue_body
    )
    handoff_records_cycle15 = (
        "cycle-15 independent-route admission gate" in handoff_body
        and "no independent current-surface route" in handoff_body
    )
    chunk_firewall = (
        not any("chunk0" in rel for rel in PARENTS.values())
        and "does not load, combine, package, or rerun mc chunks" in __doc__.lower()
    )

    independent_route_admission_gate_passed = all(
        [
            not missing_parents,
            not parent_failures,
            not proposal_allowed,
            all_work_units_blocked,
            future_presence_agrees,
            all_future_absent,
            route_family_closed,
            previous_selector_closed,
            terminal_and_reopen_closed,
            intake_and_exhaustion_closed,
            aggregates_deny,
            fanout_complete,
            queue_records_cycle15,
            handoff_records_cycle15,
            chunk_firewall,
        ]
    )
    dramatic_step_gate = {
        "passed": False,
        "admitted_independent_route_ids": admitted_frames,
        "reason": (
            "The independent-route fanout has no current-surface first action. "
            "Every frame requires an absent same-surface row, certificate, or "
            "theorem before aggregate reruns can select it."
        ),
    }

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("all-worklist-units-remain-blocked", all_work_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("future-presence-absence-agrees", future_presence_agrees, f"keys={future_presence_keys}")
    report("all-listed-future-artifacts-absent", all_future_absent, f"present={[key for key, value in worklist_presence.items() if value]}")
    report("route-family-selector-remains-closed", route_family_closed, selected_route.get("id", ""))
    report("cycle14-selector-remains-closed", previous_selector_closed, statuses["cycle14_selector"])
    report("terminal-and-reopen-gates-remain-closed", terminal_and_reopen_closed, f"reopen_candidates={reopen_candidates}")
    report("exhaustion-and-intake-gates-remain-closed", intake_and_exhaustion_closed, statuses["future_intake"])
    report("aggregate-certificates-deny-proposal", aggregates_deny, f"assembly={statuses['assembly']} retained={statuses['retained_route']} campaign={statuses['campaign']}")
    report("stuck-fanout-has-no-admitted-frame", fanout_complete, f"admitted={admitted_frames}")
    report("opportunity-queue-records-cycle15", queue_records_cycle15, "cycle-15 queue update present")
    report("handoff-records-cycle15", handoff_records_cycle15, "cycle-15 handoff update present")
    report("chunk-worker-firewall-held", chunk_firewall, "gate consumes certificates only")
    report("independent-route-admission-gate-passed", independent_route_admission_gate_passed, f"passed={independent_route_admission_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk cycle-15 independent-route "
            "admission gate: no independent current-surface route is admitted "
            "after cycle-14 route selection; positive closure still open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "All parent gates deny proposal authority, all six non-chunk work "
            "units remain blocked, all listed future artifacts are absent, and "
            "the stuck-fanout frames have no admissible first action."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "independent_route_admission_gate_passed": independent_route_admission_gate_passed,
        "dramatic_step_gate": dramatic_step_gate,
        "selected_route": {
            "id": "no_independent_current_surface_nonchunk_route",
            "route_family": "cycle-15 independent-route admission",
            "can_execute_now": False,
            "reason": (
                "The prompt continues the non-chunk loop, but no new "
                "same-surface physics artifact is present.  Continuation "
                "therefore closes as a checked no-go rather than selecting a "
                "support-only or forbidden shortcut."
            ),
        },
        "stuck_fanout_frames": frames,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "future_file_presence": worklist_presence,
        "future_presence_sources": presence_sources,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim retained or proposed-retained top-Yukawa closure",
            "does not load, combine, package, or rerun chunk MC",
            "does not convert process exhaustion into positive physics evidence",
            "does not introduce forbidden readout, operator, coupling, target, or unit shortcuts",
            "does not edit publication, authority-table, or paper-facing surfaces",
        ],
        "exact_next_action": (
            "Treat the non-chunk PR230 current surface as globally exhausted "
            "for this branch.  Reopen only after a listed same-surface row, "
            "certificate, or theorem exists as a parseable claim-status "
            "artifact; then rerun reopen-admissibility, worklist, exhaustion, "
            "intake, independent-route admission, assembly, retained-route, "
            "and campaign gates before any proposal language."
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
