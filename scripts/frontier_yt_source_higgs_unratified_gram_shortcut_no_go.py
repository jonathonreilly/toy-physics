#!/usr/bin/env python3
"""
PR #230 source-Higgs unratified-Gram shortcut no-go.

The source-Higgs route can use pole-level Gram purity only after the second
operator is a same-surface canonical-Higgs operator.  This runner closes the
shortcut where a perfect C_ss/C_sH/C_HH Gram relation against an unratified
operator is treated as O_H authority.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_source_higgs_unratified_gram_shortcut_no_go_2026-05-05.json"

PARENTS = {
    "source_higgs_unratified_smoke": "outputs/yt_source_higgs_unratified_operator_smoke_checkpoint_2026-05-03.json",
    "source_higgs_readiness": "outputs/yt_source_higgs_production_readiness_gate_2026-05-04.json",
    "source_higgs_cross_builder": "outputs/yt_source_higgs_cross_correlator_certificate_builder_2026-05-03.json",
    "source_higgs_postprocessor": "outputs/yt_source_higgs_gram_purity_postprocess_2026-05-03.json",
    "canonical_higgs_gate": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
    "cross_lane_oh_audit": "outputs/yt_cross_lane_oh_authority_audit_2026-05-05.json",
    "retained_route": "outputs/yt_retained_closure_route_certificate_2026-05-01.json",
    "campaign_status": "outputs/yt_pr230_campaign_status_certificate_2026-05-01.json",
}

FUTURE_STRICT_CERTIFICATES = {
    "source_higgs_production_candidate": "outputs/yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json",
    "canonical_higgs_operator_certificate": "outputs/yt_canonical_higgs_operator_certificate_2026-05-03.json",
}

FORBIDDEN_FALSE_FIELDS = (
    "used_observed_targets_as_selectors",
    "used_yt_ward_identity",
    "used_hunit_matrix_element_readout",
    "used_alpha_lm_or_plaquette",
    "used_static_ew_algebra_as_operator",
)

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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def gram(c_ss: float, c_sh: float, c_hh: float) -> dict[str, Any]:
    product = c_ss * c_hh
    determinant = product - c_sh * c_sh
    rho = c_sh / math.sqrt(product) if product > 0.0 else float("nan")
    return {
        "Res_C_ss": c_ss,
        "Res_C_sH": c_sh,
        "Res_C_HH": c_hh,
        "gram_determinant": determinant,
        "normalized_overlap_rho_sH": rho,
        "central_purity_passed": product > 0.0
        and abs(determinant) <= 1.0e-12
        and abs(abs(rho) - 1.0) <= 1.0e-12,
    }


def unratified_perfect_candidate() -> dict[str, Any]:
    values = gram(4.0, 6.0, 9.0)
    return {
        "phase": "synthetic_no_go_witness",
        "same_ensemble": True,
        "same_source_coordinate": True,
        "selected_source_side_normalization": "legendre_lsz_source_pole_operator_v1",
        "source_pole_operator": {
            "source_pole_operator_constructed": True,
            "source_pole_residue_normalized_to_one": True,
            "canonical_higgs_operator_identity_passed": False,
        },
        "canonical_higgs_operator_identity_passed": False,
        "canonical_higgs_operator": {
            "operator_id": "unratified_perfect_gram_operator",
            "identity_certificate": "",
            "normalization_certificate": "",
            "strict_limit": "This operator is the supplied second leg only; it is not certified as O_H.",
        },
        "hunit_used_as_operator": False,
        "residue_matrix": values,
        "retained_route_gate_passed": False,
        "proposal_allowed": False,
        "firewall": {
            "used_observed_targets_as_selectors": False,
            "used_yt_ward_identity": False,
            "used_hunit_matrix_element_readout": False,
            "used_alpha_lm_or_plaquette": False,
            "used_static_ew_algebra_as_operator": False,
        },
    }


def validate_postprocessor_contract(candidate: dict[str, Any]) -> dict[str, Any]:
    matrix = candidate.get("residue_matrix", {})
    operator = candidate.get("canonical_higgs_operator", {})
    source_pole = candidate.get("source_pole_operator", {})
    firewall = candidate.get("firewall", {})
    checks = {
        "production_phase": candidate.get("phase") == "production",
        "same_ensemble": candidate.get("same_ensemble") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "legendre_lsz_source_side_selected": candidate.get("selected_source_side_normalization")
        == "legendre_lsz_source_pole_operator_v1",
        "source_pole_operator_constructed": source_pole.get("source_pole_operator_constructed") is True,
        "source_pole_residue_unit": source_pole.get("source_pole_residue_normalized_to_one") is True,
        "source_pole_not_claimed_as_higgs_by_fiat": source_pole.get(
            "canonical_higgs_operator_identity_passed"
        )
        is False,
        "canonical_higgs_operator_identity": candidate.get("canonical_higgs_operator_identity_passed")
        is True,
        "has_identity_certificate": isinstance(operator.get("identity_certificate"), str)
        and bool(operator.get("identity_certificate")),
        "has_normalization_certificate": isinstance(operator.get("normalization_certificate"), str)
        and bool(operator.get("normalization_certificate")),
        "not_hunit_by_fiat": candidate.get("hunit_used_as_operator") is False,
        "no_observed_selectors": firewall.get("used_observed_targets_as_selectors") is False,
        "no_prior_ward_authority": firewall.get("used_yt_ward_identity") is False,
        "no_alpha_lm_or_plaquette_authority": firewall.get("used_alpha_lm_or_plaquette") is False,
        "no_hunit_matrix_element_readout": firewall.get("used_hunit_matrix_element_readout") is False,
        "no_static_ew_algebra_as_operator": firewall.get("used_static_ew_algebra_as_operator") is False,
        "has_res_c_ss": finite(matrix.get("Res_C_ss")),
        "has_res_c_sh": finite(matrix.get("Res_C_sH")),
        "has_res_c_hh": finite(matrix.get("Res_C_HH")),
        "retained_route_gate_passed": candidate.get("retained_route_gate_passed") is True,
    }
    return {
        "checks": checks,
        "failed_checks": [key for key, ok in checks.items() if not ok],
        "accepted_by_postprocessor_contract": all(checks.values()),
    }


def canonical_overlap_counterfamily() -> list[dict[str, Any]]:
    rows = []
    for theta_label, overlap in (
        ("same_operator_if_later_certified", 1.0),
        ("mixed_canonical_higgs", 0.5),
        ("orthogonal_canonical_higgs", 0.0),
    ):
        rows.append(
            {
                "case": theta_label,
                "unratified_rows_unchanged": True,
                "canonical_higgs_overlap_with_unratified_operator": overlap,
                "relative_physical_source_higgs_overlap": overlap,
            }
        )
    return rows


def main() -> int:
    print("PR #230 source-Higgs unratified-Gram shortcut no-go")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    future_present = {
        name: (ROOT / path).exists() for name, path in FUTURE_STRICT_CERTIFICATES.items()
    }

    smoke = parents["source_higgs_unratified_smoke"]
    smoke_metadata = smoke.get("source_higgs_metadata", {})
    smoke_operator = smoke_metadata.get("operator", {})
    smoke_firewall = smoke_metadata.get("firewall", {})
    smoke_unratified = (
        smoke_operator.get("canonical_higgs_operator_identity_passed") is False
        and smoke_metadata.get("used_as_physical_yukawa_readout") is False
        and smoke_metadata.get("strict_limit", "").startswith("Finite-mode source-Higgs rows")
    )
    smoke_firewall_clean = all(smoke_firewall.get(field) is False for field in FORBIDDEN_FALSE_FIELDS[:4])

    candidate = unratified_perfect_candidate()
    candidate_gram = candidate["residue_matrix"]
    contract = validate_postprocessor_contract(candidate)
    counterfamily = canonical_overlap_counterfamily()
    overlap_values = {
        row["relative_physical_source_higgs_overlap"] for row in counterfamily
    }
    forbidden_clean = all(
        candidate["firewall"].get(field) is False for field in FORBIDDEN_FALSE_FIELDS
    ) and candidate.get("hunit_used_as_operator") is False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("current-smoke-operator-is-unratified-non-evidence", smoke_unratified, status(smoke))
    report("current-smoke-firewall-clean", smoke_firewall_clean, str(smoke_firewall))
    report("synthetic-unratified-gram-is-perfect", bool(candidate_gram["central_purity_passed"]), str(candidate_gram))
    report(
        "postprocessor-contract-rejects-unratified-perfect-gram",
        not contract["accepted_by_postprocessor_contract"]
        and "canonical_higgs_operator_identity" in contract["failed_checks"]
        and "has_identity_certificate" in contract["failed_checks"],
        f"failed={contract['failed_checks']}",
    )
    report(
        "canonical-overlap-counterfamily-varies-physical-overlap",
        len(overlap_values) == len(counterfamily),
        str(counterfamily),
    )
    report("forbidden-import-firewall-clean", forbidden_clean, str(candidate["firewall"]))
    report("strict-future-certificates-absent", not any(future_present.values()), f"present={future_present}")
    report("does-not-authorize-proposed-retained", True, "no-go only")

    result = {
        "actual_current_surface_status": (
            "exact negative boundary / unratified source-Higgs Gram shortcut is not O_H authority"
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A perfect Gram relation against the supplied second operator only "
            "certifies purity relative to that supplied operator.  Without a "
            "same-surface canonical-Higgs identity and normalization certificate, "
            "the physical O_H overlap remains free."
        ),
        "bare_retained_allowed": False,
        "unratified_gram_shortcut_no_go_passed": FAIL_COUNT == 0,
        "candidate_gram": candidate_gram,
        "postprocessor_contract_evaluation": contract,
        "canonical_overlap_counterfamily": counterfamily,
        "current_smoke_summary": {
            "source_higgs_metadata": smoke_metadata,
            "status": status(smoke),
            "path": PARENTS["source_higgs_unratified_smoke"],
        },
        "parent_certificates": PARENTS,
        "parent_statuses": {name: status(cert) for name, cert in parents.items()},
        "future_strict_certificate_presence": future_present,
        "strict_non_claims": [
            "does not claim retained or proposed_retained top-Yukawa closure",
            "does not create production source-Higgs rows",
            "does not define O_H by notation or by perfect Gram against an unratified operator",
            "does not use H_unit, yt_ward_identity, y_t_bare, observed targets, alpha_LM, plaquette, u0, or unit shortcuts",
            "does not set kappa_s, c2, Z_match, or cos(theta) to one",
        ],
        "exact_next_action": (
            "Supply a same-surface canonical-Higgs operator identity and normalization "
            "certificate, then produce production C_ss/C_sH/C_HH pole residues and "
            "rerun the source-Higgs builder, Gram-purity postprocessor, retained-route "
            "certificate, and PR230 assembly gate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {rel(OUTPUT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
