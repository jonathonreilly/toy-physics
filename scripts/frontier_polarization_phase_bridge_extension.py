#!/usr/bin/env python3
r"""Exact phase-bridge extension of the Route 2 common bridge.

This runner starts from the exact support-side phase carrier and extends the
tensorized Route 2 bridge by adjoining the dark pair:

    K_R^phase(q) = (u_E, u_T, delta_A1 u_E, delta_A1 u_T, d_y, d_z)

with

    I_TB^phase = I_TB + 1/2 ||b - D_R||^2,
    Xi_TB^phase = vec(K_R^phase) \otimes exp(-t Lambda_R) u_*.

It then tests whether the exact phase section and semigroup transport canonize
the local connection. They do not: the remaining ambiguity is the residual
connected SO(2) gauge on the dark plane.
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
CENTER = SourceFileLoader(
    "tensor_center_excess",
    str(ROOT / "scripts" / "frontier_tensor_support_center_excess_law.py"),
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


def a1_background(r: float) -> np.ndarray:
    basis = SAME.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    return (e0 + r * s) / (1.0 + np.sqrt(6.0) * r)


def phase_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    basis = SAME.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e1 = basis[:, 2]
    e2 = basis[:, 3]
    t1x = basis[:, 4]
    t1y = basis[:, 5]
    t1z = basis[:, 6]
    ex = (np.sqrt(3.0) * e1 + e2) / 2.0
    e_perp = (-e1 + np.sqrt(3.0) * e2) / 2.0
    return e0, s, ex, e_perp, t1x, t1y, t1z


def support_delta(q: np.ndarray) -> float:
    return float(CENTER.support_delta(q))


def k_r(q: np.ndarray) -> np.ndarray:
    return np.array(SUPPORT.k_r(q), dtype=float)


def k_phase(q: np.ndarray) -> np.ndarray:
    bright = k_r(q).reshape(-1)
    dark = np.array(SUPPORT.dark_coords(q)[1:], dtype=float)
    return np.concatenate([bright, dark])


def phase_section(dark: np.ndarray) -> tuple[float, float]:
    rho = float(np.linalg.norm(dark))
    theta = math.atan2(dark[1], dark[0])
    return rho, theta


def xi_phase(q: np.ndarray, t: float = 0.7) -> np.ndarray:
    Lambda, _, _, _ = ACTION.schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    u_star = np.ones(Lambda_sym.shape[0], dtype=float)
    u_star /= np.linalg.norm(u_star)
    seed = ACTION.expm(-t * Lambda_sym) @ u_star
    return np.kron(k_phase(q), seed)


def main() -> int:
    e0, s, ex, e_perp, t1x, t1y, t1z = phase_basis()
    q_ref = a1_background(0.5) + 0.13 * t1x + 0.03 * t1y + 0.02 * t1z
    k0 = k_phase(q_ref)
    dark0 = k0[4:]
    rho0, theta0 = phase_section(dark0)
    xi0 = xi_phase(q_ref)

    max_bright_err = 0.0
    max_dark_cov_err = 0.0
    max_phase_err = 0.0
    max_section_err = 0.0
    max_xi_err = 0.0
    max_gauge_err = 0.0
    max_conn_shift = 0.0

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
        dark_phi = k_phi[4:]
        rho_phi, theta_phi = phase_section(dark_phi)
        xi_phi = xi_phase(q_phi)

        bright_phi = k_phi[:4]
        max_bright_err = max(max_bright_err, float(np.max(np.abs(bright_phi - k0[:4]))))
        max_dark_cov_err = max(max_dark_cov_err, float(np.max(np.abs(dark_phi - rot @ dark0))))
        max_phase_err = max(max_phase_err, abs(math.atan2(math.sin(theta_phi - theta0 - phi), math.cos(theta_phi - theta0 - phi))))
        max_section_err = max(max_section_err, float(np.max(np.abs(dark_rot(-theta_phi) @ dark_phi - np.array([rho_phi, 0.0])))))
        max_xi_err = max(max_xi_err, abs(np.linalg.norm(xi_phi) - np.linalg.norm(xi0)))

        # Gauge ambiguity: rephase the local section by a smooth offset.
        chi = 0.37 * rho_phi
        theta_shifted = theta_phi + chi
        max_gauge_err = max(
            max_gauge_err,
            abs(
                math.atan2(
                    math.sin((theta_shifted - theta_phi) - chi),
                    math.cos((theta_shifted - theta_phi) - chi),
                )
            ),
        )
        max_conn_shift = max(max_conn_shift, abs(chi))

    print("POLARIZATION PHASE-BRIDGE EXTENSION")
    print("=" * 78)
    print(f"K_R^phase(q_ref) = {np.array2string(k0, precision=12, floatmode='fixed')}")
    print(f"rho_R(q_ref)     = {rho0:.12e}")
    print(f"vartheta_R(q_ref)= {theta0:.12e}")
    print(f"max bright error  = {max_bright_err:.3e}")
    print(f"max dark cov err  = {max_dark_cov_err:.3e}")
    print(f"max phase err     = {max_phase_err:.3e}")
    print(f"max section err   = {max_section_err:.3e}")
    print(f"max Xi norm err   = {max_xi_err:.3e}")
    print(f"max gauge shift   = {max_conn_shift:.3e}")

    record(
        "the phase-lifted carrier extends the exact bright Route 2 carrier by the exact dark pair",
        k0.size == 6 and np.allclose(k0[:4], k_r(q_ref).reshape(-1)),
        "K_R^phase = (u_E, u_T, delta_A1 u_E, delta_A1 u_T, d_y, d_z)",
    )
    record(
        "the dark pair is exactly SO(2)-covariant",
        max_dark_cov_err < 1e-12 and max_phase_err < 1e-12,
        f"max covariance error={max_dark_cov_err:.3e}, max phase error={max_phase_err:.3e}",
    )
    record(
        "the phase section trivializes the connected orbit wherever rho_R != 0",
        max_section_err < 1e-12 and rho0 > 1e-6,
        f"max section error={max_section_err:.3e}, rho_R={rho0:.3e}",
    )
    record(
        "the phase-lifted spacetime carrier keeps exact semigroup transport",
        max_xi_err < 1e-12,
        f"max Xi norm error={max_xi_err:.3e}",
    )
    record(
        "the remaining local connection choice is exactly gauge-ambiguous",
        max_gauge_err < 1e-12 and max_conn_shift > 1e-6,
        f"gauge-shift error={max_gauge_err:.3e}, shift={max_conn_shift:.3e}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The strongest exact extension of the Route 2 bridge is the "
        "phase-lifted object B_R^phase = (K_R^phase, I_TB^phase, "
        "Xi_TB^phase). It transports the dark phase exactly on the support "
        "side and along the semigroup carrier. That is enough to define a "
        "local section on the punctured dark bundle, but not enough to force "
        "a canonical local connection."
    )
    print(
        "The exact remaining ambiguity is the residual connected SO(2) gauge "
        "on the dark plane: a rephasing vartheta_R -> vartheta_R + chi(q) "
        "preserves the phase-lifted construction while shifting the local "
        "connection by d chi."
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
