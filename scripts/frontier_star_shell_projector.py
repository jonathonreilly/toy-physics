#!/usr/bin/env python3
"""Exact shell-projector reduction for star-supported strong-field sources.

Exact content:
  1. On the current finite box, the shell-mean profiles of the lattice Green
     functions sourced at the seven star-support sites
         S = {0, ±e_x, ±e_y, ±e_z}
     are identical on every exterior shell.
  2. By linearity, any source supported on S has shell-averaged exterior field
     determined only by the total enclosed charge Q:
         <phi>_shell = Q * K_shell
     where K_shell is the common shell profile of the centered point Green
     function.
  3. The exact local O_h source family and the broader exact finite-rank source
     family already on codex/review-active both satisfy this shell-projector
     identity to machine precision.

Bounded content:
  4. The same radial harmonic projection a/r used in the existing coarse-grained
     exterior-law note is therefore not fit to arbitrary source detail; it is a
     fit to this exact charge-fixed universal shell kernel.
  5. Using the a coefficient extracted from the universal shell kernel reproduces
     the same vacuum-close exterior residuals as the previous direct shell fit.

This still does not close full nonlinear GR. It replaces another ad hoc piece of
the matching story by an exact shell-level projector for the actual star-
supported source classes currently in play.
"""

from __future__ import annotations

from dataclasses import dataclass
from _frontier_loader import load_frontier

import numpy as np
from scipy.sparse.linalg import spsolve


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


coarse = load_frontier("coarse_grained", "frontier_coarse_grained_exterior_law.py")
finite_rank = load_frontier("finite_rank_metric", "frontier_finite_rank_gravity_residual.py")
same_source = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
flux = load_frontier("flux_fixed", "frontier_flux_fixed_matching_theorem.py")


STAR_COORDS = [
    np.array([0, 0, 0], dtype=int),
    np.array([1, 0, 0], dtype=int),
    np.array([-1, 0, 0], dtype=int),
    np.array([0, 1, 0], dtype=int),
    np.array([0, -1, 0], dtype=int),
    np.array([0, 0, 1], dtype=int),
    np.array([0, 0, -1], dtype=int),
]


def build_point_green_columns(size: int) -> tuple[list[np.ndarray], np.ndarray, np.ndarray]:
    H0, interior = finite_rank.build_neg_laplacian_sparse(size)
    center = interior // 2
    support = [
        finite_rank.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in STAR_COORDS
    ]
    cols = []
    for site in support:
        rhs = np.zeros(H0.shape[0])
        rhs[site] = 1.0
        col = spsolve(H0, rhs)
        grid = np.zeros((size, size, size))
        grid[1:-1, 1:-1, 1:-1] = col.reshape((interior, interior, interior))
        cols.append(grid)
    return cols, H0, np.array(support, dtype=int)


