#!/usr/bin/env python3
"""
PR #230 non-chunk cycle-16 reopen-source guard.

Cycle 15 closed independent current-route admission.  This gate tests the
next admissible non-chunk question: whether the post-checkpoint surface has a
valid reopen source to consume.  It records a negative boundary when no listed
same-surface row, certificate, or theorem exists as a parseable artifact.

The runner does not load, combine, package, or rerun MC chunks.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "outputs"
    / "yt_pr230_nonchunk_cycle16_reopen_source_guard_2026-05-05.json"
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
CHECKPOINT_HEAD = "b118eeb8b970f39493b0209ea62f6988f91ab987"
REMOTE_BASE = "origin/main"

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "route_family": "outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json",
    "exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "future_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
    "terminal": "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json",
    "reopen": "outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json",
    "cycle14_selector": "outputs/yt_pr230_nonchunk_cycle14_route_selector_gate_2026-05-05.json",
    "cycle15_independent": "outputs/yt_pr230_nonchunk_cycle15_independent_route_admission_gate_2026-05-05.json",
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


def git(args: list[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def git_ok(args: list[str]) -> bool:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


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


def all_false(presence: dict[str, bool]) -> bool:
    return bool(presence) and not any(presence.values())


def present_keys(presence: dict[str, bool]) -> list[str]:
    return sorted(key for key, value in presence.items() if value)


def remote_base_state() -> dict[str, Any]:
    remote_head = git(["rev-parse", "--verify", REMOTE_BASE])
    checkpoint_is_ancestor = git_ok(["merge-base", "--is-ancestor", CHECKPOINT_HEAD, "HEAD"])
    local_head = git(["rev-parse", "HEAD"])
    remote_commit_count = git(["rev-list", "--count", f"{CHECKPOINT_HEAD}..{REMOTE_BASE}"])
    remote_subjects = git(["log", "--oneline", "--max-count=5", f"{CHECKPOINT_HEAD}..{REMOTE_BASE}"])
    return {
        "checkpoint_head": CHECKPOINT_HEAD,
        "local_head": local_head,
        "checkpoint_is_ancestor_of_local_head": checkpoint_is_ancestor,
        "remote_base_ref": REMOTE_BASE,
        "remote_base_head": remote_head,
        "remote_base_commits_not_on_checkpoint_count": remote_commit_count,
        "remote_base_recent_subjects": remote_subjects.splitlines() if remote_subjects else [],
        "remote_base_is_not_branch_evidence": True,
    }


def main() -> int:
    print("PR #230 non-chunk cycle-16 reopen-source guard")
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
    future_intake = certs["future_intake"]
    terminal = certs["terminal"]
    reopen = certs["reopen"]
    cycle15 = certs["cycle15_independent"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    blocked_ids = {str(item) for item in list_field(worklist, "blocked_work_unit_ids")}
    closed_ids = {str(item) for item in list_field(worklist, "closed_work_unit_ids")}
    worklist_presence = future_presence(worklist)
    future_intake_presence = future_presence(future_intake)
    terminal_presence = future_presence(terminal)
    reopen_presence = future_presence(reopen)
    cycle15_presence = future_presence(cycle15)
    all_presence_sources = {
        "worklist": worklist_presence,
        "future_intake": future_intake_presence,
        "terminal": terminal_presence,
        "reopen": reopen_presence,
        "cycle15_independent": cycle15_presence,
    }
    presence_keys = sorted(
        {key for source in all_presence_sources.values() for key in source}
    )
    present_by_source = {
        name: present_keys(source) for name, source in all_presence_sources.items()
    }
    presence_sources_all_absent = all(all_false(source) for source in all_presence_sources.values())
    presence_sources_agree = presence_sources_all_absent and all(
        source.get(key) is not True
        for source in all_presence_sources.values()
        for key in presence_keys
    )

    queue_body = " ".join(text(OPPORTUNITY_QUEUE).lower().split())
    handoff_body = " ".join(text(HANDOFF).lower().split())
    remote_state = remote_base_state()

    all_work_units_blocked = blocked_ids == EXPECTED_BLOCKED_UNITS and not closed_ids
    route_family_closed = (
        route_family.get("proposal_allowed") is False
        and not list_field(route_family, "executable_route_ids")
        and dict_field(route_family, "selected_route").get("id")
        == "no_current_surface_nonchunk_route"
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
    cycle15_closed = (
        "cycle-15 independent-route admission gate" in statuses["cycle15_independent"]
        and cycle15.get("proposal_allowed") is False
        and cycle15.get("independent_route_admission_gate_passed") is True
        and cycle15.get("dramatic_step_gate", {}).get("passed") is False
    )
    aggregate_gates_deny = (
        assembly.get("proposal_allowed") is False
        and retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    queue_records_stop_contract = (
        "cycle-15 update" in queue_body
        and "no independent current-surface route is admitted" in queue_body
        and "parseable claim-status artifact" in queue_body
    )
    handoff_records_stop_contract = (
        "treat the pr230 non-chunk current surface as globally exhausted" in handoff_body
        and "parseable claim-status artifact" in handoff_body
    )
    checkpoint_continuity = bool(remote_state["checkpoint_is_ancestor_of_local_head"])

    reopen_source_guard_passed = all(
        [
            not missing_parents,
            not parent_failures,
            not proposal_allowed,
            checkpoint_continuity,
            all_work_units_blocked,
            route_family_closed,
            presence_sources_agree,
            future_intake_closed,
            terminal_closed,
            reopen_closed,
            cycle15_closed,
            aggregate_gates_deny,
            queue_records_stop_contract,
            handoff_records_stop_contract,
        ]
    )

    dramatic_step_gate = {
        "passed": False,
        "admissible_reopen_source_keys": [],
        "present_by_source": present_by_source,
        "reason": (
            "The post-checkpoint surface has no listed same-surface row, "
            "certificate, or theorem to consume.  The only honest action is "
            "to preserve the stop/reopen contract until a parseable artifact "
            "exists and the aggregate gates rerun."
        ),
    }

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("checkpoint-head-is-ancestor", checkpoint_continuity, remote_state["checkpoint_head"])
    report("all-worklist-units-remain-blocked", all_work_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("route-family-selector-remains-closed", route_family_closed, dict_field(route_family, "selected_route").get("id", ""))
    report("all-reopen-sources-absent", presence_sources_agree, f"present_by_source={present_by_source}")
    report("future-intake-gate-remains-closed", future_intake_closed, statuses["future_intake"])
    report("terminal-route-exhaustion-remains-closed", terminal_closed, statuses["terminal"])
    report("reopen-admissibility-remains-closed", reopen_closed, statuses["reopen"])
    report("cycle15-independent-route-admission-remains-closed", cycle15_closed, statuses["cycle15_independent"])
    report("aggregate-gates-deny-proposal", aggregate_gates_deny, f"assembly={statuses['assembly']} campaign={statuses['campaign']}")
    report("opportunity-queue-records-stop-contract", queue_records_stop_contract, "cycle-15 stop/reopen text present")
    report("handoff-records-stop-contract", handoff_records_stop_contract, "post-cycle-15 handoff text present")
    report("reopen-source-guard-passed", reopen_source_guard_passed, f"passed={reopen_source_guard_passed}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk cycle-16 reopen-source "
            "guard: no post-checkpoint same-surface row, certificate, or "
            "theorem is present for admissible reopen; positive closure remains open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Cycle 15 closed independent current-route admission.  Cycle 16 "
            "finds no listed parseable same-surface artifact to consume, all "
            "worklist units remain blocked, and the aggregate gates still deny "
            "proposal authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "reopen_source_guard_passed": reopen_source_guard_passed,
        "dramatic_step_gate": dramatic_step_gate,
        "future_file_presence": worklist_presence,
        "presence_sources": all_presence_sources,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "remote_base_state": remote_state,
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim top-Yukawa closure or proposal authority",
            "does not reopen the non-chunk loop from path text alone",
            "does not load, combine, package, duplicate, or rerun MC chunks",
            "does not use forbidden readout, operator, coupling, target, or unit shortcuts",
            "does not edit paper-facing or authority-table surfaces",
        ],
        "exact_next_action": (
            "Do not select another current-surface non-chunk route on this "
            "branch.  Reopen only after a listed same-surface row, certificate, "
            "or theorem exists as a parseable claim-status artifact; then rerun "
            "reopen-admissibility, worklist, exhaustion, intake, independent-route "
            "admission, this reopen-source guard, assembly, retained-route, and "
            "campaign gates before any proposal language."
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
