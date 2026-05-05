#!/usr/bin/env python3
"""
PR #230 non-chunk cycle-26 post-cycle-25 main-audit-status-drift reopen guard.

Cycle 25 closed origin/main drift through 0fbd8ecd.  This guard checks the
only new resume fact available at cycle 26: after a fresh fetch, origin/main
advanced again to 3189b67ea, but the new diff still contains only
audit/effective-status surfaces and no listed PR230 same-surface row,
certificate, or theorem.

The runner does not load, combine, package, duplicate, or rerun chunk data.
It does not edit paper-authority surfaces.
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
    / "yt_pr230_nonchunk_cycle26_post_cycle25_main_audit_status_drift_guard_2026-05-05.json"
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
CLAIM_STATUS_CERTIFICATE = LOOP_PACK / "CLAIM_STATUS_CERTIFICATE.md"

CYCLE25_HEAD = "6da4e56893b0d69fd9df30f1d98c214e11d0be8a"
CYCLE25_REMOTE_MAIN_HEAD = "0fbd8ecd41fe4ee6ee84d373c84dc5291953e606"
REMOTE_PR = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
REMOTE_MAIN = "origin/main"
ALLOWED_MAIN_STATUS_DRIFT_PREFIXES = (
    "docs/audit/",
    "docs/publication/ci3_z3/",
)

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "route_family": "outputs/yt_pr230_nonchunk_route_family_import_audit_2026-05-05.json",
    "future_intake": "outputs/yt_pr230_nonchunk_future_artifact_intake_gate_2026-05-05.json",
    "terminal": "outputs/yt_pr230_nonchunk_terminal_route_exhaustion_gate_2026-05-05.json",
    "reopen": "outputs/yt_pr230_nonchunk_reopen_admissibility_gate_2026-05-05.json",
    "cycle18_reopen_freshness": "outputs/yt_pr230_nonchunk_cycle18_reopen_freshness_gate_2026-05-05.json",
    "cycle19_no_duplicate_route": "outputs/yt_pr230_nonchunk_cycle19_no_duplicate_route_gate_2026-05-05.json",
    "cycle20_process_gate": "outputs/yt_pr230_nonchunk_cycle20_process_gate_continuation_no_go_2026-05-05.json",
    "cycle21_remote_reopen": "outputs/yt_pr230_nonchunk_cycle21_remote_reopen_guard_2026-05-05.json",
    "cycle22_main_audit_drift": "outputs/yt_pr230_nonchunk_cycle22_main_audit_drift_guard_2026-05-05.json",
    "cycle23_main_effective_status_drift": "outputs/yt_pr230_nonchunk_cycle23_main_effective_status_drift_guard_2026-05-05.json",
    "cycle24_post_cycle23_main_status_drift": "outputs/yt_pr230_nonchunk_cycle24_post_cycle23_main_status_drift_guard_2026-05-05.json",
    "cycle25_post_cycle24_main_audit_status_drift": "outputs/yt_pr230_nonchunk_cycle25_post_cycle24_main_audit_status_drift_guard_2026-05-05.json",
    "assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

EXPECTED_BLOCKED_UNITS = {
    "canonical_oh_source_higgs",
    "matching_running",
    "neutral_scalar_rank_one",
    "same_source_wz_response",
    "scalar_lsz_model_fv_ir",
    "schur_scalar_denominator_rows",
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
    return (
        subprocess.run(
            ["git", *args],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
        == 0
    )


def git_path_exists(ref: str, rel: str) -> bool:
    return git_ok(["cat-file", "-e", f"{ref}:{rel}"])


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


def compact_text(path: Path) -> str:
    if not path.exists():
        return ""
    return " ".join(path.read_text(encoding="utf-8").lower().split())


def ref_future_presence(ref: str, future_paths: list[str]) -> list[str]:
    if not git(["rev-parse", "--verify", ref]):
        return []
    return sorted(rel for rel in future_paths if git_path_exists(ref, rel))


def diff_future_paths(base: str, ref: str, future_paths: list[str]) -> list[str]:
    if not git(["rev-parse", "--verify", base]) or not git(
        ["rev-parse", "--verify", ref]
    ):
        return []
    changed = set(git(["diff", "--name-only", f"{base}..{ref}"]).splitlines())
    return sorted(set(future_paths).intersection(changed))


def diff_paths(base: str, ref: str) -> list[str]:
    if not git(["rev-parse", "--verify", base]) or not git(
        ["rev-parse", "--verify", ref]
    ):
        return []
    return sorted(git(["diff", "--name-only", f"{base}..{ref}"]).splitlines())


def path_class(path: str) -> str:
    if path.startswith("docs/audit/"):
        return "audit"
    if path.startswith("docs/publication/ci3_z3/"):
        return "publication-effective-status"
    return "other"


def allowed_main_status_drift(path: str) -> bool:
    return path.startswith(ALLOWED_MAIN_STATUS_DRIFT_PREFIXES)


def branch_state(future_paths: list[str]) -> dict[str, Any]:
    local_head = git(["rev-parse", "HEAD"])
    remote_pr_head = git(["rev-parse", "--verify", REMOTE_PR])
    remote_main_head = git(["rev-parse", "--verify", REMOTE_MAIN])
    main_changed_paths = diff_paths(CYCLE25_REMOTE_MAIN_HEAD, REMOTE_MAIN)
    return {
        "cycle25_head": CYCLE25_HEAD,
        "cycle25_remote_main_head": CYCLE25_REMOTE_MAIN_HEAD,
        "local_head": local_head,
        "remote_pr_ref": REMOTE_PR,
        "remote_pr_head": remote_pr_head,
        "remote_main_ref": REMOTE_MAIN,
        "remote_main_head": remote_main_head,
        "cycle25_is_ancestor_of_local_head": git_ok(
            ["merge-base", "--is-ancestor", CYCLE25_HEAD, "HEAD"]
        ),
        "cycle25_is_ancestor_of_remote_pr": git_ok(
            ["merge-base", "--is-ancestor", CYCLE25_HEAD, REMOTE_PR]
        ),
        "cycle25_remote_main_is_ancestor_of_remote_main": git_ok(
            ["merge-base", "--is-ancestor", CYCLE25_REMOTE_MAIN_HEAD, REMOTE_MAIN]
        ),
        "local_head_matches_remote_pr_head": bool(local_head and local_head == remote_pr_head),
        "local_commits_after_cycle25": git(["rev-list", "--count", f"{CYCLE25_HEAD}..HEAD"]),
        "remote_commits_after_cycle25": git(["rev-list", "--count", f"{CYCLE25_HEAD}..{REMOTE_PR}"]),
        "remote_main_commits_after_cycle25_baseline": git(
            ["rev-list", "--count", f"{CYCLE25_REMOTE_MAIN_HEAD}..{REMOTE_MAIN}"]
        ),
        "remote_main_changed_paths_after_cycle25_baseline": main_changed_paths,
        "remote_main_changed_path_classes_after_cycle25_baseline": {
            rel: path_class(rel) for rel in main_changed_paths
        },
        "remote_main_changed_paths_are_status_drift": bool(main_changed_paths)
        and all(allowed_main_status_drift(rel) for rel in main_changed_paths),
        "local_future_paths_present": sorted(
            rel for rel in future_paths if (ROOT / rel).exists()
        ),
        "remote_pr_future_paths_present": ref_future_presence(REMOTE_PR, future_paths),
        "remote_main_future_paths_present": ref_future_presence(REMOTE_MAIN, future_paths),
        "local_changed_future_paths_after_cycle25": diff_future_paths(
            CYCLE25_HEAD, "HEAD", future_paths
        ),
        "remote_pr_changed_future_paths_after_cycle25": diff_future_paths(
            CYCLE25_HEAD, REMOTE_PR, future_paths
        ),
        "remote_main_changed_future_paths_after_cycle25_baseline": diff_future_paths(
            CYCLE25_REMOTE_MAIN_HEAD, REMOTE_MAIN, future_paths
        ),
    }


def process_gate_closed(cert: dict[str, Any], flag: str, marker: str) -> bool:
    return (
        marker in status(cert)
        and cert.get("proposal_allowed") is False
        and cert.get(flag) is True
        and cert.get("dramatic_step_gate", {}).get("passed") is False
    )


def main() -> int:
    print("PR #230 non-chunk cycle-26 post-cycle-25 main-audit-status-drift reopen guard")
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
    cycle18 = certs["cycle18_reopen_freshness"]
    cycle19 = certs["cycle19_no_duplicate_route"]
    cycle20 = certs["cycle20_process_gate"]
    cycle21 = certs["cycle21_remote_reopen"]
    cycle22 = certs["cycle22_main_audit_drift"]
    cycle23 = certs["cycle23_main_effective_status_drift"]
    cycle24 = certs["cycle24_post_cycle23_main_status_drift"]
    cycle25 = certs["cycle25_post_cycle24_main_audit_status_drift"]
    assembly = certs["assembly"]
    retained_route = certs["retained_route"]
    campaign = certs["campaign"]

    future_paths = listed_future_paths(worklist)
    branch = branch_state(future_paths)
    blocked_ids = {str(item) for item in list_field(worklist, "blocked_work_unit_ids")}
    closed_ids = {str(item) for item in list_field(worklist, "closed_work_unit_ids")}
    route_rows = route_family_summary(route_family)
    selected_route = dict_field(route_family, "selected_route")
    executable_route_ids = [str(item) for item in list_field(route_family, "executable_route_ids")]

    presence_sources = {
        "worklist": future_presence(worklist),
        "future_intake": future_presence(future_intake),
        "terminal": future_presence(terminal),
        "reopen": future_presence(reopen),
        "cycle18_reopen_freshness": future_presence(cycle18),
        "cycle22_main_audit_drift": future_presence(cycle22),
        "cycle23_main_effective_status_drift": future_presence(cycle23),
        "cycle24_post_cycle23_main_status_drift": future_presence(cycle24),
        "cycle25_post_cycle24_main_audit_status_drift": future_presence(cycle25),
    }
    present_by_source = {name: present_keys(source) for name, source in presence_sources.items()}
    source_presence_absent = all(not keys for keys in present_by_source.values())
    no_local_or_remote_future_path = not any(
        [
            branch["local_future_paths_present"],
            branch["remote_pr_future_paths_present"],
            branch["remote_main_future_paths_present"],
        ]
    )
    no_changed_future_path_since_cycle25 = not any(
        [
            branch["local_changed_future_paths_after_cycle25"],
            branch["remote_pr_changed_future_paths_after_cycle25"],
            branch["remote_main_changed_future_paths_after_cycle25_baseline"],
        ]
    )

    all_work_units_blocked = blocked_ids == EXPECTED_BLOCKED_UNITS and not closed_ids
    no_route_family_executable = (
        route_family.get("proposal_allowed") is False
        and selected_route.get("id") == "no_current_surface_nonchunk_route"
        and not executable_route_ids
        and bool(route_rows)
        and not any(row["can_execute_now"] for row in route_rows)
        and not any(row["future_file_keys_present"] for row in route_rows)
    )
    parent_process_stack_closed = all(
        [
            process_gate_closed(
                future_intake,
                "future_artifact_intake_gate_passed",
                "future-artifact intake",
            ),
            process_gate_closed(
                terminal,
                "terminal_route_exhaustion_gate_passed",
                "terminal route-exhaustion gate",
            ),
            process_gate_closed(
                reopen,
                "reopen_admissibility_gate_passed",
                "reopen-admissibility gate",
            ),
            process_gate_closed(
                cycle18,
                "reopen_freshness_gate_passed",
                "cycle-18 reopen-freshness gate",
            ),
            process_gate_closed(
                cycle19,
                "no_duplicate_route_gate_passed",
                "cycle-19 no-duplicate-route gate",
            ),
            process_gate_closed(
                cycle20,
                "process_gate_continuation_no_go_passed",
                "cycle-20 process-gate continuation no-go",
            ),
            process_gate_closed(
                cycle21,
                "cycle21_remote_reopen_guard_passed",
                "cycle-21 remote-surface reopen guard",
            ),
            process_gate_closed(
                cycle22,
                "cycle22_main_audit_drift_guard_passed",
                "cycle-22 main-audit-drift reopen guard",
            ),
            process_gate_closed(
                cycle23,
                "cycle23_main_effective_status_drift_guard_passed",
                "cycle-23 main-effective-status-drift reopen guard",
            ),
            process_gate_closed(
                cycle24,
                "cycle24_post_cycle23_main_status_drift_guard_passed",
                "cycle-24 post-cycle-23 main-status-drift reopen guard",
            ),
            process_gate_closed(
                cycle25,
                "cycle25_post_cycle24_main_audit_status_drift_guard_passed",
                "cycle-25 post-cycle-24 main-audit-status-drift reopen guard",
            ),
        ]
    )
    aggregate_gates_deny = (
        assembly.get("proposal_allowed") is False
        and retained_route.get("proposal_allowed") is False
        and campaign.get("proposal_allowed") is False
    )
    branch_current = (
        branch["cycle25_is_ancestor_of_local_head"]
        and branch["cycle25_is_ancestor_of_remote_pr"]
        and branch["cycle25_remote_main_is_ancestor_of_remote_main"]
        and branch["local_head_matches_remote_pr_head"]
        and bool(branch["remote_main_head"])
    )
    loop_pack_records_stop = (
        "cycle-25 update" in compact_text(OPPORTUNITY_QUEUE)
        and "post-cycle-24 main-audit-status-drift reopen guard" in compact_text(HANDOFF)
        and "post-cycle-24 main audit/status drift is not admissible reopen evidence"
        in compact_text(NO_GO_LEDGER)
        and "proposal_allowed: false" in compact_text(CLAIM_STATUS_CERTIFICATE)
    )
    main_drift_since_cycle25_is_status_only = (
        branch["remote_main_commits_after_cycle25_baseline"] != "0"
        and branch["remote_main_changed_paths_are_status_drift"]
        and not branch["remote_main_changed_future_paths_after_cycle25_baseline"]
    )
    no_reopen_input = (
        source_presence_absent
        and no_local_or_remote_future_path
        and no_changed_future_path_since_cycle25
        and main_drift_since_cycle25_is_status_only
    )
    cycle26_post_cycle25_main_audit_status_drift_guard_passed = all(
        [
            not missing_parents,
            not parent_failures,
            not proposal_allowed,
            branch_current,
            all_work_units_blocked,
            no_route_family_executable,
            parent_process_stack_closed,
            aggregate_gates_deny,
            loop_pack_records_stop,
            no_reopen_input,
        ]
    )

    dramatic_step_gate = {
        "passed": False,
        "selected_current_route": "none",
        "selected_remote_route": "none",
        "route_family_summaries": route_rows,
        "present_by_source": present_by_source,
        "branch_state": branch,
        "reason": (
            "Cycle 25 already rejects post-cycle-24 origin/main audit/status "
            "drift as reopen evidence.  Since then origin/main advanced again "
            "only on audit/effective-status surfaces and still contains none "
            "of the listed PR230 same-surface artifacts, so cycle 26 has no "
            "admissible non-chunk route to execute."
        ),
    }

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("parent-certificates-have-no-fails", not parent_failures, f"parent_failures={parent_failures}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("branch-has-cycle25-ancestor-and-remote-main-visible", branch_current, json.dumps(branch, sort_keys=True))
    report("all-worklist-units-remain-blocked", all_work_units_blocked, f"blocked={sorted(blocked_ids)} closed={sorted(closed_ids)}")
    report("no-route-family-executable", no_route_family_executable, f"selected={selected_route.get('id')} executable={executable_route_ids}")
    report("parent-process-stack-closed-through-cycle25", parent_process_stack_closed, "cycle-18 through cycle-25 gates deny continuation")
    report("aggregate-gates-deny-proposal", aggregate_gates_deny, f"assembly={statuses['assembly']} campaign={statuses['campaign']}")
    report("loop-pack-records-cycle25-stop-contract", loop_pack_records_stop, "cycle-25 stop text present")
    report("main-drift-since-cycle25-is-status-only", main_drift_since_cycle25_is_status_only, json.dumps(branch, sort_keys=True))
    report("no-local-or-remote-listed-future-path", no_local_or_remote_future_path, json.dumps(branch, sort_keys=True))
    report("no-changed-listed-future-path-since-cycle25", no_changed_future_path_since_cycle25, json.dumps(branch, sort_keys=True))
    report("no-source-presence-key-set", source_presence_absent, json.dumps(present_by_source, sort_keys=True))
    report(
        "cycle26-post-cycle25-main-audit-status-drift-guard-passed",
        cycle26_post_cycle25_main_audit_status_drift_guard_passed,
        f"passed={cycle26_post_cycle25_main_audit_status_drift_guard_passed}",
    )

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk cycle-26 "
            "post-cycle-25 main-audit-status-drift reopen guard: origin/main "
            "advanced again only on audit/effective-status surfaces and no "
            "listed same-surface artifact is present; positive closure remains open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Cycle 25 already rejects post-cycle-24 origin/main audit/status "
            "drift.  The cycle-25 head remains an ancestor of the aligned PR "
            "heads, origin/main advanced again only on audit/effective-status "
            "paths, no listed same-surface artifact appears on branch or "
            "remote surfaces, all six worklist units remain blocked, and "
            "aggregate gates still deny proposal authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "cycle26_post_cycle25_main_audit_status_drift_guard_passed": (
            cycle26_post_cycle25_main_audit_status_drift_guard_passed
        ),
        "nonchunk_scope_remains_stopped": (
            cycle26_post_cycle25_main_audit_status_drift_guard_passed
        ),
        "dramatic_step_gate": dramatic_step_gate,
        "future_file_presence_by_source": present_by_source,
        "listed_future_paths": future_paths,
        "branch_state": branch,
        "blocked_work_unit_ids": sorted(blocked_ids),
        "closed_work_unit_ids": sorted(closed_ids),
        "parent_statuses": statuses,
        "parent_certificates": PARENTS,
        "strict_non_claims": [
            "does not claim positive closure or proposal authority",
            "does not treat audit/effective-status drift on origin/main as same-surface physics evidence",
            "does not create or consume new same-surface rows, certificates, or theorems",
            "does not load, combine, package, duplicate, or rerun chunk data",
            "does not edit paper-authority surfaces",
        ],
        "exact_next_action": (
            "Stop PR230 current-surface non-chunk cycling on this branch. Reopen "
            "only after a listed same-surface row, certificate, or theorem exists "
            "as a parseable claim-status artifact on the target branch; then rerun "
            "reopen-admissibility, worklist, exhaustion, intake, independent-route, "
            "cycle-16, cycle-17, cycle-18, cycle-19, cycle-20, cycle-21, cycle-22, "
            "cycle-23, cycle-24, cycle-25, cycle-26, assembly, retained-route, and "
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
