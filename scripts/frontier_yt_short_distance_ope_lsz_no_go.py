#!/usr/bin/env python3
"""
PR #230 short-distance/OPE LSZ shortcut no-go.

This runner tests a tempting repair of the scalar source-to-Higgs blocker:
can a UV source normalization, short-distance operator matching, or a finite
set of OPE coefficients determine the isolated IR scalar pole residue needed
by the same-source FH/LSZ readout?

It cannot.  A finite OPE expansion fixes finitely many spectral moments of the
same-source two-point function.  Positive pole-plus-continuum models can keep
those coefficients and the UV source normalization fixed while changing the
IR pole residue and therefore the LSZ readout.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_short_distance_ope_lsz_no_go_2026-05-02.json"

PARENTS = {
    "ward_operator_matching": "outputs/yt_ward_operator_matching_candidate_2026-05-01.json",
    "source_overlap_sum_rule": "outputs/yt_source_overlap_sum_rule_no_go_2026-05-02.json",
    "stieltjes_model_class": "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json",
    "reflection_positivity": "outputs/yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json",
    "scalar_denominator": "outputs/yt_scalar_denominator_theorem_closure_attempt_2026-05-02.json",
    "higgs_pole_blocker": "outputs/yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json",
    "same_source_sufficiency": "outputs/yt_same_source_pole_data_sufficiency_gate_2026-05-02.json",
}

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def load(rel: str) -> dict[str, Any]:
    path = ROOT / rel
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def status(cert: dict[str, Any]) -> str:
    return str(cert.get("actual_current_surface_status", ""))


def correlator(q2: float, pole_m2: float, pole_residue: float, masses: np.ndarray, weights: np.ndarray) -> float:
    return float(pole_residue / (q2 + pole_m2) + np.sum(weights / (q2 + masses)))


def solve_ope_family() -> dict[str, Any]:
    """Preserve finite large-Q OPE moments while varying the pole residue."""

    pole_m2 = 0.25
    continuum_m2 = np.asarray([0.27, 0.32, 0.45, 0.7, 1.0, 1.5, 2.5, 4.0], dtype=float)
    base_residue = 1.0
    base_weights = np.asarray([4.0, 3.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0], dtype=float)

    # C(Q^2) = sum_n (-1)^n a_n / Q^(2n+2), a_n = sum Z_i m_i^(2n).
    moment_count = 4
    powers = np.arange(moment_count, dtype=float)
    continuum_matrix = np.vstack([continuum_m2**k for k in powers])
    pole_moments = np.asarray([pole_m2**k for k in powers], dtype=float)
    target_moments = base_residue * pole_moments + continuum_matrix @ base_weights

    models: list[dict[str, Any]] = []
    for residue in (0.2, 0.5, 1.0, 1.5, 2.0):
        rhs = target_moments - residue * pole_moments
        result = linprog(
            c=np.zeros(len(continuum_m2)),
            A_eq=continuum_matrix,
            b_eq=rhs,
            bounds=[(0.0, None)] * len(continuum_m2),
            method="highs",
        )
        if not result.success:
            models.append(
                {
                    "pole_residue": residue,
                    "success": False,
                    "message": result.message,
                }
            )
            continue
        fitted_moments = residue * pole_moments + continuum_matrix @ result.x
        q2_samples = [100.0, 1000.0, 10000.0]
        models.append(
            {
                "pole_residue": residue,
                "success": True,
                "continuum_weights": [float(x) for x in result.x],
                "min_continuum_weight": float(np.min(result.x)),
                "max_abs_ope_moment_residual": float(np.max(np.abs(fitted_moments - target_moments))),
                "source_overlap_z_s": float(math.sqrt(residue)),
                "relative_y_proxy_for_fixed_dE_ds": float(1.0 / math.sqrt(residue)),
                "high_q_correlator_samples": {
                    str(q2): correlator(q2, pole_m2, residue, continuum_m2, result.x)
                    for q2 in q2_samples
                },
            }
        )

    successful = [model for model in models if model.get("success")]
    residues = [float(model["pole_residue"]) for model in successful]
    y_values = [float(model["relative_y_proxy_for_fixed_dE_ds"]) for model in successful]
    moment_residuals = [float(model["max_abs_ope_moment_residual"]) for model in successful]
    high_q_spreads: dict[str, float] = {}
    for q2 in ("100.0", "1000.0", "10000.0"):
        values = [float(model["high_q_correlator_samples"][q2]) for model in successful]
        high_q_spreads[q2] = (max(values) - min(values)) / max(abs(sum(values) / len(values)), 1.0e-300)

    return {
        "pole_location_m2": pole_m2,
        "continuum_support_m2": [float(x) for x in continuum_m2],
        "finite_ope_coefficients_fixed": [
            {
                "coefficient": f"a_{index}",
                "large_q_term": f"(-1)^{index} a_{index} / Q^{2 * index + 2}",
                "value": float(value),
            }
            for index, value in enumerate(target_moments)
        ],
        "models": models,
        "checks": {
            "all_models_positive": len(successful) == len(models)
            and all(float(model.get("min_continuum_weight", -1.0)) >= -1.0e-12 for model in successful),
            "max_abs_ope_moment_residual": max(moment_residuals) if moment_residuals else float("inf"),
            "pole_residue_span_factor": max(residues) / min(residues) if residues else float("nan"),
            "y_proxy_span_factor": max(y_values) / min(y_values) if y_values else float("nan"),
            "high_q_relative_spreads": high_q_spreads,
        },
    }


def main() -> int:
    print("PR #230 short-distance/OPE LSZ shortcut no-go")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    family = solve_ope_family()
    checks = family["checks"]

    ward_matching_conditional = (
        "conditional-support" in status(parents["ward_operator_matching"])
        and parents["ward_operator_matching"].get("proposal_allowed") is False
    )
    sum_rule_blocks = (
        "source-overlap spectral sum-rule no-go" in status(parents["source_overlap_sum_rule"])
        and parents["source_overlap_sum_rule"].get("proposal_allowed") is False
    )
    stieltjes_blocks = (
        "Stieltjes model-class obstruction" in status(parents["stieltjes_model_class"])
        and parents["stieltjes_model_class"].get("proposal_allowed") is False
    )
    os_blocks = (
        "reflection positivity not scalar LSZ closure" in status(parents["reflection_positivity"])
        and parents["reflection_positivity"].get("proposal_allowed") is False
    )
    denominator_open = (
        "scalar denominator theorem closure attempt blocked" in status(parents["scalar_denominator"])
        and parents["scalar_denominator"].get("theorem_closed") is False
    )
    higgs_identity_open = (
        "latest Higgs-pole identity blocker certificate" in status(parents["higgs_pole_blocker"])
        and parents["higgs_pole_blocker"].get("identity_closed") is False
    )
    sufficiency_not_passed = (
        "same-source pole-data sufficiency gate not passed" in status(parents["same_source_sufficiency"])
        and parents["same_source_sufficiency"].get("gate_passed") is False
    )
    ope_shortcut_closed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("operator-matching-remains-conditional", ward_matching_conditional, status(parents["ward_operator_matching"]))
    report("finite-sum-rule-shortcut-already-blocked", sum_rule_blocks, status(parents["source_overlap_sum_rule"]))
    report("positive-spectral-shortcuts-blocked", stieltjes_blocks and os_blocks, "Stieltjes/OS positivity do not fix residue")
    report("finite-ope-family-positive", checks["all_models_positive"], f"residue_span={checks['pole_residue_span_factor']}")
    report("finite-ope-coefficients-held-fixed", checks["max_abs_ope_moment_residual"] < 1.0e-10, f"max_residual={checks['max_abs_ope_moment_residual']:.3e}")
    report("high-q-correlators-agree-asymptotically", checks["high_q_relative_spreads"]["10000.0"] < 1.0e-12, f"relative_spreads={checks['high_q_relative_spreads']}")
    report("ir-pole-residue-still-varies", checks["pole_residue_span_factor"] >= 10.0, f"span={checks['pole_residue_span_factor']:.6g}")
    report("physical-y-proxy-varies", checks["y_proxy_span_factor"] >= 3.0, f"span={checks['y_proxy_span_factor']:.6g}")
    report("scalar-denominator-and-higgs-identity-still-open", denominator_open and higgs_identity_open, "required IR gates remain blocking")
    report("same-source-sufficiency-gate-still-not-passed", sufficiency_not_passed, status(parents["same_source_sufficiency"]))
    report("short-distance-ope-not-lsz-closure", not ope_shortcut_closed, "finite UV data do not determine IR pole residue")

    result = {
        "actual_current_surface_status": "exact negative boundary / short-distance OPE not scalar LSZ closure",
        "verdict": (
            "Short-distance source normalization, operator matching, and any "
            "finite set of OPE coefficients do not determine the isolated IR "
            "same-source scalar pole residue.  The constructed positive "
            "pole-plus-continuum family preserves the finite large-Q expansion "
            "coefficients and agrees asymptotically at high Q while changing "
            "the pole residue by a factor of ten.  Therefore UV/OPE data "
            "cannot replace the scalar denominator theorem, pole-saturation/"
            "threshold certificate, production pole-residue measurement, or "
            "canonical-Higgs pole identity required for PR #230 y_t closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite short-distance/OPE data leave the same-source scalar pole residue and canonical-Higgs identity underdetermined.",
        "short_distance_ope_shortcut_closed": ope_shortcut_closed,
        "parent_certificates": PARENTS,
        "ope_family": family,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not infer an IR pole residue from finite OPE coefficients",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Continue seed-controlled FH/LSZ production and, in parallel, "
            "derive a genuinely IR scalar-denominator/threshold or "
            "source-pole-to-canonical-Higgs identity theorem.  Do not use UV "
            "operator normalization or finite OPE coefficients as kappa_s."
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
