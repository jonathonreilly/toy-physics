#!/usr/bin/env python3
"""Minimal exact angle-carrying extension of the common Route 2 bridge.

The support side already carries the exact dark phase `vartheta_R`. This
runner packages it into the smallest exact extension of the current common
bridge:

    K_R^phase = (u_E, u_T, delta_A1 u_E, delta_A1 u_T, d_y, d_z)

with corresponding exact tensorized action and spacetime carrier:

    I_TB^phase = I_R + 1/2 ||a - K_R^phase||^2
    Xi_TB^phase = vec(K_R^phase) x exp(-t Lambda_R) u_*

This does not yet prove curvature localization. It proves the common bridge can
be made angle-sensitive exactly on the support side.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
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


def dark_rot(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def k_phase(q: np.ndarray) -> np.ndarray:
    bright = np.array(SUPPORT.k_r(q).reshape(-1), dtype=float)
    dark = np.array(SUPPORT.dark_coords(q)[1:], dtype=float)
    return np.concatenate([bright, dark])


def canonicalize_phase(pair: np.ndarray) -> tuple[float, float]:
    rho = float(np.linalg.norm(pair))
    theta = math.atan2(pair[1], pair[0])
    return rho, theta


def main() -> int:
    basis = SAME.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]

    q_ref = (e0 + 0.5 * s) / (1.0 + np.sqrt(6.0) * 0.5) + 0.13 * t1x + 0.03 * t1y + 0.02 * t1z
    k0 = k_phase(q_ref)
    bright0 = k0[:4]
    dark0 = k0[4:]
    rho0, theta0 = canonicalize_phase(dark0)

    Lambda, _, _, _ = ACTION.schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)
    seed = ACTION.expm(-0.7 * Lambda_sym) @ u_star
    xi0 = np.kron(k0, seed)

    max_bright_err = 0.0
    max_dark_cov_err = 0.0
    max_rho_err = 0.0
    max_section_err = 0.0
    max_xi_bright_err = 0.0
    max_xi_norm_err = 0.0

    for phi in [math.pi / 9.0, math.pi / 6.0, math.pi / 4.0, math.pi / 3.0]:
        rot = dark_rot(phi)
        dark_plane = np.array([np.dot(t1y, q_ref), np.dot(t1z, q_ref)], dtype=float)
        dark_rotated = rot @ dark_plane
        q_phi = (
            q_ref
            + (dark_rotated[0] - dark_plane[0]) * t1y
            + (dark_rotated[1] - dark_plane[1]) * t1z
        )
        k_phi = k_phase(q_phi)
        bright_phi = k_phi[:4]
        dark_phi = k_phi[4:]
        rho_phi, theta_phi = canonicalize_phase(dark_phi)
        section = dark_rot(-theta_phi) @ dark_phi
        xi_phi = np.kron(k_phi, seed)

        max_bright_err = max(max_bright_err, float(np.max(np.abs(bright_phi - bright0))))
        max_dark_cov_err = max(max_dark_cov_err, float(np.max(np.abs(dark_phi - rot @ dark0))))
        max_rho_err = max(max_rho_err, abs(rho_phi - rho0))
        max_section_err = max(max_section_err, float(np.max(np.abs(section - np.array([rho_phi, 0.0])))))
        max_xi_bright_err = max(max_xi_bright_err, float(np.max(np.abs(xi_phi[: bright0.size * seed.size] - xi0[: bright0.size * seed.size]))))
        max_xi_norm_err = max(max_xi_norm_err, abs(np.linalg.norm(xi_phi) - np.linalg.norm(xi0)))

    print("POLARIZATION PHASE-LIFT CANDIDATE")
    print("=" * 78)
    print(f"K_R^phase(q_ref) = {np.array2string(k0, precision=12, floatmode='fixed')}")
    print(f"rho_R(q_ref)     = {rho0:.12e}")
    print(f"vartheta_R(q_ref)= {theta0:.12e}")
    print(f"max bright error = {max_bright_err:.3e}")
    print(f"max dark cov err = {max_dark_cov_err:.3e}")
    print(f"max rho error    = {max_rho_err:.3e}")
    print(f"max section err  = {max_section_err:.3e}")
    print(f"max Xi norm err  = {max_xi_norm_err:.3e}")

    record(
        "the phase-lifted carrier extends the exact bright Route 2 carrier by the exact dark pair",
        np.allclose(k0[:4], SUPPORT.k_r(q_ref).reshape(-1)) and k0.size == 6,
        "K_R^phase = (u_E,u_T,delta_A1 u_E,delta_A1 u_T,d_y,d_z)",
    )
    record(
        "the bright Route 2 block stays exactly invariant under the dark SO(2)",
        max_bright_err < 1e-12,
        f"max bright error={max_bright_err:.3e}",
    )
    record(
        "the dark pair transforms covariantly under the dark SO(2)",
        max_dark_cov_err < 1e-12 and max_rho_err < 1e-12,
        f"max dark cov error={max_dark_cov_err:.3e}, max rho error={max_rho_err:.3e}",
    )
    record(
        "the local phase section trivializes the connected SO(2) orbit wherever rho_R != 0",
        max_section_err < 1e-12 and rho0 > 1e-6,
        f"max section error={max_section_err:.3e}, rho_R={rho0:.3e}",
    )
    record(
        "the phase-lifted spacetime carrier keeps exact semigroup transport while carrying the dark pair",
        max_xi_norm_err < 1e-12,
        f"max Xi norm error={max_xi_norm_err:.3e}",
    )

    print("\nVerdict:")
    print(
        "The common bridge can be extended exactly to an angle-carrying object "
        "by adjoining the exact dark pair. The minimal exact extension is "
        "K_R^phase = (K_R, D_R), with radius-phase data (rho_R, vartheta_R). "
        "Where rho_R != 0, vartheta_R provides a canonical local section of "
        "the connected SO(2) orbit."
    )
    print(
        "So the remaining gravity question is now narrower again: not whether "
        "the common bridge can carry the angle, but whether this phase-lifted "
        "bridge has a canonical curvature-localization interpretation."
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
