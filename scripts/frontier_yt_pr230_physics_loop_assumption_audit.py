#!/usr/bin/env python3
"""
Process/assumption audit for the PR #230 physics-loop campaign.

This is not a new physics theorem.  It checks whether the PR #230 loop package
contains the core physics-loop surfaces the skill expects:

  * explicit assumption/import ledger;
  * orthogonal route portfolio and no-go ledger;
  * assumption sensitivity tests rather than a single tunnel route;
  * claim-status firewall preventing retained overclaim;
  * documented process gaps where the run did not satisfy the full unattended
    campaign ideal.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOOP = ROOT / ".claude/science/physics-loops/yt-pr230-retained-closure-12h-20260501"
OUTPUT = ROOT / "outputs" / "yt_pr230_physics_loop_assumption_audit_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def assert_loop_pack() -> dict[str, object]:
    required = [
        "STATE.yaml",
        "GOAL.md",
        "ASSUMPTIONS_AND_IMPORTS.md",
        "ROUTE_PORTFOLIO.md",
        "OPPORTUNITY_QUEUE.md",
        "NO_GO_LEDGER.md",
        "LITERATURE_BRIDGES.md",
        "ARTIFACT_PLAN.md",
        "CLAIM_STATUS_CERTIFICATE.md",
        "REVIEW_HISTORY.md",
        "HANDOFF.md",
        "PR_BACKLOG.md",
    ]
    missing = [name for name in required if not (LOOP / name).exists()]
    report("loop-pack-required-files", not missing, f"missing={missing}")

    state = text(LOOP / "STATE.yaml")
    pr_backlog = text(LOOP / "PR_BACKLOG.md")
    review_history = text(LOOP / "REVIEW_HISTORY.md")
    direct_pr_branch_exception = "integrated directly into PR #230 by user instruction" in pr_backlog
    review_gap_documented = "No independent review-loop pass has been run" in review_history
    no_bare_retained = "bare_retained_allowed: false" in state
    status_open = "open / no full retained closure" in state

    report(
        "branch-exception-documented",
        direct_pr_branch_exception,
        "skill's separate-branch preference is overridden/documented by explicit PR #230 instruction",
    )
    report(
        "review-loop-gap-documented",
        review_gap_documented,
        "independent review-loop was not run and is explicitly documented",
    )
    report(
        "claim-firewall-open-status",
        no_bare_retained and status_open,
        "state marks no full retained closure and forbids bare retained",
    )

    return {
        "missing_pack_files": missing,
        "branch_exception_documented": direct_pr_branch_exception,
        "review_loop_gap_documented": review_gap_documented,
        "claim_firewall_open_status": no_bare_retained and status_open,
    }


def assert_assumption_ledger() -> dict[str, bool]:
    assumptions = text(LOOP / "ASSUMPTIONS_AND_IMPORTS.md")
    certificate = text(LOOP / "CLAIM_STATUS_CERTIFICATE.md")

    checks = {
        "beta_stationarity_open": "`beta_lambda(M_Pl)=0` | needed selector | open import" in assumptions,
        "observables_comparators_only": "Observed `y_t`, `m_t`, `m_H`" in assumptions
        and "comparators" in assumptions,
        "ward_forbidden": "Old `H_unit` Ward route" in assumptions and "forbidden" in assumptions,
        "production_data_absent": "Direct MC production data" in assumptions and "absent" in assumptions,
        "top_mass_pin_absent": "Top mass parameter pin" in assumptions and "absent" in assumptions,
        "proposal_not_allowed": "proposal_allowed: false" in certificate,
        "bare_retained_forbidden": "bare_retained_allowed: false" in certificate,
    }
    for name, ok in checks.items():
        report(f"assumption-{name}", ok, f"{name}={ok}")
    return checks


def assert_route_fanout() -> dict[str, object]:
    portfolio = text(LOOP / "ROUTE_PORTFOLIO.md")
    no_go = text(LOOP / "NO_GO_LEDGER.md")
    route_headers = re.findall(r"^## R\d+:", portfolio, re.M)
    expected_phrases = [
        "Fixed-lattice scale symmetry",
        "Boundary value implies tangent",
        "Finite source response implies RG tangent",
        "Trace-anomaly route",
        "Multiple-point / Planck stationarity selector",
        "Direct MC",
    ]
    present = {phrase: phrase in portfolio for phrase in expected_phrases}
    report("route-portfolio-six-routes", len(route_headers) >= 6, f"route_headers={len(route_headers)}")
    for phrase, ok in present.items():
        report(f"route-present-{phrase.lower().replace(' ', '-')}", ok, phrase)

    no_go_entries = [
        "`lambda(M_Pl)=0` does not imply `beta_lambda(M_Pl)=0`",
        "Fixed `Z^3` lattice does not supply a scale current",
        "Current Noether theorem does not close quantum trace anomaly",
        "One-sided vacuum stability does not imply beta stationarity",
    ]
    no_go_present = {entry: entry in no_go for entry in no_go_entries}
    for entry, ok in no_go_present.items():
        report(f"no-go-ledger-{entry[:24]}", ok, entry)

    return {
        "route_header_count": len(route_headers),
        "route_phrases_present": present,
        "no_go_entries_present": no_go_present,
    }


def assert_assumption_sensitivity() -> dict[str, object]:
    selector = load_json("outputs/yt_planck_double_criticality_selector_2026-04-30.json")
    beta_no_go = load_json("outputs/yt_beta_lambda_planck_stationarity_no_go_2026-05-01.json")
    scale_no_go = load_json("outputs/yt_scale_stationarity_substrate_no_go_2026-05-01.json")
    trace_no_go = load_json("outputs/yt_trace_anomaly_stationarity_no_go_2026-05-01.json")
    vacuum_no_go = load_json("outputs/yt_vacuum_stability_stationarity_no_go_2026-05-01.json")

    selector_conditional = (
        selector["status"]["actual_current_surface_status"] == "conditional-support / open selector route"
        and selector["status"]["proposal_allowed"] is False
        and selector["fail_count"] == 0
    )
    beta_stationarity_blocked = (
        beta_no_go["actual_current_surface_status"] == "no-go / exact-negative-boundary"
        and beta_no_go["fail_count"] == 0
        and "codimension-one" in beta_no_go["verdict"]
    )
    scale_route_blocked = (
        scale_no_go["z3_automorphism_boundary"]["continuous_dilation_tangent_dimension"] == 0
        and scale_no_go["fail_count"] == 0
    )
    trace_route_blocked = (
        trace_no_go["actual_current_surface_status"] == "no-go / exact-negative-boundary"
        and "quantum EMT/trace-anomaly" in trace_no_go["verdict"]
        and trace_no_go["fail_count"] == 0
    )
    vacuum_route_blocked = (
        vacuum_no_go["actual_current_surface_status"] == "no-go / exact-negative-boundary"
        and "beta_lambda(M_Pl)<=0" in vacuum_no_go["verdict"]
        and vacuum_no_go["fail_count"] == 0
    )

    checks = {
        "if_beta_stationarity_added_selector_runs_conditional": selector_conditional,
        "without_beta_stationarity_algebra_blocks": beta_stationarity_blocked,
        "adding_scale_symmetry_not_supported_current_surface": scale_route_blocked,
        "trace_anomaly_route_not_supported_current_surface": trace_route_blocked,
        "one_sided_stability_gives_inequality_not_selector": vacuum_route_blocked,
    }
    for name, ok in checks.items():
        report(f"sensitivity-{name}", ok, f"{name}={ok}")

    return checks


def assert_artifact_coverage() -> dict[str, bool]:
    artifacts = {
        "top_mass_substrate_pin_no_go": "docs/YT_TOP_MASS_SUBSTRATE_PIN_NO_GO_NOTE_2026-04-30.md",
        "ward_decomp_no_go": "docs/YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md",
        "planck_selector": "docs/YT_PLANCK_DOUBLE_CRITICALITY_SELECTOR_NOTE_2026-04-30.md",
        "beta_lambda_no_go": "docs/YT_BETA_LAMBDA_PLANCK_STATIONARITY_NO_GO_NOTE_2026-05-01.md",
        "scale_stationarity_no_go": "docs/YT_SCALE_STATIONARITY_SUBSTRATE_NO_GO_NOTE_2026-05-01.md",
        "trace_anomaly_no_go": "docs/YT_TRACE_ANOMALY_STATIONARITY_NO_GO_NOTE_2026-05-01.md",
        "vacuum_stability_no_go": "docs/YT_VACUUM_STABILITY_STATIONARITY_NO_GO_NOTE_2026-05-01.md",
    }
    results = {name: (ROOT / path).exists() for name, path in artifacts.items()}
    for name, ok in results.items():
        report(f"artifact-{name}", ok, artifacts[name])
    return results


def main() -> int:
    print("PR #230 physics-loop assumption/route audit")
    print("=" * 72)

    loop_pack = assert_loop_pack()
    assumptions = assert_assumption_ledger()
    routes = assert_route_fanout()
    sensitivity = assert_assumption_sensitivity()
    artifacts = assert_artifact_coverage()

    result = {
        "actual_current_surface_status": "open / no full retained closure",
        "verdict": (
            "The PR #230 physics-loop did perform route fan-out and assumption "
            "sensitivity checks across top-mass pins, Ward decomposition, "
            "Planck double-criticality, beta-lambda algebra, scale symmetry, "
            "trace anomaly, and one-sided vacuum stability.  It did not satisfy "
            "the full ideal campaign process because no independent review-loop "
            "pass or literal 12-hour wall-clock run was completed."
        ),
        "loop_pack": loop_pack,
        "assumptions": assumptions,
        "routes": routes,
        "sensitivity": sensitivity,
        "artifacts": artifacts,
        "documented_process_gaps": [
            "no independent review-loop/backpressure pass",
            "not a literal 12-hour unattended wall-clock execution",
            "integrated directly into PR #230 branch by user instruction rather than separate physics-loop branch",
        ],
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
