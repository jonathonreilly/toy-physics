#!/usr/bin/env python3
"""Exact projector-shell source law for the strong-field sewing band.

Exact content:
  1. For any exact lattice field phi and exterior radial projector Pi_R^ext,
     the projected field phi_ext = Pi_R^ext phi is represented exactly as
     phi_ext = G_0 sigma_R with sigma_R = H_0 phi_ext.
  2. If the physical source support lies inside the cutoff ball B_R, then
     sigma_R is supported only on the discrete shell band straddling r = R.
  3. The shell source carries the same total enclosed charge as the original
     field, so the exterior monopole law is preserved exactly.

Bounded consequence:
  4. For the exact local O_h family and the exact finite-rank family already
     on codex/review-active, choosing R = 4 localizes the exact shell source
     to the same finite sewing band 3 < r <= 5 identified previously by the
     bounded blend construction.

This does not yet derive full nonlinear GR. It replaces the ad hoc sewing
blend by an exact lattice-native shell-source decomposition.
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


same_source = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
coarse = load_frontier("coarse_grained", "frontier_coarse_grained_exterior_law.py")
finite_rank = load_frontier("finite_rank_metric", "frontier_finite_rank_gravity_residual.py")


def full_neg_laplacian(field: np.ndarray) -> np.ndarray:
    lap = np.zeros_like(field)
    lap[1:-1, 1:-1, 1:-1] = (
        6.0 * field[1:-1, 1:-1, 1:-1]
        - field[2:, 1:-1, 1:-1]
        - field[:-2, 1:-1, 1:-1]
        - field[1:-1, 2:, 1:-1]
        - field[1:-1, :-2, 1:-1]
        - field[1:-1, 1:-1, 2:]
        - field[1:-1, 1:-1, :-2]
    )
    return lap


def radii_grid(size: int) -> np.ndarray:
    center = (size - 1) / 2.0
    i, j, k = np.mgrid[0:size, 0:size, 0:size]
    return np.sqrt((i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2)


def exterior_projector(field: np.ndarray, cutoff_radius: float) -> np.ndarray:
    radii = radii_grid(field.shape[0])
    return np.where(radii > cutoff_radius + 1e-12, field, 0.0)


def solve_from_source(source_grid: np.ndarray) -> np.ndarray:
    size = source_grid.shape[0]
    H0, interior = finite_rank.build_neg_laplacian_sparse(size)
    rhs = source_grid[1:-1, 1:-1, 1:-1].reshape(-1)
    sol = spsolve(H0, rhs)
    out = np.zeros_like(source_grid)
    out[1:-1, 1:-1, 1:-1] = sol.reshape((interior, interior, interior))
    return out


def support_band(source_grid: np.ndarray, tol: float = 1e-12) -> tuple[float, float, int]:
    radii = radii_grid(source_grid.shape[0])
    mask = np.abs(source_grid) > tol
    values = radii[mask]
    return float(np.min(values)), float(np.max(values)), int(np.sum(mask))


def analyze_family(name: str, phi_grid: np.ndarray, cutoff_radius: float):
    phi_ext = exterior_projector(phi_grid, cutoff_radius)
    phi_in = phi_grid - phi_ext
    sigma_shell = full_neg_laplacian(phi_ext)
    phi_ext_rec = solve_from_source(sigma_shell)

    ext_err = float(np.max(np.abs(phi_ext_rec - phi_ext)))
    full_err = float(np.max(np.abs((phi_in + phi_ext_rec) - phi_grid)))

    q_total = float(np.sum(full_neg_laplacian(phi_grid)))
    q_shell = float(np.sum(sigma_shell))

    r_min, r_max, count = support_band(sigma_shell)

    print(
        f"{name}: R={cutoff_radius:.1f}, ext_err={ext_err:.3e}, full_err={full_err:.3e}, "
        f"Q_total={q_total:.8f}, Q_shell={q_shell:.8f}, band=[{r_min:.6f}, {r_max:.6f}], "
        f"count={count}"
    )

    return {
        "ext_err": ext_err,
        "full_err": full_err,
        "q_total": q_total,
        "q_shell": q_shell,
        "r_min": r_min,
        "r_max": r_max,
        "count": count,
    }


def main() -> None:
    print("Exact projector-shell source law")
    print("=" * 72)

    cutoff_radius = 4.0

    phi_oh = same_source.build_best_phi_grid()
    oh = analyze_family("exact local O_h family", phi_oh, cutoff_radius)

    phi_fr = coarse.build_finite_rank_phi_grid()
    fr = analyze_family("exact finite-rank family", phi_fr, cutoff_radius)

    record(
        "the local O_h exterior field is reconstructed exactly from the shell source",
        oh["ext_err"] < 1e-12,
        f"max exterior reconstruction error={oh['ext_err']:.3e}",
    )
    record(
        "the finite-rank exterior field is reconstructed exactly from the shell source",
        fr["ext_err"] < 1e-12,
        f"max exterior reconstruction error={fr['ext_err']:.3e}",
    )
    record(
        "the local O_h field decomposes exactly into interior field plus shell-generated exterior",
        oh["full_err"] < 1e-12,
        f"max full-field decomposition error={oh['full_err']:.3e}",
    )
    record(
        "the finite-rank field decomposes exactly into interior field plus shell-generated exterior",
        fr["full_err"] < 1e-12,
        f"max full-field decomposition error={fr['full_err']:.3e}",
    )
    record(
        "the local O_h shell source carries the same total charge as the full field",
        abs(oh["q_shell"] - oh["q_total"]) < 1e-12,
        f"Q_total={oh['q_total']:.8f}, Q_shell={oh['q_shell']:.8f}",
    )
    record(
        "the finite-rank shell source carries the same total charge as the full field",
        abs(fr["q_shell"] - fr["q_total"]) < 1e-12,
        f"Q_total={fr['q_total']:.8f}, Q_shell={fr['q_shell']:.8f}",
    )
    record(
        "the local O_h shell source is confined to the finite sewing band 3 < r <= 5",
        oh["r_min"] > 3.0 and oh["r_max"] <= 5.0 + 1e-12,
        f"support band=[{oh['r_min']:.6f}, {oh['r_max']:.6f}], count={oh['count']}",
    )
    record(
        "the finite-rank shell source is confined to the finite sewing band 3 < r <= 5",
        fr["r_min"] > 3.0 and fr["r_max"] <= 5.0 + 1e-12,
        f"support band=[{fr['r_min']:.6f}, {fr['r_max']:.6f}], count={fr['count']}",
    )
    record(
        "the exact shell-source support coincides with the previously bounded sewing band",
        (
            oh["r_min"] > 3.0
            and oh["r_max"] <= 5.0 + 1e-12
            and fr["r_min"] > 3.0
            and fr["r_max"] <= 5.0 + 1e-12
        ),
        (
            f"O_h band=[{oh['r_min']:.3f}, {oh['r_max']:.3f}], "
            f"finite-rank band=[{fr['r_min']:.3f}, {fr['r_max']:.3f}]"
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
