#!/usr/bin/env python3
"""
Postprocess a future PR #230 source-Higgs Gram-purity production certificate.

This is the executable acceptance surface for the selected source-overlap
route.  If a future production run supplies pole residues Res(C_ss),
Res(C_sH), and Res(C_HH) for a certified same-surface canonical Higgs operator,
this runner uses the already-derived Legendre/LSZ source-pole operator
O_sp = sqrt(D'_ss) O_s to compute the O_sp-Higgs Gram determinant and
normalized overlap.  With no candidate certificate present, it records the
route as open.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "outputs" / "yt_source_higgs_cross_correlator_production_certificate_2026-05-03.json"
DEFAULT_OUTPUT = ROOT / "outputs" / "yt_source_higgs_gram_purity_postprocess_2026-05-03.json"

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


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def nonnegative(value: float) -> float:
    return max(float(value), 0.0)


def uncertainty(candidate: dict[str, Any], key: str) -> float | None:
    matrix = candidate.get("residue_matrix", {})
    value = matrix.get(key)
    return float(value) if finite(value) and float(value) >= 0.0 else None


def compute_gate(candidate: dict[str, Any], tolerance: float, sigma: float) -> dict[str, Any]:
    matrix = candidate.get("residue_matrix", {})
    c_ss = float(matrix["Res_C_ss"])
    c_sh = float(matrix["Res_C_sH"])
    c_hh = float(matrix["Res_C_HH"])
    product = c_ss * c_hh
    delta = product - c_sh * c_sh
    rho = c_sh / math.sqrt(product) if product > 0.0 else float("nan")
    dgamma_ss = 1.0 / c_ss if c_ss > 0.0 else float("nan")
    c_sp_h = c_sh * math.sqrt(dgamma_ss) if dgamma_ss > 0.0 else float("nan")
    c_sp_sp = 1.0 if c_ss > 0.0 else float("nan")
    delta_sp_h = c_sp_sp * c_hh - c_sp_h * c_sp_h
    rho_sp_h = c_sp_h / math.sqrt(c_sp_sp * c_hh) if c_sp_sp > 0.0 and c_hh > 0.0 else float("nan")
    rho_sp_h_abs_error = abs(abs(rho_sp_h) - 1.0) if math.isfinite(rho_sp_h) else float("inf")
    rho_abs_error = abs(abs(rho) - 1.0) if math.isfinite(rho) else float("inf")

    err_ss = uncertainty(candidate, "Res_C_ss_err")
    err_sh = uncertainty(candidate, "Res_C_sH_err")
    err_hh = uncertainty(candidate, "Res_C_HH_err")

    delta_err = None
    rho_err = None
    if err_ss is not None and err_sh is not None and err_hh is not None and product > 0.0:
        # First-order independent-error propagation.  A future production
        # certificate may override this with a full bootstrap covariance.
        delta_err = math.sqrt(
            (c_hh * err_ss) ** 2
            + (c_ss * err_hh) ** 2
            + (2.0 * c_sh * err_sh) ** 2
        )
        d_rho_d_ss = -0.5 * c_sh * c_hh / (product ** 1.5)
        d_rho_d_hh = -0.5 * c_sh * c_ss / (product ** 1.5)
        d_rho_d_sh = 1.0 / math.sqrt(product)
        rho_err = math.sqrt(
            (d_rho_d_ss * err_ss) ** 2
            + (d_rho_d_hh * err_hh) ** 2
            + (d_rho_d_sh * err_sh) ** 2
        )

    delta_bound = max(tolerance, sigma * delta_err) if delta_err is not None else tolerance
    rho_bound = max(tolerance, sigma * rho_err) if rho_err is not None else tolerance
    positive_residues = c_ss > 0.0 and c_hh > 0.0 and c_sp_sp > 0.0
    raw_purity_gate_passed = positive_residues and abs(delta) <= delta_bound and rho_abs_error <= rho_bound
    osp_higgs_purity_gate_passed = positive_residues and abs(delta_sp_h) <= delta_bound / max(c_ss, tolerance) and rho_sp_h_abs_error <= rho_bound
    purity_gate_passed = raw_purity_gate_passed and osp_higgs_purity_gate_passed

    return {
        "Res_C_ss": c_ss,
        "Res_C_sH": c_sh,
        "Res_C_HH": c_hh,
        "Dprime_ss_at_pole": dgamma_ss,
        "Res_C_sp_sp": c_sp_sp,
        "Res_C_spH": c_sp_h,
        "gram_determinant": delta,
        "normalized_overlap_rho_sH": rho,
        "rho_abs_error_from_one": rho_abs_error,
        "osp_higgs_gram_determinant": delta_sp_h,
        "normalized_overlap_rho_spH": rho_sp_h,
        "rho_spH_abs_error_from_one": rho_sp_h_abs_error,
        "delta_error": delta_err,
        "rho_error": rho_err,
        "delta_acceptance_bound": delta_bound,
        "rho_acceptance_bound": rho_bound,
        "positive_residues": positive_residues,
        "raw_source_higgs_purity_gate_passed": raw_purity_gate_passed,
        "osp_higgs_purity_gate_passed": osp_higgs_purity_gate_passed,
        "purity_gate_passed": purity_gate_passed,
    }


def validate_candidate(candidate: dict[str, Any]) -> dict[str, bool]:
    matrix = candidate.get("residue_matrix", {})
    firewall = candidate.get("firewall", {})
    operator = candidate.get("canonical_higgs_operator", {})
    source_pole = candidate.get("source_pole_operator", {})
    return {
        "production_phase": candidate.get("phase") == "production",
        "same_ensemble": candidate.get("same_ensemble") is True,
        "same_source_coordinate": candidate.get("same_source_coordinate") is True,
        "legendre_lsz_source_side_selected": candidate.get("selected_source_side_normalization")
        == "legendre_lsz_source_pole_operator_v1",
        "source_pole_operator_constructed": source_pole.get("source_pole_operator_constructed") is True,
        "source_pole_residue_unit": source_pole.get("source_pole_residue_normalized_to_one") is True,
        "genuine_source_pole_intake_passed": source_pole.get("genuine_source_pole_intake_passed") is True,
        "genuine_source_pole_current_surface_support": source_pole.get(
            "artifact_is_genuine_current_surface_support"
        )
        is True,
        "source_pole_support_not_physics_closure": source_pole.get("artifact_is_physics_closure")
        is False,
        "source_pole_same_surface_coordinate": source_pole.get("same_surface_source_coordinate") is True,
        "source_pole_rescaling_invariant": source_pole.get("source_rescaling_invariant") is True,
        "source_pole_contact_term_invariant": source_pole.get("contact_term_invariant") is True,
        "source_pole_not_claimed_as_higgs_by_fiat": source_pole.get("canonical_higgs_operator_identity_passed") is False,
        "canonical_higgs_operator_identity": candidate.get("canonical_higgs_operator_identity_passed") is True,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--tolerance", type=float, default=1.0e-9)
    parser.add_argument("--sigma", type=float, default=3.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("PR #230 source-Higgs Gram-purity postprocessor")
    print("=" * 72)

    candidate = load_json(args.input)
    candidate_present = bool(candidate)
    checks = validate_candidate(candidate) if candidate_present else {}
    missing_checks = [key for key, ok in checks.items() if not ok]
    gate = None
    gate_passed = False

    report("candidate-certificate-state-recorded", True, f"present={candidate_present}")
    if not candidate_present:
        report("candidate-certificate-absent", True, str(args.input.relative_to(ROOT)))
    else:
        report("candidate-schema-complete", not missing_checks, f"missing_or_failed={missing_checks}")
        if all(checks[key] for key in ("has_res_c_ss", "has_res_c_sh", "has_res_c_hh")):
            gate = compute_gate(candidate, args.tolerance, args.sigma)
            gate_passed = bool(gate["purity_gate_passed"]) and not missing_checks
            report("gram-determinant-computed", True, f"Delta={gate['gram_determinant']}")
            report("normalized-overlap-computed", True, f"rho={gate['normalized_overlap_rho_sH']}")
            report("purity-gate-evaluated", True, f"passed={gate_passed}")
        else:
            report("gram-determinant-not-computable", True, "required residues absent")

    result = {
        "actual_current_surface_status": (
            "open / O_sp-Higgs Gram-purity postprocess awaiting production certificate"
            if not gate_passed
            else "support / O_sp-Higgs Gram-purity candidate numerically passed"
        ),
        "verdict": (
            "No source-Higgs production certificate is present, so the selected "
            "Gram-purity lane remains open."
            if not candidate_present
            else (
                "The candidate certificate was evaluated.  A numerical Gram "
                "purity pass is support only until all schema checks and the "
                "retained-route gate pass."
            )
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "This postprocessor is an acceptance gate; retained/proposed-retained wording still requires the retained-route certificate."
        ),
        "input_certificate": str(args.input.relative_to(ROOT)) if args.input.is_relative_to(ROOT) else str(args.input),
        "candidate_present": candidate_present,
        "candidate_checks": checks,
        "candidate_missing_or_failed_checks": missing_checks,
        "required_source_side_contract": "genuine_osp_lsz_intake_required_v1",
        "gram_purity": gate,
        "source_higgs_gram_purity_gate_passed": gate_passed,
        "osp_higgs_gram_purity_gate_passed": gate_passed,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not define O_H by fiat",
            "does not treat H_unit as O_H",
            "does not set kappa_s = 1 or cos(theta) = 1",
            "does not identify O_sp with O_H without an O_sp-Higgs Gram-purity pass",
            "does not treat the genuine O_sp intake artifact as physical y_t closure",
            "does not use yt_ward_identity, observed targets, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Supply a production same-surface O_H/C_sH/C_HH certificate, "
            "attach the genuine Legendre/LSZ O_sp source-side intake, then "
            "rerun this postprocessor and the retained-route gate."
        ),
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_display = str(args.output.relative_to(ROOT)) if args.output.is_relative_to(ROOT) else str(args.output)
    print(f"\nWrote certificate: {output_display}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
