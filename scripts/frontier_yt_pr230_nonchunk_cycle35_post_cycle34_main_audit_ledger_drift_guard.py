#!/usr/bin/env python3
"""
PR #230 non-chunk cycle-35 post-cycle-34 main audit-ledger drift guard.

Cycle 34 closed origin/main drift through bbef5c490.  After the next fetch,
origin/main advanced to 457be579b with audit metadata only.  This runner checks
whether that new remote movement supplies any listed PR230 same-surface reopen
artifact.  It does not load or rerun chunk data and it does not claim closure.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_nonchunk_cycle35_post_cycle34_main_audit_ledger_drift_guard_2026-05-05.json"

PREVIOUS_REMOTE_MAIN = "bbef5c4905a034cb75e9d7eaeb12cdcffbb03b25"
REMOTE_PR = "origin/claude/yt-direct-lattice-correlator-2026-04-30"
REMOTE_MAIN = "origin/main"

EXPECTED_AUDIT_METADATA_PATHS = {
    "docs/audit/data/audit_ledger.json",
    "docs/audit/data/citation_graph.json",
}

EXPECTED_BLOCKED_UNITS = {
    "canonical_oh_source_higgs",
    "matching_running",
    "neutral_scalar_rank_one",
    "same_source_wz_response",
    "scalar_lsz_model_fv_ir",
    "schur_scalar_denominator_rows",
}

PARENTS = {
    "worklist": "outputs/yt_pr230_non_chunk_closure_worklist_2026-05-05.json",
    "cycle34": "outputs/yt_pr230_nonchunk_cycle34_post_cycle33_main_nonpr230_drift_guard_2026-05-05.json",
    "completion_audit": "outputs/yt_pr230_positive_closure_completion_audit_2026-05-05.json",
    "assembly": "outputs/yt_pr230_full_positive_closure_assembly_gate_2026-05-04.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
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


def listed_future_paths(worklist: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for row in worklist.get("work_units", []):
        if not isinstance(row, dict):
            continue
        for rel in row.get("remaining", []):
            if isinstance(rel, str):
                paths.append(rel)
    return sorted(set(paths))


def present_future_paths(paths: list[str], ref: str | None = None) -> list[str]:
    present = []
    for rel in paths:
        if ref is None:
            if (ROOT / rel).exists():
                present.append(rel)
        elif git_path_exists(ref, rel):
            present.append(rel)
    return present


def main() -> int:
    print("PR #230 non-chunk cycle-35 post-cycle-34 main audit-ledger drift guard")
    print("=" * 72)

    certs = {name: load(path) for name, path in PARENTS.items()}
    missing_parents = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in certs.items()}

    local_head = git(["rev-parse", "HEAD"])
    remote_pr_head = git(["rev-parse", REMOTE_PR])
    remote_main_head = git(["rev-parse", REMOTE_MAIN])
    previous_main_is_ancestor = git_ok(["merge-base", "--is-ancestor", PREVIOUS_REMOTE_MAIN, REMOTE_MAIN])
    local_head_matches_remote_pr = bool(local_head) and local_head == remote_pr_head

    changed_paths = [
        line
        for line in git(["diff", "--name-only", f"{PREVIOUS_REMOTE_MAIN}..{REMOTE_MAIN}"]).splitlines()
        if line
    ]
    changed_path_set = set(changed_paths)
    audit_metadata_only = bool(changed_paths) and changed_path_set.issubset(EXPECTED_AUDIT_METADATA_PATHS)

    future_paths = listed_future_paths(certs["worklist"])
    changed_future_paths = sorted(changed_path_set.intersection(future_paths))
    local_future_paths = present_future_paths(future_paths)
    remote_pr_future_paths = present_future_paths(future_paths, REMOTE_PR)
    remote_main_future_paths = present_future_paths(future_paths, REMOTE_MAIN)

    blocked_units = set(certs["worklist"].get("blocked_work_unit_ids", []))
    worklist_still_blocked = blocked_units == EXPECTED_BLOCKED_UNITS
    cycle34_closed = (
        "cycle-34 post-cycle-33 main non-PR230 drift reopen guard" in statuses["cycle34"]
        and certs["cycle34"].get("proposal_allowed") is False
        and certs["cycle34"].get("cycle34_post_cycle33_main_nonpr230_drift_guard_passed") is True
        and certs["cycle34"].get("dramatic_step_gate", {}).get("passed") is False
    )
    completion_audit_open = (
        certs["completion_audit"].get("completion_audit_passed") is True
        and certs["completion_audit"].get("closure_achieved") is False
        and certs["completion_audit"].get("proposal_allowed") is False
    )
    aggregate_denies_proposal = (
        certs["assembly"].get("proposal_allowed") is False
        and certs["retained_route"].get("proposal_allowed") is False
        and certs["campaign"].get("proposal_allowed") is False
    )
    no_reopen_artifact = (
        not changed_future_paths
        and not local_future_paths
        and not remote_pr_future_paths
        and not remote_main_future_paths
    )
    dramatic_step_gate = {
        "passed": False,
        "selected_current_route": "none",
        "selected_remote_route": "none",
        "reason": (
            "origin/main advanced after cycle 34 only on audit ledger/citation "
            "metadata.  No listed PR230 same-surface artifact exists locally, "
            "on the PR remote branch, or on origin/main."
        ),
        "changed_future_paths": changed_future_paths,
        "present_by_source": {
            "local": local_future_paths,
            "remote_pr": remote_pr_future_paths,
            "remote_main": remote_main_future_paths,
        },
    }
    guard_passed = (
        not missing_parents
        and not proposal_allowed
        and local_head_matches_remote_pr
        and previous_main_is_ancestor
        and audit_metadata_only
        and no_reopen_artifact
        and worklist_still_blocked
        and cycle34_closed
        and completion_audit_open
        and aggregate_denies_proposal
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("local-head-matches-remote-pr", local_head_matches_remote_pr, f"{local_head} == {remote_pr_head}")
    report("previous-main-is-ancestor-of-origin-main", previous_main_is_ancestor, PREVIOUS_REMOTE_MAIN)
    report("origin-main-advanced", remote_main_head != PREVIOUS_REMOTE_MAIN, f"{PREVIOUS_REMOTE_MAIN}..{remote_main_head}")
    report("changed-paths-are-audit-metadata-only", audit_metadata_only, str(changed_paths))
    report("no-changed-listed-future-paths", not changed_future_paths, str(changed_future_paths))
    report("no-local-listed-future-paths-present", not local_future_paths, str(local_future_paths))
    report("no-remote-pr-listed-future-paths-present", not remote_pr_future_paths, str(remote_pr_future_paths))
    report("no-origin-main-listed-future-paths-present", not remote_main_future_paths, str(remote_main_future_paths))
    report("worklist-six-units-still-blocked", worklist_still_blocked, str(sorted(blocked_units)))
    report("cycle34-remains-closed", cycle34_closed, statuses["cycle34"])
    report("completion-audit-still-open", completion_audit_open, statuses["completion_audit"])
    report("aggregate-gates-deny-proposal", aggregate_denies_proposal, "assembly/retained/campaign proposal_allowed=false")
    report("cycle35-guard-recorded", guard_passed, "nonchunk scope remains stopped")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / PR230 non-chunk cycle-35 post-cycle-34 "
            "main audit-ledger drift reopen guard: origin/main advanced only on "
            "audit ledger/citation metadata with no listed same-surface artifact "
            "present; positive closure remains open"
        ),
        "conditional_surface_status": None,
        "hypothetical_axiom_status": None,
        "admitted_observation_status": None,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "origin/main advanced after cycle 34 only on audit metadata.  The "
            "aligned PR branch, local branch, and origin/main contain none of "
            "the listed PR230 same-surface rows, certificates, or theorems; "
            "all six worklist units remain blocked and aggregate gates still "
            "deny proposal authority."
        ),
        "audit_required_before_effective_retained": True,
        "bare_retained_allowed": False,
        "cycle35_post_cycle34_main_audit_ledger_drift_guard_passed": guard_passed,
        "nonchunk_scope_remains_stopped": True,
        "branch_state": {
            "previous_remote_main": PREVIOUS_REMOTE_MAIN,
            "remote_main_head": remote_main_head,
            "local_head": local_head,
            "remote_pr_head": remote_pr_head,
            "local_head_matches_remote_pr": local_head_matches_remote_pr,
            "previous_main_is_ancestor_of_remote_main": previous_main_is_ancestor,
            "changed_paths_after_cycle34": changed_paths,
            "changed_paths_are_audit_metadata_only": audit_metadata_only,
            "changed_future_paths_after_cycle34": changed_future_paths,
            "local_future_paths_present": local_future_paths,
            "remote_pr_future_paths_present": remote_pr_future_paths,
            "remote_main_future_paths_present": remote_main_future_paths,
        },
        "blocked_work_unit_ids": sorted(blocked_units),
        "closed_work_unit_ids": certs["worklist"].get("closed_work_unit_ids", []),
        "listed_future_paths": future_paths,
        "future_file_presence_by_source": dramatic_step_gate["present_by_source"],
        "dramatic_step_gate": dramatic_step_gate,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim positive closure or proposal authority",
            "does not treat audit ledger/citation metadata drift as PR230 physics evidence",
            "does not create, consume, load, combine, package, duplicate, or rerun chunk data",
            "does not edit paper-authority surfaces",
            "does not use forbidden shortcut inputs or external comparator values",
        ],
        "exact_next_action": (
            "Do not reopen the PR230 non-chunk queue from audit metadata drift. "
            "Reopen only after a listed same-surface row, certificate, or "
            "theorem exists as a parseable claim-status artifact, then rerun "
            "reopen-admissibility, worklist, exhaustion/intake, assembly, "
            "retained-route, and campaign gates before proposal wording."
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
