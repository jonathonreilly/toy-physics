#!/usr/bin/env python3
"""
PR #230 source-overlap route selector.

This runner reviews the current PR #230 source-pole/canonical-Higgs overlap
surface and chooses the next engineering lane.  It is deliberately a route
selection certificate, not a closure theorem: no retained/proposed-retained
wording is authorized here.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_pr230_source_overlap_route_selection_2026-05-03.json"

PARENTS = {
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
    "source_functional_lsz_identifiability": "outputs/yt_source_functional_lsz_identifiability_theorem_2026-05-03.json",
    "legendre_source_pole_operator": "outputs/yt_legendre_source_pole_operator_construction_2026-05-03.json",
    "osp_oh_identity_stretch": "outputs/yt_osp_oh_identity_stretch_attempt_2026-05-03.json",
    "same_source_pole_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
    "source_higgs_manifest": "outputs/yt_source_higgs_cross_correlator_manifest_2026-05-02.json",
    "source_higgs_gram_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "fms_oh_construction_attempt": "outputs/yt_fms_oh_certificate_construction_attempt_2026-05-04.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "hunit_operator_gate": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
    "source_higgs_import_audit": "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json",
    "same_source_wz_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "wz_harness_absence": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
    "wz_implementation_plan": "outputs/yt_wz_response_harness_implementation_plan_2026-05-04.json",
    "wz_same_source_ew_action": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_correlator_mass_fit_path": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "gauge_mass_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "neutral_scalar_rank_one": "outputs/yt_neutral_scalar_rank_one_purity_gate_2026-05-02.json",
    "neutral_scalar_tomography": "outputs/yt_neutral_scalar_top_coupling_tomography_gate_2026-05-02.json",
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


def load_json(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def has_false(cert: dict[str, Any], key: str) -> bool:
    return cert.get(key) is False


def route_rows(certs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Return scored route rows.  Scores are engineering priority, not proof."""
    return [
        {
            "route": "same_surface_source_higgs_gram_purity",
            "priority_score": 91,
            "selected_primary": True,
            "why": [
                "directly targets the missing source-pole/canonical-Higgs overlap",
                "the source side now has a clean O_sp Legendre/LSZ normalization certificate",
                "reuses the existing same-source C_ss and dE_top/ds production stream",
                "has an existing algebraic acceptance gate: Res(C_sH)^2 = Res(C_ss) Res(C_HH)",
                "remains the sharpest positive route if a same-surface EW/O_H certificate is supplied",
            ],
            "current_blockers": [
                "FMS construction attempt shows the current PR230 harness lacks a same-surface EW gauge-Higgs/O_H surface",
                "same-surface canonical-Higgs operator O_H is absent",
                "O_sp is not yet proved equal to O_H",
                "C_sH and C_HH pole rows are absent",
                "H_unit is explicitly not accepted as O_H without pole-purity and canonical-normalization certificates",
                "source-Higgs Gram gate is open, not passed",
            ],
            "first_engineering_step": (
                "derive or supply a same-surface EW gauge-Higgs/O_H certificate, "
                "measure O_H/C_sH/C_HH pole rows, then feed them into the "
                "Gram-purity gate"
            ),
            "audit_boundary": "support only until O_H/C_sH/C_HH production rows and retained-route gates pass",
        },
        {
            "route": "same_source_wz_mass_response",
            "priority_score": 76,
            "selected_primary": False,
            "why": [
                "physical observable route can cancel source normalization through dE_top/ds over dM_W/ds",
                "has a clear acceptance certificate schema",
                "good fallback if O_H construction remains blocked",
                "implementation-plan, EW-action, and W/Z mass-fit gates now name the missing work units",
            ],
            "current_blockers": [
                "current PR230 harness is QCD top-correlator only",
                "same-source EW gauge-Higgs action is absent",
                "W/Z correlator mass-fit path is absent",
                "no W/Z mass-response rows or dM_W/ds certificate exist",
                "sector-overlap identity and canonical-Higgs identity are still required",
            ],
            "first_engineering_step": "implement a genuine same-source EW action plus W/Z correlator response harness",
            "audit_boundary": "support only until production W/Z mass fits and identity certificates pass",
        },
        {
            "route": "dynamical_neutral_scalar_rank_one_theorem",
            "priority_score": 48,
            "selected_primary": False,
            "why": [
                "would close the overlap without extra correlator rows if proven",
                "current gates make the exact theorem target explicit",
            ],
            "current_blockers": [
                "symmetry and D17 labels do not force rank one",
                "current dynamics permit a rank-two neutral scalar witness",
                "no existing theorem excludes an orthogonal neutral top-coupled scalar",
            ],
            "first_engineering_step": "derive a genuinely dynamical rank-one theorem or deprioritize",
            "audit_boundary": "analytic route currently blocked by no-go certificates",
        },
        {
            "route": "source_only_fh_lsz",
            "priority_score": 18,
            "selected_primary": False,
            "why": [
                "same-source invariant product is still valuable as a measured source-pole coupling",
                "production chunk work should continue for evidence quality",
            ],
            "current_blockers": [
                "source-only data do not identify canonical-Higgs overlap",
                "source-only data do not set orthogonal neutral scalar top coupling to zero",
            ],
            "first_engineering_step": "continue chunks as supporting data, not as closure",
            "audit_boundary": "cannot close physical y_t without non-source-only identity data",
        },
    ]


