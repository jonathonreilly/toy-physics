#!/usr/bin/env python3
"""Exact DtN origin of the universal anisotropic orbit-channel mode.

Exact content:
  1. For every star-support point-Green column, the anisotropic DtN shell
     remainder has the same normalized orbit-sum vector.
  2. The same normalized orbit-sum vector and normalized shell-mean exterior
     response agree with the current exact source families.

Bounded content:
  3. On the reduced orbit/shell-mean surface, the anisotropic sewing-shell
     sector therefore collapses to one exact DtN mode times one scalar
     amplitude.
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


star = SourceFileLoader(
    "star_shell_projector",
    "/private/tmp/physics-review-active/scripts/frontier_star_shell_projector.py",
).load_module()
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


ACTIVE_ORBITS = [
    (3, 2, 2),
    (3, 3, 0),
    (4, 1, 0),
    (4, 1, 1),
]
ANCHOR_ORBIT = (3, 3, 0)


def orbit_key(i: int, j: int, k: int, size: int) -> tuple[int, int, int]:
    center = (size - 1) // 2
    return tuple(sorted([abs(i - center), abs(j - center), abs(k - center)], reverse=True))


def shell_mean_rows(field: np.ndarray, cutoff: float = 5.0) -> list[tuple[float, float]]:
    size = field.shape[0]
    center = (size - 1) / 2.0
    groups: dict[int, list[tuple[int, int, int]]] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                d2 = int((i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2)
                groups.setdefault(d2, []).append((i, j, k))
    rows = []
    for d2 in sorted(groups):
        radius = float(np.sqrt(d2))
        if radius <= cutoff + 1e-12:
            continue
        vals = np.array([field[p] for p in groups[d2]], dtype=float)
        rows.append((radius, float(np.mean(vals))))
    return rows


def reduced_mode_data(phi_grid: np.ndarray, shell_radius: float = 4.0) -> dict[str, object]:
    sigma = sew.full_neg_laplacian(sew.exterior_projector(phi_grid, shell_radius))
    sigma_rad = rad.radial_average_shell(sigma)
    delta_sigma = sigma - sigma_rad
    phi_aniso = rad.solve_from_source(delta_sigma)

    size = delta_sigma.shape[0]
    orbit_sums: dict[tuple[int, int, int], float] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                key = orbit_key(i, j, k, size)
                orbit_sums.setdefault(key, 0.0)
                orbit_sums[key] += float(delta_sigma[i, j, k])
    active = {k: v for k, v in orbit_sums.items() if abs(v) > 1e-12}
    anchor = active[ANCHOR_ORBIT]
    normalized = {k: active[k] / anchor for k in ACTIVE_ORBITS}
    mean_rows = [(r, m / anchor) for r, m in shell_mean_rows(phi_aniso)]
    return {"normalized": normalized, "mean_rows": mean_rows}


def max_mode_diff(
    a: dict[tuple[int, int, int], float], b: dict[tuple[int, int, int], float]
) -> float:
    return max(abs(a[k] - b[k]) for k in ACTIVE_ORBITS)


def max_row_diff(
    rows_a: list[tuple[float, float]], rows_b: list[tuple[float, float]]
) -> float:
    return max(abs(ma - mb) for (_, ma), (_, mb) in zip(rows_a, rows_b))


def format_mode(mode: dict[tuple[int, int, int], float]) -> str:
    return ", ".join(f"{k}:{mode[k]:+.12f}" for k in ACTIVE_ORBITS)


def main() -> None:
    print("Exact DtN origin of the anisotropic orbit-channel mode")
    print("=" * 72)

    columns, _, _ = star.build_point_green_columns(15)
    point_modes = [reduced_mode_data(col) for col in columns]
    family_oh = reduced_mode_data(same_source.build_best_phi_grid())
    family_fr = reduced_mode_data(coarse.build_finite_rank_phi_grid())

    ref_mode = point_modes[0]["normalized"]
    ref_rows = point_modes[0]["mean_rows"]
    max_point_mode_diff = max(max_mode_diff(ref_mode, pm["normalized"]) for pm in point_modes)
    max_point_row_diff = max(max_row_diff(ref_rows, pm["mean_rows"]) for pm in point_modes)
    family_mode_diff = max(
        max_mode_diff(ref_mode, fam["normalized"]) for fam in [family_oh, family_fr]
    )
    family_row_diff = max(
        max_row_diff(ref_rows, fam["mean_rows"]) for fam in [family_oh, family_fr]
    )

    print("Reference DtN orbit mode:")
    print("  " + format_mode(ref_mode))
    print(f"max point-column mode difference = {max_point_mode_diff:.3e}")
    print(f"max point-column shell-mean difference = {max_point_row_diff:.3e}")
    print(f"max family-vs-DtN mode difference = {family_mode_diff:.3e}")
    print(f"max family-vs-DtN shell-mean difference = {family_row_diff:.3e}")

    record(
        "all seven star-support point-Green columns induce the same normalized anisotropic orbit mode",
        max_point_mode_diff < 1e-12,
        f"max mode difference={max_point_mode_diff:.3e}",
    )
    record(
        "all seven star-support point-Green columns induce the same normalized shell-mean exterior response for the anisotropic mode",
        max_point_row_diff < 1e-12,
        f"max shell-mean difference={max_point_row_diff:.3e}",
    )
    record(
        "the exact local O_h and finite-rank source families excite the same normalized anisotropic orbit mode as the DtN point-Green columns",
        family_mode_diff < 1e-12,
        f"max family-vs-DtN mode difference={family_mode_diff:.3e}",
    )
    record(
        "the exact local O_h and finite-rank source families excite the same normalized shell-mean anisotropic response as the DtN point-Green columns",
        family_row_diff < 1e-12,
        f"max family-vs-DtN shell-mean difference={family_row_diff:.3e}",
    )
    record(
        "on the reduced orbit/shell-mean surface the anisotropic sewing-shell sector collapses to one exact DtN mode times one scalar amplitude",
        family_mode_diff < 1e-12 and family_row_diff < 1e-12,
        (
            f"mode difference={family_mode_diff:.3e}, "
            f"shell-mean difference={family_row_diff:.3e}"
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
