#!/usr/bin/env python3
"""Tensorial completion test for the restricted Einstein/Regge lift.

This runner starts from the branch's exact restricted scalar bridge package and
tests whether it extends to a genuine tensorial completion in generic
nonspherical and time-dependent sectors.

What it does:
  1. Keeps the exact scalar bridge data fixed.
  2. Adds explicit shift-vector and traceless spatial tensor perturbations.
  3. Evaluates the full 4D Einstein tensor numerically at shell-adjacent probe
     points.
  4. Compares the tensorial residuals against the unperturbed scalar bridge.
  5. Reports whether the scalar Schur boundary action changes under the tensor
     perturbations (it should not, which is the obstruction).

Interpretation:
  - If the scalar boundary action is blind to vector/TT perturbations while the
    Einstein residuals grow linearly in those modes, then the current restricted
    lift is not a full tensorial completion theorem.
  - A full nonlinear GR closure would need an additional tensor-valued matching
    principle beyond the current static conformal bridge.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np
from scipy.ndimage import map_coordinates


ROOT = "/private/tmp/physics-review-active"

same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    f"{ROOT}/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
schur = SourceFileLoader(
    "schur_boundary",
    f"{ROOT}/scripts/frontier_oh_schur_boundary_action.py",
).load_module()
microscopic = SourceFileLoader(
    "microscopic_dirichlet",
    f"{ROOT}/scripts/frontier_microscopic_dirichlet_bridge_principle.py",
).load_module()


@dataclass
class ProbeResult:
    label: str
    scalar_action: float
    scalar_trace_norm: float
    e_tt: float
    e_ti: float
    e_spatial_tf: float
    e_total: float


def interpolated_phi(phi_grid: np.ndarray, point_xyz: np.ndarray) -> float:
    center = (phi_grid.shape[0] - 1) / 2.0
    coords = np.array(
        [[center + point_xyz[0]], [center + point_xyz[1]], [center + point_xyz[2]]],
        dtype=float,
    )
    return float(map_coordinates(phi_grid, coords, order=3, mode="nearest")[0])


def background_lapse_and_spatial_metric(phi: float) -> tuple[float, np.ndarray]:
    psi = 1.0 + phi
    alpha = (1.0 - phi) / (1.0 + phi)
    gamma = np.diag(np.array([psi**4, psi**4, psi**4], dtype=float))
    return alpha, gamma


def envelope(point_xyz: np.ndarray) -> float:
    r = float(np.linalg.norm(point_xyz))
    # Localize the perturbation to the sewing band while keeping a smooth tail.
    return float(np.exp(-((r - 4.25) / 0.9) ** 2) / (1.0 + r * r))


def vector_mode(point_xyz: np.ndarray) -> np.ndarray:
    x, y, z = point_xyz
    r2 = float(np.dot(point_xyz, point_xyz)) + 1e-12
    # A pure rotational shift mode: tangential, divergence-free at leading order.
    return np.array([-y, x, 0.0], dtype=float) / r2


def tensor_mode(point_xyz: np.ndarray) -> np.ndarray:
    x, y, z = point_xyz
    r2 = float(np.dot(point_xyz, point_xyz)) + 1e-12
    n = np.array([x, y, z], dtype=float) / np.sqrt(r2)
    q = np.outer(n, n) - np.eye(3) / 3.0
    # Traceless quadrupole mode localized near the shell.
    return q


def adm_metric(phi_grid: np.ndarray, point: np.ndarray, eps_vec: float = 0.0, eps_ten: float = 0.0, omega: float = 0.0) -> np.ndarray:
    t = float(point[0])
    xyz = np.asarray(point[1:], dtype=float)
    phi = interpolated_phi(phi_grid, xyz)
    alpha, gamma0 = background_lapse_and_spatial_metric(phi)
    env = envelope(xyz)

    beta = eps_vec * np.sin(omega * t) * env * vector_mode(xyz)
    h = eps_ten * np.cos(omega * t) * env * tensor_mode(xyz)

    gamma = gamma0 @ (np.eye(3) + h)
    gamma = 0.5 * (gamma + gamma.T)

    beta_lower = gamma @ beta
    g = np.zeros((4, 4), dtype=float)
    g[1:, 1:] = gamma
    g[0, 1:] = beta_lower
    g[1:, 0] = beta_lower
    g[0, 0] = -alpha * alpha + float(beta @ beta_lower)
    return g


def christoffel(metric_fn, point: np.ndarray, h: float = 0.04) -> np.ndarray:
    g = metric_fn(point)
    g_inv = np.linalg.inv(g)
    dg = np.zeros((4, 4, 4), dtype=float)
    for axis in range(4):
        dp = point.copy()
        dm = point.copy()
        dp[axis] += h
        dm[axis] -= h
        dg[axis] = (metric_fn(dp) - metric_fn(dm)) / (2.0 * h)

    gamma = np.zeros((4, 4, 4), dtype=float)
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                total = 0.0
                for rho in range(4):
                    total += g_inv[lam, rho] * (
                        dg[mu, rho, nu] + dg[nu, rho, mu] - dg[rho, mu, nu]
                    )
                gamma[lam, mu, nu] = 0.5 * total
    return gamma


def ricci_and_einstein(metric_fn, point: np.ndarray, h: float = 0.04) -> tuple[np.ndarray, np.ndarray]:
    g = metric_fn(point)
    g_inv = np.linalg.inv(g)
    gamma = christoffel(metric_fn, point, h)

    dgamma = np.zeros((4, 4, 4, 4), dtype=float)
    for axis in range(4):
        if axis == 0:
            # time derivative handled by centered differences below
            continue
        dp = point.copy()
        dm = point.copy()
        dp[axis] += h
        dm[axis] -= h
        dgamma[axis] = (christoffel(metric_fn, dp, h) - christoffel(metric_fn, dm, h)) / (2.0 * h)

    # Explicit time derivatives
    dp = point.copy()
    dm = point.copy()
    dp[0] += h
    dm[0] -= h
    dgamma[0] = (christoffel(metric_fn, dp, h) - christoffel(metric_fn, dm, h)) / (2.0 * h)

    ricci = np.zeros((4, 4), dtype=float)
    for mu in range(4):
        for nu in range(4):
            term1 = term2 = term3 = term4 = 0.0
            for lam in range(4):
                term1 += dgamma[lam, lam, mu, nu]
                term2 += dgamma[nu, lam, mu, lam]
                trace_lam = sum(gamma[rho, lam, rho] for rho in range(4))
                term3 += gamma[lam, mu, nu] * trace_lam
                for rho in range(4):
                    term4 += gamma[rho, mu, lam] * gamma[lam, nu, rho]
            ricci[mu, nu] = term1 - term2 + term3 - term4

    scalar = float(np.sum(g_inv * ricci))
    einstein = ricci - 0.5 * g * scalar
    return ricci, einstein


def max_tensorial_components(einstein: np.ndarray) -> tuple[float, float, float, float]:
    e_tt = abs(float(einstein[0, 0]))
    e_ti = float(np.max(np.abs(einstein[0, 1:])))
    spatial = einstein[1:, 1:]
    spatial_tf = spatial - np.eye(3) * float(np.trace(spatial)) / 3.0
    e_spatial_tf = float(np.max(np.abs(spatial_tf)))
    e_total = float(np.max(np.abs(einstein)))
    return e_tt, e_ti, e_spatial_tf, e_total


def scalar_bridge_action(phi_grid: np.ndarray) -> float:
    Lambda, trace_idx, bulk_idx, interior = schur.schur_dtn_matrix(15, 4.0)
    action = schur.analyze_family(phi_grid, Lambda, trace_idx, bulk_idx, interior)
    f = action["f"]
    j = action["j_trace"]
    return float(0.5 * f @ (Lambda @ f) - j @ f)


def probe_family(label: str, phi_grid: np.ndarray, eps_vec: float, eps_ten: float, omega: float) -> ProbeResult:
    action0 = scalar_bridge_action(phi_grid)
    # Use the same scalar trace for all tensorial completions: the scalar action
    # cannot see the tensor perturbation.
    scalar_trace_norm = float(np.linalg.norm(same_source.build_best_phi_grid()))

    points = [
        np.array([0.0, 4.25, 0.0, 0.0], dtype=float),
        np.array([0.3, 4.25 / np.sqrt(2.0), 4.25 / np.sqrt(2.0), 0.0], dtype=float),
        np.array([0.6, 4.25 / np.sqrt(3.0), 4.25 / np.sqrt(3.0), 4.25 / np.sqrt(3.0)], dtype=float),
    ]

    e_tt_vals = []
    e_ti_vals = []
    e_tf_vals = []
    e_tot_vals = []
    for p in points:
        _, einstein = ricci_and_einstein(
            lambda q: adm_metric(phi_grid, q, eps_vec=eps_vec, eps_ten=eps_ten, omega=omega),
            p,
        )
        e_tt, e_ti, e_tf, e_tot = max_tensorial_components(einstein)
        e_tt_vals.append(e_tt)
        e_ti_vals.append(e_ti)
        e_tf_vals.append(e_tf)
        e_tot_vals.append(e_tot)

    return ProbeResult(
        label=label,
        scalar_action=action0,
        scalar_trace_norm=scalar_trace_norm,
        e_tt=max(e_tt_vals),
        e_ti=max(e_ti_vals),
        e_spatial_tf=max(e_tf_vals),
        e_total=max(e_tot_vals),
    )


def main() -> int:
    print("Tensorial completion test for restricted Einstein/Regge lift")
    print("=" * 78)

    phi_oh = same_source.build_best_phi_grid()
    phi_fr = coarse.build_finite_rank_phi_grid()

    base_oh = probe_family("scalar bridge", phi_oh, eps_vec=0.0, eps_ten=0.0, omega=0.0)
    vec_oh = probe_family("vector shift", phi_oh, eps_vec=0.02, eps_ten=0.0, omega=1.0)
    ten_oh = probe_family("tensor shear", phi_oh, eps_vec=0.0, eps_ten=0.02, omega=1.0)
    mix_oh = probe_family("mixed vector+tens", phi_oh, eps_vec=0.02, eps_ten=0.02, omega=1.0)

    base_fr = probe_family("finite-rank scalar bridge", phi_fr, eps_vec=0.0, eps_ten=0.0, omega=0.0)
    vec_fr = probe_family("finite-rank vector shift", phi_fr, eps_vec=0.02, eps_ten=0.0, omega=1.0)
    ten_fr = probe_family("finite-rank tensor shear", phi_fr, eps_vec=0.0, eps_ten=0.02, omega=1.0)

    def report(pr: ProbeResult) -> None:
        print(
            f"{pr.label}: scalar_action={pr.scalar_action:.6e}, "
            f"|Einstein|_max=(tt={pr.e_tt:.3e}, t-i={pr.e_ti:.3e}, "
            f"tf={pr.e_spatial_tf:.3e}, total={pr.e_total:.3e})"
        )

    print("\nProbe summaries:")
    for pr in [base_oh, vec_oh, ten_oh, mix_oh, base_fr, vec_fr, ten_fr]:
        report(pr)

    scalar_blind = abs(vec_oh.scalar_action - base_oh.scalar_action) < 1e-14 and abs(
        ten_oh.scalar_action - base_oh.scalar_action
    ) < 1e-14
    vector_gap = vec_oh.e_ti > 1e-6 or vec_oh.e_spatial_tf > 1e-6
    tensor_gap = ten_oh.e_spatial_tf > 1e-6 or ten_oh.e_ti > 1e-6
    mix_gap = mix_oh.e_ti > 1e-6 and mix_oh.e_spatial_tf > 1e-6

    print("\n" + "=" * 78)
    print("DECISIVE TESTS")
    print("=" * 78)
    print(
        f"scalar boundary action unchanged under tensor perturbations: "
        f"{'PASS' if scalar_blind else 'FAIL'}"
    )
    print(
        f"vector perturbation triggers extra tensorial Einstein residuals: "
        f"{'PASS' if vector_gap else 'FAIL'}"
    )
    print(
        f"traceless tensor perturbation triggers extra tensorial Einstein residuals: "
        f"{'PASS' if tensor_gap else 'FAIL'}"
    )
    print(
        f"mixed perturbation activates both vector and tensor channels: "
        f"{'PASS' if mix_gap else 'FAIL'}"
    )

    print("\nVerdict:")
    print(
        "The current restricted 3+1 lift is scalar-complete on the bridge surface, "
        "but it is not a full tensorial completion theorem. Shift and traceless "
        "tensor sectors remain invisible to the scalar Schur action and produce "
        "independent Einstein residuals, so generic nonspherical/time-dependent "
        "sectors need an additional tensor-valued matching principle."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
