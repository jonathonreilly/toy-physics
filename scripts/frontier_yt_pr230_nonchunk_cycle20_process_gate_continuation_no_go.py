#!/usr/bin/env python3
"""
PR #230 non-chunk cycle-20 process-gate continuation no-go.

Cycle 19 closed the route-replay question: without a fresh parseable
same-surface row, certificate, or theorem, another current-surface non-chunk
route selection would duplicate an already closed family.  This gate tests the
remaining process-level continuation question: whether another branch-local
process gate can itself count as a new science route after cycle 19.

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
    / "yt_pr230_nonchunk_cycle20_process_gate_continuation_no_go_2026-05-05.json"
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
CYCLE19_HEAD = "e2f319dd7415bc42eea9385e37a6ef8c1a0f786a"
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
    "cycle18_reopen_freshness": "outputs/yt_pr230_nonchunk_cycle18_reopen_freshness_gate_2026-05-05.json",
    "cycle19_no_duplicate_route": "outputs/yt_pr230_nonchunk_cycle19_no_duplicate_route_gate_2026-05-05.json",
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


def compact_text(path: Path) -> str:
    if not path.exists():
        return ""
    return " ".join(path.read_text(encoding="utf-8").lower().split())


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


def route_family_summary(route_family: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in list_field(route_family, "route_families_audited"):
        if not isinstance(row, dict):
            continue
        future_files = row.get("future_files", {})
        if not isinstance(future_files, dict):
            future_files = {}
        rows.append(
            {
                "id": str(row.get("id", "")),
                "route_family": str(row.get("route_family", "")),
                "can_execute_now": row.get("can_execute_now") is True,
                "future_file_keys_present": sorted(
                    str(key) for key, value in future_files.items() if value
                ),
            }
        )
    return rows


def branch_state(future_paths: list[str]) -> dict[str, Any]:
    local_head = git(["rev-parse", "HEAD"])
    remote_pr_head = git(["rev-parse", "--verify", REMOTE_PR])
    local_changed = (
        git(["diff", "--name-only", f"{CYCLE19_HEAD}..HEAD"]).splitlines()
        if local_head and git_ok(["merge-base", "--is-ancestor", CYCLE19_HEAD, "HEAD"])
        else []
    )
    remote_changed = (
        git(["diff", "--name-only", f"{CYCLE19_HEAD}..{REMOTE_PR}"]).splitlines()
        if remote_pr_head
        and git_ok(["merge-base", "--is-ancestor", CYCLE19_HEAD, REMOTE_PR])
        else []
    )
    listed_future_set = set(future_paths)
    changed_future_candidates = sorted(
        listed_future_set.intersection(set(local_changed).union(remote_changed))
    )
    return {
        "cycle19_head": CYCLE19_HEAD,
        "local_head": local_head,
        "remote_pr_ref": REMOTE_PR,
        "remote_pr_head": remote_pr_head,
        "cycle19_is_ancestor_of_local_head": git_ok(
            ["merge-base", "--is-ancestor", CYCLE19_HEAD, "HEAD"]
        ),
        "cycle19_is_ancestor_of_remote_pr": git_ok(
            ["merge-base", "--is-ancestor", CYCLE19_HEAD, REMOTE_PR]
        ),
        "local_head_matches_remote_pr_head": bool(local_head and local_head == remote_pr_head),
        "local_commits_after_cycle19": git(["rev-list", "--count", f"{CYCLE19_HEAD}..HEAD"]),
        "remote_commits_after_cycle19": git(["rev-list", "--count", f"{CYCLE19_HEAD}..{REMOTE_PR}"]),
        "post_cycle19_changed_future_paths": changed_future_candidates,
        "post_cycle19_changes_are_not_reopen_evidence": not changed_future_candidates,
    }


def process_gate_closed(name: str, cert: dict[str, Any], flag: str, text: str) -> bool:
    return (
        text in status(cert)
        and cert.get("proposal_allowed") is False
        and cert.get(flag) is True
        and cert.get("dramatic_step_gate", {}).get("passed") is False
    )


def main() -> int:
    print("PR #230 non-chunk cycle-20 process-gate continuation no-go")
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
    cycle15 = certs["cycle15_independent"]
    cycle16 = certs["cycle16_reopen_source"]
    cycle17 = certs["cycle17_stop_condition"]
    cycle18 = certs["cycle18_reopen_freshness"]
    cycle19 = certs["cycle19_no_duplicate_route"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    blocked_ids = {str(item) for item in list_field(worklist, "blocked_work_unit_ids")}
    closed_ids = {str(item) for item in list_field(worklist, "closed_work_unit_ids")}
    route_rows = route_family_summary(route_family)
    executable_route_ids = [str(item) for item in list_field(route_family, "executable_route_ids")]
    selected_route = dict_field(route_family, "selected_route")

    presence_sources = {
        "worklist": future_presence(worklist),
        "future_intake": future_presence(future_intake),
        "terminal": future_presence(terminal),
        "reopen": future_presence(reopen),
        "cycle15_independent": future_presence(cycle15),
        "cycle16_reopen_source": future_presence(cycle16),
        "cycle17_stop_condition": future_presence(cycle17),
        "cycle18_reopen_freshness": future_presence(cycle18),
    }
    present_by_source = {name: present_keys(source) for name, source in presence_sources.items()}
    all_presence_absent = all(all_false(source) for source in presence_sources.values())
    future_paths = listed_future_paths(worklist)
    present_future_paths = sorted(rel for rel in future_paths if (ROOT / rel).exists())
    branch = branch_state(future_paths)

    queue_body = compact_text(OPPORTUNITY_QUEUE)
    handoff_body = compact_text(HANDOFF)
    no_go_body = compact_text(NO_GO_LEDGER)
    portfolio_body = compact_text(ROUTE_PORTFOLIO)
    certificate_body = compact_text(CLAIM_STATUS_CERTIFICATE)

    all_work_units_blocked = blocked_ids == EXPECTED_BLOCKED_UNITS and not closed_ids
    no_route_family_executable = (
        route_family.get("proposal_allowed") is False
        and selected_route.get("id") == "no_current_surface_nonchunk_route"
        and not executable_route_ids
        and bool(route_rows)
        and not any(row["can_execute_now"] for row in route_rows)
        and not any(row["future_file_keys_present"] for row in route_rows)
    )
    current_surface_exhaustion_closed = (
        "current PR230 non-chunk route queue exhausted" in status(exhaustion)
        and exhaustion.get("proposal_allowed") is False
        and exhaustion.get("current_surface_exhaustion_gate_passed") is True
    )
    process_gate_chain_closed = all(
        [
            current_surface_exhaustion_closed,
            process_gate_closed(
                "future_intake",
                future_intake,
                "future_artifact_intake_gate_passed",
                "future-artifact intake",
            ),
            process_gate_closed(
                "terminal",
                terminal,
                "terminal_route_exhaustion_gate_passed",
                "terminal route-exhaustion gate",
            ),
            process_gate_closed(
                "reopen",
                reopen,
                "reopen_admissibility_gate_passed",
                "reopen-admissibility gate",
            ),
            process_gate_closed(
                "cycle14",
                cycle14,
                "route_selector_gate_passed",
                "cycle-14 route-selector gate",
            ),
            process_gate_closed(
                "cycle15",
                cycle15,
                "independent_route_admission_gate_passed",
                "cycle-15 independent-route admission gate",
            ),
            process_gate_closed(
                "cycle16",
                cycle16,
                "reopen_source_guard_passed",
                "cycle-16 reopen-source guard",
            ),
            process_gate_closed(
                "cycle17",
                cycle17,
                "stop_condition_gate_passed",
                "cycle-17 stop-condition gate",
            )
            and cycle17.get("nonchunk_scope_stop_condition_satisfied") is True,
            process_gate_closed(
                "cycle18",
                cycle18,
                "reopen_freshness_gate_passed",
                "cycle-18 reopen-freshness gate",
            )
            and cycle18.get("nonchunk_scope_remains_stopped") is True,
            process_gate_closed(
                "cycle19",
                cycle19,
                "no_duplicate_route_gate_passed",
                "cycle-19 no-duplicate-route gate",
            )
            and cycle19.get("nonchunk_scope_remains_stopped") is True,
        ]
    )
    aggregate_gates_deny = (
        assembly.get("proposal_allowed") is False
        and retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    no_reopen_input = (
        all_presence_absent
        and not present_future_paths
        and branch["post_cycle19_changes_are_not_reopen_evidence"]
    )
    branch_current = (
        branch["cycle19_is_ancestor_of_local_head"]
        and branch["cycle19_is_ancestor_of_remote_pr"]
        and branch["local_head_matches_remote_pr_head"]
    )
    loop_pack_records_cycle19_stop = (
        "cycle-19 update" in queue_body
        and "no current-surface non-chunk route is admissible" in queue_body
        and "cycle 19 tested the only admissible continuation" in handoff_body
        and "keep pr230 current-surface non-chunk route cycling stopped" in handoff_body
        and "selecting another current-surface non-chunk route after cycle 18" in no_go_body
        and "r13: cycle-19 no-duplicate-route gate" in portfolio_body
        and "cycle-19 no-duplicate-route gate" in certificate_body
        and "proposal_allowed: false" in certificate_body
    )
    process_gate_churn_closed = (
        process_gate_chain_closed
        and all_work_units_blocked
        and no_route_family_executable
        and no_reopen_input
        and aggregate_gates_deny
        and loop_pack_records_cycle19_stop
    )
    process_gate_continuation_no_go_passed = all(
        [
            not missing_parents,
            not parent_failures,
            not proposal_allowed,
            branch_current,
            process_gate_churn_closed,
        ]
    )

    dramatic_step_gate = {
        "passed": False,
        "selected_current_route": "none",
        "selected_process_route": "none",
        "route_family_summaries": route_rows,
        "present_by_source": present_by_source,
        "present_future_paths": present_future_paths,
        "reason": (
            "Cycle 19 already proves that no non-duplicate current route can be "
            "selected without a fresh parseable same-surface artifact.  A new "
            "process-only gate would restate the same stopped surface rather "
            "than retire an import, add support, or create a new no-go."
        ),
    }

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("cycle19-head-is-ancestor-of-local", bool(branch["cycle19_is_ancestor_of_local_head"]), branch["cycle19_head"])
    report("cycle19-head-is-ancestor-of-remote", bool(branch["cycle19_is_ancestor_of_remote_pr"]), branch["remote_pr_head"])
    report("local-and-remote-pr-branch-aligned", bool(branch["local_head_matches_remote_pr_head"]), branch["remote_pr_head"])
    report("post-cycle19-changes-are-not-reopen-evidence", branch["post_cycle19_changes_are_not_reopen_evidence"], str(branch["post_cycle19_changed_future_paths"]))
    report("all-worklist-units-remain-blocked", all_work_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("no-route-family-executable", no_route_family_executable, f"selected={selected_route.get('id')} executable={executable_route_ids}")
    report("process-gate-chain-remains-closed", process_gate_chain_closed, "cycle-8 through cycle-19 process gates deny continuation")
    report("no-listed-reopen-input-present", no_reopen_input, f"present_by_source={present_by_source} present_paths={present_future_paths}")
    report("aggregate-gates-deny-proposal", aggregate_gates_deny, f"assembly={statuses['assembly']} campaign={statuses['campaign']}")
    report("loop-pack-records-cycle19-stop-contract", loop_pack_records_cycle19_stop, "cycle-19 stop text present")
    report("process-gate-churn-is-closed", process_gate_churn_closed, f"passed={process_gate_churn_closed}")
    report("cycle20-process-gate-continuation-no-go-passed", process_gate_continuation_no_go_passed, f"passed={process_gate_continuation_no_go_passed}")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk cycle-20 process-gate "
            "continuation no-go: no further branch-local process gate is an "
            "admissible science route without a fresh parseable same-surface "
            "artifact; positive closure remains open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Cycle 19 already blocks non-duplicate route selection.  All six "
            "worklist units remain blocked, every listed reopen input remains "
            "absent, process gates through cycle 19 remain closed, and aggregate "
            "gates still deny proposal authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "process_gate_continuation_no_go_passed": process_gate_continuation_no_go_passed,
        "nonchunk_scope_remains_stopped": process_gate_continuation_no_go_passed,
        "dramatic_step_gate": dramatic_step_gate,
        "branch_state": branch,
        "presence_source_present_keys": present_by_source,
        "listed_future_paths": future_paths,
        "present_future_paths": present_future_paths,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim PR230 positive closure or proposal authority",
            "does not treat a process-only gate as a proof input",
            "does not create or consume same-surface rows, certificates, or theorems",
            "does not load, combine, package, duplicate, or rerun MC chunks",
            "does not edit paper-facing or authority-table surfaces",
        ],
        "exact_next_action": (
            "Stop PR230 current-surface non-chunk cycling on this branch. Reopen "
            "only after a listed same-surface row, certificate, or theorem exists "
            "as a parseable claim-status artifact; then rerun reopen-admissibility, "
            "worklist, exhaustion, intake, independent-route, cycle-16, cycle-17, "
            "cycle-18, cycle-19, cycle-20, assembly, retained-route, and campaign "
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
