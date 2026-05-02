#!/usr/bin/env python3
"""
PR #230 FH/LSZ pole-saturation threshold gate.

This runner turns the Stieltjes obstruction into an executable acceptance test.
Given finite Euclidean shell values, a named scalar pole, positivity, and a
candidate continuum threshold, it solves the linear feasibility problem for the
allowed pole residue interval.  Retained use is blocked unless a future
pole-saturation/threshold certificate makes that interval tight.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
STIELTJES = ROOT / "outputs" / "yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json"
MODEL_CLASS_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json"
THRESHOLD_CERT = ROOT / "outputs" / "yt_fh_lsz_pole_saturation_threshold_certificate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_pole_saturation_threshold_gate_2026-05-02.json"

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


def solve_residue_interval(
    shells: np.ndarray,
    target_c: np.ndarray,
    pole_m2: float,
    continuum_m2: np.ndarray,
) -> dict[str, Any]:
    pole_column = 1.0 / (shells + pole_m2)
    continuum_matrix = 1.0 / (shells[:, None] + continuum_m2[None, :])
    matrix = np.column_stack([pole_column, continuum_matrix])
    bounds = [(0.0, None)] * matrix.shape[1]
    min_result = linprog(
        c=np.r_[1.0, np.zeros(len(continuum_m2))],
        A_eq=matrix,
        b_eq=target_c,
        bounds=bounds,
        method="highs",
    )
    max_result = linprog(
        c=np.r_[-1.0, np.zeros(len(continuum_m2))],
        A_eq=matrix,
        b_eq=target_c,
        bounds=bounds,
        method="highs",
    )
    if not min_result.success or not max_result.success:
        return {
            "feasible": False,
            "min_message": min_result.message,
            "max_message": max_result.message,
        }
    residue_min = float(min_result.fun)
    residue_max = float(-max_result.fun)
    if residue_min <= 0.0:
        relative_width = None
        y_proxy_span = None
    else:
        relative_width = float((residue_max - residue_min) / residue_min)
        y_proxy_span = float(math.sqrt(residue_max / residue_min))
    return {
        "feasible": True,
        "residue_min": residue_min,
        "residue_max": residue_max,
        "relative_width_over_lower": relative_width,
        "y_proxy_span_factor": y_proxy_span,
        "lower_bound_is_zero": residue_min <= 1.0e-12,
    }


def build_gate_scan() -> dict[str, Any]:
    one_link = 4.0 * math.sin(math.pi / 12.0) ** 2
    shells = np.asarray([0.0, one_link, 2.0 * one_link, 1.0], dtype=float)
    pole_m2 = 0.25
    continuum_m2 = np.asarray([0.260, 0.28, 0.33, 0.45, 0.7, 1.2, 2.0, 4.0, 8.0, 16.0])
    target_c = 1.0 / (shells + pole_m2) + (
        1.0 / (shells[:, None] + continuum_m2[None, :])
    ) @ np.full(len(continuum_m2), 2.0)
    thresholds = [0.251, 0.260, 0.300, 0.500, 1.000]
    rows = []
    for threshold in thresholds:
        grid = continuum_m2[continuum_m2 >= threshold]
        if len(grid) < len(shells):
            grid = np.linspace(threshold, 32.0, 16)
        interval = solve_residue_interval(shells, target_c, pole_m2, grid)
        rows.append(
            {
                "continuum_threshold_m2": threshold,
                "continuum_grid_size": int(len(grid)),
                **interval,
            }
        )
    return {
        "shells_p_hat_sq": [float(x) for x in shells],
        "pole_p_hat_sq": -pole_m2,
        "target_c_shell_values": [float(x) for x in target_c],
        "threshold_rows": rows,
    }


def main() -> int:
    print("PR #230 FH/LSZ pole-saturation threshold gate")
    print("=" * 72)

    stieltjes = load_json(STIELTJES)
    model_gate = load_json(MODEL_CLASS_GATE)
    threshold_cert = load_json(THRESHOLD_CERT)
    scan = build_gate_scan()
    near_threshold = scan["threshold_rows"][0]
    accepted_rows = [
        row
        for row in scan["threshold_rows"]
        if row.get("feasible")
        and not row.get("lower_bound_is_zero")
        and float(row.get("relative_width_over_lower", float("inf"))) <= 0.02
    ]
    gate_passed = bool(threshold_cert.get("pole_saturation_threshold_gate_passed")) and bool(accepted_rows)

    report("stieltjes-obstruction-loaded", bool(stieltjes), str(STIELTJES.relative_to(ROOT)))
    report("model-class-gate-loaded", bool(model_gate), str(MODEL_CLASS_GATE.relative_to(ROOT)))
    report("threshold-certificate-absent", not threshold_cert, str(THRESHOLD_CERT.relative_to(ROOT)))
    report("positive-continuum-lp-feasible", bool(near_threshold.get("feasible")), f"threshold={near_threshold['continuum_threshold_m2']}")
    report("residue-interval-not-tight", near_threshold.get("lower_bound_is_zero") is True, f"interval=[{near_threshold.get('residue_min')}, {near_threshold.get('residue_max')}]")
    report("retained-use-blocked-without-pole-saturation", not gate_passed, f"gate_passed={gate_passed}")
    report("does-not-authorize-retained-proposal", True, "threshold gate is open/blocking, not closure")

    result = {
        "actual_current_surface_status": "open / FH-LSZ pole-saturation threshold gate blocks current finite-shell fit",
        "verdict": (
            "The finite-shell FH/LSZ residue problem can be written as a linear "
            "positive-Stieltjes feasibility interval for the pole residue.  On "
            "the current finite-shell surface, a continuum threshold arbitrarily "
            "near the pole leaves the pole residue interval with zero lower "
            "bound and a broad upper bound.  A future finite-shell pole fit "
            "therefore needs a certified pole-saturation, continuum-threshold, "
            "or microscopic scalar-denominator input that makes this interval "
            "tight before dGamma_ss/dp^2 can be load-bearing."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "No pole-saturation/continuum-threshold certificate makes the pole residue interval tight.",
        "pole_saturation_threshold_gate_passed": gate_passed,
        "acceptance_rule": {
            "required_certificate": str(THRESHOLD_CERT.relative_to(ROOT)),
            "required_interval": "positive lower bound and relative_width_over_lower <= 0.02",
            "current_result": "not passed",
        },
        "parent_certificates": {
            "stieltjes_obstruction": str(STIELTJES.relative_to(ROOT)),
            "model_class_gate": str(MODEL_CLASS_GATE.relative_to(ROOT)),
        },
        "gate_scan": scan,
        "strict_non_claims": [
            "does not claim a physical scalar pole residue",
            "does not set kappa_s = 1",
            "does not use observed top mass or observed y_t",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Either derive a microscopic scalar denominator/pole-saturation "
            "theorem, or obtain production data plus a continuum-threshold "
            "certificate that makes the LP residue interval tight."
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
