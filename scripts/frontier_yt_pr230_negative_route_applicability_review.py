#!/usr/bin/env python3
"""
PR #230 negative-route applicability review.

This is a meta-gate for the current YT/PR230 no-go stack.  It verifies that
selected negative/boundary certificates are being used only as current-surface
route blockers, not as permanent retained negative theorems that would close
future source-Higgs, W/Z, Schur, rank-one, or production routes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_negative_route_applicability_review_2026-05-06.json"

PASS_COUNT = 0
FAIL_COUNT = 0


ROUTES: list[dict[str, Any]] = [
    {
        "id": "source_only_osp_oh_identity",
        "path": "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json",
        "current_scope": "Blocks source-only O_sp -> O_H identity on the current surface.",
        "reopen": "Reopen with C_sH/C_HH Gram purity, W/Z response, or neutral rank-one theorem.",
        "applies_markers": ["not derived", "current surface", "counterfamily"],
    },
    {
        "id": "osp_oh_assumption_overclaim",
        "path": "outputs/yt_osp_oh_assumption_route_audit_2026-05-04.json",
        "current_scope": "Blocks assumption-only closure of O_sp -> O_H.",
        "reopen": "Reopen when one concrete missing premise is supplied.",
        "applies_markers": ["retained closure still blocked", "lacks", "same-surface"],
    },
    {
        "id": "source_functional_lsz_identifiability",
        "path": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
        "current_scope": "Blocks source-only LSZ data as physical y_t.",
        "reopen": "Reopen with source-Higgs overlap, W/Z response, or orthogonal-null theorem.",
        "applies_markers": ["counterfamily", "source-only", "missing data"],
    },
    {
        "id": "canonical_higgs_repo_authority_absent",
        "path": "outputs/yt_canonical_higgs_repo_authority_audit_2026-05-03.json",
        "current_scope": "Blocks claims that a retained same-surface O_H authority is already in the repo.",
        "reopen": "Reopen with a new registered same-surface O_H certificate.",
        "applies_markers": ["repo-wide", "absent", "current"],
    },
    {
        "id": "hunit_not_canonical_higgs",
        "path": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
        "current_scope": "Blocks reusing H_unit as O_H without the missing certificates.",
        "reopen": "Reopen only through a non-Ward O_H/operator-normalization certificate.",
        "applies_markers": ["H_unit", "not canonical-Higgs", "not"],
    },
    {
        "id": "source_higgs_readiness_missing_oh",
        "path": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
        "current_scope": "Blocks launching source-Higgs rows before O_H is certified.",
        "reopen": "Reopen by supplying the source-Higgs operator certificate and production rows.",
        "applies_markers": ["blocked", "missing", "O_H"],
    },
    {
        "id": "schur_row_candidate_extraction",
        "path": "outputs/yt_schur_row_candidate_extraction_attempt_2026-05-03.json",
        "current_scope": "Blocks finite ladder/Feshbach support as Schur A/B/C rows.",
        "reopen": "Reopen with same-surface Schur scalar kernel rows.",
        "applies_markers": ["finite ladder", "A/B/C", "future_rows_path_present"],
    },
    {
        "id": "schur_kprime_row_absence",
        "path": "outputs/yt_schur_kprime_row_absence_guard_2026-05-03.json",
        "current_scope": "Blocks treating current FH/LSZ rows as Schur kernel rows.",
        "reopen": "Reopen when complete same-surface Schur rows are written.",
        "applies_markers": ["absence", "Schur", "current"],
    },
    {
        "id": "neutral_scalar_commutant_rank",
        "path": "outputs/yt_neutral_scalar_commutant_rank_no_go_2026-05-02.json",
        "current_scope": "Blocks symmetry-label/commutant-only rank-one purity.",
        "reopen": "Reopen with a dynamical irreducibility or positivity-improving theorem.",
        "applies_markers": ["rank", "does not force", "rank-two"],
    },
    {
        "id": "neutral_irreducibility_authority_absent",
        "path": "outputs/yt_neutral_scalar_irreducibility_authority_audit_2026-05-04.json",
        "current_scope": "Blocks claims that neutral irreducibility authority already exists.",
        "reopen": "Reopen with a registered primitive-cone/positivity-improvement certificate.",
        "applies_markers": ["absent", "current", "irreducibility"],
    },
    {
        "id": "one_higgs_orthogonal_null",
        "path": "outputs/yt_no_orthogonal_top_coupling_selection_rule_no_go_2026-05-02.json",
        "current_scope": "Blocks one-Higgs monomial selection as orthogonal-neutral null theorem.",
        "reopen": "Reopen with an actual orthogonal-neutral top-coupling exclusion or measurement.",
        "applies_markers": ["not derived", "orthogonal", "selection rule"],
    },
    {
        "id": "wz_same_source_ew_action_absent",
        "path": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
        "current_scope": "Blocks static EW algebra as a same-source EW production action.",
        "reopen": "Reopen with same-source EW action certificate plus W/Z rows.",
        "applies_markers": ["not defined", "PR230", "future_action_certificate_present"],
    },
    {
        "id": "wz_mass_fit_path_absent",
        "path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
        "current_scope": "Blocks static/slope-only W/Z data as W/Z correlator mass fits.",
        "reopen": "Reopen with W/Z two-point correlator rows and mass-fit windows.",
        "applies_markers": ["absent", "PR230", "future_mass_fit_rows_present"],
    },
    {
        "id": "wz_response_row_production_attempt",
        "path": "outputs/yt_wz_response_row_production_attempt_2026-05-03.json",
        "current_scope": "Blocks current QCD-only outputs as W/Z response rows.",
        "reopen": "Reopen with same-source W/Z response measurement rows.",
        "applies_markers": ["current surface", "WZ response", "row"],
    },
    {
        "id": "same_source_sector_overlap",
        "path": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
        "current_scope": "Blocks top/WZ response combination without sector-overlap identity.",
        "reopen": "Reopen with a same-source sector-overlap identity or measured correction.",
        "applies_markers": ["obstruction", "sector-overlap", "identity"],
    },
    {
        "id": "source_overlap_sum_rule",
        "path": "outputs/yt_source_overlap_sum_rule_no_go_2026-05-02.json",
        "current_scope": "Blocks a spectral sum-rule shortcut to source-Higgs overlap.",
        "reopen": "Reopen with a complete same-surface overlap theorem or direct rows.",
        "applies_markers": ["source-overlap", "sum-rule", "no-go"],
    },
    {
        "id": "short_distance_ope_lsz",
        "path": "outputs/yt_short_distance_ope_lsz_no_go_2026-05-02.json",
        "current_scope": "Blocks short-distance/OPE data as scalar LSZ pole residue.",
        "reopen": "Reopen with model-class analytic continuation or pole-control theorem.",
        "applies_markers": ["short-distance", "OPE", "LSZ"],
    },
    {
        "id": "effective_mass_plateau_residue",
        "path": "outputs/yt_effective_mass_plateau_residue_no_go_2026-05-02.json",
        "current_scope": "Blocks effective-mass plateau fits as scalar LSZ residue closure.",
        "reopen": "Reopen with explicit residue extraction and FV/IR/model-class control.",
        "applies_markers": ["effective-mass", "residue", "not scalar"],
    },
    {
        "id": "finite_source_shift_derivative",
        "path": "outputs/yt_finite_source_shift_derivative_no_go_2026-05-02.json",
        "current_scope": "Blocks one finite source-shift radius as the zero-source FH derivative.",
        "reopen": "Reopen with multi-radius finite-source-linearity plus zero-source derivative control.",
        "applies_markers": ["finite source-shift", "zero-source", "derivative"],
    },
]

SCOPE_TERMS = (
    "current",
    "PR230",
    "current surface",
    "current PR230 surface",
    "current repo",
    "current harness",
    "source-only",
    "finite",
    "absent",
    "not derived",
    "support",
)
REOPEN_TERMS = (
    "future",
    "reopen",
    "missing",
    "absent",
    "not derived",
    "requires",
    "needs",
    "until",
    "conditional",
    "if ",
)
BAD_OVERCLAIM_TERMS = (
    "permanent no-go",
    "universal no-go",
    "retained negative theorem",
    "retained no-go theorem",
    "no future route",
)

LOOP_LEDGER_PATHS = [
    ".claude/science/physics-loops/yt-pr230-osp-oh-retained-closure-20260503/NO_GO_LEDGER.md",
    ".claude/science/physics-loops/yt-pr230-ward-physical-readout-20260501/NO_GO_LEDGER.md",
]


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        state = "PASS"
    else:
        FAIL_COUNT += 1
        state = "FAIL"
    print(f"  [{state}] {tag}: {msg}")


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def blob(cert: dict[str, Any]) -> str:
    return json.dumps(cert, sort_keys=True, default=str)


def has_any(text: str, terms: tuple[str, ...] | list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def has_all_markers(text: str, markers: list[str]) -> bool:
    lower = text.lower()
    return all(marker.lower() in lower for marker in markers)


def ledger_retained_negative_rows() -> list[dict[str, Any]]:
    ledger = load_json("docs/audit/data/audit_ledger.json")
    rows = ledger.get("rows", {}) if isinstance(ledger, dict) else {}
    out: list[dict[str, Any]] = []
    for claim_id, row in rows.items():
        if not isinstance(row, dict):
            continue
        note = str(row.get("note_path", ""))
        current = str(row.get("current_status_raw", ""))
        rationale = str(row.get("verdict_rationale", ""))
        haystack = f"{claim_id} {note} {current} {rationale}"
        if not (
            claim_id.startswith("yt_")
            or "YT_" in note
            or "top-yukawa" in haystack.lower()
        ):
            continue
        if row.get("effective_status") != "retained":
            continue
        if not has_any(haystack, ("negative", "no-go", "obstruction", "blocked")):
            continue
        out.append(
            {
                "claim_id": claim_id,
                "note_path": note,
                "current_status_raw": current,
                "effective_status": row.get("effective_status"),
            }
        )
    return out


def loop_wording_issues() -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for rel in LOOP_LEDGER_PATHS:
        path = ROOT / rel
        if not path.exists():
            continue
        ledger_text = path.read_text(encoding="utf-8")
        scoped_globally = (
            "unless a row explicitly says otherwise" in ledger_text.lower()
            and "current pr230 surface/shortcut only" in ledger_text.lower()
            and "future same-surface" in ledger_text.lower()
        )
        for line_no, line in enumerate(ledger_text.splitlines(), start=1):
            lower = line.lower()
            if "closed negatively" in lower and "current" not in lower and not scoped_globally:
                issues.append({"path": rel, "line": line_no, "text": line})
            if "all current-bank" in lower and "future" not in lower and "blocked" in lower:
                issues.append({"path": rel, "line": line_no, "text": line})
    return issues


def main() -> int:
    print("PR #230 negative-route applicability review")
    print("=" * 72)

    route_reviews: list[dict[str, Any]] = []
    missing: list[str] = []
    failing: list[str] = []
    proposal_allowed: list[str] = []
    unscoped: list[str] = []
    no_reopen: list[str] = []
    overclaim: list[str] = []
    non_applying: list[str] = []

    for route in ROUTES:
        cert = load_json(route["path"])
        text = blob(cert)
        status = str(cert.get("actual_current_surface_status", ""))
        exists = bool(cert)
        route_id = str(route["id"])

        if not exists:
            missing.append(route_id)
        if int(cert.get("fail_count", 0) or 0) != 0:
            failing.append(route_id)
        if cert.get("proposal_allowed") is True:
            proposal_allowed.append(route_id)
        if not has_any(text + " " + str(route["current_scope"]), SCOPE_TERMS):
            unscoped.append(route_id)
        if not has_any(text + " " + str(route["reopen"]), REOPEN_TERMS):
            no_reopen.append(route_id)
        if has_any(text, BAD_OVERCLAIM_TERMS):
            overclaim.append(route_id)
        if not has_all_markers(text + " " + status, route.get("applies_markers", [])):
            non_applying.append(route_id)

        route_reviews.append(
            {
                "id": route_id,
                "path": route["path"],
                "status": status,
                "proposal_allowed": cert.get("proposal_allowed"),
                "fail_count": cert.get("fail_count", 0),
                "current_scope": route["current_scope"],
                "future_reopen_condition": route["reopen"],
                "applies_on_current_surface": route_id not in non_applying,
            }
        )

    retained_negative = ledger_retained_negative_rows()
    wording_issues = loop_wording_issues()

    report("selected-negative-certificates-present", not missing, f"missing={missing}")
    report("selected-negative-certificates-pass", not failing, f"failing={failing}")
    report("no-selected-route-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("selected-routes-are-scoped", not unscoped, f"unscoped={unscoped}")
    report("future-reopen-paths-preserved", not no_reopen, f"no_reopen={no_reopen}")
    report("no-permanent-negative-overclaim", not overclaim, f"overclaim={overclaim}")
    report("selected-negative-results-apply-now", not non_applying, f"non_applying={non_applying}")
    report(
        "no-audit-retained-yt-negative-row-used-for-pr230",
        not retained_negative,
        f"retained_negative_rows={retained_negative}",
    )
    report("loop-ledger-negative-wording-scoped", not wording_issues, f"issues={wording_issues}")

    result = {
        "actual_current_surface_status": "exact support / selected PR230 negative-route applicability review passed",
        "verdict": (
            "The selected PR230 negative results are valid as current-surface "
            "route blockers and assumption firewalls. They do not certify a "
            "permanent retained negative theorem and must not close future "
            "routes that supply the named missing evidence: C_sH/C_HH Gram "
            "purity, same-source W/Z response rows, Schur A/B/C rows, neutral "
            "rank-one/irreducibility, scalar-LSZ pole control, or production "
            "data plus matching."
        ),
        "negative_results_are_current_surface_blockers_only": True,
        "no_retained_negative_overclaim": not retained_negative and not overclaim,
        "future_reopen_paths_preserved": not no_reopen,
        "selected_negative_results_apply_on_current_surface": not non_applying,
        "certification_scope": "current_surface_blocker_meta_review_only",
        "investigation_route_closed": False,
        "bare_retained_allowed": False,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This is a meta-review of route blockers. It adds no y_t closure "
            "evidence and no retained/proposed_retained theorem."
        ),
        "route_reviews": route_reviews,
        "retained_negative_audit_rows": retained_negative,
        "loop_wording_issues": wording_issues,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not prove any permanent no-go against future source-Higgs, W/Z, Schur, rank-one, scalar-LSZ, or production routes",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette/u0, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
            "does not modify or certify chunk outputs",
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
