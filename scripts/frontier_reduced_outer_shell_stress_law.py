#!/usr/bin/env python3
"""Exact reduced outer-shell stress law under the static isotropic bridge.

Exact content on the reduced outer-shell surface:
  1. The outer-shell radial source profile per unit charge and the outer-shell
     exterior potential profile per unit charge are identical across the
     star-support point-Green columns.
  2. Therefore, under the static isotropic conformal bridge, the reduced
     shell-mean density and stress-trace obey one exact charge-parameterized
     law on 4 < r <= 5:
         rho_Q(r) = Q k(r) / (2 pi (1 + Q u(r))^5)
         S_Q(r)   = 0.5 rho_Q(r) (1/alpha_Q(r) - 1)
         alpha_Q(r) = (1 - Q u(r)) / (1 + Q u(r))
  3. The current exact local O_h and finite-rank source families satisfy that
     reduced stress law to machine precision.

Bounded content:
  4. This is the reduced shell-stress lift of the exact junction operator on
     the static isotropic bridge surface; it is not yet the full local 4D
     shell-stress theorem.
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


def shell_groups(size: int) -> dict[int, list[tuple[int, int, int]]]:
    center = (size - 1) / 2.0
    groups: dict[int, list[tuple[int, int, int]]] = {}
    for i in range(size):
        for j in range(size):
            for k in range(size):
                d2 = int((i - center) ** 2 + (j - center) ** 2 + (k - center) ** 2)
                groups.setdefault(d2, []).append((i, j, k))
    return groups


GROUPS = shell_groups(15)
OUTER_D2 = [d2 for d2 in sorted(GROUPS) if 4.0 < np.sqrt(d2) <= 5.0]


def reduced_outer_profiles(phi_grid: np.ndarray, shell_radius: float = 4.0):
    ext = sew.exterior_projector(phi_grid, shell_radius)
    sigma = sew.full_neg_laplacian(ext)
    sigma_rad = rad.radial_average_shell(sigma)
    total_charge = float(np.sum(sigma))

    rows = []
    for d2 in OUTER_D2:
        pts = GROUPS[d2]
        radius = float(np.sqrt(d2))
        k = float(np.mean([sigma_rad[p] for p in pts])) / total_charge
        u = float(np.mean([ext[p] for p in pts])) / total_charge
        rows.append((radius, k, u))
    return total_charge, rows


def reduced_outer_stress(rows: list[tuple[float, float, float]], total_charge: float):
    out = []
    for radius, k, u in rows:
        psi = 1.0 + total_charge * u
        alpha = (1.0 - total_charge * u) / (1.0 + total_charge * u)
        rho = total_charge * k / (2.0 * np.pi * psi**5)
        stress = 0.5 * rho * (1.0 / alpha - 1.0)
        out.append((radius, rho, stress))
    return out


def max_profile_diff(a, b, col: int) -> float:
    return max(abs(x[col] - y[col]) for x, y in zip(a, b))


def main() -> None:
    print("Exact reduced outer-shell stress law")
    print("=" * 72)

    columns, _, _ = star.build_point_green_columns(15)
    point_profiles = [reduced_outer_profiles(col) for col in columns]
    ref_q, ref_rows = point_profiles[0]

    point_k_diff = max(max_profile_diff(ref_rows, rows, 1) for _, rows in point_profiles)
    point_u_diff = max(max_profile_diff(ref_rows, rows, 2) for _, rows in point_profiles)
    point_q_diff = max(abs(q - 1.0) for q, _ in point_profiles)

    ref_stress = reduced_outer_stress(ref_rows, 1.0)

    family_oh_q, family_oh_rows = reduced_outer_profiles(same_source.build_best_phi_grid())
    family_fr_q, family_fr_rows = reduced_outer_profiles(coarse.build_finite_rank_phi_grid())
    family_oh_pred = reduced_outer_stress(ref_rows, family_oh_q)
    family_fr_pred = reduced_outer_stress(ref_rows, family_fr_q)
    family_oh_direct = reduced_outer_stress(family_oh_rows, family_oh_q)
    family_fr_direct = reduced_outer_stress(family_fr_rows, family_fr_q)

    oh_rho_diff = max_profile_diff(family_oh_pred, family_oh_direct, 1)
    oh_s_diff = max_profile_diff(family_oh_pred, family_oh_direct, 2)
    fr_rho_diff = max_profile_diff(family_fr_pred, family_fr_direct, 1)
    fr_s_diff = max_profile_diff(family_fr_pred, family_fr_direct, 2)

    print(f"outer-shell radii = {[round(r, 6) for r, _, _ in ref_rows]}")
    print(f"max point-column k(r) difference = {point_k_diff:.3e}")
    print(f"max point-column u(r) difference = {point_u_diff:.3e}")
    print(f"max point-column |Q-1| = {point_q_diff:.3e}")
    print(
        f"family stress-law agreement: "
        f"O_h rho={oh_rho_diff:.3e}, O_h S={oh_s_diff:.3e}, "
        f"finite-rank rho={fr_rho_diff:.3e}, finite-rank S={fr_s_diff:.3e}"
    )

    record(
        "all seven point-Green columns induce the same outer-shell radial source profile per unit charge",
        point_k_diff < 1e-12,
        f"max k(r) difference = {point_k_diff:.3e}",
    )
    record(
        "all seven point-Green columns induce the same outer-shell exterior potential profile per unit charge",
        point_u_diff < 1e-12 and point_q_diff < 1e-12,
        (
            f"max u(r) difference = {point_u_diff:.3e}, "
            f"max |Q-1| = {point_q_diff:.3e}"
        ),
    )
    record(
        "the reduced outer-shell density law is fixed exactly by total charge on the static isotropic bridge surface",
        oh_rho_diff < 1e-12 and fr_rho_diff < 1e-12,
        f"O_h rho diff = {oh_rho_diff:.3e}, finite-rank rho diff = {fr_rho_diff:.3e}",
    )
    record(
        "the reduced outer-shell stress-trace law is fixed exactly by total charge on the static isotropic bridge surface",
        oh_s_diff < 1e-12 and fr_s_diff < 1e-12,
        f"O_h S diff = {oh_s_diff:.3e}, finite-rank S diff = {fr_s_diff:.3e}",
    )
    record(
        "the exact local O_h and finite-rank source families satisfy the same one-parameter reduced outer-shell stress law",
        oh_rho_diff < 1e-12 and oh_s_diff < 1e-12 and fr_rho_diff < 1e-12 and fr_s_diff < 1e-12,
        (
            f"O_h (rho,S)=({oh_rho_diff:.3e},{oh_s_diff:.3e}), "
            f"finite-rank (rho,S)=({fr_rho_diff:.3e},{fr_s_diff:.3e})"
        ),
    )
    record(
        "under the static isotropic conformal bridge the reduced shell-stress lift is no longer open on the outer half of the sewing band",
        oh_rho_diff < 1e-12 and oh_s_diff < 1e-12 and fr_rho_diff < 1e-12 and fr_s_diff < 1e-12,
        "exact one-parameter reduced outer-shell stress family",
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
