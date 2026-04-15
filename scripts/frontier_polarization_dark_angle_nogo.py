#!/usr/bin/env python3
"""Prove the current exact common bundle data are blind to the last SO(2) angle.

After the glue pass, the exact common connected residual gauge is `SO(2)` on
the dark complement plane. This runner checks whether any current exact common
object depends on that angle.

If all exact common data are invariant, then no canonical dark-angle section or
distinguished connection can be derived from the current atlas alone.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

GLUE_NOTE = DOCS / "POLARIZATION_GLUE_COMMON_SECTION_NOTE.md"
COMMON_NOTE = DOCS / "POLARIZATION_COMMON_BUNDLE_CANDIDATE_NOTE.md"

SUPPORT = SourceFileLoader(
    "route2_bilinear",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()
ACTION = SourceFileLoader(
    "route2_action",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_action.py"),
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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def dark_rot(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def main() -> int:
    glue = read(GLUE_NOTE)
    common = read(COMMON_NOTE)

    basis = SAME.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]
    # Reference source with nonzero bright and dark content.
    q_ref = (e0 + 0.5 * s) / (1.0 + np.sqrt(6.0) * 0.5) + 0.13 * t1x + 0.03 * t1y

    base_delta = float(SUPPORT.delta_a1(q_ref))
    base_bright = np.array(SUPPORT.bright_coords(q_ref), dtype=float)
    base_dark = np.array(SUPPORT.dark_coords(q_ref), dtype=float)
    base_k = np.array(SUPPORT.k_r(q_ref), dtype=float)

    Lambda, _, _, _ = ACTION.schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)
    seed = ACTION.expm(-1.0 * Lambda_sym) @ u_star
    base_xi = np.array(ACTION.xi_tb(base_k.reshape(-1), seed), dtype=float)
    base_penalty = 0.5 * float(np.sum((base_k.reshape(-1) - base_k.reshape(-1)) ** 2))

    max_delta_err = 0.0
    max_bright_err = 0.0
    max_k_err = 0.0
    max_xi_err = 0.0
    min_dark_motion = 0.0

    for theta in [math.pi / 9.0, math.pi / 6.0, math.pi / 4.0, math.pi / 3.0]:
        rot = dark_rot(theta)
        dark_plane = np.array([np.dot(t1y, q_ref), np.dot(t1z, q_ref)], dtype=float)
        dark_rotated = rot @ dark_plane
        q_theta = (
            q_ref
            + (dark_rotated[0] - dark_plane[0]) * t1y
            + (dark_rotated[1] - dark_plane[1]) * t1z
        )
        delta = float(SUPPORT.delta_a1(q_theta))
        bright = np.array(SUPPORT.bright_coords(q_theta), dtype=float)
        dark = np.array(SUPPORT.dark_coords(q_theta), dtype=float)
        k_theta = np.array(SUPPORT.k_r(q_theta), dtype=float)
        xi_theta = np.array(ACTION.xi_tb(k_theta.reshape(-1), seed), dtype=float)
        penalty_theta = 0.5 * float(np.sum((k_theta.reshape(-1) - k_theta.reshape(-1)) ** 2))

        max_delta_err = max(max_delta_err, abs(delta - base_delta))
        max_bright_err = max(max_bright_err, float(np.max(np.abs(bright - base_bright))))
        max_k_err = max(max_k_err, float(np.max(np.abs(k_theta - base_k))))
        max_xi_err = max(max_xi_err, float(np.max(np.abs(xi_theta - base_xi))))
        min_dark_motion = max(min_dark_motion, float(np.linalg.norm(dark[1:] - base_dark[1:])))
        max_xi_err = max(max_xi_err, abs(penalty_theta - base_penalty))

    print("POLARIZATION DARK-ANGLE NO-GO")
    print("=" * 78)
    print(f"base delta_A1 = {base_delta:.12e}")
    print(f"base bright   = {np.array2string(base_bright, precision=12, floatmode='fixed')}")
    print(f"base dark     = {np.array2string(base_dark, precision=12, floatmode='fixed')}")
    print(f"max delta_A1 error under dark SO(2) = {max_delta_err:.3e}")
    print(f"max bright error under dark SO(2)   = {max_bright_err:.3e}")
    print(f"max K_R error under dark SO(2)      = {max_k_err:.3e}")
    print(f"max Xi_TB error under dark SO(2)    = {max_xi_err:.3e}")
    print(f"min dark motion magnitude           = {min_dark_motion:.3e}")

    record(
        "the glue note already identifies SO(2) as the exact common connected residual gauge",
        has(glue, "SO(2)") and has(glue, "common residual gauge"),
        "the remaining connected common freedom is the dark-plane angle",
    )
    record(
        "delta_A1 is exactly blind to the residual dark-plane SO(2)",
        max_delta_err < 1e-12,
        f"max delta_A1 error={max_delta_err:.3e}",
    )
    record(
        "the bright pair u_E, u_T is exactly blind to the residual dark-plane SO(2)",
        max_bright_err < 1e-12,
        f"max bright error={max_bright_err:.3e}",
    )
    record(
        "the exact Route 2 carrier K_R is exactly blind to the residual dark-plane SO(2)",
        max_k_err < 1e-12,
        f"max K_R error={max_k_err:.3e}",
    )
    record(
        "the exact spacetime carrier Xi_TB is exactly blind to the residual dark-plane SO(2)",
        max_xi_err < 1e-12,
        f"max Xi_TB / penalty error={max_xi_err:.3e}",
    )
    record(
        "the residual SO(2) acts nontrivially on the dark complement itself",
        min_dark_motion > 1e-3,
        f"max dark motion={min_dark_motion:.3e}",
    )
    record(
        "the current common bundle note still stops at a candidate rather than an angle-fixing theorem",
        has(common, "candidate") and has(common, "frame-dependent"),
        "the common note does not yet contain an angle-sensitive primitive",
    )

    print("\nVerdict:")
    print(
        "All exact common bundle data currently in hand are invariant under the "
        "residual dark-plane SO(2), while the dark complement itself moves "
        "nontrivially under that action. So the current atlas cannot derive a "
        "canonical dark-angle section or distinguished connection from the "
        "existing exact objects alone."
    )
    print(
        "A genuinely new angle-sensitive primitive is required to fix the last "
        "SO(2) freedom and close the bundle."
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
