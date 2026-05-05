#!/usr/bin/env python3
"""
PR #230 same-source EW action gate for the W/Z response route.

The W/Z bypass can only become a measurement route after a real electroweak
gauge/Higgs action block is defined with the same scalar source coordinate used
by the top FH/LSZ run.  This gate checks the current repo surface for that
block.  It does not synthesize W/Z rows and it does not treat static EW
gauge-mass algebra as a same-source lattice action.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_same_source_ew_action_gate_2026-05-04.json"

PRODUCTION_HARNESS = ROOT / "scripts" / "yt_direct_lattice_correlator_production.py"
MINIMAL_AXIOMS = ROOT / "docs" / "MINIMAL_AXIOMS_2026-04-11.md"
NATIVE_GAUGE = ROOT / "docs" / "NATIVE_GAUGE_CLOSURE_NOTE.md"
EW_GAUGE_MASS_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"
SM_ONE_HIGGS_NOTE = ROOT / "docs" / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
SU2_BETA_NOTE = ROOT / "docs" / "SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM_NOTE_2026-04-26.md"
FUTURE_ACTION_CERT = ROOT / "outputs" / "yt_wz_same_source_ew_action_certificate_2026-05-04.json"
FUTURE_ROWS = ROOT / "outputs" / "yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json"

PARENTS = {
    "wz_implementation_plan": "outputs/yt_wz_response_harness_implementation_plan_2026-05-04.json",
    "wz_action_certificate_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "wz_observable_gap": "outputs/yt_fh_gauge_mass_response_observable_gap_2026-05-02.json",
    "wz_row_production_attempt": "outputs/yt_wz_response_row_production_attempt_2026-05-03.json",
    "wz_repo_import_audit": "outputs/yt_wz_response_repo_harness_import_audit_2026-05-03.json",
    "wz_builder": "outputs/yt_fh_gauge_mass_response_certificate_builder_2026-05-03.json",
    "same_source_wz_gate": "outputs/yt_same_source_wz_response_certificate_gate_2026-05-02.json",
    "sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "canonical_higgs_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
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
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def action_contract() -> list[dict[str, Any]]:
    return [
        {
            "id": "dynamical_ew_fields",
            "required": "lattice SU(2)_L and U(1)_Y gauge fields with update or ensemble semantics",
            "current_surface": "native gauge notes give structural SU(2)/hypercharge support, not a same-source EW production action",
        },
        {
            "id": "canonical_higgs_radial_source",
            "required": "scalar source s coupled to the canonical Higgs radial direction",
            "current_surface": "current top harness source is an additive staggered mass/source coordinate; canonical O_H certificate is absent",
        },
        {
            "id": "matched_top_wz_source_coordinate",
            "required": "certificate that the top dE/ds source and W/Z dM/ds source are the same coordinate",
            "current_surface": "sector-overlap and canonical-Higgs identity gates remain open",
        },
        {
            "id": "wz_correlator_observables",
            "required": "W/Z two-point correlators and mass fits under source shifts",
            "current_surface": "production harness has a W/Z absent guard and no W/Z correlator CLI path",
        },
        {
            "id": "firewall",
            "required": "explicit exclusion of H_unit, yt_ward, observed masses/couplings, alpha_LM, plaquette/u0, and static EW algebra",
            "current_surface": "existing W/Z gates enforce this firewall; this gate keeps it active",
        },
    ]


def shortcut_rejections() -> list[dict[str, str]]:
    return [
        {
            "candidate": "EW Higgs gauge-mass diagonalization theorem",
            "classification": "tree-level dictionary after canonical H is supplied",
            "why_not_action": "It proves M_W(g,v) and M_Z(g,gY,v), not a lattice EW action or dM_W/ds measurement.",
        },
        {
            "candidate": "native gauge closure / SU(2) structural notes",
            "classification": "structural gauge support",
            "why_not_action": "They do not provide a same-source SU(2)xU(1) production action with W/Z correlator rows.",
        },
        {
            "candidate": "SM one-Higgs Yukawa/gauge selection",
            "classification": "operator-pattern support after H is supplied",
            "why_not_action": "It does not identify the PR230 source with canonical O_H or define W/Z source shifts.",
        },
        {
            "candidate": "top FH/LSZ production harness",
            "classification": "QCD top and scalar-source response harness",
            "why_not_action": "It has no raw W/Z correlator mass-fit path and explicitly guards W/Z response as absent.",
        },
    ]


def main() -> int:
    print("PR #230 same-source EW action gate")
    print("=" * 72)

    certs = {name: load_json(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in certs.items() if not cert]
    proposal_allowed = [name for name, cert in certs.items() if cert.get("proposal_allowed") is True]

    production_text = read_text(PRODUCTION_HARNESS)
    minimal_text = read_text(MINIMAL_AXIOMS)
    native_text = read_text(NATIVE_GAUGE)
    ew_text = read_text(EW_GAUGE_MASS_NOTE)
    sm_higgs_text = read_text(SM_ONE_HIGGS_NOTE)
    su2_beta_text = read_text(SU2_BETA_NOTE)
    contract = action_contract()
    rejections = shortcut_rejections()

    implementation_plan_names_ew_action = any(
        row.get("id") == "ew_same_source_action"
        for row in certs["wz_implementation_plan"].get("implementation_work_units", [])
    )
    current_harness_is_qcd_top = (
        "Cl3Z3_SU3_Wilson_staggered" in production_text
        and "staggered_top_correlator_mass_extraction" in production_text
    )
    current_harness_wz_absent_guard = (
        '"wz_mass_response"' in production_text
        and '"implementation_status": "absent_guarded"' in production_text
    )
    current_harness_has_wz_smoke_schema_path = all(
        token in production_text
        for token in (
            "--wz-mass-response-smoke",
            "smoke_schema_enabled_not_ew_production",
            "synthetic_scout_contract_not_EW_field",
        )
    )
    current_harness_has_real_wz_path = any(
        token in production_text
        for token in (
            "wz_correlator_measurement",
            "fit_wz_mass_correlator",
            "gauge_mass_response_analysis",
            "per_source_shift_mass_fits",
        )
    ) or (
        "--wz-source-shifts" in production_text
        and not current_harness_has_wz_smoke_schema_path
    )
    minimal_axioms_are_staggered_su3 = (
        "staggered-Dirac partition" in minimal_text
        and "g_bare = 1" in minimal_text
        and "graph-first structural `SU(3)`" in minimal_text
    )
    native_gauge_is_structural_not_action = (
        "exact native cubic `Cl(3)` / `SU(2)` algebra" in native_text
        and "downstream phenomenology remains separate" in native_text
    )
    ew_note_is_static_tree_dictionary = (
        "Assume a neutral Higgs vacuum" in ew_text
        and "standard covariant derivative" in ew_text
        and "M_W = g_2 v / 2" in ew_text
    )
    sm_note_after_h_supplied = (
        "does not select the numerical entries" in sm_higgs_text
        or "does not select numerical Yukawa entries" in sm_higgs_text
    )
    su2_beta_is_running_not_action = (
        "1-loop" in su2_beta_text
        and "does NOT claim" in su2_beta_text
        and "open Science Lane" in su2_beta_text
    )
    future_action_cert_present = FUTURE_ACTION_CERT.exists()
    future_action_cert_valid = (
        certs["wz_action_certificate_builder"].get("same_source_ew_action_certificate_valid")
        is True
    )
    future_rows_present = FUTURE_ROWS.exists()
    observable_gap_open = (
        "FH gauge-mass response observable gap" in status(certs["wz_observable_gap"])
        and certs["wz_observable_gap"].get("gauge_mass_response_observable_ready") is False
    )
    row_production_still_negative = (
        "WZ response row production attempt" in status(certs["wz_row_production_attempt"])
        and certs["wz_row_production_attempt"].get("measurement_rows_written") is False
    )
    repo_import_finds_no_hidden_harness = (
        certs["wz_repo_import_audit"].get("repo_wz_response_harness_found") is False
        and certs["wz_repo_import_audit"].get("exact_negative_boundary_passed") is True
    )
    builder_rows_absent = (
        "same-source WZ response rows absent" in status(certs["wz_builder"])
        and certs["wz_builder"].get("input_present") is False
    )
    same_source_gate_open = (
        "same-source WZ response certificate gate not passed" in status(certs["same_source_wz_gate"])
        and certs["same_source_wz_gate"].get("same_source_wz_response_certificate_gate_passed") is False
    )
    sector_identity_open = (
        "same-source sector-overlap identity obstruction" in status(certs["sector_overlap"])
        and certs["sector_overlap"].get("sector_overlap_identity_gate_passed") is False
    )
    canonical_higgs_gate_open = (
        "canonical-Higgs operator certificate absent" in status(certs["canonical_higgs_gate"])
        and certs["canonical_higgs_gate"].get("candidate_valid") is False
    )
    retained_route_open = (
        "closure not yet reached" in status(certs["retained_route"])
        and certs["retained_route"].get("proposal_allowed") is False
    )
    same_source_ew_action_ready = future_action_cert_valid

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("implementation-plan-names-ew-action-work-unit", implementation_plan_names_ew_action, "ew_same_source_action")
    report("current-harness-is-qcd-top", current_harness_is_qcd_top, display(PRODUCTION_HARNESS))
    report("current-harness-wz-absent-guarded", current_harness_wz_absent_guard, display(PRODUCTION_HARNESS))
    report(
        "current-harness-has-wz-smoke-schema-path",
        current_harness_has_wz_smoke_schema_path,
        "default-off synthetic schema path only",
    )
    report(
        "current-harness-has-no-real-wz-path",
        not current_harness_has_real_wz_path,
        "no production W/Z correlator or mass-slope CLI",
    )
    report("minimal-axioms-do-not-supply-ew-action", minimal_axioms_are_staggered_su3, display(MINIMAL_AXIOMS))
    report("native-gauge-is-structural-not-production-action", native_gauge_is_structural_not_action, display(NATIVE_GAUGE))
    report("ew-gauge-mass-note-is-static-dictionary", ew_note_is_static_tree_dictionary, display(EW_GAUGE_MASS_NOTE))
    report("sm-one-higgs-note-after-h-supplied", sm_note_after_h_supplied, display(SM_ONE_HIGGS_NOTE))
    report("su2-beta-note-not-ew-action", su2_beta_is_running_not_action, display(SU2_BETA_NOTE))
    report("future-ew-action-certificate-absent", not future_action_cert_present, display(FUTURE_ACTION_CERT))
    report(
        "future-ew-action-certificate-builder-loaded",
        "same-source EW action certificate" in status(certs["wz_action_certificate_builder"]),
        status(certs["wz_action_certificate_builder"]),
    )
    report(
        "future-ew-action-certificate-not-valid",
        not future_action_cert_valid,
        f"valid={future_action_cert_valid}",
    )
    report("future-wz-row-file-absent", not future_rows_present, display(FUTURE_ROWS))
    report("observable-gap-still-open", observable_gap_open, status(certs["wz_observable_gap"]))
    report("row-production-still-negative", row_production_still_negative, status(certs["wz_row_production_attempt"]))
    report("repo-import-finds-no-hidden-wz-harness", repo_import_finds_no_hidden_harness, status(certs["wz_repo_import_audit"]))
    report("builder-rows-absent", builder_rows_absent, status(certs["wz_builder"]))
    report("same-source-wz-gate-open", same_source_gate_open, status(certs["same_source_wz_gate"]))
    report("sector-identity-open", sector_identity_open, status(certs["sector_overlap"]))
    report("canonical-higgs-gate-open", canonical_higgs_gate_open, status(certs["canonical_higgs_gate"]))
    report("retained-route-open", retained_route_open, status(certs["retained_route"]))
    report("same-source-ew-action-not-ready", not same_source_ew_action_ready, f"same_source_ew_action_ready={same_source_ew_action_ready}")

    result = {
        "actual_current_surface_status": "exact negative boundary / same-source EW action not defined on PR230 surface",
        "verdict": (
            "The first W/Z implementation work unit is not satisfied on the "
            "current PR230 surface.  Existing EW/Higgs notes supply static "
            "tree-level dictionaries after canonical H is supplied, and native "
            "gauge notes supply structural SU(2)/hypercharge support, but no "
            "same-source SU(2)xU(1)/Higgs production action, W/Z correlator "
            "mass-fit path, top/WZ source-coordinate identity, or canonical "
            "Higgs pole identity is present.  Static EW algebra, the QCD "
            "top harness absent guard, and the synthetic smoke-schema path "
            "remain rejected as W/Z measurement data."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No same-source EW action certificate, W/Z correlator rows, sector-overlap identity, or canonical-Higgs identity exists.",
        "bare_retained_allowed": False,
        "same_source_ew_action_ready": same_source_ew_action_ready,
        "action_block_written": False,
        "future_action_certificate": display(FUTURE_ACTION_CERT),
        "future_action_certificate_builder": PARENTS["wz_action_certificate_builder"],
        "future_action_certificate_present": future_action_cert_present,
        "future_action_certificate_valid": future_action_cert_valid,
        "future_rows_path": display(FUTURE_ROWS),
        "action_contract": contract,
        "shortcut_rejections": rejections,
        "parent_certificates": PARENTS,
        "current_surface_findings": {
            "qcd_top_harness": display(PRODUCTION_HARNESS),
            "current_harness_is_qcd_top": current_harness_is_qcd_top,
            "current_harness_wz_absent_guard": current_harness_wz_absent_guard,
            "current_harness_has_wz_smoke_schema_path": current_harness_has_wz_smoke_schema_path,
            "current_harness_has_real_wz_path": current_harness_has_real_wz_path,
            "minimal_axioms_surface": display(MINIMAL_AXIOMS),
            "native_gauge_surface": display(NATIVE_GAUGE),
            "ew_tree_dictionary_surface": display(EW_GAUGE_MASS_NOTE),
            "sm_one_higgs_surface": display(SM_ONE_HIGGS_NOTE),
            "su2_beta_surface": display(SU2_BETA_NOTE),
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not write production W/Z measurement rows",
            "does not treat synthetic smoke-schema rows as W/Z evidence",
            "does not treat static EW gauge-mass algebra as dM_W/ds",
            "does not treat structural SU(2) or beta-function notes as a production EW action",
            "does not use H_unit, yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Either implement a genuine same-source EW gauge/Higgs production "
            "action and W/Z correlator mass-fit harness, or pivot back to "
            "source-Higgs C_sH/C_HH pole rows, Schur A/B/C kernel rows, "
            "neutral-sector irreducibility, or FH/LSZ production evidence."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
