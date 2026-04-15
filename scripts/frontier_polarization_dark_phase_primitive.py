#!/usr/bin/env python3
"""Construct the minimal angle-sensitive candidate on the dark complement.

The current common exact data are blind to the residual connected `SO(2)` dark
angle. The smallest natural candidate from the existing atlas is the exact dark
support pair on the `T1` dark plane:

    D_R(q) = (d_y, d_z)

with associated radius and phase

    rho_R = ||D_R||
    vartheta_R = atan2(d_z, d_y).

This runner checks that `D_R` transforms covariantly under the residual dark
`SO(2)` action and that `vartheta_R` trivializes the connected gauge wherever
`rho_R != 0`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

SUPPORT = SourceFileLoader(
    "route2_bilinear",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()
SAME = SourceFileLoader(
    "same_source_metric",
    str(ROOT / "scripts" / "frontier_same_source_metric_ansatz_scan.py"),
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def dark_rot(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def wrap_angle(theta: float) -> float:
    return math.atan2(math.sin(theta), math.cos(theta))


def main() -> int:
    basis = SAME.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]

    q_ref = (e0 + 0.5 * s) / (1.0 + np.sqrt(6.0) * 0.5) + 0.13 * t1x + 0.03 * t1y + 0.02 * t1z
    dark0 = np.array(SUPPORT.dark_coords(q_ref)[1:], dtype=float)
    rho0 = float(np.linalg.norm(dark0))
    theta0 = math.atan2(dark0[1], dark0[0])

    max_cov_err = 0.0
    max_radius_err = 0.0
    max_phase_err = 0.0
    min_radius = rho0

    for phi in [math.pi / 9.0, math.pi / 6.0, math.pi / 4.0, math.pi / 3.0]:
        rot = dark_rot(phi)
        dark_plane = np.array([np.dot(t1y, q_ref), np.dot(t1z, q_ref)], dtype=float)
        dark_rotated = rot @ dark_plane
        q_phi = (
            q_ref
            + (dark_rotated[0] - dark_plane[0]) * t1y
            + (dark_rotated[1] - dark_plane[1]) * t1z
        )

        dark_phi = np.array(SUPPORT.dark_coords(q_phi)[1:], dtype=float)
        rho_phi = float(np.linalg.norm(dark_phi))
        theta_phi = math.atan2(dark_phi[1], dark_phi[0])

        max_cov_err = max(max_cov_err, float(np.max(np.abs(dark_phi - rot @ dark0))))
        max_radius_err = max(max_radius_err, abs(rho_phi - rho0))
        max_phase_err = max(max_phase_err, abs(wrap_angle(theta_phi - theta0 - phi)))
        min_radius = min(min_radius, rho_phi)

    print("POLARIZATION DARK-PHASE PRIMITIVE")
    print("=" * 78)
    print(f"dark pair D_R(q_ref) = {np.array2string(dark0, precision=12, floatmode='fixed')}")
    print(f"rho_R(q_ref)         = {rho0:.12e}")
    print(f"vartheta_R(q_ref)    = {theta0:.12e}")
    print(f"max covariant error  = {max_cov_err:.3e}")
    print(f"max radius error     = {max_radius_err:.3e}")
    print(f"max phase error      = {max_phase_err:.3e}")
    print(f"min sampled radius   = {min_radius:.3e}")

    record(
        "the dark support pair transforms covariantly under the residual SO(2)",
        max_cov_err < 1e-12,
        f"max covariance error={max_cov_err:.3e}",
    )
    record(
        "the dark radius rho_R is exactly SO(2)-invariant",
        max_radius_err < 1e-12,
        f"max radius error={max_radius_err:.3e}",
    )
    record(
        "the dark phase vartheta_R shifts exactly by the residual SO(2) angle",
        max_phase_err < 1e-12,
        f"max phase error={max_phase_err:.3e}",
    )
    record(
        "the sampled dark orbit stays away from the singular rho_R=0 locus",
        min_radius > 1e-6,
        f"min sampled radius={min_radius:.3e}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The smallest angle-sensitive primitive already latent on the support "
        "side is the exact dark pair D_R(q) on the residual dark T1 plane, or "
        "equivalently its radius-phase form (rho_R, vartheta_R). Wherever "
        "rho_R != 0, vartheta_R trivializes the connected SO(2) gauge."
    )
    print(
        "So the final gravity question is no longer whether an angle-sensitive "
        "primitive exists at all. It does. The remaining question is whether "
        "that support-side dark phase can be lifted canonically into the common "
        "bundle / curvature-localization side."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
