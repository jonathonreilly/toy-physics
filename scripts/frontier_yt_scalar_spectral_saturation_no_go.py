#!/usr/bin/env python3
"""
PR #230 scalar spectral-saturation no-go.

A possible scalar-LSZ repair is to invoke a positive spectral representation:

    C(p^2) = sum_i rho_i / (p^2 + m_i^2)

and hope that the source curvature fixes the Higgs-carrier pole residue.  This
runner checks the assumption.  Even with positivity and fixed low-order
curvature data, the isolated pole residue can vary unless a pole-saturation or
continuum-bound theorem is supplied.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_spectral_saturation_no_go_2026-05-01.json"

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


def moments(weights: np.ndarray, masses_sq: np.ndarray) -> tuple[float, float]:
    c0 = float(np.sum(weights / masses_sq))
    c1 = float(-np.sum(weights / (masses_sq * masses_sq)))
    return c0, c1


def solve_continuum_weights(
    *,
    pole_residue: float,
    pole_mass_sq: float,
    continuum_masses_sq: tuple[float, float],
    target_c0: float,
    target_c1: float,
) -> tuple[float, float]:
    s1, s2 = continuum_masses_sq
    rhs = np.asarray(
        [
            target_c0 - pole_residue / pole_mass_sq,
            target_c1 + pole_residue / (pole_mass_sq * pole_mass_sq),
        ],
        dtype=float,
    )
    matrix = np.asarray(
        [
            [1.0 / s1, 1.0 / s2],
            [-1.0 / (s1 * s1), -1.0 / (s2 * s2)],
        ],
        dtype=float,
    )
    weights = np.linalg.solve(matrix, rhs)
    return float(weights[0]), float(weights[1])


def main() -> int:
    print("PR #230 scalar spectral-saturation no-go")
    print("=" * 72)

    pole_mass_sq = 1.0
    continuum_masses_sq = (2.0, 9.0)
    reference_weights = np.asarray([0.50, 5.00, 5.00], dtype=float)
    masses_sq = np.asarray([pole_mass_sq, *continuum_masses_sq], dtype=float)
    target_c0, target_c1 = moments(reference_weights, masses_sq)

    candidate_pole_residues = [0.20, 0.35, 0.50, 0.65, 0.80]
    models = []
    for pole_residue in candidate_pole_residues:
        w1, w2 = solve_continuum_weights(
            pole_residue=pole_residue,
            pole_mass_sq=pole_mass_sq,
            continuum_masses_sq=continuum_masses_sq,
            target_c0=target_c0,
            target_c1=target_c1,
        )
        weights = np.asarray([pole_residue, w1, w2], dtype=float)
        c0, c1 = moments(weights, masses_sq)
        models.append(
            {
                "pole_residue": pole_residue,
                "continuum_weights": [w1, w2],
                "all_weights_positive": bool(np.all(weights > 0.0)),
                "C0": c0,
                "C1": c1,
                "C0_error": abs(c0 - target_c0),
                "C1_error": abs(c1 - target_c1),
                "canonical_y_proxy_relative_to_reference": math.sqrt(pole_residue / reference_weights[0]),
            }
        )

    positive_models = [model for model in models if model["all_weights_positive"]]
    max_c0_error = max(model["C0_error"] for model in models)
    max_c1_error = max(model["C1_error"] for model in models)
    pole_values = [model["pole_residue"] for model in positive_models]
    y_proxy_values = [model["canonical_y_proxy_relative_to_reference"] for model in positive_models]
    y_proxy_spread = (max(y_proxy_values) - min(y_proxy_values)) / max(sum(y_proxy_values) / len(y_proxy_values), 1.0e-30)

    report("positive-spectral-models-built", len(positive_models) >= 3, f"positive_models={len(positive_models)}")
    report("low-order-curvature-held-fixed", max_c0_error < 1.0e-12 and max_c1_error < 1.0e-12, f"max_errors=({max_c0_error:.3e}, {max_c1_error:.3e})")
    report("pole-residue-varies", max(pole_values) / min(pole_values) > 2.0, f"pole_range=[{min(pole_values):.3g}, {max(pole_values):.3g}]")
    report("canonical-y-proxy-varies", y_proxy_spread > 0.30, f"relative_spread={y_proxy_spread:.6g}")
    report("spectral-positivity-not-saturation", True, "positivity plus two curvature moments does not force pole saturation")
    report("not-retained-closure", True, "requires scalar-channel pole saturation or continuum bound from retained dynamics")

    result = {
        "actual_current_surface_status": "exact negative boundary / scalar spectral saturation no-go",
        "verdict": (
            "Positive scalar spectral representations and fixed low-order "
            "source-curvature data do not determine the isolated scalar pole "
            "residue.  Multiple positive pole-plus-continuum models have the "
            "same C(0) and C'(0) but different pole residues and therefore "
            "different canonical Yukawa proxies.  PR #230 still needs a "
            "retained pole-saturation/continuum-bound theorem or direct "
            "measurement of the pole residue."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Pole saturation and continuum control remain open imports.",
        "target_moments": {
            "C0": target_c0,
            "C1": target_c1,
            "reference_weights": reference_weights.tolist(),
            "masses_sq": masses_sq.tolist(),
        },
        "models": models,
        "strict_non_claims": [
            "does not rule out a future scalar pole theorem",
            "does not use observed top/Higgs/Yukawa values",
            "does not define y_t through H_unit matrix elements",
            "does not use alpha_LM/plaquette/u0 as proof input",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
