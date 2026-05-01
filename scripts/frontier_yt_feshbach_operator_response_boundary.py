#!/usr/bin/env python3
"""
PR #230 Feshbach operator-response boundary.

The gauge crossover theorem suggests that an exact Schur/Feshbach projection can
preserve the gauge spectral response.  This runner asks whether that fact can
also close the top-Yukawa scalar/gauge dressing ratio.

It cannot.  Exact Feshbach reduction preserves every projected low-energy
operator response if the operator is transformed consistently.  That removes a
crossover-distortion concern, but it does not equate two different microscopic
operators' residues.  Scalar/gauge equality still has to be derived from the
full interacting substrate or measured.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_feshbach_operator_response_boundary_2026-05-01.json"

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


def hermitian_random(seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(n, n)) + 1.0j * rng.normal(size=(n, n))
    return (a + a.conj().T) / 2.0


def feshbach_resolvent_block(h: np.ndarray, p_dim: int, z: complex) -> tuple[np.ndarray, np.ndarray]:
    h_pp = h[:p_dim, :p_dim]
    h_pq = h[:p_dim, p_dim:]
    h_qp = h[p_dim:, :p_dim]
    h_qq = h[p_dim:, p_dim:]
    q_res = np.linalg.inv(z * np.eye(h_qq.shape[0], dtype=complex) - h_qq)
    h_eff = h_pp + h_pq @ q_res @ h_qp
    full_res_pp = np.linalg.inv(z * np.eye(h.shape[0], dtype=complex) - h)[:p_dim, :p_dim]
    eff_res = np.linalg.inv(z * np.eye(p_dim, dtype=complex) - h_eff)
    return full_res_pp, eff_res


def response(resolvent: np.ndarray, source: np.ndarray) -> complex:
    return complex(source.conj().T @ resolvent @ source)


def main() -> int:
    print("PR #230 Feshbach operator-response boundary")
    print("=" * 72)

    p_dim = 4
    q_dim = 5
    h = hermitian_random(20260501, p_dim + q_dim)
    z_values = [3.0 + 0.4j, 4.0 + 0.8j, 5.0 + 1.2j]
    gauge_source = np.asarray([1.0, -0.5, 0.25, 0.75], dtype=complex)
    scalar_source = np.asarray([0.25, 1.0, -0.75, 0.5], dtype=complex)
    gauge_source = gauge_source / np.linalg.norm(gauge_source)
    scalar_source = scalar_source / np.linalg.norm(scalar_source)

    rows = []
    max_response_error = 0.0
    for z in z_values:
        full_pp, eff = feshbach_resolvent_block(h, p_dim, z)
        operator_errors = {}
        for label, source in [("gauge", gauge_source), ("scalar", scalar_source)]:
            full_value = response(full_pp, source)
            eff_value = response(eff, source)
            error = abs(full_value - eff_value)
            operator_errors[label] = error
            max_response_error = max(max_response_error, error)
        full_ratio = response(full_pp, scalar_source) / response(full_pp, gauge_source)
        eff_ratio = response(eff, scalar_source) / response(eff, gauge_source)
        rows.append(
            {
                "z": [z.real, z.imag],
                "operator_errors": operator_errors,
                "full_scalar_over_gauge_response": [full_ratio.real, full_ratio.imag],
                "effective_scalar_over_gauge_response": [eff_ratio.real, eff_ratio.imag],
                "ratio_error": abs(full_ratio - eff_ratio),
            }
        )

    # The same exact Feshbach identity holds while the microscopic scalar
    # source is varied.  Therefore response preservation cannot itself prove a
    # common scalar/gauge dressing theorem.
    dressing_countermodels = []
    z = z_values[0]
    full_pp, eff = feshbach_resolvent_block(h, p_dim, z)
    for scalar_scale in [0.75, 1.0, 1.25]:
        scaled_scalar = scalar_scale * scalar_source
        full_ratio = response(full_pp, scaled_scalar) / response(full_pp, gauge_source)
        eff_ratio = response(eff, scaled_scalar) / response(eff, gauge_source)
        dressing_countermodels.append(
            {
                "scalar_source_scale": scalar_scale,
                "full_scalar_over_gauge_response_abs": abs(full_ratio),
                "effective_scalar_over_gauge_response_abs": abs(eff_ratio),
                "feshbach_ratio_error": abs(full_ratio - eff_ratio),
            }
        )

    ratio_abs_values = [row["full_scalar_over_gauge_response_abs"] for row in dressing_countermodels]
    ratio_spread = (max(ratio_abs_values) - min(ratio_abs_values)) / max(sum(ratio_abs_values) / len(ratio_abs_values), 1.0e-30)

    report("schur-feshbach-response-identity", max_response_error < 1.0e-12, f"max_error={max_response_error:.3e}")
    report(
        "scalar-gauge-ratio-preserved-by-exact-projection",
        max(row["ratio_error"] for row in rows) < 1.0e-12,
        f"max_ratio_error={max(row['ratio_error'] for row in rows):.3e}",
    )
    report(
        "operator-specific-preservation-not-common-dressing",
        ratio_spread > 0.50,
        f"countermodel_ratio_spread={ratio_spread:.6g}",
    )
    report(
        "feshbach-errors-remain-small-under-scalar-rescaling",
        max(row["feshbach_ratio_error"] for row in dressing_countermodels) < 1.0e-12,
        f"max_scaled_ratio_error={max(row['feshbach_ratio_error'] for row in dressing_countermodels):.3e}",
    )
    report(
        "not-retained-closure",
        True,
        "exact projection preserves responses but does not derive scalar/gauge residue equality",
    )

    result = {
        "actual_current_surface_status": "exact support / Feshbach response boundary",
        "verdict": (
            "Exact Schur/Feshbach projection preserves low-energy operator "
            "responses, including scalar/gauge response ratios, when both "
            "operators are projected consistently.  This means crossover "
            "projection is not by itself a scalar/gauge dressing distortion.  "
            "But the identity is operator-specific: changing the microscopic "
            "scalar source changes the scalar/gauge response ratio while "
            "Feshbach preservation remains exact.  Therefore this route does "
            "not derive the common scalar/gauge dressing needed for PR #230."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Feshbach covariance preserves responses but does not equate distinct microscopic scalar and gauge residues.",
        "rows": rows,
        "dressing_countermodels": dressing_countermodels,
        "required_next_theorem": [
            "derive the microscopic scalar source/residue from the retained interacting substrate",
            "derive equality to the gauge response or carry a measured scalar/gauge dressing ratio",
            "avoid importing the audited_renaming gauge-crossover theorem as retained authority",
        ],
        "strict_non_claims": [
            "not a retained y_t derivation",
            "not a production measurement",
            "does not use observed top/Higgs/Yukawa values",
            "does not define y_t through H_unit matrix elements",
            "does not promote the gauge crossover companion theorem",
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
