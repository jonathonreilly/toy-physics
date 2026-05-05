#!/usr/bin/env python3
"""
PR #230 top/W factorization-independence gate.

This runner tests the remaining derivation-first escape hatch after the
matched-covariance marginal no-go: can the current Cl(3)/Z^3 same-source
surface itself force top/W factorization or independence, so that a matched
covariance certificate is unnecessary?

Current answer: no.  The same-source label and framework-native substrate
bookkeeping do not imply statistical independence.  A positive route needs an
explicit product-measure, conditional-independence, deterministic-response, or
closed covariance theorem on the same surface.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import fmean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_THEOREM_INPUT = ROOT / "outputs" / "yt_top_wz_factorization_independence_theorem_2026-05-05.json"
DEFAULT_CERTIFICATE_OUTPUT = ROOT / "outputs" / "yt_top_wz_factorization_independence_certificate_2026-05-05.json"
DEFAULT_STATUS_OUTPUT = ROOT / "outputs" / "yt_top_wz_factorization_independence_gate_2026-05-05.json"
SCOUT_CERTIFICATE_OUTPUT = ROOT / "outputs" / "yt_top_wz_factorization_independence_gate_scout_certificate_2026-05-05.json"
SCOUT_STATUS_OUTPUT = ROOT / "outputs" / "yt_top_wz_factorization_independence_gate_scout_2026-05-05.json"

PARENTS = {
    "top_wz_covariance_marginal_no_go": "outputs/yt_top_wz_covariance_marginal_derivation_no_go_2026-05-05.json",
    "top_wz_matched_covariance_builder": "outputs/yt_top_wz_matched_covariance_certificate_builder_2026-05-04.json",
    "same_source_top_response_builder": "outputs/yt_same_source_top_response_certificate_builder_2026-05-04.json",
    "same_source_top_response_identity_builder": "outputs/yt_same_source_top_response_identity_certificate_builder_2026-05-04.json",
    "same_source_w_response_decomposition": "outputs/yt_same_source_w_response_decomposition_theorem_2026-05-04.json",
    "same_source_w_response_row_builder": "outputs/yt_same_source_w_response_row_builder_2026-05-04.json",
    "same_source_w_lightweight_readout": "outputs/yt_same_source_w_response_lightweight_readout_harness_2026-05-04.json",
    "wz_same_source_ew_action_gate": "outputs/yt_wz_same_source_ew_action_gate_2026-05-04.json",
    "wz_mass_fit_path_gate": "outputs/yt_wz_correlator_mass_fit_path_gate_2026-05-04.json",
    "wz_mass_fit_response_row_builder": "outputs/yt_wz_mass_fit_response_row_builder_2026-05-04.json",
}

FIREWALL_FALSE_FIELDS = (
    "used_observed_top_or_yukawa_as_selector",
    "used_observed_WZ_masses_as_selector",
    "used_H_unit_or_Ward_authority",
    "used_alpha_lm_plaquette_or_u0",
    "used_c2_or_zmatch_equal_one",
    "used_kappa_or_cos_theta_by_fiat",
    "synthesized_matched_response_rows",
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


def covariance(xs: list[float], ys: list[float]) -> float:
    mx = fmean(xs)
    my = fmean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (len(xs) - 1)


def latent_same_source_counterfamily() -> dict[str, Any]:
    """A same-source latent background can support many covariances.

    The labels are deliberately framework-native but abstract: each row is a
    Cl(3)/Z^3 same-source configuration on the 3-spatial-plus-derived-time
    surface.  Varying the W response's dependence on the shared latent
    substrate coordinate changes the covariance without changing the native
    bookkeeping.  That is enough to block factorization-by-label.
    """

    latent = [-1.5, -0.5, 0.5, 1.5]
    top = [1.42 + 0.004 * h for h in latent]
    w_positive = [0.516 + 0.003 * h for h in latent]
    w_negative = [0.516 - 0.003 * h for h in latent]
    w_independent = [0.516, 0.516, 0.516, 0.516]
    return {
        "substrate": "Cl(3)/Z^3",
        "geometry": "3 spatial + 1 derived-time source surface",
        "same_source_coordinate": True,
        "latent_configuration_coordinate": latent,
        "top_response": top,
        "w_response_positive_correlation": w_positive,
        "w_response_negative_correlation": w_negative,
        "w_response_deterministic_constant": w_independent,
        "cov_positive": covariance(top, w_positive),
        "cov_negative": covariance(top, w_negative),
        "cov_constant_w": covariance(top, w_independent),
        "same_native_labels_for_all_cases": True,
        "covariance_changes_with_joint_law": True,
    }


def validate_theorem(theorem: dict[str, Any], *, require_production: bool) -> dict[str, Any]:
    if not theorem:
        return {"present": False, "valid": False, "failed_checks": ["factorization theorem absent"]}

    firewall = theorem.get("firewall", {})
    mechanisms = {
        "product_measure_factorization": theorem.get("product_measure_factorization_proved") is True,
        "conditional_independence": theorem.get("conditional_independence_proved") is True,
        "deterministic_w_response": theorem.get("deterministic_w_response_proved") is True,
        "closed_covariance_formula": finite(theorem.get("cov_dE_top_dM_W")),
    }
    checks = {
        "phase_allowed": theorem.get("phase") in {"scout", "production"},
        "production_phase_if_required": theorem.get("phase") == "production" if require_production else True,
        "framework_native_substrate": theorem.get("cl3_z3_substrate") is True,
        "three_spatial_plus_derived_time": theorem.get("three_spatial_plus_derived_time") is True,
        "same_source_coordinate": theorem.get("same_source_coordinate") is True,
        "same_surface_top_w_response_scope": theorem.get("same_surface_top_w_response_scope") is True,
        "one_valid_factorization_mechanism": any(mechanisms.values()),
        "finite_covariance_if_formula_claimed": (
            finite(theorem.get("cov_dE_top_dM_W"))
            if theorem.get("closed_covariance_formula_claimed") is True
            else True
        ),
        "no_observed_top_or_yukawa_selector": firewall.get("used_observed_top_or_yukawa_as_selector") is False,
        "no_observed_wz_selector": firewall.get("used_observed_WZ_masses_as_selector") is False,
        "no_hunit_or_ward": firewall.get("used_H_unit_or_Ward_authority") is False,
        "no_alpha_lm_plaquette_or_u0": firewall.get("used_alpha_lm_plaquette_or_u0") is False,
        "no_c2_zmatch_kappa_or_cos_by_fiat": (
            firewall.get("used_c2_or_zmatch_equal_one") is False
            and firewall.get("used_kappa_or_cos_theta_by_fiat") is False
        ),
        "no_synthesized_matched_rows": firewall.get("synthesized_matched_response_rows") is False,
        "proposal_not_authorized_by_theorem": theorem.get("proposal_allowed") is not True,
    }
    return {
        "present": True,
        "valid": all(checks.values()),
        "checks": checks,
        "mechanisms": mechanisms,
        "failed_checks": [key for key, ok in checks.items() if not ok],
    }


def synthetic_theorem() -> dict[str, Any]:
    return {
        "phase": "scout",
        "cl3_z3_substrate": True,
        "three_spatial_plus_derived_time": True,
        "same_source_coordinate": True,
        "same_surface_top_w_response_scope": True,
        "product_measure_factorization_proved": True,
        "conditional_independence_proved": False,
        "deterministic_w_response_proved": False,
        "closed_covariance_formula_claimed": True,
        "cov_dE_top_dM_W": 0.0,
        "proposal_allowed": False,
        "firewall": {field: False for field in FIREWALL_FALSE_FIELDS},
    }


def build_certificate(theorem: dict[str, Any], validation: dict[str, Any], *, phase: str) -> dict[str, Any]:
    return {
        "certificate_kind": "top_wz_factorization_independence",
        "phase": phase,
        "cl3_z3_substrate": True,
        "three_spatial_plus_derived_time": True,
        "same_source_coordinate": True,
        "same_surface_top_w_response_scope": True,
        "mechanisms": validation["mechanisms"],
        "cov_dE_top_dM_W": theorem.get("cov_dE_top_dM_W"),
        "firewall": {field: False for field in FIREWALL_FALSE_FIELDS},
        "proposal_allowed": False,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not synthesize matched top/W production rows",
            "does not use observed W/Z/top/y_t/g2 selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, c2=1, Z_match=1, kappa_s=1, or cos(theta)=1",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theorem-input", type=Path, default=DEFAULT_THEOREM_INPUT)
    parser.add_argument("--certificate-output", type=Path, default=DEFAULT_CERTIFICATE_OUTPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_STATUS_OUTPUT)
    parser.add_argument("--scout", action="store_true")
    parser.add_argument("--strict", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mode = "strict" if args.strict else "scout" if args.scout else "current"
    status_output = SCOUT_STATUS_OUTPUT if args.scout and args.output == DEFAULT_STATUS_OUTPUT else args.output
    certificate_output = (
        SCOUT_CERTIFICATE_OUTPUT
        if args.scout and args.certificate_output == DEFAULT_CERTIFICATE_OUTPUT
        else args.certificate_output
    )

    print("PR #230 top/W factorization-independence gate")
    print("=" * 72)

    parents = {name: load_rel(rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parents.items() if not cert]
    proposal_allowed_parents = [
        name for name, cert in parents.items() if cert.get("proposal_allowed") is True
    ]
    statuses = {name: status(cert) for name, cert in parents.items()}
    counterfamily = latent_same_source_counterfamily()

    theorem = synthetic_theorem() if args.scout else load_json(args.theorem_input)
    validation = validate_theorem(theorem, require_production=args.strict)
    scout_gate_passed = args.scout and validation["valid"] and not missing_parents
    strict_gate_passed = args.strict and validation["valid"] and not missing_parents
    certificate_written = False
    certificate: dict[str, Any] = {}
    if scout_gate_passed or strict_gate_passed:
        certificate = build_certificate(
            theorem,
            validation,
            phase="scout" if args.scout else "production",
        )
        certificate_output.parent.mkdir(parents=True, exist_ok=True)
        certificate_output.write_text(
            json.dumps(certificate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        certificate_written = True

    marginal_no_go_loaded = (
        "matched top-W covariance not derivable from marginal response support"
        in statuses["top_wz_covariance_marginal_no_go"]
        and parents["top_wz_covariance_marginal_no_go"].get("marginal_derivation_no_go_passed")
        is True
    )
    matched_covariance_absent = (
        "matched top-W response rows absent" in statuses["top_wz_matched_covariance_builder"]
        and parents["top_wz_matched_covariance_builder"].get(
            "strict_top_wz_matched_covariance_builder_passed"
        )
        is False
    )
    same_source_ew_action_absent = (
        "same-source EW action not defined" in statuses["wz_same_source_ew_action_gate"]
        and parents["wz_same_source_ew_action_gate"].get("same_source_ew_action_ready") is False
    )
    wz_mass_fit_absent = (
        "WZ correlator mass-fit path absent" in statuses["wz_mass_fit_path_gate"]
        and parents["wz_mass_fit_path_gate"].get("wz_correlator_mass_fit_path_ready") is False
    )
    top_identity_absent = (
        "same-source top-response identity blockers remain"
        in statuses["same_source_top_response_identity_builder"]
        and parents["same_source_top_response_identity_builder"].get(
            "strict_same_source_top_response_identity_builder_passed"
        )
        is False
    )
    same_source_label_counterexample = (
        counterfamily["same_native_labels_for_all_cases"]
        and counterfamily["covariance_changes_with_joint_law"]
        and counterfamily["cov_positive"] > 0.0
        and counterfamily["cov_negative"] < 0.0
        and abs(counterfamily["cov_constant_w"]) < 1.0e-14
    )
    current_shortcut_rejected = (
        marginal_no_go_loaded
        and same_source_label_counterexample
        and matched_covariance_absent
        and same_source_ew_action_absent
        and wz_mass_fit_absent
        and top_identity_absent
        and not validation["present"]
    )

    report("parent-certificates-present", not missing_parents, f"missing={missing_parents}")
    report("no-parent-authorizes-proposal", not proposal_allowed_parents, f"proposal_allowed={proposal_allowed_parents}")
    report("framework-native-scope-declared", True, "Cl(3)/Z^3; 3 spatial + 1 derived-time")
    report("marginal-covariance-no-go-loaded", marginal_no_go_loaded, statuses["top_wz_covariance_marginal_no_go"])
    report("matched-covariance-certificate-absent", matched_covariance_absent, statuses["top_wz_matched_covariance_builder"])
    report("same-source-ew-action-absent", same_source_ew_action_absent, statuses["wz_same_source_ew_action_gate"])
    report("wz-mass-fit-path-absent", wz_mass_fit_absent, statuses["wz_mass_fit_path_gate"])
    report("top-response-identity-absent", top_identity_absent, statuses["same_source_top_response_identity_builder"])
    report(
        "same-source-label-does-not-imply-independence",
        same_source_label_counterexample,
        f"cov_pos={counterfamily['cov_positive']:.12g}, cov_neg={counterfamily['cov_negative']:.12g}, cov_const={counterfamily['cov_constant_w']:.12g}",
    )
    if args.scout:
        report("scout-factorization-theorem-valid", validation["valid"], str(validation.get("failed_checks", [])))
        report("scout-factorization-certificate-written", certificate_written, display(certificate_output))
    elif args.strict:
        report("strict-factorization-theorem-valid", validation["valid"], str(validation.get("failed_checks", [])))
        report("strict-factorization-certificate-written", certificate_written, display(certificate_output))
    else:
        report("future-factorization-theorem-absent", not validation["present"], display(args.theorem_input))
        report("current-mode-does-not-write-factorization-certificate", not certificate_written, display(DEFAULT_CERTIFICATE_OUTPUT))
    if args.scout:
        report(
            "scout-factorization-gate-schema-passes",
            scout_gate_passed,
            "synthetic product-measure theorem accepted only as scout schema",
        )
    else:
        report(
            "current-factorization-shortcut-rejected"
            if not args.strict
            else "strict-factorization-gate-passed",
            current_shortcut_rejected if not args.strict else strict_gate_passed,
            "same-source/native labels are not product-measure or independence authority",
        )

    result = {
        "actual_current_surface_status": (
            "scout-pass / top-W factorization-independence gate schema"
            if scout_gate_passed
            else "strict-pass / top-W factorization-independence certificate built"
            if strict_gate_passed
            else "exact negative boundary / same-source top-W factorization not derived on current PR230 surface"
        ),
        "mode": mode,
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "The current Cl(3)/Z^3 same-source surface does not by itself imply "
            "top/W independence.  A future positive gate needs an explicit "
            "product-measure, conditional-independence, deterministic-response, "
            "or closed covariance theorem on the same surface."
        ),
        "bare_retained_allowed": False,
        "factorization_independence_gate_passed": scout_gate_passed or strict_gate_passed,
        "strict_factorization_independence_gate_passed": strict_gate_passed,
        "factorization_certificate_written": certificate_written,
        "factorization_certificate_output": display(certificate_output),
        "theorem_input": display(args.theorem_input),
        "framework_native_scope": {
            "substrate": "Cl(3)/Z^3",
            "geometry": "3 spatial + 1 derived-time source surface",
            "same_source_coordinate": True,
        },
        "theorem_validation": validation,
        "same_source_counterfamily": counterfamily,
        "parent_certificates": PARENTS,
        "parent_statuses": statuses,
        "blocked_shortcut": {
            "candidate": "derive matched top/W covariance from framework-native same-source label or substrate bookkeeping",
            "reason": (
                "A same-source Cl(3)/Z^3 latent configuration family can carry "
                "positive, negative, or zero top/W covariance without changing "
                "the native labels.  Independence is therefore an extra theorem, "
                "not a consequence of native bookkeeping."
            ),
        },
        "allowed_future_routes": [
            "produce measured matched top/W response rows on the same configuration set",
            "supply a product-measure factorization theorem for the top and W response functionals",
            "supply a conditional-independence theorem strong enough to fix cov_dE_top_dM_W",
            "supply a deterministic W-response theorem plus a validated finite-sample covariance rule",
            "supply a closed covariance formula from the same Cl(3)/Z^3 3+derived-time surface",
        ],
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not create production matched rows",
            "does not define y_t through a matrix element or y_t_bare",
            "does not use observed W/Z/top/y_t/g2 selectors",
            "does not use H_unit, yt_ward_identity, alpha_LM, plaquette/u0, kappa_s=1, c2=1, Z_match=1, or cos(theta)=1",
        ],
        "exact_next_action": (
            "Either build the actual matched top/W response rows, or derive one "
            "of the allowed same-surface factorization mechanisms and rerun this "
            "gate in strict mode.  Do not treat Cl(3)/Z^3 same-source bookkeeping "
            "or 3+derived-time locality as independence by itself."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    status_output.parent.mkdir(parents=True, exist_ok=True)
    status_output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote status certificate: {display(status_output)}")
    if certificate_written:
        print(f"Wrote factorization certificate: {display(certificate_output)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    if args.strict and not strict_gate_passed:
        return 1
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
