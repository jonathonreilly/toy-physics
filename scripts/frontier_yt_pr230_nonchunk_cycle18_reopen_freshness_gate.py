#!/usr/bin/env python3
"""
PR #230 non-chunk cycle-18 reopen-freshness gate.

Cycle 17 stopped current-surface non-chunk route cycling until a listed
same-surface row, certificate, or theorem exists as a parseable claim-status
artifact.  This gate tests the only admissible next non-chunk question:
whether anything has changed since that stop condition which can reopen the
surface.

The runner does not load, combine, package, duplicate, or rerun MC chunks.
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
    / "yt_pr230_nonchunk_cycle18_reopen_freshness_gate_2026-05-05.json"
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
NO_GO_LEDGER = LOOP_PACK / "NO_GO_LEDGER.md"
ROUTE_PORTFOLIO = LOOP_PACK / "ROUTE_PORTFOLIO.md"
CLAIM_STATUS_CERTIFICATE = LOOP_PACK / "CLAIM_STATUS_CERTIFICATE.md"
CYCLE17_HEAD = "4e02c23eb61f966cdd63f46ce4e17844d184cbde"
REMOTE_PR = "origin/claude/yt-direct-lattice-correlator-2026-04-30"

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "route_family": "outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json",
    "exhaustion": "outputs/yt_pr230_nonchunk_current_surface_exhaustion_gate_2026-05-05.json",
    "future_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
    "terminal": "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json",
    "reopen": "outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json",
    "cycle14_selector": "outputs/yt_pr230_nonchunk_cycle14_route_selector_gate_2026-05-05.json",
    "cycle15_independent": "outputs/yt_pr230_nonchunk_cycle15_independent_route_admission_gate_2026-05-05.json",
    "cycle16_reopen_source": "outputs/yt_pr230_nonchunk_cycle16_reopen_source_guard_2026-05-05.json",
    "cycle17_stop_condition": "outputs/yt_pr230_nonchunk_cycle17_stop_condition_gate_2026-05-05.json",
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


def compact(value: str) -> str:
    return " ".join(value.lower().split())


def all_false(presence: dict[str, bool]) -> bool:
    return bool(presence) and not any(presence.values())


def present_keys(presence: dict[str, bool]) -> list[str]:
    return sorted(key for key, value in presence.items() if value)


def listed_future_paths(worklist: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for row in list_field(worklist, "work_units"):
        if not isinstance(row, dict):
            continue
        for rel in row.get("remaining", []):
            if isinstance(rel, str):
                paths.append(rel)
    return sorted(set(paths))


def branch_state() -> dict[str, Any]:
    local_head = git(["rev-parse", "HEAD"])
    remote_pr_head = git(["rev-parse", "--verify", REMOTE_PR])
    return {
        "cycle17_head": CYCLE17_HEAD,
        "local_head": local_head,
        "remote_pr_ref": REMOTE_PR,
        "remote_pr_head": remote_pr_head,
        "cycle17_is_ancestor_of_local_head": git_ok(
            ["merge-base", "--is-ancestor", CYCLE17_HEAD, "HEAD"]
        ),
        "local_head_matches_remote_pr_head": bool(local_head and local_head == remote_pr_head),
        "commits_after_cycle17_on_remote_pr": git(
            ["rev-list", "--count", f"{CYCLE17_HEAD}..{REMOTE_PR}"]
        ),
        "recent_remote_pr_subjects_after_cycle17": (
            git(["log", "--oneline", "--max-count=5", f"{CYCLE17_HEAD}..{REMOTE_PR}"]).splitlines()
            if git(["log", "--oneline", "--max-count=5", f"{CYCLE17_HEAD}..{REMOTE_PR}"])
            else []
        ),
        "remote_pr_state_is_not_reopen_evidence": True,
    }


def main() -> int:
    print("PR #230 non-chunk cycle-18 reopen-freshness gate")
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
    cycle16 = certs["cycle16_reopen_source"]
    cycle17 = certs["cycle17_stop_condition"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    blocked_ids = {str(item) for item in list_field(worklist, "blocked_work_unit_ids")}
    closed_ids = {str(item) for item in list_field(worklist, "closed_work_unit_ids")}
    presence_sources = {
        "worklist": future_presence(worklist),
        "future_intake": future_presence(future_intake),
        "terminal": future_presence(terminal),
        "reopen": future_presence(reopen),
        "cycle15_independent": future_presence(cycle15),
        "cycle16_reopen_source": future_presence(cycle16),
        "cycle17_stop_condition": future_presence(cycle17),
    }
    present_by_source = {name: present_keys(source) for name, source in presence_sources.items()}
    all_presence_absent = all(all_false(source) for source in presence_sources.values())
    future_paths = listed_future_paths(worklist)
    present_future_paths = sorted(rel for rel in future_paths if (ROOT / rel).exists())

    queue_body = compact(text(OPPORTUNITY_QUEUE))
    handoff_body = compact(text(HANDOFF))
    no_go_body = compact(text(NO_GO_LEDGER))
    portfolio_body = compact(text(ROUTE_PORTFOLIO))
    certificate_body = compact(text(CLAIM_STATUS_CERTIFICATE))
    branch = branch_state()

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
    cycle16_closed = (
        "cycle-16 reopen-source guard" in statuses["cycle16_reopen_source"]
        and cycle16.get("proposal_allowed") is False
        and cycle16.get("reopen_source_guard_passed") is True
        and cycle16.get("dramatic_step_gate", {}).get("passed") is False
    )
    cycle17_closed = (
        "cycle-17 stop-condition gate" in statuses["cycle17_stop_condition"]
        and cycle17.get("proposal_allowed") is False
        and cycle17.get("stop_condition_gate_passed") is True
        and cycle17.get("nonchunk_scope_stop_condition_satisfied") is True
        and cycle17.get("dramatic_step_gate", {}).get("passed") is False
    )
    aggregate_gates_deny = (
        assembly.get("proposal_allowed") is False
        and retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    loop_pack_records_stop = (
        "cycle-17 update" in queue_body
        and "non-chunk scope is stopped" in queue_body
        and "cycle 17 tested the stop condition" in handoff_body
        and "stop pr230 current-surface non-chunk route cycling" in handoff_body
        and "continuing pr230 current-surface non-chunk route cycling" in no_go_body
        and "r11: cycle-17 stop-condition gate" in portfolio_body
        and "cycle-17 stop-condition gate" in certificate_body
        and "proposal_allowed: false" in certificate_body
    )
    no_reopen_input = all_presence_absent and not present_future_paths
    branch_fresh = (
        branch["cycle17_is_ancestor_of_local_head"]
        and branch["local_head_matches_remote_pr_head"]
        and branch["commits_after_cycle17_on_remote_pr"] == "0"
    )
    reopen_freshness_gate_passed = all(
        [
            not missing_parents,
            not parent_failures,
            not proposal_allowed,
            branch_fresh,
            all_work_units_blocked,
            route_family_closed,
            future_intake_closed,
            terminal_closed,
            reopen_closed,
            cycle16_closed,
            cycle17_closed,
            no_reopen_input,
            aggregate_gates_deny,
            loop_pack_records_stop,
        ]
    )

    dramatic_step_gate = {
        "passed": False,
        "selected_current_route": "none",
        "present_by_source": present_by_source,
        "present_future_paths": present_future_paths,
        "reason": (
            "Cycle 17 already stopped current-surface non-chunk route cycling. "
            "No listed same-surface row, certificate, or theorem is present as "
            "a parseable reopen artifact, and the remote PR branch has no new "
            "post-cycle-17 commit to inspect."
        ),
    }

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("cycle17-head-is-ancestor", bool(branch["cycle17_is_ancestor_of_local_head"]), branch["cycle17_head"])
    report("remote-pr-branch-aligned", bool(branch["local_head_matches_remote_pr_head"]), branch["remote_pr_head"])
    report("remote-pr-has-no-post-cycle17-commits", branch["commits_after_cycle17_on_remote_pr"] == "0", branch["commits_after_cycle17_on_remote_pr"])
    report("all-worklist-units-remain-blocked", all_work_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("route-family-selector-remains-closed", route_family_closed, dict_field(route_family, "selected_route").get("id", ""))
    report("future-intake-gate-remains-closed", future_intake_closed, statuses["future_intake"])
    report("terminal-route-exhaustion-remains-closed", terminal_closed, statuses["terminal"])
    report("reopen-admissibility-remains-closed", reopen_closed, statuses["reopen"])
    report("cycle16-reopen-source-guard-remains-closed", cycle16_closed, statuses["cycle16_reopen_source"])
    report("cycle17-stop-condition-remains-closed", cycle17_closed, statuses["cycle17_stop_condition"])
    report("no-listed-reopen-input-present", no_reopen_input, f"present_by_source={present_by_source} present_paths={present_future_paths}")
    report("aggregate-gates-deny-proposal", aggregate_gates_deny, f"assembly={statuses['assembly']} campaign={statuses['campaign']}")
    report("loop-pack-records-stop-contract", loop_pack_records_stop, "cycle-17 stop text present")
    report("cycle18-reopen-freshness-gate-passed", reopen_freshness_gate_passed, f"passed={reopen_freshness_gate_passed}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk cycle-18 reopen-freshness "
            "gate: no post-cycle-17 same-surface artifact is present for "
            "admissible reopen; positive closure remains open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Cycle 17 already satisfies the non-chunk stop condition, all "
            "listed reopen inputs remain absent, the remote PR branch has no "
            "new post-cycle-17 commit, and aggregate gates still deny proposal "
            "authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "reopen_freshness_gate_passed": reopen_freshness_gate_passed,
        "nonchunk_scope_remains_stopped": reopen_freshness_gate_passed,
        "dramatic_step_gate": dramatic_step_gate,
        "branch_state": branch,
        "future_file_presence": future_presence(worklist),
        "presence_sources": presence_sources,
        "listed_future_paths": future_paths,
        "present_future_paths": present_future_paths,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim PR230 positive closure or proposal authority",
            "does not convert a stopped queue into positive evidence",
            "does not select a new shortcut route without a parseable same-surface artifact",
            "does not load, combine, package, duplicate, or rerun MC chunks",
            "does not edit paper-facing or authority-table surfaces",
        ],
        "exact_next_action": (
            "Keep PR230 current-surface non-chunk route cycling stopped on this "
            "branch. Reopen only after a listed same-surface row, certificate, "
            "or theorem exists as a parseable claim-status artifact; then rerun "
            "reopen-admissibility, worklist, exhaustion, intake, independent-route, "
            "cycle-16, cycle-17, cycle-18, assembly, retained-route, and campaign "
            "gates before any proposal language."
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
