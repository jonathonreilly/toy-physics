#!/usr/bin/env python3
"""Exact one-parameter reduced sewing-shell law on the star-supported source class.

Exact content:
  1. Every star-support point-Green column has unit total charge and induces
     the same normalized reduced shell law:
       - same radial shell kernel per unit charge
       - same anisotropic orbit-mode vector per unit charge
       - same shell-mean exterior response per unit charge
  2. By linearity, any star-supported source therefore has reduced sewing-shell
     law fixed exactly by total charge Q alone on this reduced surface.
  3. The anisotropic anchor amplitude obeys
         A_aniso = c_aniso * Q
     with one exact lattice constant c_aniso.

Bounded content:
  4. On the reduced surface, this behaves like an isotropic shell density plus
     one universal cubic shear mode, both tied to the same scalar charge.
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


def radial_profile(source_grid: np.ndarray) -> list[tuple[float, float]]:
    sigma_rad = rad.radial_average_shell(source_grid)
    total_charge = float(np.sum(sigma_rad))
    size = source_grid.shape[0]
    center = (size - 1) / 2.0
    groups: dict[int, list[tuple[int, int, int]]] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                if abs(sigma_rad[i, j, k]) <= 1e-12:
                    continue
                d2 = int((i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2)
                groups.setdefault(d2, []).append((i, j, k))
    rows = []
    for d2 in sorted(groups):
        shell_sum = float(np.sum([sigma_rad[p] for p in groups[d2]]))
        rows.append((float(np.sqrt(d2)), shell_sum / total_charge))
    return rows


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


def reduced_data(phi_grid: np.ndarray, shell_radius: float = 4.0) -> dict[str, object]:
    sigma = sew.full_neg_laplacian(sew.exterior_projector(phi_grid, shell_radius))
    sigma_rad = rad.radial_average_shell(sigma)
    delta_sigma = sigma - sigma_rad
    phi_shell = rad.solve_from_source(sigma)
    phi_aniso = rad.solve_from_source(delta_sigma)

    size = sigma.shape[0]
    orbit_sums: dict[tuple[int, int, int], float] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                key = orbit_key(i, j, k, size)
                orbit_sums.setdefault(key, 0.0)
                orbit_sums[key] += float(delta_sigma[i, j, k])
    active = {k: v for k, v in orbit_sums.items() if abs(v) > 1e-12}

    total_charge = float(np.sum(sigma))
    anchor = active[ANCHOR_ORBIT]
    norm_orbit = {k: active[k] / total_charge for k in ACTIVE_ORBITS}
    mean_shell = [(r, m / total_charge) for r, m in shell_mean_rows(phi_shell)]
    mean_aniso = [(r, m / total_charge) for r, m in shell_mean_rows(phi_aniso)]
    return {
        "Q": total_charge,
        "anchor_per_Q": anchor / total_charge,
        "radial_profile": radial_profile(sigma),
        "norm_orbit": norm_orbit,
        "mean_shell": mean_shell,
        "mean_aniso": mean_aniso,
    }


def max_profile_diff(a: list[tuple[float, float]], b: list[tuple[float, float]]) -> float:
    return max(abs(va - vb) for (_, va), (_, vb) in zip(a, b))


def max_mode_diff(
    a: dict[tuple[int, int, int], float], b: dict[tuple[int, int, int], float]
) -> float:
    return max(abs(a[k] - b[k]) for k in ACTIVE_ORBITS)


def main() -> None:
    print("Exact one-parameter reduced sewing-shell law")
    print("=" * 72)

    columns, _, _ = star.build_point_green_columns(15)
    point_data = [reduced_data(col) for col in columns]
    ref = point_data[0]

    point_charge_diff = max(abs(d["Q"] - 1.0) for d in point_data)
    point_rad_diff = max(max_profile_diff(ref["radial_profile"], d["radial_profile"]) for d in point_data)
    point_mode_diff = max(max_mode_diff(ref["norm_orbit"], d["norm_orbit"]) for d in point_data)
    point_shell_diff = max(max_profile_diff(ref["mean_shell"], d["mean_shell"]) for d in point_data)
    point_aniso_diff = max(max_profile_diff(ref["mean_aniso"], d["mean_aniso"]) for d in point_data)
    c_aniso = ref["anchor_per_Q"]

    family_oh = reduced_data(same_source.build_best_phi_grid())
    family_fr = reduced_data(coarse.build_finite_rank_phi_grid())
    family_rad_diff = max(
        max_profile_diff(ref["radial_profile"], fam["radial_profile"])
        for fam in [family_oh, family_fr]
    )
    family_mode_diff = max(
        max_mode_diff(ref["norm_orbit"], fam["norm_orbit"])
        for fam in [family_oh, family_fr]
    )
    family_shell_diff = max(
        max_profile_diff(ref["mean_shell"], fam["mean_shell"])
        for fam in [family_oh, family_fr]
    )
    family_aniso_diff = max(
        max_profile_diff(ref["mean_aniso"], fam["mean_aniso"])
        for fam in [family_oh, family_fr]
    )
    family_c_diff = max(abs(fam["anchor_per_Q"] - c_aniso) for fam in [family_oh, family_fr])

    print(f"c_aniso = {c_aniso:.15f}")
    print(f"max point-column charge difference from unity = {point_charge_diff:.3e}")
    print(f"max point-column radial-profile difference = {point_rad_diff:.3e}")
    print(f"max point-column orbit-mode difference = {point_mode_diff:.3e}")
    print(f"max point-column shell-mean total-field difference = {point_shell_diff:.3e}")
    print(f"max point-column shell-mean anisotropic-field difference = {point_aniso_diff:.3e}")
    print(f"max family-vs-reference c_aniso difference = {family_c_diff:.3e}")

    record(
        "all seven point-Green columns carry unit total charge",
        point_charge_diff < 1e-12,
        f"max |Q-1| across columns = {point_charge_diff:.3e}",
    )
    record(
        "all seven point-Green columns induce the same radial shell kernel per unit charge",
        point_rad_diff < 1e-12,
        f"max radial-profile difference = {point_rad_diff:.3e}",
    )
    record(
        "all seven point-Green columns induce the same anisotropic orbit mode per unit charge",
        point_mode_diff < 1e-12,
        f"max orbit-mode difference = {point_mode_diff:.3e}",
    )
    record(
        "all seven point-Green columns induce the same shell-mean exterior response per unit charge",
        point_shell_diff < 1e-12 and point_aniso_diff < 1e-12,
        (
            f"max total-field difference = {point_shell_diff:.3e}, "
            f"max anisotropic-field difference = {point_aniso_diff:.3e}"
        ),
    )
    record(
        "the anisotropic anchor amplitude obeys A_aniso = c_aniso * Q with one exact lattice constant",
        point_mode_diff < 1e-12 and point_charge_diff < 1e-12,
        f"c_aniso = {c_aniso:.15f}",
    )
    record(
        "the exact local O_h and finite-rank source families satisfy the same one-parameter reduced shell law",
        family_rad_diff < 1e-12
        and family_mode_diff < 1e-12
        and family_shell_diff < 1e-12
        and family_aniso_diff < 1e-12
        and family_c_diff < 1e-12,
        (
            f"radial={family_rad_diff:.3e}, orbit={family_mode_diff:.3e}, "
            f"shell={family_shell_diff:.3e}, aniso={family_aniso_diff:.3e}, "
            f"c_diff={family_c_diff:.3e}"
        ),
    )
    record(
        "on the reduced surface the sewing-shell law behaves like one isotropic shell density plus one cubic shear mode tied to total charge",
        family_mode_diff < 1e-12 and family_c_diff < 1e-12,
        f"c_aniso = {c_aniso:.15f}",
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
