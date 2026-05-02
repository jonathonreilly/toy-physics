#!/usr/bin/env python3
"""
PR #230 FH/LSZ Stieltjes model-class obstruction.

This runner checks whether imposing a positive spectral/Stieltjes form is
enough to turn finite Euclidean shell rows into a unique scalar LSZ residue.  It
is not.  Positive pole-plus-continuum models can agree on the finite shell
values and share the same isolated pole while changing the pole residue.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
FINITE_SHELL_NO_GO = ROOT / "outputs" / "yt_fh_lsz_finite_shell_identifiability_no_go_2026-05-02.json"
MODEL_CLASS_GATE = ROOT / "outputs" / "yt_fh_lsz_pole_fit_model_class_gate_2026-05-02.json"
OUTPUT = ROOT / "outputs" / "yt_fh_lsz_stieltjes_model_class_obstruction_2026-05-02.json"

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


def solve_positive_continuum(
    shells: np.ndarray,
    continuum_m2: np.ndarray,
    target_c: np.ndarray,
    pole_m2: float,
    pole_residue: float,
) -> dict[str, Any]:
    continuum_matrix = 1.0 / (shells[:, None] + continuum_m2[None, :])
    pole_column = 1.0 / (shells + pole_m2)
    rhs = target_c - pole_residue * pole_column
    result = linprog(
        c=np.zeros(len(continuum_m2)),
        A_eq=continuum_matrix,
        b_eq=rhs,
        bounds=[(0.0, None)] * len(continuum_m2),
        method="highs",
    )
    if not result.success:
        return {
            "pole_residue": pole_residue,
            "success": False,
            "message": result.message,
        }
    fitted = pole_residue * pole_column + continuum_matrix @ result.x
    return {
        "pole_residue": pole_residue,
        "success": True,
        "continuum_weights": [float(x) for x in result.x],
        "min_continuum_weight": float(np.min(result.x)),
        "max_abs_shell_residual": float(np.max(np.abs(fitted - target_c))),
        "dGamma_dp2_at_pole_proxy": float(1.0 / pole_residue),
        "relative_y_proxy_for_fixed_dE_ds": float(math.sqrt(1.0 / pole_residue)),
    }


def build_family() -> dict[str, Any]:
    one_link = 4.0 * math.sin(math.pi / 12.0) ** 2
    shells = np.asarray([0.0, one_link, 2.0 * one_link, 1.0], dtype=float)
    pole_m2 = 0.25
    continuum_m2 = np.asarray([0.260, 0.28, 0.33, 0.45, 0.7, 1.2, 2.0, 4.0, 8.0, 16.0])
    base_residue = 1.0
    base_continuum_weights = np.full(len(continuum_m2), 2.0)
    target_c = (
        base_residue / (shells + pole_m2)
        + (1.0 / (shells[:, None] + continuum_m2[None, :])) @ base_continuum_weights
    )
    residues = [0.25, 0.5, 1.0, 2.0]
    models = [
        solve_positive_continuum(shells, continuum_m2, target_c, pole_m2, residue)
        for residue in residues
    ]
    successful = [model for model in models if model.get("success")]
    derivative_values = [model["dGamma_dp2_at_pole_proxy"] for model in successful]
    residual_values = [model["max_abs_shell_residual"] for model in successful]
    return {
        "shells_p_hat_sq": [float(x) for x in shells],
        "pole_p_hat_sq": -pole_m2,
        "continuum_mass_squared_grid": [float(x) for x in continuum_m2],
        "target_c_shell_values": [float(x) for x in target_c],
        "models": models,
        "checks": {
            "all_models_positive_stieltjes": len(successful) == len(models)
            and all(float(model.get("min_continuum_weight", -1.0)) >= -1e-12 for model in successful),
            "max_shell_residual": max(residual_values) if residual_values else float("inf"),
            "pole_residue_span_factor": max(residues) / min(residues),
            "inverse_derivative_span_factor": max(derivative_values) / min(derivative_values)
            if derivative_values
            else float("nan"),
        },
    }


def main() -> int:
    print("PR #230 FH/LSZ Stieltjes model-class obstruction")
    print("=" * 72)

    finite_shell = load_json(FINITE_SHELL_NO_GO)
    model_gate = load_json(MODEL_CLASS_GATE)
    family = build_family()
    checks = family["checks"]

    report("finite-shell-no-go-loaded", bool(finite_shell), str(FINITE_SHELL_NO_GO.relative_to(ROOT)))
    report("model-class-gate-loaded", bool(model_gate), str(MODEL_CLASS_GATE.relative_to(ROOT)))
    report("positive-stieltjes-family-constructed", checks["all_models_positive_stieltjes"], f"residue span={checks['pole_residue_span_factor']}")
    report("finite-shell-values-held-fixed", checks["max_shell_residual"] < 1e-10, f"max residual={checks['max_shell_residual']:.3e}")
    report("pole-residue-not-identified-by-positivity", checks["inverse_derivative_span_factor"] >= 8.0, f"inverse-derivative span={checks['inverse_derivative_span_factor']:.6g}")
    report("does-not-authorize-retained-proposal", True, "Stieltjes positivity alone is not a scalar LSZ theorem")

    result = {
        "actual_current_surface_status": "exact negative boundary / FH-LSZ Stieltjes model-class obstruction",
        "verdict": (
            "Positive spectral/Stieltjes structure alone does not close the "
            "FH/LSZ finite-shell model-class gate.  The constructed "
            "pole-plus-positive-continuum models share the same finite "
            "Euclidean C_ss shell values and the same pole location, while "
            "the pole residue and inverse-propagator derivative proxy vary.  "
            "A retained closure still needs a stronger microscopic scalar "
            "denominator theorem, pole-saturation/continuum bound, or "
            "production continuum acceptance certificate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Finite-shell Stieltjes positivity does not uniquely determine the scalar pole residue.",
        "parent_certificates": {
            "finite_shell_no_go": str(FINITE_SHELL_NO_GO.relative_to(ROOT)),
            "model_class_gate": str(MODEL_CLASS_GATE.relative_to(ROOT)),
        },
        "family": family,
        "strict_non_claims": [
            "does not claim a physical scalar pole residue",
            "does not set kappa_s = 1",
            "does not use observed top mass or observed y_t",
            "does not use H_unit, Ward authority, alpha_LM, plaquette, or u0",
        ],
        "exact_next_action": (
            "Strengthen the model-class gate to require pole-saturation, a "
            "continuum threshold/gap theorem, multi-volume production "
            "continuum evidence, or a microscopic scalar denominator theorem."
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
