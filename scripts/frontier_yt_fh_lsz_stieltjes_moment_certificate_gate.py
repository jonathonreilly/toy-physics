#!/usr/bin/env python3
"""
PR #230 FH/LSZ Stieltjes moment-certificate gate.

This runner turns the scalar-LSZ model-class residual into a strict positive
certificate contract.  A future finite-shell pole fit is not enough; the
scalar channel must also supply a positive Stieltjes moment certificate,
threshold/pole-saturation control, FV/IR control, and the usual PR230
forbidden-import firewall.

The current branch intentionally has no such future certificate, so this gate
records exact support for the acceptance rule and keeps proposal_allowed false.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_stieltjes_moment_certificate_gate_2026-05-05.json"
FUTURE_CERTIFICATE = (
    ROOT / "outputs" / "yt_fh_lsz_stieltjes_moment_certificate_2026-05-05.json"
)

PARENTS = {
    "model_class_gate": "outputs/yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json",
    "model_class_semantic_firewall": (
        "outputs/yt_fh_lsz_model_class_semantic_firewall_2026-05-04.json"
    ),
    "stieltjes_obstruction": (
        "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json"
    ),
    "pole_saturation_threshold": (
        "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json"
    ),
    "finite_volume_obstruction": (
        "outputs/yt_fh_lsz_finite_volume_pole_saturation_obstruction_2026-05-02.json"
    ),
    "soft_continuum_no_go": "outputs/yt_fh_lsz_soft_continuum_threshold_no_go_2026-05-02.json",
    "common_window_response": "outputs/yt_fh_lsz_common_window_response_gate_2026-05-04.json",
    "polefit8x8_postprocessor": "outputs/yt_fh_lsz_polefit8x8_postprocessor_2026-05-04.json",
}

FORBIDDEN_TEXT_FRAGMENTS = (
    "H_unit",
    "yt_ward_identity",
    "YT_WARD_IDENTITY_DERIVATION_THEOREM",
    "alpha_LM",
    "plaquette",
    "u0",
    "observed top mass",
    "observed y_t",
    "kappa_s = 1",
    "c2 = 1",
    "Z_match = 1",
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


def det(matrix: list[list[float]]) -> float:
    n = len(matrix)
    if n == 0:
        return 1.0
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    total = 0.0
    for column, value in enumerate(matrix[0]):
        minor = [
            [row[j] for j in range(n) if j != column]
            for row in matrix[1:]
        ]
        total += ((-1.0) ** column) * value * det(minor)
    return total


def hankel(moments: list[float], order: int, shift: int = 0) -> list[list[float]]:
    return [[moments[i + j + shift] for j in range(order)] for i in range(order)]


def principal_minors(matrix: list[list[float]]) -> list[dict[str, Any]]:
    rows = range(len(matrix))
    out = []
    for size in range(1, len(matrix) + 1):
        for indices in itertools.combinations(rows, size):
            sub = [[matrix[i][j] for j in indices] for i in indices]
            out.append(
                {
                    "indices": list(indices),
                    "determinant": det(sub),
                }
            )
    return out


def psd_check(matrix: list[list[float]], tolerance: float = 1.0e-12) -> dict[str, Any]:
    minors = principal_minors(matrix)
    minimum = min(row["determinant"] for row in minors)
    return {
        "minimum_principal_minor": minimum,
        "principal_minors": minors,
        "psd": minimum >= -tolerance,
    }


def stieltjes_moments(atoms: list[dict[str, float]], nmax: int, shift: float = 1.0) -> list[float]:
    moments = []
    for n in range(nmax + 1):
        moments.append(
            sum(atom["weight"] / (atom["mass_squared"] + shift) ** (n + 1) for atom in atoms)
        )
    return moments


def witness_family() -> dict[str, Any]:
    positive_atoms = [
        {"weight": 1.20, "mass_squared": 0.80},
        {"weight": 0.45, "mass_squared": 2.40},
        {"weight": 0.18, "mass_squared": 5.25},
    ]
    positive_moments = stieltjes_moments(positive_atoms, nmax=5)
    invalid_moments = [1.0, 1.0, 0.50, 0.25, 0.125, 0.0625]

    positive_h2 = psd_check(hankel(positive_moments, 2))
    positive_h3 = psd_check(hankel(positive_moments, 3))
    positive_shifted_h2 = psd_check(hankel(positive_moments, 2, shift=1))
    invalid_h2 = psd_check(hankel(invalid_moments, 2))

    return {
        "theorem": (
            "If C(q^2) is a positive Stieltjes transform "
            "int dmu(s)/(q^2+s), then the moment sequence m_n has positive "
            "Hankel matrices H_ij=m_{i+j} and shifted Hankel matrices "
            "H'_ij=m_{i+j+1}.  A finite-shell fit that does not provide this "
            "moment-positivity certificate is not a scalar-LSZ model-class "
            "certificate."
        ),
        "positive_atoms": positive_atoms,
        "positive_moments": positive_moments,
        "positive_checks": {
            "hankel_order_2": positive_h2,
            "hankel_order_3": positive_h3,
            "shifted_hankel_order_2": positive_shifted_h2,
        },
        "invalid_shell_like_moments": invalid_moments,
        "invalid_checks": {
            "hankel_order_2": invalid_h2,
            "violates_psd": invalid_h2["psd"] is False,
        },
    }


def string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        values: list[str] = []
        for child in value.values():
            values.extend(string_values(child))
        return values
    if isinstance(value, list):
        values = []
        for child in value:
            values.extend(string_values(child))
        return values
    return []


def forbidden_fragment_present(candidate: dict[str, Any]) -> list[str]:
    encoded_values = "\n".join(string_values(candidate))
    return [fragment for fragment in FORBIDDEN_TEXT_FRAGMENTS if fragment in encoded_values]


def validate_future_certificate(candidate: dict[str, Any]) -> dict[str, bool]:
    moments = candidate.get("moments")
    if isinstance(moments, list) and len(moments) >= 5:
        try:
            moment_values = [float(x) for x in moments]
            h2 = psd_check(hankel(moment_values, 2))
            h3 = psd_check(hankel(moment_values, 3))
            shifted = psd_check(hankel(moment_values, 2, shift=1))
            moment_psd = h2["psd"] and h3["psd"] and shifted["psd"]
        except (TypeError, ValueError):
            moment_psd = False
    else:
        moment_psd = False

    firewall = candidate.get("firewall", {}) if isinstance(candidate.get("firewall"), dict) else {}
    residue_interval = (
        candidate.get("residue_interval", {})
        if isinstance(candidate.get("residue_interval"), dict)
        else {}
    )
    return {
        "certificate_kind": candidate.get("certificate_kind")
        == "fh_lsz_stieltjes_moment_certificate",
        "same_surface_cl3_z3": candidate.get("same_surface_cl3_z3") is True,
        "source_coordinate_declared": isinstance(candidate.get("source_coordinate"), str)
        and bool(candidate.get("source_coordinate")),
        "zero_source_limit_declared": candidate.get("zero_source_limit_declared") is True,
        "moment_hankel_psd": moment_psd,
        "pole_location_certified": candidate.get("pole_location_certified") is True,
        "pole_residue_positive": float(candidate.get("pole_residue", 0.0) or 0.0) > 0.0,
        "residue_interval_tight": (
            residue_interval.get("lower_bound_positive") is True
            and float(residue_interval.get("relative_width_over_lower", 1.0) or 1.0) <= 0.02
        ),
        "threshold_gap_certified": candidate.get("threshold_gap_certified") is True,
        "fv_ir_control_certified": candidate.get("fv_ir_control_certified") is True,
        "analytic_continuation_or_denominator_authority": candidate.get(
            "analytic_continuation_or_denominator_authority"
        )
        is True,
        "no_observed_selector": firewall.get("used_observed_targets_as_selectors") is False,
        "no_hunit_or_ward_authority": firewall.get("used_hunit_or_ward_authority") is False,
        "no_alpha_lm_or_plaquette": firewall.get("used_alpha_lm_or_plaquette") is False,
        "no_unit_shortcut": firewall.get("set_kappa_c2_zmatch_equal_one") is False,
        "no_forbidden_text_fragments": not forbidden_fragment_present(candidate),
    }


def main() -> int:
    print("PR #230 FH/LSZ Stieltjes moment-certificate gate")
    print("=" * 72)

    parent_certs = {name: load_json(ROOT / rel) for name, rel in PARENTS.items()}
    missing_parents = [name for name, cert in parent_certs.items() if not cert]
    statuses = {
        name: str(cert.get("actual_current_surface_status", "")) for name, cert in parent_certs.items()
    }
    future = load_json(FUTURE_CERTIFICATE)
    future_checks = validate_future_certificate(future) if future else {}
    future_missing_or_failed = [name for name, ok in future_checks.items() if not ok]
    future_gate_passed = bool(future) and not future_missing_or_failed
    witness = witness_family()

    positive_witness_passes = (
        witness["positive_checks"]["hankel_order_2"]["psd"]
        and witness["positive_checks"]["hankel_order_3"]["psd"]
        and witness["positive_checks"]["shifted_hankel_order_2"]["psd"]
    )
    invalid_witness_rejected = witness["invalid_checks"]["violates_psd"] is True

    report("parents-loaded", not missing_parents, f"missing={missing_parents}")
    report(
        "model-class-gate-still-open",
        "model-class gate blocks finite-shell fit" in statuses["model_class_gate"],
        statuses["model_class_gate"],
    )
    report(
        "stieltjes-positivity-alone-blocked",
        "Stieltjes model-class obstruction" in statuses["stieltjes_obstruction"],
        statuses["stieltjes_obstruction"],
    )
    report(
        "pole-saturation-threshold-still-required",
        "pole-saturation threshold gate" in statuses["pole_saturation_threshold"],
        statuses["pole_saturation_threshold"],
    )
    report(
        "fv-ir-boundary-still-required",
        "finite-volume pole-saturation obstruction" in statuses["finite_volume_obstruction"]
        and "soft-continuum threshold no-go" in statuses["soft_continuum_no_go"],
        f"{statuses['finite_volume_obstruction']} / {statuses['soft_continuum_no_go']}",
    )
    report(
        "positive-stieltjes-moment-witness-passes-hankel-psd",
        positive_witness_passes,
        "H2/H3/shifted-H2 PSD",
    )
    report(
        "invalid-finite-shell-moment-witness-rejected",
        invalid_witness_rejected,
        "H2 determinant is negative",
    )
    report(
        "future-moment-certificate-absent",
        not future,
        str(FUTURE_CERTIFICATE.relative_to(ROOT)),
    )
    if future:
        report(
            "future-moment-certificate-valid",
            future_gate_passed,
            f"missing_or_failed={future_missing_or_failed}",
        )
    report(
        "moment-certificate-gate-not-passed-on-current-surface",
        not future_gate_passed,
        f"future_gate_passed={future_gate_passed}",
    )
    report("does-not-authorize-proposed-retained", True, "strict positive certificate is absent")

    result = {
        "actual_current_surface_status": (
            "exact-support / FH-LSZ Stieltjes moment-certificate gate; strict "
            "positive certificate absent"
        ),
        "verdict": (
            "The scalar-LSZ model-class route now has a strict positive "
            "Stieltjes moment certificate contract.  Future finite-shell or "
            "pole-fit rows must be accompanied by Hankel moment positivity, "
            "a tight positive pole-residue interval, threshold-gap control, "
            "FV/IR control, analytic-continuation or scalar-denominator "
            "authority, and the PR230 forbidden-import firewall.  The current "
            "surface supplies no such certificate, so this is an exact support "
            "gate rather than closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": (
            "No strict positive Stieltjes moment certificate is present; "
            "finite-shell pole fits remain support-only."
        ),
        "moment_certificate_gate_passed": future_gate_passed,
        "future_certificate": str(FUTURE_CERTIFICATE.relative_to(ROOT)),
        "future_certificate_checks": future_checks,
        "future_certificate_missing_or_failed_checks": future_missing_or_failed,
        "parent_certificates": PARENTS,
        "witness_family": witness,
        "acceptance_contract": {
            "certificate_kind": "fh_lsz_stieltjes_moment_certificate",
            "required_fields": [
                "same_surface_cl3_z3",
                "source_coordinate",
                "zero_source_limit_declared",
                "moments",
                "pole_location_certified",
                "pole_residue",
                "residue_interval.lower_bound_positive",
                "residue_interval.relative_width_over_lower <= 0.02",
                "threshold_gap_certified",
                "fv_ir_control_certified",
                "analytic_continuation_or_denominator_authority",
                "firewall.used_observed_targets_as_selectors == false",
                "firewall.used_hunit_or_ward_authority == false",
                "firewall.used_alpha_lm_or_plaquette == false",
                "firewall.set_kappa_c2_zmatch_equal_one == false",
            ],
            "mathematical_checks": [
                "Hankel H_ij=m_{i+j} positive semidefinite through order 3",
                "shifted Hankel H'_ij=m_{i+j+1} positive semidefinite through order 2",
                "positive pole residue with tight residue interval",
            ],
        },
        "strict_non_claims": [
            "does not claim scalar LSZ closure",
            "does not accept finite-shell pole fits as physical residue evidence",
            "does not define y_t_bare",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, u0, or observed targets",
            "does not set kappa_s, c2, or Z_match to one",
        ],
        "exact_next_action": (
            "Either produce the strict Stieltjes moment certificate from "
            "production scalar data, or derive a stronger microscopic scalar "
            "denominator theorem that supplies the same positivity, threshold, "
            "and FV/IR authority without finite-shell fitting."
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