def main() -> int:
    print("PR #230 source-overlap route selector")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    retained_open = "retained closure not yet reached" in status(certs["retained_route"])
    campaign_open = "active campaign" in status(certs["campaign_status"])
    source_identifiability_text = str(certs["source_functional_lsz_identifiability"].get("verdict", ""))
    retained_text = str(certs["retained_route"].get("verdict", ""))
    source_only_blocked = (
        "source-only pole data" in source_identifiability_text
        or "source-only data" in source_identifiability_text
        or "source-only C_ss" in retained_text
    )
    same_source_text = str(certs["same_source_pole_sufficiency"].get("verdict", ""))
    same_source_support = (
        "source-rescaling invariant" in same_source_text
        or "source-coordinate normalization freedom" in same_source_text
        or "invariant product" in same_source_text
        or "same-source pole-data sufficiency gate records the positive side" in retained_text
    )
    source_pole_constructed = (
        certs["legendre_source_pole_operator"].get("source_pole_operator_constructed") is True
        and certs["legendre_source_pole_operator"].get("canonical_higgs_operator_identity_passed") is False
    )
    osp_oh_stretch_blocks = (
        "O_sp-to-O_H identity not derived" in status(certs["osp_oh_identity_stretch"])
        and certs["osp_oh_identity_stretch"].get("identity_derived") is False
        and certs["osp_oh_identity_stretch"].get("proposal_allowed") is False
    )
    gram_gate_open = has_false(certs["source_higgs_gram_gate"], "source_higgs_gram_purity_gate_passed")
    canonical_operator_open = has_false(
        certs["canonical_higgs_operator_gate"],
        "canonical_higgs_operator_realization_gate_passed",
    )
    hunit_blocked = has_false(certs["hunit_operator_gate"], "hunit_canonical_higgs_operator_gate_passed")
    csh_missing = has_false(
        certs["source_higgs_import_audit"],
        "source_higgs_cross_correlator_authority_found",
    )
    source_higgs_launch_blocked = (
        "source-Higgs production launch blocked" in status(certs["source_higgs_readiness"])
        and certs["source_higgs_readiness"].get("source_higgs_launch_ready") is False
    )
    fms_oh_surface_blocked = (
        "FMS O_H certificate construction blocked"
        in status(certs["fms_oh_construction_attempt"])
        and certs["fms_oh_construction_attempt"].get("fms_oh_certificate_available") is False
        and certs["fms_oh_construction_attempt"].get("proposal_allowed") is False
    )
    wz_absent = (
        has_false(certs["same_source_wz_gate"], "same_source_wz_response_certificate_gate_passed")
        and "absent" in str(certs["wz_harness_absence"].get("verdict", "")).lower()
    )
    wz_plan_loaded = (
        "WZ response harness implementation plan" in status(certs["wz_implementation_plan"])
        and certs["wz_implementation_plan"].get("proposal_allowed") is False
    )
    wz_ew_action_absent = (
        "same-source EW action not defined" in status(certs["wz_same_source_ew_action"])
        and certs["wz_same_source_ew_action"].get("same_source_ew_action_ready") is False
    )
    wz_massfit_absent = (
        "WZ correlator mass-fit path absent" in status(certs["wz_correlator_mass_fit_path"])
        and certs["wz_correlator_mass_fit_path"].get("wz_correlator_mass_fit_path_ready") is False
    )
    rank_one_blocked = has_false(certs["neutral_scalar_rank_one"], "neutral_scalar_rank_one_purity_gate_passed")
    tomography_rank_deficient = "null direction" in str(
        certs["neutral_scalar_tomography"].get("verdict", "")
    )

    rows = route_rows(certs)
    selected = next(row for row in rows if row["selected_primary"])

    report("parent-certificates-mostly-present", len(missing) <= 1, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("retained-route-open", retained_open, status(certs["retained_route"]))
    report("campaign-open", campaign_open, status(certs["campaign_status"]))
    report("source-only-route-blocked", source_only_blocked, "source-functional LSZ cannot close alone")
    report("legendre-source-pole-operator-available", source_pole_constructed, status(certs["legendre_source_pole_operator"]))
    report("osp-oh-stretch-attempt-blocks-source-only-identity", osp_oh_stretch_blocks, status(certs["osp_oh_identity_stretch"]))
    report("same-source-fh-lsz-still-supports-measurement", same_source_support, "source-pole coupling support")
    report("gram-gate-open", gram_gate_open, status(certs["source_higgs_gram_gate"]))
    report("canonical-operator-open", canonical_operator_open, status(certs["canonical_higgs_operator_gate"]))
    report("hunit-substitute-blocked", hunit_blocked, status(certs["hunit_operator_gate"]))
    report("csh-data-missing", csh_missing, status(certs["source_higgs_import_audit"]))
    report("source-higgs-launch-blocked", source_higgs_launch_blocked, status(certs["source_higgs_readiness"]))
    report("fms-oh-current-surface-blocked", fms_oh_surface_blocked, status(certs["fms_oh_construction_attempt"]))
    report("wz-route-absent", wz_absent, status(certs["wz_harness_absence"]))
    report("wz-implementation-plan-loaded", wz_plan_loaded, status(certs["wz_implementation_plan"]))
    report("wz-ew-action-absent", wz_ew_action_absent, status(certs["wz_same_source_ew_action"]))
    report("wz-massfit-path-absent", wz_massfit_absent, status(certs["wz_correlator_mass_fit_path"]))
    report("rank-one-route-blocked", rank_one_blocked and tomography_rank_deficient, "rank-one theorem not available")
    report(
        "selected-route-is-gram-purity-with-fms-blocker",
        selected["route"] == "same_surface_source_higgs_gram_purity" and fms_oh_surface_blocked,
        selected["route"],
    )

    result = {
        "actual_current_surface_status": "bounded-support / PR230 source-overlap route selected",
        "verdict": (
            "The best next PR #230 overlap lane is the same-surface "
            "source-Higgs Gram-purity route, but the FMS construction attempt "
            "now makes its immediate current-surface blocker explicit.  It directly targets the missing "
            "source-pole/canonical-Higgs overlap.  The source pole now has a "
            "Legendre/LSZ normalized operator O_sp, so the remaining object is "
            "the O_sp/O_H overlap.  A first-principles stretch attempt did not "
            "derive that identity from current source-only, taste, EW, or "
            "rank-one surfaces, and the current PR230 harness lacks a "
            "same-surface EW gauge-Higgs/O_H certificate.  The route reuses the "
            "existing same-source C_ss and dE_top/ds production stream only "
            "after that O_H surface exists.  The W/Z response lane remains the "
            "fallback physical observable route, but it also requires a new "
            "same-source EW action, W/Z correlator mass fits, covariance rows, "
            "and sector-overlap certificates.  Source-only FH/LSZ and "
            "symmetry-only rank-one routes are not closure routes on the current "
            "surface."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This is a route-selection certificate; no O_H/C_sH/C_HH or W/Z production evidence has been supplied.",
        "selected_primary_route": selected["route"],
        "selected_primary_current_surface_blocked": fms_oh_surface_blocked,
        "selected_primary_requires_new_ew_oh_surface": True,
        "selected_primary_reason": selected["why"],
        "route_rows": rows,
        "parent_certificates": PARENTS,
        "implementation_packet": {
            "do_now": [
                "keep FH/LSZ chunk reruns running in parallel as source-pole support",
                "use O_sp as the normalized source side",
                "start a new same-surface EW gauge-Higgs/O_H certificate if that surface is in scope",
                "feed any resulting pole residues through the existing Gram-purity gate",
            ],
            "do_not_do": [
                "do not treat H_unit as O_H",
                "do not treat source-only C_ss as canonical-Higgs purity",
                "do not use static EW W/Z algebra as dM_W/ds",
                "do not claim retained or proposed_retained closure",
            ],
            "fallback": "if O_H remains absent on the current surface, continue FH/LSZ chunks and implement same-source W/Z mass-response only after the EW action surface exists",
        },
        "strict_non_claims": [
            "not retained y_t closure",
            "not proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not set cos(theta) = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Do not cycle back to source-only O_sp/O_H.  The next positive "
            "source-Higgs action is a new same-surface EW gauge-Higgs/O_H "
            "certificate plus C_sH/C_HH pole rows.  If that new surface is not "
            "in scope, keep FH/LSZ production running and pursue W/Z, Schur, or "
            "rank-one alternatives only where they add real rows or theorems."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
