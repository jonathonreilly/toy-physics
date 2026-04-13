#!/usr/bin/env python3
"""Exact discrete DtN shell kernel for the strong-field matching law.

Exact content:
  1. Fix a cutoff radius R and the exterior domain Omega_R = {r > R} on the
     finite Dirichlet lattice box. For any prescribed inner trace f on the
     first exterior layer Gamma_R, there is a unique discrete harmonic
     extension u_f on Omega_R with zero outer-box boundary data.
  2. For the centered point-Green field G_0, that harmonic extension exactly
     equals the exterior projector Pi_R^ext G_0.
  3. The associated shell source
         Lambda_R(f) = H_0 u_f
     is therefore an exact Dirichlet-to-Neumann shell source supported on the
     finite sewing band.
  4. The normalized radial profile of Lambda_R(f_0), where f_0 is the inner
     trace of G_0, coincides exactly with the previously extracted universal
     shell profile.
  5. Repeating the construction for all seven star-support point-Green columns
     gives the same normalized radial shell kernel to machine precision.

Bounded content:
  6. The charge-fixed exterior law already used on codex/review-active is
     therefore tied to an exact microscopic boundary operator, not just an
     extracted family fit.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

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


same_source = SourceFileLoader(
    "same_source_metric",
    "/private/tmp/physics-review-active/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
coarse = SourceFileLoader(
    "coarse_grained",
    "/private/tmp/physics-review-active/scripts/frontier_coarse_grained_exterior_law.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    "/private/tmp/physics-review-active/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()
rad = SourceFileLoader(
    "radial_shell",
    "/private/tmp/physics-review-active/scripts/frontier_radial_shell_matching_law.py",
).load_module()
star = SourceFileLoader(
    "star_shell_projector",
    "/private/tmp/physics-review-active/scripts/frontier_star_shell_projector.py",
).load_module()
univ = SourceFileLoader(
    "universal_shell",
    "/private/tmp/physics-review-active/scripts/frontier_universal_shell_profile.py",
).load_module()


def flat_from_full(i: int, j: int, k: int, interior: int) -> int:
    return finite_rank.flat_idx(i - 1, j - 1, k - 1, interior)


def full_from_flat(idx: int, interior: int) -> tuple[int, int, int]:
    i = idx // (interior * interior)
    rem = idx % (interior * interior)
    j = rem // interior
    k = rem % interior
    return i + 1, j + 1, k + 1


def exterior_sets(size: int, cutoff_radius: float):
    radii = sew.radii_grid(size)
    ext_full = np.zeros((size, size, size), dtype=bool)
    ext_full[1:-1, 1:-1, 1:-1] = radii[1:-1, 1:-1, 1:-1] > cutoff_radius + 1e-12

    interior = size - 2
    trace: list[int] = []
    bulk: list[int] = []
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            for k in range(1, size - 1):
                if not ext_full[i, j, k]:
                    continue
                is_trace = False
                for di, dj, dk in [
                    (1, 0, 0),
                    (-1, 0, 0),
                    (0, 1, 0),
                    (0, -1, 0),
                    (0, 0, 1),
                    (0, 0, -1),
                ]:
                    if not ext_full[i + di, j + dj, k + dk]:
                        is_trace = True
                        break
                idx = flat_from_full(i, j, k, interior)
                if is_trace:
                    trace.append(idx)
                else:
                    bulk.append(idx)
    return np.array(trace, dtype=int), np.array(bulk, dtype=int)


def trace_values_from_grid(grid: np.ndarray, trace_idx: np.ndarray, interior: int) -> np.ndarray:
    vals = np.zeros(trace_idx.shape[0], dtype=float)
    for row, idx in enumerate(trace_idx):
        i, j, k = full_from_flat(int(idx), interior)
        vals[row] = float(grid[i, j, k])
    return vals


def solve_exterior_dirichlet(trace_vals: np.ndarray, trace_idx: np.ndarray, bulk_idx: np.ndarray, size: int) -> np.ndarray:
    H0, interior = finite_rank.build_neg_laplacian_sparse(size)
    A = H0[bulk_idx][:, bulk_idx].tocsr()
    B = H0[bulk_idx][:, trace_idx].tocsr()
    rhs = -(B @ trace_vals)
    bulk_sol = spsolve(A, rhs) if bulk_idx.size else np.zeros(0, dtype=float)

    interior_vec = np.zeros(H0.shape[0], dtype=float)
    interior_vec[trace_idx] = trace_vals
    if bulk_idx.size:
        interior_vec[bulk_idx] = bulk_sol

    grid = np.zeros((size, size, size), dtype=float)
    grid[1:-1, 1:-1, 1:-1] = interior_vec.reshape((interior, interior, interior))
    return grid


def normalized_shell_profile_from_source(source_grid: np.ndarray):
    sigma_rad = rad.radial_average_shell(source_grid)
    total_charge = float(np.sum(sigma_rad))
    size = source_grid.shape[0]
    center = (size - 1) / 2.0
    rows = []
    groups: dict[int, list[tuple[int, int, int]]] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if abs(sigma_rad[i, j, k]) <= 1e-12:
                    continue
                dx = i - center
                dy = j - center
                dz = k - center
                d2 = int(dx * dx + dy * dy + dz * dz)
                groups.setdefault(d2, []).append((i, j, k))
    for d2 in sorted(groups):
        shell_sum = float(np.sum([sigma_rad[p] for p in groups[d2]]))
        rows.append((float(np.sqrt(d2)), shell_sum / total_charge))
    return total_charge, rows


def max_profile_diff(rows_a, rows_b) -> float:
    return max(abs(a[1] - b[1]) for a, b in zip(rows_a, rows_b))


def analyze_point_green_dtn(size: int, cutoff_radius: float):
    green_cols, _, _ = star.build_point_green_columns(size)
    trace_idx, bulk_idx = exterior_sets(size, cutoff_radius)
    interior = size - 2

    center_grid = green_cols[0]
    center_trace = trace_values_from_grid(center_grid, trace_idx, interior)
    center_ext_dtn = solve_exterior_dirichlet(center_trace, trace_idx, bulk_idx, size)
    center_ext_proj = sew.exterior_projector(center_grid, cutoff_radius)
    center_err = float(np.max(np.abs(center_ext_dtn - center_ext_proj)))

    sigma_center = sew.full_neg_laplacian(center_ext_dtn)
    center_band = sew.support_band(sigma_center)
    q_center, rows_center = normalized_shell_profile_from_source(sigma_center)

    max_star_diff = 0.0
    for grid in green_cols:
        trace_vals = trace_values_from_grid(grid, trace_idx, interior)
        ext_dtn = solve_exterior_dirichlet(trace_vals, trace_idx, bulk_idx, size)
        sigma = sew.full_neg_laplacian(ext_dtn)
        _, rows = normalized_shell_profile_from_source(sigma)
        max_star_diff = max(max_star_diff, max_profile_diff(rows_center, rows))

    return {
        "center_err": center_err,
        "center_band": center_band,
        "rows_center": rows_center,
        "q_center": q_center,
        "max_star_diff": max_star_diff,
        "trace_count": int(trace_idx.size),
        "bulk_count": int(bulk_idx.size),
    }


def main() -> None:
    print("Discrete DtN shell kernel for the strong-field sewing law")
    print("=" * 72)

    size = 15
    cutoff_radius = 4.0
    dtn = analyze_point_green_dtn(size, cutoff_radius)

    q_oh, rows_oh = univ.normalized_shell_profile(same_source.build_best_phi_grid(), cutoff_radius)
    q_fr, rows_fr = univ.normalized_shell_profile(coarse.build_finite_rank_phi_grid(), cutoff_radius)
    diff_oh = max_profile_diff(dtn["rows_center"], rows_oh)
    diff_fr = max_profile_diff(dtn["rows_center"], rows_fr)

    print(f"trace nodes on Gamma_R: {dtn['trace_count']}")
    print(f"harmonic bulk nodes in Omega_R: {dtn['bulk_count']}")
    print(f"center-point DtN reconstruction error: {dtn['center_err']:.3e}")
    print(
        "center-point shell band: "
        f"[{dtn['center_band'][0]:.6f}, {dtn['center_band'][1]:.6f}], "
        f"count={dtn['center_band'][2]}"
    )
    print(f"Q_center_shell = {dtn['q_center']:.8f}")
    print(f"Q_Oh = {q_oh:.8f}")
    print(f"Q_FR = {q_fr:.8f}")

    print("\nr        k_DTN(r)")
    for r, w in dtn["rows_center"]:
        print(f"{r:8.6f}   {w: .12f}")

    record(
        "the exterior projector of the centered point-Green field equals the unique exterior Dirichlet extension of its trace",
        dtn["center_err"] < 1e-12,
        f"max exterior DtN/projector mismatch={dtn['center_err']:.3e}",
    )
    record(
        "the centered-point DtN shell source is confined to the exact sewing band 3 < r <= 5",
        dtn["center_band"][0] > 3.0 and dtn["center_band"][1] <= 5.0 + 1e-12,
        (
            f"support band=[{dtn['center_band'][0]:.6f}, {dtn['center_band'][1]:.6f}], "
            f"count={dtn['center_band'][2]}"
        ),
    )
    record(
        "all seven star-support point-Green columns induce the same normalized DtN shell kernel",
        dtn["max_star_diff"] < 1e-12,
        f"max star-support DtN kernel difference={dtn['max_star_diff']:.3e}",
    )
    record(
        "the DtN shell kernel matches the exact local O_h universal shell profile",
        diff_oh < 1e-12,
        f"max profile difference={diff_oh:.3e}",
    )
    record(
        "the DtN shell kernel matches the exact finite-rank universal shell profile",
        diff_fr < 1e-12,
        f"max profile difference={diff_fr:.3e}",
    )
    record(
        "the universal shell kernel is the charge-normalized DtN image of the star-support trace mode",
        diff_oh < 1e-12 and diff_fr < 1e-12 and dtn["max_star_diff"] < 1e-12,
        (
            f"DtN-vs-O_h={diff_oh:.3e}, DtN-vs-finite-rank={diff_fr:.3e}, "
            f"star-universality={dtn['max_star_diff']:.3e}"
        ),
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
