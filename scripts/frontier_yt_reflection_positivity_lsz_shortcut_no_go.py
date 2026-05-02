#!/usr/bin/env python3
"""
PR #230 reflection-positivity LSZ shortcut no-go.

This runner tests a tempting analytic shortcut after the Stieltjes and
threshold blocks: can reflection positivity / OS reconstruction itself supply
the scalar pole-saturation premise needed by the same-source FH/LSZ readout?

It cannot.  Reflection positivity gives a positive spectral representation.
The existing positive pole-plus-continuum family can be realized as a
reflection-positive Euclidean time correlator while preserving the finite
Euclidean shell data and varying the pole residue.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
STIELTJES = ROOT / "outputs" / "yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json"
THRESHOLD = ROOT / "outputs" / "yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json"
HIGGS_IDENTITY = ROOT / "outputs" / "yt_higgs_pole_identity_latest_blocker_certificate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_reflection_positivity_lsz_shortcut_no_go_2026-05-02.json"

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


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def reflection_matrix(
    times: np.ndarray,
    pole_m2: float,
    pole_residue: float,
    continuum_m2: np.ndarray,
    continuum_weights: np.ndarray,
) -> np.ndarray:
    """OS reflection matrix M_ij = C(t_i + t_j) for a positive KL measure."""

    masses = np.sqrt(np.concatenate(([pole_m2], continuum_m2)))
    weights = np.concatenate(([pole_residue], continuum_weights))
    matrix = np.zeros((len(times), len(times)), dtype=float)
    for mass, weight in zip(masses, weights):
        vec = np.exp(-mass * times)
        matrix += (weight / (2.0 * mass)) * np.outer(vec, vec)
    return matrix


def analyze_reflection_positive_family(stieltjes: dict[str, Any]) -> dict[str, Any]:
    family = stieltjes.get("family", {})
    continuum_m2 = np.asarray(family.get("continuum_mass_squared_grid", []), dtype=float)
    pole_m2 = -float(family.get("pole_p_hat_sq", -0.25))
    times = np.asarray([0.25, 0.5, 1.0, 1.5, 2.5, 4.0], dtype=float)
    rows = []
    for model in family.get("models", []):
        weights = np.asarray(model.get("continuum_weights", []), dtype=float)
        if not model.get("success") or len(weights) != len(continuum_m2):
            rows.append(
                {
                    "pole_residue": model.get("pole_residue"),
                    "success": False,
                    "reason": "missing successful positive-continuum fit",
                }
            )
            continue
        matrix = reflection_matrix(
            times=times,
            pole_m2=pole_m2,
            pole_residue=float(model["pole_residue"]),
            continuum_m2=continuum_m2,
            continuum_weights=weights,
        )
        eigvals = np.linalg.eigvalsh(matrix)
        rows.append(
            {
                "pole_residue": float(model["pole_residue"]),
                "success": True,
                "min_continuum_weight": float(np.min(weights)),
                "min_reflection_matrix_eigenvalue": float(np.min(eigvals)),
                "condition_number_proxy": float(np.max(eigvals) / max(np.min(eigvals), 1.0e-300)),
                "dGamma_dp2_at_pole_proxy": float(model["dGamma_dp2_at_pole_proxy"]),
                "relative_y_proxy_for_fixed_dE_ds": float(model["relative_y_proxy_for_fixed_dE_ds"]),
            }
        )
    successful = [row for row in rows if row.get("success")]
    derivative_values = [float(row["dGamma_dp2_at_pole_proxy"]) for row in successful]
    y_values = [float(row["relative_y_proxy_for_fixed_dE_ds"]) for row in successful]
    return {
        "times": [float(t) for t in times],
        "pole_m2": pole_m2,
        "rows": rows,
        "all_reflection_matrices_positive": bool(successful)
        and all(float(row["min_reflection_matrix_eigenvalue"]) >= -1.0e-12 for row in successful),
        "all_spectral_weights_positive": bool(successful)
        and all(float(row["min_continuum_weight"]) >= -1.0e-12 for row in successful),
        "inverse_derivative_span_factor": float(max(derivative_values) / min(derivative_values))
        if derivative_values
        else float("nan"),
        "relative_y_proxy_span_factor": float(max(y_values) / min(y_values))
        if y_values
        else float("nan"),
    }


def main() -> int:
    print("PR #230 reflection-positivity LSZ shortcut no-go")
    print("=" * 72)

    stieltjes = load_json(STIELTJES)
    threshold = load_json(THRESHOLD)
    higgs_identity = load_json(HIGGS_IDENTITY)
    analysis = analyze_reflection_positive_family(stieltjes) if stieltjes else {}
    stieltjes_checks = stieltjes.get("family", {}).get("checks", {})

    report("stieltjes-parent-loaded", bool(stieltjes), str(STIELTJES.relative_to(ROOT)))
    report("threshold-gate-loaded", bool(threshold), str(THRESHOLD.relative_to(ROOT)))
    report("higgs-identity-blocker-loaded", bool(higgs_identity), str(HIGGS_IDENTITY.relative_to(ROOT)))
    report(
        "same-finite-shell-data-preserved",
        float(stieltjes_checks.get("max_shell_residual", float("inf"))) < 1.0e-10,
        f"max shell residual={stieltjes_checks.get('max_shell_residual')}",
    )
    report(
        "reflection-positive-family-constructed",
        bool(analysis.get("all_reflection_matrices_positive"))
        and bool(analysis.get("all_spectral_weights_positive")),
        f"rows={len(analysis.get('rows', []))}",
    )
    report(
        "reflection-positivity-does-not-fix-residue",
        float(analysis.get("inverse_derivative_span_factor", 0.0)) >= 8.0,
        f"inverse-derivative span={analysis.get('inverse_derivative_span_factor')}",
    )
    report(
        "threshold-gate-still-open",
        threshold.get("proposal_allowed") is False
        and threshold.get("pole_saturation_threshold_gate_passed") is False,
        threshold.get("actual_current_surface_status", ""),
    )
    report(
        "canonical-higgs-identity-still-open",
        higgs_identity.get("proposal_allowed") is False,
        higgs_identity.get("actual_current_surface_status", ""),
    )
    report(
        "does-not-authorize-retained-proposal",
        True,
        "OS positivity is a positive-measure condition, not a scalar LSZ theorem",
    )

    result = {
        "actual_current_surface_status": "exact negative boundary / reflection positivity not scalar LSZ closure",
        "verdict": (
            "Reflection positivity / OS reconstruction does not supply the "
            "missing PR #230 scalar LSZ normalization.  It promotes Euclidean "
            "two-point functions to positive spectral measures, but the "
            "existing positive pole-plus-continuum family is itself "
            "reflection-positive and still preserves the finite same-source "
            "shell values while changing the pole residue and inverse "
            "propagator derivative.  Therefore reflection positivity cannot "
            "replace the needed pole-saturation/threshold, microscopic scalar "
            "denominator, production continuum, or canonical-Higgs identity "
            "certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Reflection positivity gives spectral positivity, which still underidentifies the same-source scalar pole residue.",
        "parent_certificates": {
            "stieltjes_model_class": str(STIELTJES.relative_to(ROOT)),
            "pole_saturation_threshold_gate": str(THRESHOLD.relative_to(ROOT)),
            "higgs_identity_latest_blocker": str(HIGGS_IDENTITY.relative_to(ROOT)),
        },
        "reflection_positive_family": analysis,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not infer pole saturation from OS positivity",
            "does not use H_unit, yt_ward_identity, observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Continue seed-controlled production chunks when they finish, or "
            "derive a microscopic scalar-denominator/canonical-Higgs identity "
            "theorem stronger than positive spectral reconstruction."
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
