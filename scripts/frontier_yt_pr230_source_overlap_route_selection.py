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
    "same_source_pole_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
    "source_higgs_manifest": "outputs/yt_source_higgs_cross_correlator_manifest_2026-05-02.json",
    "source_higgs_gram_gate": "outputs/yt_source_higgs_gram_purity_gate_2026-05-02.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_realization_gate_2026-05-02.json",
    "hunit_operator_gate": "outputs/yt_hunit_canonical_higgs_operator_candidate_gate_2026-05-02.json",
    "source_higgs_import_audit": "outputs/yt_source_higgs_cross_correlator_import_audit_2026-05-02.json",
    "same_source_wz_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "wz_harness_absence": "outputs/yt_wz_response_harness_absence_guard_2026-05-02.json",
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
                "reuses the existing same-source C_ss and dE_top/ds production stream",
                "has an existing algebraic acceptance gate: Res(C_sH)^2 = Res(C_ss) Res(C_HH)",
                "does not require introducing an electroweak gauge-sector MC harness before the first useful test",
            ],
            "current_blockers": [
                "same-surface canonical-Higgs operator O_H is absent",
                "C_sH and C_HH pole rows are absent",
                "H_unit is explicitly not accepted as O_H without pole-purity and canonical-normalization certificates",
                "source-Higgs Gram gate is open, not passed",
            ],
            "first_engineering_step": (
                "implement a same-surface O_H/C_sH/C_HH measurement path or a "
                "candidate O_H operator certificate, then feed it into the Gram-purity gate"
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
            ],
            "current_blockers": [
                "current PR230 harness is QCD top-correlator only",
                "no W/Z mass-response rows or dM_W/ds certificate exist",
                "sector-overlap identity and canonical-Higgs identity are still required",
            ],
            "first_engineering_step": "design a genuine same-source W/Z correlator response harness",
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
    wz_absent = (
        has_false(certs["same_source_wz_gate"], "same_source_wz_response_certificate_gate_passed")
        and "absent" in str(certs["wz_harness_absence"].get("verdict", "")).lower()
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
    report("same-source-fh-lsz-still-supports-measurement", same_source_support, "source-pole coupling support")
    report("gram-gate-open", gram_gate_open, status(certs["source_higgs_gram_gate"]))
    report("canonical-operator-open", canonical_operator_open, status(certs["canonical_higgs_operator_gate"]))
    report("hunit-substitute-blocked", hunit_blocked, status(certs["hunit_operator_gate"]))
    report("csh-data-missing", csh_missing, status(certs["source_higgs_import_audit"]))
    report("wz-route-absent", wz_absent, status(certs["wz_harness_absence"]))
    report("rank-one-route-blocked", rank_one_blocked and tomography_rank_deficient, "rank-one theorem not available")
    report("selected-route-is-gram-purity", selected["route"] == "same_surface_source_higgs_gram_purity", selected["route"])

    result = {
        "actual_current_surface_status": "bounded-support / PR230 source-overlap route selected",
        "verdict": (
            "The best next PR #230 overlap lane is the same-surface "
            "source-Higgs Gram-purity route.  It directly targets the missing "
            "source-pole/canonical-Higgs overlap, reuses the existing same-source "
            "C_ss and dE_top/ds production stream, and has a sharp acceptance "
            "condition.  The W/Z response lane remains the fallback physical "
            "observable route, but it requires a new electroweak gauge-response "
            "harness plus sector-overlap certificates.  Source-only FH/LSZ and "
            "symmetry-only rank-one routes are not closure routes on the current "
            "surface."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "This is a route-selection certificate; no O_H/C_sH/C_HH or W/Z production evidence has been supplied.",
        "selected_primary_route": selected["route"],
        "selected_primary_reason": selected["why"],
        "route_rows": rows,
        "parent_certificates": PARENTS,
        "implementation_packet": {
            "do_now": [
                "keep FH/LSZ chunk reruns running in parallel as source-pole support",
                "start same-surface O_H/C_sH/C_HH implementation or candidate-O_H audit",
                "feed any resulting pole residues through the existing Gram-purity gate",
            ],
            "do_not_do": [
                "do not treat H_unit as O_H",
                "do not treat source-only C_ss as canonical-Higgs purity",
                "do not use static EW W/Z algebra as dM_W/ds",
                "do not claim retained or proposed_retained closure",
            ],
            "fallback": "if O_H remains absent after candidate audit, implement same-source W/Z mass-response harness",
        },
        "strict_non_claims": [
            "not retained y_t closure",
            "not proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not set cos(theta) = 1",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Work the same-surface source-Higgs Gram-purity lane first: implement "
            "or audit a canonical O_H operator on the PR230 surface, then add "
            "C_sH/C_HH pole-residue rows and run the Gram-purity gate.  Keep W/Z "
            "response as the fallback physical-observable route."
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
