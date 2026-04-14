#!/usr/bin/env python3
"""Exact support-irrep origin of intra-orbit shell structure.

This runner uses the exact star-supported source class already retained on the
branch and decomposes it into the canonical O_h support irreps carried by the
seven-site star:

  A1(center) ⊕ A1(shell-average) ⊕ E(quadrupole pair) ⊕ T1(vector triplet)

It then lifts each support basis vector through the exact lattice Green solve
and exact projector-shell source law to the sewing band.

Goal:
  identify which microscopic source irreps generate the shell data already
  localized as the remaining tensor-transfer datum.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


ROOT = "/private/tmp/physics-review-active"

same_source = SourceFileLoader(
    "same_source_metric",
    f"{ROOT}/scripts/frontier_same_source_metric_ansatz_scan.py",
).load_module()
finite_rank = SourceFileLoader(
    "finite_rank_metric",
    f"{ROOT}/scripts/frontier_finite_rank_gravity_residual.py",
).load_module()
sew = SourceFileLoader(
    "sewing_shell",
    f"{ROOT}/scripts/frontier_sewing_shell_source.py",
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str


CHECKS: list[Check] = []

SIZE = 15
CENTER = (SIZE - 1) // 2
RADII = sew.radii_grid(SIZE)
BAND_MASK = (RADII > 3.0 + 1e-12) & (RADII <= 5.0 + 1e-12)
LABELS = ["A1(center)", "A1(shell)", "E1", "E2", "T1x", "T1y", "T1z"]


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def orbit_key(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(sorted([abs(i - CENTER), abs(j - CENTER), abs(k - CENTER)], reverse=True))


def solve_support_field(q: np.ndarray) -> np.ndarray:
    H0, interior = same_source.build_neg_laplacian_sparse(SIZE)
    center = interior // 2
    support = [
        same_source.flat_idx(center + v[0], center + v[1], center + v[2], interior)
        for v in same_source.SUPPORT_COORDS
    ]
    G0P = same_source.solve_columns(H0, support)
    phi_flat = G0P @ q
    phi_grid = np.zeros((SIZE, SIZE, SIZE), dtype=float)
    phi_grid[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))
    return phi_grid


def shell_source(phi_grid: np.ndarray) -> np.ndarray:
    return sew.full_neg_laplacian(sew.exterior_projector(phi_grid, 4.0))


def orbit_stats(source_grid: np.ndarray) -> dict[tuple[int, int, int], dict[str, float]]:
    values: dict[tuple[int, int, int], list[float]] = defaultdict(list)
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if not BAND_MASK[i, j, k]:
                    continue
                val = float(source_grid[i, j, k])
                if abs(val) < 1e-14:
                    continue
                values[orbit_key(i, j, k)].append(val)

    out: dict[tuple[int, int, int], dict[str, float]] = {}
    for key, vals in values.items():
        arr = np.array(vals, dtype=float)
        out[key] = {
            "mean": float(np.mean(arr)),
            "std": float(np.std(arr)),
            "count": float(arr.size),
        }
    return out


def max_abs_orbit_mean(stats: dict[tuple[int, int, int], dict[str, float]]) -> float:
    return max(abs(v["mean"]) for v in stats.values())


def max_orbit_std(stats: dict[tuple[int, int, int], dict[str, float]]) -> float:
    return max(v["std"] for v in stats.values())


def weighted_rms_std(stats: dict[tuple[int, int, int], dict[str, float]]) -> float:
    num = sum(v["count"] * (v["std"] ** 2) for v in stats.values())
    den = sum(v["count"] for v in stats.values())
    return float(np.sqrt(num / max(den, 1.0)))


def max_orbit_mean_diff(a: np.ndarray, b: np.ndarray) -> float:
    stats_a = orbit_stats(a)
    stats_b = orbit_stats(b)
    keys = sorted(set(stats_a) | set(stats_b))
    return max(abs(stats_a[k]["mean"] - stats_b[k]["mean"]) for k in keys)


def finite_rank_qeff() -> np.ndarray:
    _, _, _, _, _, GS, W, masses = finite_rank.finite_rank_setup()
    return np.linalg.solve(np.eye(W.shape[0]) - W @ GS, masses)


def main() -> int:
    print("Exact support-irrep lift to intra-orbit shell structure")
    print("=" * 78)

    basis = same_source.build_adapted_basis()
    basis_shells: list[np.ndarray] = []
    basis_stats: list[dict[tuple[int, int, int], dict[str, float]]] = []

    for idx, label in enumerate(LABELS):
        sigma = shell_source(solve_support_field(basis[:, idx]))
        stats = orbit_stats(sigma)
        basis_shells.append(sigma)
        basis_stats.append(stats)
        print(
            f"{label}: total={np.sum(sigma):+.6e}, "
            f"max|orbit mean|={max_abs_orbit_mean(stats):.3e}, "
            f"max orbit std={max_orbit_std(stats):.3e}"
        )

    sigma_a1 = basis_shells[0] + basis_shells[1]
    sigma_non = sum(basis_shells[2:], start=np.zeros_like(basis_shells[0]))

    q_fr = finite_rank_qeff()
    coeff_fr = basis.T @ q_fr
    sigma_recon = sum(coeff_fr[i] * basis_shells[i] for i in range(len(LABELS)))
    sigma_a1_fr = coeff_fr[0] * basis_shells[0] + coeff_fr[1] * basis_shells[1]
    sigma_non_fr = sum(coeff_fr[i] * basis_shells[i] for i in range(2, len(LABELS)))

    phi_fr = np.zeros((SIZE, SIZE, SIZE), dtype=float)
    size, H0, interior, support, G0P, GS, W, masses = finite_rank.finite_rank_setup()
    q_eff = np.linalg.solve(np.eye(W.shape[0]) - W @ GS, masses)
    phi_flat = G0P @ q_eff
    phi_fr[1:-1, 1:-1, 1:-1] = phi_flat.reshape((interior, interior, interior))
    sigma_fr = shell_source(phi_fr)

    recon_err = float(np.max(np.abs(sigma_recon - sigma_fr)))
    orbit_mean_reduction_err = max_orbit_mean_diff(sigma_a1_fr, sigma_fr)
    non_residual_err = float(np.max(np.abs((sigma_fr - sigma_a1_fr) - sigma_non_fr)))

    print("\nFinite-rank source decomposition in support-irrep basis:")
    for label, coeff in zip(LABELS, coeff_fr):
        print(f"  {label}: {coeff:+.6e}")
    print(f"  exact shell-source reconstruction error = {recon_err:.3e}")
    print(f"  A1-only orbit-mean reproduction error   = {orbit_mean_reduction_err:.3e}")
    print(f"  non-A1 fine-structure reconstruction error = {non_residual_err:.3e}")

    record(
        "the two A1 support basis vectors lift to orbit-constant shell-source patterns",
        all(max_orbit_std(basis_stats[i]) < 1e-12 for i in [0, 1]),
        (
            f"A1(center) std={max_orbit_std(basis_stats[0]):.3e}, "
            f"A1(shell) std={max_orbit_std(basis_stats[1]):.3e}"
        ),
    )
    record(
        "the E and T1 support irreps lift with zero orbit means but nonzero intra-orbit shell structure",
        all(max_abs_orbit_mean(basis_stats[i]) < 1e-12 for i in range(2, 7))
        and all(weighted_rms_std(basis_stats[i]) > 1e-4 for i in range(2, 7)),
        (
            "all non-scalar support irreps have vanishing orbit means and "
            "positive intra-orbit RMS structure"
        ),
    )
    record(
        "the finite-rank shell source is reconstructed exactly from the support-irrep lift",
        recon_err < 1e-12,
        f"max shell-source reconstruction error={recon_err:.3e}",
    )
    record(
        "the finite-rank orbit-summed shell data come entirely from the A1 support sector",
        orbit_mean_reduction_err < 1e-12,
        f"max orbit-mean error between full finite-rank shell source and its A1 sector={orbit_mean_reduction_err:.3e}",
    )
    record(
        "the finite-rank intra-orbit shell fine structure comes entirely from the non-A1 support sector",
        non_residual_err < 1e-12,
        f"max non-A1 fine-structure reconstruction error={non_residual_err:.3e}",
    )

    print("\nVerdict:")
    print(
        "The missing microscopic gravity datum is now identified more precisely "
        "than 'intra-orbit shell structure': it is the non-scalar E ⊕ T1 "
        "support-irrep content of the exact seven-site source, lifted exactly "
        "to the sewing band by the lattice Green solve and projector-shell law."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    if n_fail == 0:
        print("All checks passed.")
        return 0
    print("Some checks failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