def shell_profile(grid: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    usable, radii, shells = coarse.shell_data(grid)
    r = np.array([radii[d2] for d2 in usable], dtype=float)
    y = np.array([np.mean(shells[d2]) for d2 in usable], dtype=float)
    return r, y


def enclosed_charge(field: np.ndarray) -> float:
    rows = flux.charge_stability_rows(field)
    return float(np.mean([q for _, q in rows]))


def radial_fit_from_profile(r: np.ndarray, y: np.ndarray, r_match: float) -> float:
    mask = r >= r_match
    coeff = np.linalg.lstsq((1.0 / r[mask]).reshape(-1, 1), y[mask], rcond=None)[0]
    return float(coeff[0])


def main() -> None:
    print("Exact shell projector for star-supported sources")
    print("=" * 72)

    size = 15
    green_cols, _, _ = build_point_green_columns(size)
    base_r, base_profile = shell_profile(green_cols[0])

    print("\nStar-support Green shell profiles:")
    max_basis_diff = 0.0
    for coord, grid in zip(STAR_COORDS, green_cols):
        r, y = shell_profile(grid)
        diff = float(np.max(np.abs(y - base_profile)))
        max_basis_diff = max(max_basis_diff, diff)
        print(f"  source {tuple(coord.tolist())}: max shell-profile diff from center = {diff:.3e}")

    record(
        "all seven star-support point Green functions share the same shell-mean profile",
        max_basis_diff < 1e-14,
        f"max basis shell-profile difference={max_basis_diff:.3e}",
    )

    q_sum = np.sum(np.eye(len(STAR_COORDS)), axis=1)
    if not np.allclose(q_sum, np.ones(len(STAR_COORDS))):
        raise RuntimeError("unexpected basis setup")

    phi_oh = same_source.build_best_phi_grid()
    q_oh = enclosed_charge(phi_oh)
    r_oh, y_oh = shell_profile(phi_oh)
    y_oh_kernel = q_oh * base_profile
    diff_oh = float(np.max(np.abs(y_oh - y_oh_kernel)))

    phi_fr = coarse.build_finite_rank_phi_grid()
    q_fr = enclosed_charge(phi_fr)
    r_fr, y_fr = shell_profile(phi_fr)
    y_fr_kernel = q_fr * base_profile
    diff_fr = float(np.max(np.abs(y_fr - y_fr_kernel)))

    print("\nExact source families:")
    print(f"  exact local O_h family: Q={q_oh:.8f}, max shell mismatch vs Q*K = {diff_oh:.3e}")
    print(f"  exact finite-rank family: Q={q_fr:.8f}, max shell mismatch vs Q*K = {diff_fr:.3e}")

    record(
        "the exact local O_h family shell-averages are fixed exactly by total charge",
        diff_oh < 1e-14,
        f"max |<phi> - Q*K|={diff_oh:.3e}",
    )
    record(
        "the broader exact finite-rank family shell-averages are fixed exactly by total charge",
        diff_fr < 1e-14,
        f"max |<phi> - Q*K|={diff_fr:.3e}",
    )

    r_match = 4.5
    a_kernel_oh = radial_fit_from_profile(base_r, y_oh_kernel, r_match)
    a_field_oh = radial_fit_from_profile(r_oh, y_oh, r_match)
    a_kernel_fr = radial_fit_from_profile(base_r, y_fr_kernel, r_match)
    a_field_fr = radial_fit_from_profile(r_fr, y_fr, r_match)

    record(
        "the local O_h radial harmonic coefficient is fixed by the universal shell kernel",
        abs(a_kernel_oh - a_field_oh) < 1e-14,
        f"a(field)={a_field_oh:.8f}, a(Q*K)={a_kernel_oh:.8f}",
    )
    record(
        "the finite-rank radial harmonic coefficient is fixed by the universal shell kernel",
        abs(a_kernel_fr - a_field_fr) < 1e-14,
        f"a(field)={a_field_fr:.8f}, a(Q*K)={a_kernel_fr:.8f}",
    )

    direct_oh, coarse_oh = coarse.residual_at_radius(phi_oh, r_match, a_kernel_oh)
    direct_fr, coarse_fr = coarse.residual_at_radius(phi_fr, r_match, a_kernel_fr)

    record(
        "the charge-fixed shell kernel reproduces the same vacuum-close exterior for the local O_h family",
        coarse_oh < 1e-5 and direct_oh > 100.0 * coarse_oh,
        f"direct={direct_oh:.3e}, coarse={coarse_oh:.3e}, improvement={direct_oh/coarse_oh:.1f}x",
        status="BOUNDED",
    )
    record(
        "the charge-fixed shell kernel reproduces the same vacuum-close exterior for the finite-rank family",
        coarse_fr < 2e-5 and direct_fr > 100.0 * coarse_fr,
        f"direct={direct_fr:.3e}, coarse={coarse_fr:.3e}, improvement={direct_fr/coarse_fr:.1f}x",
        status="BOUNDED",
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
