#!/usr/bin/env python3
"""
PR #230 W/Z source-coordinate transport no-go.

This runner tests a narrow W/Z shortcut after the same-source EW action gate:
can static electroweak mass algebra become same-source W/Z row authority by
transporting the PR230 scalar source coordinate to the canonical Higgs radial
coordinate?

Current answer: no.  Static dM_W/dh is not dM_W/ds until the source-to-Higgs
Jacobian is certified on the same surface.  The counterfamily below keeps the
top source response and static W mass dictionary fixed while varying that
Jacobian and compensating with an allowed orthogonal neutral top coupling, so
the implied W source response changes.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_wz_source_coordinate_transport_no_go_2026-05-05.json"
FUTURE_TRANSPORT_CERT = ROOT / "outputs" / "yt_wz_source_coordinate_transport_certificate_2026-05-05.json"
FUTURE_WZ_ROWS = ROOT / "outputs" / "yt_fh_gauge_mass_response_measurement_rows_2026-05-03.json"
EW_GAUGE_MASS_NOTE = ROOT / "docs" / "EW_HIGGS_GAUGE_MASS_DIAGONALIZATION_THEOREM_NOTE_2026-04-26.md"

PARENTS = {
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "wz_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "wz_response_measurement_row_contract": "outputs/yt_wz_response_measurement_row_contract_gate_2026-05-03.json",
    "same_source_w_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "canonical_oh_premise_stretch": "outputs/yt_canonical_oh_premise_stretch_no_go_2026-05-05.json",
    "canonical_higgs_operator_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def transport_counterfamily() -> list[dict[str, float]]:
    """Same top response and static W dictionary, different W source slopes."""

    g2 = 0.64
    y_h = 0.91
    fixed_top_response = 0.73
    orthogonal_source_projection = 0.40
    rows = []
    for source_to_higgs_jacobian in (0.70, 1.00, 1.30):
        orthogonal_top_coupling = (
            math.sqrt(2.0) * fixed_top_response
            - y_h * source_to_higgs_jacobian
        ) / orthogonal_source_projection
        top_response = (
            y_h * source_to_higgs_jacobian
            + orthogonal_top_coupling * orthogonal_source_projection
        ) / math.sqrt(2.0)
        static_w_derivative = g2 / 2.0
        w_source_response = static_w_derivative * source_to_higgs_jacobian
        rows.append(
            {
                "g2": g2,
                "canonical_higgs_yukawa": y_h,
                "source_to_higgs_jacobian": source_to_higgs_jacobian,
                "orthogonal_source_projection": orthogonal_source_projection,
                "orthogonal_top_coupling": orthogonal_top_coupling,
                "top_source_response": top_response,
                "static_dM_W_dh": static_w_derivative,
                "transported_dM_W_ds": w_source_response,
                "top_over_w_source_response": top_response / w_source_response,
            }
        )
    return rows


def validate_transport_certificate(candidate: dict[str, Any]) -> dict[str, Any]:
    if not candidate:
        return {
            "present": False,
            "valid": False,
            "failed_checks": ["source-coordinate transport certificate absent"],
        }

    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    certificates = (
        candidate.get("certificates", {}) if isinstance(candidate.get("certificates"), dict) else {}
    )
    checks = {
        "certificate_kind": candidate.get("certificate_kind") == "wz_source_coordinate_transport",
        "phase_allowed": candidate.get("phase") in {"theorem", "production", "exact-support"},
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "finite_nonzero_source_to_higgs_jacobian": finite(candidate.get("source_to_higgs_jacobian"))
        and abs(float(candidate.get("source_to_higgs_jacobian"))) > 0.0,
        "canonical_higgs_identity_reference": isinstance(
            certificates.get("canonical_higgs_identity_certificate"), str
        )
        and bool(certificates.get("canonical_higgs_identity_certificate")),
        "same_source_ew_action_reference": isinstance(
            certificates.get("same_source_ew_action_certificate"), str
        )
        and bool(certificates.get("same_source_ew_action_certificate")),
        "wz_mass_fit_or_row_reference": isinstance(
            certificates.get("wz_mass_fit_or_response_row_certificate"), str
        )
        and bool(certificates.get("wz_mass_fit_or_response_row_certificate")),
        "no_static_dictionary_only": firewall.get("used_static_dictionary_only") is False,
        "no_empirical_selector": firewall.get("used_empirical_selector") is False,
        "no_user_banned_shortcut_authority": firewall.get("used_user_banned_shortcut_authority")
        is False,
        "no_by_fiat_normalization": firewall.get("used_by_fiat_normalization") is False,
        "proposal_not_authorized_by_candidate": candidate.get("proposal_allowed") is not True,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def rounded_values(rows: list[dict[str, float]], key: str) -> set[float]:
    return {round(float(row[key]), 12) for row in rows}


def main() -> int:
    print("PR #230 W/Z source-coordinate transport no-go")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in parents.items()}
    ew_text = read_text(EW_GAUGE_MASS_NOTE)
    candidate = load_json(FUTURE_TRANSPORT_CERT)
    validation = validate_transport_certificate(candidate)
    rows = transport_counterfamily()

    top_response_fixed = len(rounded_values(rows, "top_source_response")) == 1
    static_derivative_fixed = len(rounded_values(rows, "static_dM_W_dh")) == 1
    source_to_higgs_varies = len(rounded_values(rows, "source_to_higgs_jacobian")) == len(rows)
    w_source_response_varies = len(rounded_values(rows, "transported_dM_W_ds")) == len(rows)
    ratio_varies = len(rounded_values(rows, "top_over_w_source_response")) == len(rows)

    same_source_ew_action_absent = (
        "same-source EW action not defined" in statuses["wz_same_source_ew_action_gate"]
        and parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
    )
    action_builder_open = (
        "same-source EW action certificate absent" in statuses["wz_same_source_ew_action_builder"]
        and parents["wz_same_source_ew_action_builder"].get("same_source_ew_action_certificate_valid")
        is False
    )
    mass_fit_path_absent = (
        "WZ correlator mass-fit path absent" in statuses["wz_mass_fit_path_gate"]
        and parents["wz_mass_fit_path_gate"].get("wz_correlator_mass_fit_path_ready") is False
    )
    response_rows_absent = (
        "WZ mass-fit response-row builder" in statuses["wz_mass_fit_response_row_builder"]
        and parents["wz_mass_fit_response_row_builder"].get(
            "strict_wz_mass_fit_response_row_builder_passed"
        )
        is False
    )
    canonical_higgs_absent = (
        "canonical-Higgs operator certificate absent" in statuses["canonical_higgs_operator_gate"]
        and parents["canonical_higgs_operator_gate"].get("candidate_valid") is False
    )
    current_primitives_no_transport = (
        "same-surface O_H identity and normalization"
        in statuses["canonical_oh_premise_stretch"]
        and parents["canonical_oh_premise_stretch"].get("premise_lattice_stretch_no_go_passed")
        is True
    )
    sector_overlap_open = (
        "same-source sector-overlap identity obstruction" in statuses["same_source_sector_overlap"]
        and parents["same_source_sector_overlap"].get("sector_overlap_identity_gate_passed") is False
    )
    matched_covariance_open = (
        "matched top-W" in statuses["top_wz_matched_covariance_builder"]
        and parents["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
    )
    static_ew_dictionary_present = (
        "M_W = g_2 v / 2" in ew_text
        and "Assume a neutral Higgs vacuum" in ew_text
    )
    future_transport_present = FUTURE_TRANSPORT_CERT.exists()
    future_rows_present = FUTURE_WZ_ROWS.exists()
    shortcut_rejected = (
        not validation["present"]
        and top_response_fixed
        and static_derivative_fixed
        and source_to_higgs_varies
        and w_source_response_varies
        and ratio_varies
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("static-ew-dictionary-present", static_ew_dictionary_present, display(EW_GAUGE_MASS_NOTE))
    report("same-source-ew-action-absent", same_source_ew_action_absent, statuses["wz_same_source_ew_action_gate"])
    report("same-source-ew-action-builder-open", action_builder_open, statuses["wz_same_source_ew_action_builder"])
    report("wz-mass-fit-path-absent", mass_fit_path_absent, statuses["wz_mass_fit_path_gate"])
    report("wz-response-rows-absent", response_rows_absent, statuses["wz_mass_fit_response_row_builder"])
    report("canonical-higgs-certificate-absent", canonical_higgs_absent, statuses["canonical_higgs_operator_gate"])
    report("current-primitives-do-not-supply-transport", current_primitives_no_transport, statuses["canonical_oh_premise_stretch"])
    report("sector-overlap-still-open", sector_overlap_open, statuses["same_source_sector_overlap"])
    report("matched-top-w-covariance-open", matched_covariance_open, statuses["top_wz_matched_covariance_builder"])
    report("future-transport-certificate-absent", not future_transport_present, display(FUTURE_TRANSPORT_CERT))
    report("future-wz-row-file-absent", not future_rows_present, display(FUTURE_WZ_ROWS))
    report("counterfamily-keeps-top-response-fixed", top_response_fixed, str(sorted(rounded_values(rows, "top_source_response"))))
    report("counterfamily-keeps-static-dMdh-fixed", static_derivative_fixed, str(sorted(rounded_values(rows, "static_dM_W_dh"))))
    report("counterfamily-varies-source-to-higgs-jacobian", source_to_higgs_varies, str(sorted(rounded_values(rows, "source_to_higgs_jacobian"))))
    report("counterfamily-varies-transported-w-response", w_source_response_varies, str(sorted(rounded_values(rows, "transported_dM_W_ds"))))
    report("counterfamily-varies-top-over-w-ratio", ratio_varies, str(sorted(rounded_values(rows, "top_over_w_source_response"))))
    report("transport-shortcut-rejected", shortcut_rejected, f"candidate_present={validation['present']}")
    report("does-not-authorize-proposal", True, "exact negative boundary only")

    result = {
        "actual_current_surface_status": "exact negative boundary / WZ source-coordinate transport shortcut rejected",
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "Static electroweak mass algebra does not determine W/Z source rows "
            "until a same-surface source-to-canonical-Higgs transport certificate "
            "and W/Z mass-fit rows are supplied."
        ),
        "bare_retained_allowed": False,
        "wz_source_coordinate_transport_no_go_passed": shortcut_rejected,
        "future_transport_certificate": display(FUTURE_TRANSPORT_CERT),
        "future_transport_certificate_present": future_transport_present,
        "future_transport_certificate_valid": validation["valid"],
        "transport_certificate_validation": validation,
        "future_wz_rows": display(FUTURE_WZ_ROWS),
        "future_wz_rows_present": future_rows_present,
        "counterfamily": {
            "fixed_quantities": [
                "top_source_response",
                "static_dM_W_dh",
                "same source label",
                "same static electroweak mass dictionary",
            ],
            "varying_quantities": [
                "source_to_higgs_jacobian",
                "orthogonal_top_coupling",
                "transported_dM_W_ds",
                "top_over_w_source_response",
            ],
            "rows": rows,
        },
        "blocked_requirements": [
            "same-source EW action certificate",
            "same-surface source-to-canonical-Higgs transport certificate",
            "W/Z correlator mass-fit rows by source shift",
            "same-source sector-overlap identity",
            "canonical-Higgs identity certificate",
            "matched top/W covariance or measured paired rows",
        ],
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "strict_non_claims": [
            "does not claim closure",
            "does not write or synthesize W/Z measurement rows",
            "does not treat static mass algebra as a source-response row",
            "does not set the source-to-Higgs Jacobian by convention",
            "does not use empirical selectors or user-listed shortcut authorities",
        ],
        "exact_next_action": (
            "Supply a real same-source EW action and source-transport certificate, "
            "then W/Z correlator mass-fit rows; otherwise pursue measured matched "
            "top/W rows, source-Higgs rows after canonical-Higgs identity, Schur "
            "rows, or neutral-sector irreducibility."
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
