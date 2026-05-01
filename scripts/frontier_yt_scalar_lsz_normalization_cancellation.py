#!/usr/bin/env python3
"""
PR #230 scalar LSZ normalization-cancellation check.

Earlier scalar-ladder checks showed that a finite pole test is not invariant if
one rescales the scalar source while holding the kernel fixed.  That is a real
obstruction to a shortcut, but it is not the final word: in a correctly derived
Bethe-Salpeter/RPA scalar channel, the source normalization, auxiliary kernel
normalization, and LSZ residue must transform together.

This runner tests that algebraic route.  It shows that source rescaling cancels
from the canonical LSZ Yukawa proxy when the pole denominator is transformed
consistently, while also exposing the remaining hard import: the interacting
kernel/pole condition and its momentum derivative must be derived, not chosen.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_scalar_lsz_normalization_cancellation_2026-05-01.json"

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


def momentum_grid(spatial_l: int, time_t: int) -> np.ndarray:
    axes = [
        2.0 * math.pi * np.arange(spatial_l) / spatial_l,
        2.0 * math.pi * np.arange(spatial_l) / spatial_l,
        2.0 * math.pi * np.arange(spatial_l) / spatial_l,
        2.0 * math.pi * (np.arange(time_t) + 0.5) / time_t,
    ]
    grids = np.meshgrid(*axes, indexing="ij")
    return np.stack([grid.ravel() for grid in grids], axis=1)


def d_psi(k: np.ndarray, mass: float) -> np.ndarray:
    return mass * mass + np.sum(np.sin(k) ** 2, axis=1)


def bubble_pi(momenta: np.ndarray, mass: float, p: np.ndarray) -> float:
    den1 = d_psi(momenta, mass)
    den2 = d_psi(momenta + p[None, :], mass)
    return float(np.mean(1.0 / (den1 * den2)))


def main() -> int:
    print("PR #230 scalar LSZ normalization cancellation")
    print("=" * 72)

    spatial_l = 32
    time_t = 64
    mass = 0.25
    momenta = momentum_grid(spatial_l, time_t)
    p0 = np.zeros(4)
    p1 = np.asarray([2.0 * math.pi / spatial_l, 0.0, 0.0, 0.0])
    p_hat_sq = float(np.sum((2.0 * np.sin(p1 / 2.0)) ** 2))

    pi0 = bubble_pi(momenta, mass, p0)
    pi1 = bubble_pi(momenta, mass, p1)
    dpi_dp_hat_sq = (pi1 - pi0) / p_hat_sq
    z_inv_base = -dpi_dp_hat_sq
    base_kernel = 1.0 / pi0

    source_scales = [0.5, 1.0, 2.0, 3.0]
    rows = []
    for scale in source_scales:
        pi0_s = scale * scale * pi0
        pi1_s = scale * scale * pi1
        z_inv_s = scale * scale * z_inv_base
        kernel_s = base_kernel / (scale * scale)

        fixed_kernel_pole_residual = (1.0 / base_kernel) - pi0_s
        covariant_pole_residual = (1.0 / kernel_s) - pi0_s
        source_vertex_s = scale
        canonical_y_proxy = source_vertex_s / math.sqrt(z_inv_s)
        scalar_prop_residue_s = 1.0 / z_inv_s
        rows.append(
            {
                "source_scale": scale,
                "Pi0_scaled": pi0_s,
                "Pi1_scaled": pi1_s,
                "fixed_kernel_pole_residual": fixed_kernel_pole_residual,
                "covariant_kernel": kernel_s,
                "covariant_pole_residual": covariant_pole_residual,
                "Z_inverse_scaled": z_inv_s,
                "source_vertex_scaled": source_vertex_s,
                "canonical_y_proxy": canonical_y_proxy,
                "scalar_propagator_residue_proxy": scalar_prop_residue_s,
            }
        )

    fixed_residuals = [abs(row["fixed_kernel_pole_residual"]) for row in rows]
    covariant_residuals = [abs(row["covariant_pole_residual"]) for row in rows]
    y_proxies = [row["canonical_y_proxy"] for row in rows]
    y_spread = (max(y_proxies) - min(y_proxies)) / max(abs(sum(y_proxies) / len(y_proxies)), 1.0e-30)
    residue_scale_ratio = rows[0]["scalar_propagator_residue_proxy"] / rows[2]["scalar_propagator_residue_proxy"]

    report("free-bubble-derivative-finite", math.isfinite(z_inv_base) and z_inv_base > 0.0, f"Z_inv_base={z_inv_base:.12g}")
    report(
        "fixed-kernel-source-rescaling-breaks-pole",
        fixed_residuals[0] > 1.0e-6 and fixed_residuals[2] > 1.0e-6,
        f"fixed_residuals={[round(x, 6) for x in fixed_residuals]}",
    )
    report(
        "covariant-kernel-rescaling-restores-pole",
        max(covariant_residuals) < 1.0e-10,
        f"max_covariant_residual={max(covariant_residuals):.3e}",
    )
    report(
        "lsz-canonical-y-proxy-source-scale-invariant",
        y_spread < 1.0e-12,
        f"relative_spread={y_spread:.3e}",
    )
    report(
        "source-propagator-residue-scales-inversely",
        abs(residue_scale_ratio - 16.0) < 1.0e-10,
        f"residue(scale=0.5)/residue(scale=2.0)={residue_scale_ratio:.12g}",
    )
    report(
        "not-retained-closure",
        True,
        "the pole kernel and interacting derivative are still chosen in this model, not derived",
    )

    result = {
        "actual_current_surface_status": "conditional-support / scalar LSZ normalization cancellation",
        "verdict": (
            "A correctly covariant scalar LSZ construction can cancel pure "
            "source normalization from the canonical Yukawa proxy: O -> c O "
            "scales the bubble and inverse-propagator derivative by c^2, while "
            "the source vertex scales by c, leaving vertex/sqrt(Z_inverse) "
            "invariant.  This repairs only the normalization bookkeeping.  It "
            "does not close PR #230 because the interacting pole denominator, "
            "kernel normalization, pole location, and derivative were imposed "
            "inside the model rather than derived from the retained substrate."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The interacting scalar-channel kernel and pole-residue derivative remain open imports.",
        "parameters": {
            "spatial_L": spatial_l,
            "time_T": time_t,
            "mass": mass,
            "p_hat_sq": p_hat_sq,
            "Pi0": pi0,
            "Pi1": pi1,
            "dPi_dp_hat_sq": dpi_dp_hat_sq,
            "Z_inverse_base": z_inv_base,
            "base_kernel_chosen_for_pole": base_kernel,
        },
        "rows": rows,
        "canonical_y_proxy_relative_spread": y_spread,
        "required_next_theorem": [
            "derive the interacting scalar-channel Bethe-Salpeter/RPA denominator from Wilson-staggered dynamics",
            "derive the scalar source/projector and its covariant kernel normalization together",
            "prove an isolated pole in the controlled finite-volume/IR limit",
            "compute the inverse-propagator derivative at the pole",
            "only then identify the canonical LSZ-normalized Yukawa readout",
        ],
        "strict_non_claims": [
            "not a retained y_t derivation",
            "not a production measurement",
            "does not use observed top/Higgs/Yukawa values",
            "does not define y_t through H_unit matrix elements",
            "does not set the contact kernel by fiat as proof",
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
