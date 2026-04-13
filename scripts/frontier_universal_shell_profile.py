#!/usr/bin/env python3
"""Universal normalized radial shell profile for the strong-field sewing law.

Exact content:
  1. For the current exact star-supported source families on codex/review-active,
     the normalized radial shell source profile is identical to machine
     precision.
  2. Therefore the exact sewing-shell source reduces to one universal radial
     shell kernel times the total charge Q.

Bounded consequence:
  3. The remaining gravity problem is no longer to find a family-dependent
     shell profile. It is to interpret this universal shell kernel as the
     coarse-grained shell stress / matching law of the nonlinear closure.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader

import numpy as np


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
sew = SourceFileLoader(
    "sewing_shell",
    "/private/tmp/physics-review-active/scripts/frontier_sewing_shell_source.py",
).load_module()
rad = SourceFileLoader(
    "radial_shell",
    "/private/tmp/physics-review-active/scripts/frontier_radial_shell_matching_law.py",
).load_module()


def normalized_shell_profile(phi_grid: np.ndarray, cutoff_radius: float = 4.0):
    sigma = sew.full_neg_laplacian(sew.exterior_projector(phi_grid, cutoff_radius))
    sigma_rad = rad.radial_average_shell(sigma)
    total_charge = float(np.sum(sigma_rad))
    size = sigma.shape[0]
    center = (size - 1) / 2.0
    rows = []
    groups: dict[int, list[tuple[int, int, int]]] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if abs(sigma_rad[i, j, k]) > 1e-12:
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


def main() -> None:
    print("Universal normalized radial shell profile")
    print("=" * 72)

    q_oh, rows_oh = normalized_shell_profile(same_source.build_best_phi_grid())
    q_fr, rows_fr = normalized_shell_profile(coarse.build_finite_rank_phi_grid())

    print(f"local O_h total charge = {q_oh:.8f}")
    print(f"finite-rank total charge = {q_fr:.8f}")
    print("\nr        profile weight")
    for (r, w_oh), (_, w_fr) in zip(rows_oh, rows_fr):
        print(f"{r:8.6f}   {w_oh: .12f}   {w_fr: .12f}")

    max_diff = max_profile_diff(rows_oh, rows_fr)

    record(
        "the local O_h and finite-rank shell profiles live on the same discrete radii",
        [r for r, _ in rows_oh] == [r for r, _ in rows_fr],
        f"{len(rows_oh)} shared shell radii in the sewing band",
    )
    record(
        "the normalized radial shell profile is identical across the two exact source families",
        max_diff < 1e-12,
        f"max normalized profile difference={max_diff:.3e}",
    )
    record(
        "the exact sewing-shell source reduces to one universal radial shell kernel times total charge",
        max_diff < 1e-12,
        f"Q_Oh={q_oh:.8f}, Q_FR={q_fr:.8f}, universal profile on {len(rows_oh)} shells",
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
