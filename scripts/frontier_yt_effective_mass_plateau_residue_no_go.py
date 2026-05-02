#!/usr/bin/env python3
"""
PR #230 effective-mass plateau residue no-go.

Future FH/LSZ production postprocessing may naturally try to extract the
same-source scalar residue from Euclidean-time correlator plateaus.  This
runner checks the shortcut claim:

    a finite effective-mass plateau fixes the ground/source-pole residue.

It does not.  Positive multi-exponential correlators can agree exactly on a
finite Euclidean-time window, and therefore have the same effective masses on
that window, while changing the ground-state residue by a large factor.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_effective_mass_plateau_residue_no_go_2026-05-02.json"

PARENTS = {
    "postprocess_gate": "outputs/yt_fh_lsz_production_postprocess_gate_2026-05-01.json",
    "same_source_two_point": "outputs/yt_same_source_scalar_two_point_lsz_measurement_2026-05-01.json",
    "finite_shell_identifiability": "outputs/yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json",
    "stieltjes_model_class": "outputs/yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json",
    "threshold_gate": "outputs/yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json",
    "short_distance_ope": "outputs/yt_short_distance_ope_lsz_no_go_2026-05-02.json",
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


def effective_masses(values: np.ndarray) -> np.ndarray:
    return np.log(values[:-1] / values[1:])


def solve_plateau_family() -> dict[str, Any]:
    ground_mass = 0.5
    excited_masses = np.asarray([0.52, 0.57, 0.65, 0.85, 1.2, 1.8, 2.8, 4.0], dtype=float)
    times = np.asarray([3.0, 4.0, 5.0, 6.0], dtype=float)
    base_residue = 1.0
    base_weights = np.asarray([2.0, 2.0, 2.0, 1.5, 1.0, 1.0, 0.8, 0.5], dtype=float)

    ground_column = np.exp(-ground_mass * times)
    excited_matrix = np.exp(-np.outer(times, excited_masses))
    target_values = base_residue * ground_column + excited_matrix @ base_weights
    target_effective_masses = effective_masses(target_values)

    models: list[dict[str, Any]] = []
    for residue in (0.2, 0.5, 1.0, 1.5, 2.0):
        rhs = target_values - residue * ground_column
        result = linprog(
            c=np.zeros(len(excited_masses)),
            A_eq=excited_matrix,
            b_eq=rhs,
            bounds=[(0.0, None)] * len(excited_masses),
            method="highs",
        )
        if not result.success:
            models.append(
                {
                    "ground_residue": residue,
                    "success": False,
                    "message": result.message,
                }
            )
            continue
        values = residue * ground_column + excited_matrix @ result.x
        model_effective_masses = effective_masses(values)
        models.append(
            {
                "ground_residue": residue,
                "success": True,
                "excited_weights": [float(x) for x in result.x],
                "min_excited_weight": float(np.min(result.x)),
                "max_abs_correlator_residual": float(np.max(np.abs(values - target_values))),
                "effective_masses": [float(x) for x in model_effective_masses],
                "max_abs_effective_mass_residual": float(
                    np.max(np.abs(model_effective_masses - target_effective_masses))
                ),
                "relative_y_proxy_for_fixed_dE_ds": float(1.0 / math.sqrt(residue)),
            }
        )

    successful = [model for model in models if model.get("success")]
    residues = [float(model["ground_residue"]) for model in successful]
    y_values = [float(model["relative_y_proxy_for_fixed_dE_ds"]) for model in successful]
    correlator_residuals = [float(model["max_abs_correlator_residual"]) for model in successful]
    meff_residuals = [float(model["max_abs_effective_mass_residual"]) for model in successful]
    return {
        "ground_mass": ground_mass,
        "times": [float(x) for x in times],
        "excited_masses": [float(x) for x in excited_masses],
        "target_correlator_values": [float(x) for x in target_values],
        "target_effective_masses": [float(x) for x in target_effective_masses],
        "target_effective_mass_spread": float(max(target_effective_masses) - min(target_effective_masses)),
        "models": models,
        "checks": {
            "all_models_positive": len(successful) == len(models)
            and all(float(model.get("min_excited_weight", -1.0)) >= -1.0e-12 for model in successful),
            "max_abs_correlator_residual": max(correlator_residuals) if correlator_residuals else float("inf"),
            "max_abs_effective_mass_residual": max(meff_residuals) if meff_residuals else float("inf"),
            "ground_residue_span_factor": max(residues) / min(residues) if residues else float("nan"),
            "y_proxy_span_factor": max(y_values) / min(y_values) if y_values else float("nan"),
        },
    }


def main() -> int:
    print("PR #230 effective-mass plateau residue no-go")
    print("=" * 72)

    parents = {name: load(path) for name, path in PARENTS.items()}
    missing = [name for name, cert in parents.items() if not cert]
    proposal_allowed = [name for name, cert in parents.items() if cert.get("proposal_allowed") is True]
    family = solve_plateau_family()
    checks = family["checks"]

    postprocess_gate_blocks = (
        "postprocess gate" in status(parents["postprocess_gate"])
        and parents["postprocess_gate"].get("retained_proposal_gate_ready") is False
    )
    two_point_support_only = (
        "same-source scalar two-point" in status(parents["same_source_two_point"])
        and parents["same_source_two_point"].get("proposal_allowed") is False
    )
    finite_shell_blocks = (
        "finite-shell pole-fit identifiability no-go" in status(parents["finite_shell_identifiability"])
        and parents["finite_shell_identifiability"].get("proposal_allowed") is False
    )
    stieltjes_blocks = (
        "Stieltjes model-class obstruction" in status(parents["stieltjes_model_class"])
        and parents["stieltjes_model_class"].get("proposal_allowed") is False
    )
    threshold_gate_blocks = (
        "pole-saturation threshold gate" in status(parents["threshold_gate"])
        and parents["threshold_gate"].get("pole_saturation_threshold_gate_passed") is False
    )
    ope_blocks_uv_shortcut = (
        "short-distance OPE not scalar LSZ closure" in status(parents["short_distance_ope"])
        and parents["short_distance_ope"].get("proposal_allowed") is False
    )
    sufficiency_not_passed = (
        "same-source pole-data sufficiency gate not passed" in status(parents["same_source_sufficiency"])
        and parents["same_source_sufficiency"].get("gate_passed") is False
    )
    plateau_residue_gate_passed = False

    report("parent-certificates-present", not missing, f"missing={missing}")
    report("no-parent-authorizes-proposal", not proposal_allowed, f"proposal_allowed={proposal_allowed}")
    report("postprocess-gate-still-blocks-production-use", postprocess_gate_blocks, status(parents["postprocess_gate"]))
    report("same-source-two-point-is-support-only", two_point_support_only, status(parents["same_source_two_point"]))
    report("finite-shell-and-stieltjes-shortcuts-blocked", finite_shell_blocks and stieltjes_blocks, "momentum and positivity ambiguity already loaded")
    report("threshold-gate-still-blocks-pole-residue-use", threshold_gate_blocks, status(parents["threshold_gate"]))
    report("uv-ope-shortcut-blocked", ope_blocks_uv_shortcut, status(parents["short_distance_ope"]))
    report("finite-time-positive-family-constructed", checks["all_models_positive"], f"residue_span={checks['ground_residue_span_factor']}")
    report("finite-time-correlator-window-held-fixed", checks["max_abs_correlator_residual"] < 1.0e-12, f"max_residual={checks['max_abs_correlator_residual']:.3e}")
    report("effective-mass-window-held-fixed", checks["max_abs_effective_mass_residual"] < 1.0e-12, f"max_meff_residual={checks['max_abs_effective_mass_residual']:.3e}")
    report("window-is-plateau-like-but-not-residue-fixing", family["target_effective_mass_spread"] < 0.03, f"meff_spread={family['target_effective_mass_spread']:.6g}")
    report("ground-residue-still-varies", checks["ground_residue_span_factor"] >= 10.0, f"span={checks['ground_residue_span_factor']:.6g}")
    report("physical-y-proxy-varies", checks["y_proxy_span_factor"] >= 3.0, f"span={checks['y_proxy_span_factor']:.6g}")
    report("same-source-sufficiency-gate-still-not-passed", sufficiency_not_passed, status(parents["same_source_sufficiency"]))
    report("effective-mass-plateau-not-lsz-closure", not plateau_residue_gate_passed, "finite plateau window does not identify residue")

    result = {
        "actual_current_surface_status": "exact negative boundary / effective-mass plateau not scalar LSZ residue closure",
        "verdict": (
            "A finite Euclidean-time effective-mass plateau does not determine "
            "the same-source scalar pole residue needed by PR #230.  Positive "
            "multi-exponential correlators can agree exactly on a finite time "
            "window, and therefore have identical effective masses on that "
            "window, while the ground/source-pole residue varies by a factor "
            "of ten.  A production plateau can be useful diagnostics, but it "
            "needs a model-class, spectral-gap/pole-saturation, continuum, or "
            "microscopic scalar-denominator certificate before its amplitude "
            "can be load-bearing for FH/LSZ y_t closure."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite effective-mass plateau data leave the same-source pole residue underdetermined.",
        "effective_mass_plateau_residue_gate_passed": plateau_residue_gate_passed,
        "parent_certificates": PARENTS,
        "finite_time_family": family,
        "strict_non_claims": [
            "does not claim retained or proposed_retained y_t closure",
            "does not set kappa_s = 1",
            "does not infer source-pole residue from a finite plateau window",
            "does not use H_unit matrix-element readout or yt_ward_identity",
            "does not use observed top mass, observed y_t, alpha_LM, plaquette, u0, c2 = 1, or Z_match = 1",
        ],
        "exact_next_action": (
            "Process seed-controlled chunks through the combiner when they "
            "finish, but require a spectral-gap/model-class/FV/IR/Higgs-"
            "identity certificate before any finite-time plateau amplitude is "
            "used as scalar LSZ residue evidence."
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
