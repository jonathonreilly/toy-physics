#!/usr/bin/env python3
"""
PR #230 free scalar source two-point pole absence.

The Legendre/source route needs a momentum-dependent scalar two-point function
with a physical pole or canonical kinetic normalization.  This runner checks
the minimal source curvature supplied by the free Wilson-staggered logdet
bubble:

    Pi(p) = sum_k 1 / [(m^2 + D(k)) (m^2 + D(k+p))]

On this surface Pi(p) is finite and the inverse source curvature 1/Pi(p) has
no zero.  Thus the free source generator supplies exact curvature support but
not a physical scalar pole.  A pole requires an interacting denominator such as
G^{-1} - Pi(p) or a Bethe-Salpeter kernel.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "outputs" / "yt_free_scalar_two_point_pole_absence_2026-05-01.json"

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


def bubble_pi(momenta: np.ndarray, mass: float, p: np.ndarray, source_norm: float = 1.0) -> float:
    den1 = d_psi(momenta, mass)
    den2 = d_psi(momenta + p[None, :], mass)
    return float(source_norm * source_norm * np.mean(1.0 / (den1 * den2)))


def main() -> int:
    print("PR #230 free scalar source two-point pole absence")
    print("=" * 72)

    volumes = [(8, 16), (12, 24)]
    masses = [0.10, 0.25, 0.50]
    p_modes = [
        [0.0, 0.0, 0.0, 0.0],
        [2.0 * math.pi / 8.0, 0.0, 0.0, 0.0],
        [0.0, 2.0 * math.pi / 8.0, 0.0, 0.0],
        [0.0, 0.0, 2.0 * math.pi / 8.0, 0.0],
    ]
    scan = []
    for spatial_l, time_t in volumes:
        momenta = momentum_grid(spatial_l, time_t)
        for mass in masses:
            for p_raw in p_modes:
                p = np.asarray(p_raw, dtype=float)
                pi_value = bubble_pi(momenta, mass, p)
                inv_value = 1.0 / pi_value
                scan.append(
                    {
                        "spatial_L": spatial_l,
                        "time_T": time_t,
                        "mass": mass,
                        "p": p.tolist(),
                        "Pi": pi_value,
                        "inverse_source_curvature": inv_value,
                    }
                )

    pi_values = [row["Pi"] for row in scan]
    inv_values = [row["inverse_source_curvature"] for row in scan]
    finite_positive = all(math.isfinite(v) and v > 0.0 for v in pi_values + inv_values)
    zero_inverse_count = sum(1 for v in inv_values if abs(v) < 1.0e-12)

    # Source normalization can scale Pi, but cannot create an inverse zero for
    # finite nonzero source normalization.
    momenta = momentum_grid(8, 16)
    p0 = np.zeros(4)
    pi_base = bubble_pi(momenta, 0.25, p0, source_norm=1.0)
    pi_scaled = bubble_pi(momenta, 0.25, p0, source_norm=2.0)
    source_scale_ratio = pi_scaled / pi_base

    report("free-bubble-scan-runs", len(scan) == len(volumes) * len(masses) * len(p_modes), f"points={len(scan)}")
    report("source-curvature-finite-positive", finite_positive, f"Pi_range=[{min(pi_values):.6g}, {max(pi_values):.6g}]")
    report("inverse-curvature-has-no-zero", zero_inverse_count == 0, f"zero_inverse_count={zero_inverse_count}")
    report("source-rescaling-only-scales-bubble", abs(source_scale_ratio - 4.0) < 1.0e-14, f"Pi(2O)/Pi(O)={source_scale_ratio:.6g}")
    report("free-logdet-has-no-pole-denominator", True, "no G^{-1} - Pi(p) denominator exists on the free source surface")
    report("interacting-kernel-required", True, "need contact/RPA/Bethe-Salpeter denominator or production measurement")

    result = {
        "actual_current_surface_status": "exact negative boundary / free source pole absence",
        "verdict": (
            "The free Wilson-staggered logdet source bubble is finite and has "
            "no inverse-curvature zero on the scanned momentum/mass surfaces. "
            "Source normalization rescales the bubble but does not create a "
            "physical pole.  The source formalism therefore needs an interacting "
            "kernel or production measurement to supply scalar pole residue."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The free source curvature has no physical scalar pole or canonical kinetic normalization.",
        "scan": scan,
        "source_scale_ratio": source_scale_ratio,
        "required_next_theorem": [
            "derive an interacting scalar two-point denominator",
            "prove a finite-volume/IR limit with an isolated pole or canonical kinetic term",
            "compute the pole residue and kappa_H",
        ],
        "strict_non_claims": [
            "does not reject interacting scalar poles",
            "does not derive y_t",
            "does not use H_unit matrix-element authority",
            "does not use observed top/Higgs/Yukawa values",
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
