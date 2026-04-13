#!/usr/bin/env python3
"""Coarse-grained exterior point-source law for strong-field gravity.

Bounded content:
  1. For the exact local O_h source class, fit the unique radial harmonic
     projection phi_eff(r) = a/r outside a matching radius R_match.
  2. Test whether the corresponding static isotropic metric is vacuum-close at
     and beyond that matching radius.
  3. Compare against the direct same-source metric built from the exact field.
  4. Repeat the harmonic-projection test on the broader exact finite-rank
     source class for robustness.

This does not close full nonlinear GR. It tests whether a genuine
coarse-grained exterior source law emerges from the exact lattice field.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np
from scipy.ndimage import map_coordinates


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "BOUNDED") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    "/private/tmp/physics-review-active/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()


def shell_data(phi_grid: np.ndarray):
    size = phi_grid.shape[0]
    center = (size - 1) / 2.0
    shells: dict[int, list[float]] = {}
    radii: dict[int, float] = {}
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            for k in range(1, size - 1):
                dx = i - center
                dy = j - center
                dz = k - center
                d2 = int(dx * dx + dy * dy + dz * dz)
                if d2 <= 1 or d2 == 0:
                    continue
                shells.setdefault(d2, []).append(float(phi_grid[i, j, k]))
                radii[d2] = float(np.sqrt(d2))
    usable = sorted(d2 for d2, vals in shells.items() if len(vals) >= 6 and radii[d2] <= center - 1)
    return usable, radii, shells


def fit_radial_harmonic_projection(phi_grid: np.ndarray, r_match: float):
    usable, radii, shells = shell_data(phi_grid)
    d2s = [d2 for d2 in usable if radii[d2] >= r_match]
    r = np.array([radii[d2] for d2 in d2s], dtype=float)
    y = np.array([np.mean(shells[d2]) for d2 in d2s], dtype=float)
    a = float(np.linalg.lstsq((1.0 / r).reshape(-1, 1), y, rcond=None)[0][0])
    pred = a / r
    rel_rms = float(np.sqrt(np.mean((y - pred) ** 2)) / max(np.max(np.abs(y)), 1e-12))
    max_rel = float(np.max(np.abs(y - pred) / np.maximum(np.abs(y), 1e-12)))
    return a, rel_rms, max_rel


def interpolate_phi(phi_grid: np.ndarray, point: np.ndarray) -> float:
    center = (phi_grid.shape[0] - 1) / 2.0
    coords = np.array([[center + point[0]], [center + point[1]], [center + point[2]]], dtype=float)
    return float(map_coordinates(phi_grid, coords, order=3, mode="nearest")[0])


def metric_from_phi(phi: float) -> np.ndarray:
    psi = 1.0 + phi
    alpha = (1.0 - phi) / (1.0 + phi)
    return np.diag(np.array([-(alpha**2), psi**4, psi**4, psi**4], dtype=float))


def christoffel(metric_fn, point: np.ndarray, h: float = 0.05) -> np.ndarray:
    g = metric_fn(point)
    g_inv = np.linalg.inv(g)
    dg = np.zeros((4, 4, 4))
    for axis in range(1, 4):
        dp = point.copy()
        dm = point.copy()
        dp[axis - 1] += h
        dm[axis - 1] -= h
        dg[axis] = (metric_fn(dp) - metric_fn(dm)) / (2.0 * h)
    gamma = np.zeros((4, 4, 4))
    for lam in range(4):
        for mu in range(4):
            for nu in range(4):
                total = 0.0
                for rho in range(4):
                    total += g_inv[lam, rho] * (dg[mu, rho, nu] + dg[nu, rho, mu] - dg[rho, mu, nu])
                gamma[lam, mu, nu] = 0.5 * total
    return gamma


def dgamma(metric_fn, point: np.ndarray, axis: int, h: float = 0.05) -> np.ndarray:
    if axis == 0:
        return np.zeros((4, 4, 4))
    dp = point.copy()
    dm = point.copy()
    dp[axis - 1] += h
    dm[axis - 1] -= h
    return (christoffel(metric_fn, dp, h) - christoffel(metric_fn, dm, h)) / (2.0 * h)


def einstein_tensor(metric_fn, point: np.ndarray, h: float = 0.05) -> np.ndarray:
    g = metric_fn(point)
    g_inv = np.linalg.inv(g)
    gamma = christoffel(metric_fn, point, h)
    dgammas = np.zeros((4, 4, 4, 4))
    for axis in range(1, 4):
        dgammas[axis] = dgamma(metric_fn, point, axis, h)

    ricci = np.zeros((4, 4))
    for mu in range(4):
        for nu in range(4):
            term1 = term2 = term3 = term4 = 0.0
            for lam in range(4):
                term1 += dgammas[lam, lam, mu, nu]
                term2 += dgammas[nu, lam, mu, lam]
                trace_lam = sum(gamma[rho, lam, rho] for rho in range(4))
                term3 += gamma[lam, mu, nu] * trace_lam
                for rho in range(4):
                    term4 += gamma[rho, mu, lam] * gamma[lam, nu, rho]
            ricci[mu, nu] = term1 - term2 + term3 - term4
    scalar = float(np.sum(g_inv * ricci))
    return ricci - 0.5 * g * scalar


def probe_points(r_match: float):
    return [
        np.array([r_match, 0.0, 0.0]),
        np.array([r_match / np.sqrt(2.0), r_match / np.sqrt(2.0), 0.0]),
        np.array([r_match / np.sqrt(3.0)] * 3),
    ]


def residual_at_radius(phi_grid: np.ndarray, r_match: float, a: float):
    def direct_metric(point: np.ndarray) -> np.ndarray:
        return metric_from_phi(interpolate_phi(phi_grid, point))

    def coarse_metric(point: np.ndarray) -> np.ndarray:
        r = max(np.linalg.norm(point), 1e-12)
        return metric_from_phi(a / r)

    direct_vals = []
    coarse_vals = []
    for p in probe_points(r_match):
        direct_vals.append(float(np.max(np.abs(einstein_tensor(direct_metric, p)))))
        coarse_vals.append(float(np.max(np.abs(einstein_tensor(coarse_metric, p)))))
    return max(direct_vals), max(coarse_vals)


def analyze_family(name: str, phi_grid: np.ndarray):
    rows = []
    for r_match in [3.0, 3.5, 4.0, 4.5, 5.0]:
        a, rel_rms, max_rel = fit_radial_harmonic_projection(phi_grid, r_match)
        direct_res, coarse_res = residual_at_radius(phi_grid, r_match, a)
        rows.append((r_match, a, rel_rms, max_rel, direct_res, coarse_res))
    print(f"\n{name} family:")
    for row in rows:
        print(
            f"  R_match={row[0]:.1f}  a={row[1]:.6f}  shell_rms={row[2]:.3f}  "
            f"shell_max_rel={row[3]:.3f}  direct={row[4]:.3e}  coarse={row[5]:.3e}"
        )
    return rows


def build_finite_rank_phi_grid():
    size, H0, interior, support, G0P, GS, W, masses = finite_rank.finite_rank_setup()
    P = finite_rank.support_projector(H0.shape[0], support)
    full = finite_rank.solve_columns(H0 - finite_rank.sparse.csr_matrix(P @ W @ P.T), support)
    phi_flat = full @ masses
    phi_grid = np.zeros((size, size, size))
    phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))
    return phi_grid


def main() -> None:
    print("Coarse-grained exterior point-source law")
    print("=" * 72)

    phi_oh = same_source.build_best_phi_grid()
    rows_oh = analyze_family("exact local O_h", phi_oh)
    best_oh = rows_oh[3]  # R_match = 4.5

    phi_fr = build_finite_rank_phi_grid()
    rows_fr = analyze_family("exact finite-rank", phi_fr)
    best_fr = rows_fr[3]  # R_match = 4.5

    record(
        "local O_h source admits a vacuum-close coarse-grained point-source exterior law",
        best_oh[5] < 1e-5 and best_oh[4] < 1e-3,
        (
            f"at R_match={best_oh[0]:.1f}: direct={best_oh[4]:.3e}, "
            f"coarse={best_oh[5]:.3e}, shell RMS={best_oh[2]:.3f}"
        ),
    )
    record(
        "finite-rank source also admits a vacuum-close harmonic projection after coarse-graining",
        best_fr[5] < 2e-5,
        (
            f"at R_match={best_fr[0]:.1f}: direct={best_fr[4]:.3e}, "
            f"coarse={best_fr[5]:.3e}, shell RMS={best_fr[2]:.3f}"
        ),
    )
    record(
        "remaining gravity gap is localized to matching, not the exterior harmonic law",
        best_oh[5] * 100.0 < best_oh[4] and best_fr[5] * 100.0 < best_fr[4],
        (
            f"O_h improvement={best_oh[4]/best_oh[5]:.1f}x, "
            f"finite-rank improvement={best_fr[4]/best_fr[5]:.1f}x"
        ),
    )

    print("\n" + "=" * 72)
    print("SUMMARY")
    print("=" * 72)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
    else:
        print("Some checks failed.")


if __name__ == "__main__":
    main()
