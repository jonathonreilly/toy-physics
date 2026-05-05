#!/usr/bin/env python3
"""
PR #230 top/W deterministic-response covariance gate.

This runner narrows the remaining W/Z derivation-first escape hatch.  The
previous factorization gate allowed a future deterministic W-response theorem
as one possible substitute for measured matched top/W rows.  This gate records
the missing contract: a deterministic W response is useful only when it is tied
to the same latent surface as the top response, with either paired top rows or
a closed covariance formula.

Current answer: no such strict certificate exists on the PR230 surface.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import fmean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_top_wz_deterministic_response_covariance_certificate_2026-05-05.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_top_wz_deterministic_response_covariance_gate_2026-05-05.json"
SCOUT_OUTPUT = ROOT / "outputs" / "yt_top_wz_deterministic_response_covariance_gate_scout_2026-05-05.json"
SCOUT_CERTIFICATE = ROOT / "outputs" / "yt_top_wz_deterministic_response_covariance_gate_scout_certificate_2026-05-05.json"

PARENTS = {
    "top_wz_covariance_marginal_no_go": "outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json",
    "top_wz_factorization_independence_gate": "outputs/yt_top_wz_factorization_independence_gate_2026-05-05.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "same_source_top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_response_orthogonal_correction": "outputs/yt_same_source_w_response_orthogonal_correction_gate_2026-05-04.json",
    "one_higgs_completeness_orthogonal_null": "outputs/yt_one_higgs_completeness_orthogonal_null_gate_2026-05-04.json",
    "delta_perp_tomography_builder": "outputs/yt_delta_perp_tomography_correction_builder_2026-05-04.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_same_source_ew_action_builder": "outputs/yt_wz_same_source_ew_action_certificate_builder_2026-05-04.json",
    "wz_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
    "electroweak_g2_certificate_builder": "outputs/yt_electroweak_g2_certificate_builder_2026-05-05.json",
    "wz_g2_authority_firewall": "outputs/yt_wz_g2_authority_firewall_2026-05-05.json",
    "same_source_sector_overlap": "outputs/yt_same_source_sector_overlap_identity_obstruction_2026-05-02.json",
    "canonical_higgs_operator": "outputs/yt_canonical_higgs_operator_certificate_gate_2026-05-03.json",
}

FORBIDDEN_FALSE_FIELDS = (
    "used_observed_top_or_yukawa_as_selector",
    "used_observed_WZ_masses_as_selector",
    "used_observed_g2_as_selector",
    "used_H_unit_or_Ward_authority",
    "used_alpha_lm_plaquette_or_u0",
    "used_c2_or_zmatch_equal_one",
    "used_kappa_or_cos_theta_by_fiat",
    "synthesized_matched_response_rows",
)

SHORTCUT_REFERENCE_TOKENS = (
    "GATE",
    "GUARD",
    "FIREWALL",
    "BUILDER",
    "SCOUT",
    "NO_GO",
    "NOGO",
    "OBSTRUCTION",
    "ABSENCE",
    "ABSENT",
    "IMPORT_AUDIT",
    "PRODUCTION_ATTEMPT",
    "IMPLEMENTATION_PLAN",
    "CONTRACT",
    "MANIFEST",
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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_rel(rel: str) -> dict[str, Any]:
    return load_json(ROOT / rel)


def display(path: Path) -> str:
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def finite_list(value: Any, min_len: int = 2) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= min_len
        and all(isinstance(item, (int, float)) and math.isfinite(float(item)) for item in value)
    )


def covariance(xs: list[float], ys: list[float]) -> float:
    mx = fmean(xs)
    my = fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def deterministic_w_counterfamily() -> dict[str, Any]:
    """Same deterministic W response, same top marginal, different covariance."""

    latent = [-1.5, -0.5, 0.5, 1.5]
    w_response = [0.516 + 0.003 * h for h in latent]
    top_plus = [1.42 + 0.004 * h for h in latent]
    top_minus = [1.42 - 0.004 * h for h in latent]
    return {
        "substrate": "Cl(3)/Z^3",
        "geometry": "3 spatial + 1 derived-time source surface",
        "same_source_coordinate": True,
        "latent_configuration_coordinate": latent,
        "deterministic_w_response": "R_W(h)=0.516+0.003 h",
        "w_response_rows": w_response,
        "top_response_plus_rows": top_plus,
        "top_response_minus_rows": top_minus,
        "top_marginals_equal": sorted(round(x, 12) for x in top_plus)
        == sorted(round(x, 12) for x in top_minus),
        "w_law_identical": True,
        "cov_plus": covariance(top_plus, w_response),
        "cov_minus": covariance(top_minus, w_response),
        "deterministic_w_alone_fixes_covariance": False,
    }


def path_ref_ok(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    return value.startswith(("docs/", "outputs/", "scripts/")) and (ROOT / value).exists()


def nonshortcut_path_ref_ok(value: Any) -> bool:
    if not path_ref_ok(value):
        return False
    upper = str(value).upper()
    return not any(token in upper for token in SHORTCUT_REFERENCE_TOKENS)


def validate_candidate(candidate: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not candidate:
        return {
            "present": False,
            "valid": False,
            "checks": {},
            "failed_checks": ["deterministic-response covariance certificate absent"],
        }

    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    refs = candidate.get("certificates", {}) if isinstance(candidate.get("certificates"), dict) else {}
    top_rows = candidate.get("top_response_rows")
    w_rows = candidate.get("deterministic_w_response_rows")
    mechanisms = {
        "paired_top_rows_with_deterministic_w_rows": finite_list(top_rows) and finite_list(w_rows) and len(top_rows) == len(w_rows),
        "closed_covariance_formula": candidate.get("closed_covariance_formula_proved") is True
        and finite(candidate.get("cov_dE_top_dM_W")),
    }
    ref_check = path_ref_ok if candidate.get("phase") == "scout" else nonshortcut_path_ref_ok
    checks = {
        "certificate_kind": candidate.get("certificate_kind") == "top_wz_deterministic_response_covariance",
        "phase_supported": candidate.get("phase") in {"scout", "theorem", "production"},
        "production_phase_if_required": candidate.get("phase") == "production" if require_production else True,
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "three_spatial_plus_derived_time": candidate.get("three_spatial_plus_derived_time") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "deterministic_w_response_proved": candidate.get("deterministic_w_response_proved") is True,
        "one_covariance_mechanism": any(mechanisms.values()),
        "covariance_finite": finite(candidate.get("cov_dE_top_dM_W")),
        "same_source_ew_action_certificate_ref": ref_check(refs.get("same_source_ew_action_certificate")),
        "wz_mass_fit_or_theorem_ref": ref_check(refs.get("wz_mass_fit_or_theorem_certificate")),
        "top_response_identity_ref": ref_check(refs.get("top_response_identity_certificate")),
        "electroweak_g2_ref": ref_check(refs.get("electroweak_g2_certificate")),
        "sector_or_canonical_higgs_identity_ref": ref_check(refs.get("sector_or_canonical_higgs_identity_certificate")),
        "orthogonal_correction_control_ref": ref_check(refs.get("orthogonal_correction_control_certificate")),
        "proposal_not_authorized_by_candidate": candidate.get("proposal_allowed") is not True,
    }
    checks.update({f"forbidden_{field}_false": firewall.get(field) is False for field in FORBIDDEN_FALSE_FIELDS})
    failed = [key for key, ok in checks.items() if not ok]
    return {
        "present": True,
        "valid": not failed,
        "checks": checks,
        "mechanisms": mechanisms,
        "failed_checks": failed,
    }


def scout_candidate() -> dict[str, Any]:
    return {
        "certificate_kind": "top_wz_deterministic_response_covariance",
        "phase": "scout",
        "same_surface_cl3_z3": True,
        "three_spatial_plus_derived_time": True,
        "same_source_coordinate": True,
        "deterministic_w_response_proved": True,
        "closed_covariance_formula_proved": True,
        "cov_dE_top_dM_W": 0.0,
        "top_response_rows": [1.0, 1.1, 0.9, 1.0],
        "deterministic_w_response_rows": [0.5, 0.5, 0.5, 0.5],
        "proposal_allowed": False,
        "certificates": {
            "same_source_ew_action_certificate": PARENTS["wz_same_source_ew_action_gate"],
            "wz_mass_fit_or_theorem_certificate": PARENTS["wz_mass_fit_path_gate"],
            "top_response_identity_certificate": PARENTS["same_source_top_response_identity_builder"],
            "electroweak_g2_certificate": PARENTS["electroweak_g2_certificate_builder"],
            "sector_or_canonical_higgs_identity_certificate": PARENTS["same_source_sector_overlap"],
            "orthogonal_correction_control_certificate": PARENTS["same_source_w_response_orthogonal_correction"],
        },
        "firewall": {field: False for field in FORBIDDEN_FALSE_FIELDS},
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--scout", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = SCOUT_OUTPUT if args.scout and args.output == DEFAULT_OUTPUT else args.output
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    print("PR #230 top/W deterministic-response covariance gate")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    statuses = {name: status(cert) for name, cert in parents.items()}
    candidate = scout_candidate() if args.scout else load_json(args.input)
    validation = validate_candidate(candidate, require_production=args.strict)
    counterfamily = deterministic_w_counterfamily()

    marginal_no_go_loaded = (
        "matched top-W covariance not derivable from marginal response support"
        in statuses["top_wz_covariance_marginal_no_go"]
        and parents["top_wz_covariance_marginal_no_go"].get("marginal_derivation_no_go_passed") is True
    )
    factorization_gate_loaded = (
        "same-source top-W factorization not derived" in statuses["top_wz_factorization_independence_gate"]
        and parents["top_wz_factorization_independence_gate"].get("strict_factorization_independence_gate_passed")
        is False
    )
    matched_rows_absent = (
        "matched top-W" in statuses["top_wz_matched_covariance_builder"]
        and parents["top_wz_matched_covariance_builder"].get("strict_top_wz_matched_covariance_builder_passed")
        is False
    )
    ew_action_absent = (
        "same-source EW action not defined" in statuses["wz_same_source_ew_action_gate"]
        and parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
    )
    top_identity_absent = (
        "same-source top-response identity" in statuses["same_source_top_response_identity_builder"]
        and parents["same_source_top_response_identity_builder"].get(
            "strict_same_source_top_response_identity_builder_passed"
        )
        is False
    )
    mass_fit_absent = (
        "WZ correlator mass-fit path absent" in statuses["wz_mass_fit_path_gate"]
        and parents["wz_mass_fit_path_gate"].get("wz_correlator_mass_fit_path_ready") is False
    )
    g2_absent = (
        "electroweak g2 certificate builder inputs absent" in statuses["electroweak_g2_certificate_builder"]
        and parents["electroweak_g2_certificate_builder"].get("strict_electroweak_g2_certificate_passed")
        is False
    )
    counterfamily_blocks_shortcut = (
        counterfamily["top_marginals_equal"]
        and counterfamily["w_law_identical"]
        and counterfamily["cov_plus"] > 0.0
        and counterfamily["cov_minus"] < 0.0
    )
    scout_passed = args.scout and validation["valid"] and not missing
    strict_passed = args.strict and validation["valid"] and not missing
    current_shortcut_rejected = (
        not args.scout
        and not args.strict
        and not validation["present"]
        and marginal_no_go_loaded
        and factorization_gate_loaded
        and matched_rows_absent
        and ew_action_absent
        and top_identity_absent
        and mass_fit_absent
        and g2_absent
        and counterfamily_blocks_shortcut
    )

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("framework-native-scope-declared", True, "Cl(3)/Z^3; 3 spatial + 1 derived-time")
    report("marginal-covariance-no-go-loaded", marginal_no_go_loaded, statuses["top_wz_covariance_marginal_no_go"])
    report("factorization-independence-gate-loaded", factorization_gate_loaded, statuses["top_wz_factorization_independence_gate"])
    report("matched-top-w-rows-absent", matched_rows_absent, statuses["top_wz_matched_covariance_builder"])
    report("same-source-ew-action-absent", ew_action_absent, statuses["wz_same_source_ew_action_gate"])
    report("top-response-identity-absent", top_identity_absent, statuses["same_source_top_response_identity_builder"])
    report("wz-mass-fit-path-absent", mass_fit_absent, statuses["wz_mass_fit_path_gate"])
    report("non-observed-g2-certificate-absent", g2_absent, statuses["electroweak_g2_certificate_builder"])
    report(
        "deterministic-w-alone-counterexample",
        counterfamily_blocks_shortcut,
        f"cov_plus={counterfamily['cov_plus']:.12g}, cov_minus={counterfamily['cov_minus']:.12g}",
    )
    if args.scout:
        report("scout-deterministic-response-certificate-valid", validation["valid"], str(validation["failed_checks"]))
        if scout_passed:
            SCOUT_CERTIFICATE.write_text(
                json.dumps(candidate, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        report("scout-certificate-written", scout_passed, display(SCOUT_CERTIFICATE))
    elif args.strict:
        report("strict-deterministic-response-certificate-valid", validation["valid"], str(validation["failed_checks"]))
    else:
        report("future-deterministic-response-certificate-absent", not validation["present"], display(args.input))
    report(
        "deterministic-response-shortcut-rejected" if not args.scout and not args.strict else "gate-pass",
        current_shortcut_rejected if not args.scout and not args.strict else scout_passed or strict_passed,
        "deterministic W response is not covariance authority without paired top rows or a closed same-surface formula",
    )

    result = {
        "actual_current_surface_status": (
            "scout-pass / top-W deterministic-response covariance schema"
            if scout_passed
            else "strict-pass / top-W deterministic-response covariance certificate accepted"
            if strict_passed
            else "exact negative boundary / deterministic W response covariance shortcut not derived on current PR230 surface"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "A deterministic W response does not by itself fix matched top/W "
            "covariance.  The current surface lacks paired top/W response rows, "
            "a same-source EW action, top-response identity, W/Z mass-fit path, "
            "non-observed g2 authority, and a closed covariance theorem."
        ),
        "bare_retained_allowed": False,
        "deterministic_response_covariance_gate_passed": scout_passed or strict_passed,
        "strict_deterministic_response_covariance_gate_passed": strict_passed,
        "candidate_input": display(args.input),
        "candidate_validation": validation,
        "framework_native_scope": {
            "substrate": "Cl(3)/Z^3",
            "geometry": "3 spatial + 1 derived-time source surface",
            "same_source_coordinate": True,
        },
        "deterministic_w_counterfamily": counterfamily,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "future_acceptance_contract": {
            "future_certificate": display(DEFAULT_INPUT),
            "required": [
                "same-surface Cl(3)/Z^3 and 3+derived-time scope",
                "deterministic W response proved on the same source coordinate",
                "paired top response rows or a closed covariance formula",
                "same-source EW action certificate",
                "W/Z mass-fit path or theorem certificate",
                "same-source top-response identity certificate",
                "non-observed electroweak g2 authority certificate",
                "sector/canonical-Higgs identity plus orthogonal correction control",
                "forbidden-import firewall",
            ],
        },
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not create matched top/W rows",
            "does not define y_t through a matrix element or y_t_bare",
            "does not use observed W/Z/top/y_t/g2 selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
        ],
        "exact_next_action": (
            "To use the deterministic-response W/Z route, supply the future "
            "certificate with paired top rows or a closed covariance formula.  "
            "Otherwise produce matched top/WZ response rows directly."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {display(output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
