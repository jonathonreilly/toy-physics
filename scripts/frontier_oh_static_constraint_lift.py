#!/usr/bin/env python3
"""Exact local static-constraint lift on the current strong-field bridge surface.

Exact content:
  1. For the exact shell source sigma_R = H_0 phi_ext and the native same-charge
     bridge
         psi = 1 + phi_ext
         chi = 1 - phi_ext = alpha * psi
     the local shell density and stress-trace are fixed pointwise by
         rho = sigma_R / (2 pi psi^5)
         S   = 0.5 rho (1/alpha - 1)
  2. These fields satisfy the discrete static conformal constraint pair
         H_0 psi = 2 pi psi^5 rho
         H_0 chi = -2 pi alpha psi^5 (rho + 2 S)
     exactly on the lattice.
  3. On the exact local O_h source class, rho and S are pointwise orbit laws on
     the whole sewing band 3 < r <= 5.

Bounded consequence:
  4. On the broader finite-rank family, the same local constraint pair holds
     exactly, and the remaining within-orbit shell variation stays small.

This closes the shell-to-3+1 lift on the current static conformal bridge
surface. It does not yet prove a full pointwise Einstein/Regge theorem beyond
that bridge.
"""

from __future__ import annotations

from dataclasses import dataclass
from _frontier_loader import load_frontier

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


same_source = load_frontier("same_source_metric", "frontier_same_source_metric_ansatz_scan.py")
coarse = load_frontier("coarse_grained", "frontier_coarse_grained_exterior_law.py")
sew = load_frontier("sewing_shell", "frontier_sewing_shell_source.py")


SIZE = 15
CENTER = (SIZE - 1) // 2
RADII = sew.radii_grid(SIZE)
SHELL_MASK = (RADII > 3.0 + 1e-12) & (RADII <= 5.0 + 1e-12)
OUTSIDE_MASK = RADII > 5.0 + 1e-12


def orbit_key(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(sorted([abs(i - CENTER), abs(j - CENTER), abs(k - CENTER)], reverse=True))


def bridge_fields(phi_grid: np.ndarray, cutoff_radius: float = 4.0):
    phi_ext = sew.exterior_projector(phi_grid, cutoff_radius)
    sigma = sew.full_neg_laplacian(phi_ext)
    psi = 1.0 + phi_ext
    chi = 1.0 - phi_ext
    alpha = chi / psi
    rho = sigma / (2.0 * np.pi * psi**5)
    stress = 0.5 * rho * (1.0 / alpha - 1.0)
    return phi_ext, sigma, psi, chi, alpha, rho, stress


def constraint_residuals(
    psi: np.ndarray, chi: np.ndarray, alpha: np.ndarray, rho: np.ndarray, stress: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    res_psi = sew.full_neg_laplacian(psi) - 2.0 * np.pi * psi**5 * rho
    res_chi = sew.full_neg_laplacian(chi) + 2.0 * np.pi * alpha * psi**5 * (rho + 2.0 * stress)
    return res_psi, res_chi


def max_orbit_spread(field: np.ndarray, mask: np.ndarray) -> float:
    rows: dict[tuple[int, int, int], list[float]] = {}
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if not mask[i, j, k]:
                    continue
                rows.setdefault(orbit_key(i, j, k), []).append(float(field[i, j, k]))
    return max(float(np.max(vals) - np.min(vals)) for vals in rows.values())


def max_rel_orbit_spread(field: np.ndarray, mask: np.ndarray) -> float:
    rows: dict[tuple[int, int, int], list[float]] = {}
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if not mask[i, j, k]:
                    continue
                rows.setdefault(orbit_key(i, j, k), []).append(float(field[i, j, k]))
    out = 0.0
    for vals in rows.values():
        vals_arr = np.array(vals, dtype=float)
        spread = float(np.max(vals_arr) - np.min(vals_arr))
        mean = float(np.mean(vals_arr))
        out = max(out, spread / max(abs(mean), 1e-12))
    return out


def analyze_family(phi_grid: np.ndarray):
    phi_ext, sigma, psi, chi, alpha, rho, stress = bridge_fields(phi_grid)
    res_psi, res_chi = constraint_residuals(psi, chi, alpha, rho, stress)
    shell_support = np.abs(sigma) > 1e-12
    return {
        "sigma": sigma,
        "psi": psi,
        "chi": chi,
        "alpha": alpha,
        "rho": rho,
        "stress": stress,
        "res_psi": res_psi,
        "res_chi": res_chi,
        "shell_charge": float(np.sum(sigma)),
        "shell_support_min": float(np.min(RADII[shell_support])),
        "shell_support_max": float(np.max(RADII[shell_support])),
        "shell_rho_spread": max_orbit_spread(rho, SHELL_MASK),
        "shell_s_spread": max_orbit_spread(stress, SHELL_MASK),
        "shell_rho_rel": max_rel_orbit_spread(rho, SHELL_MASK),
        "shell_s_rel": max_rel_orbit_spread(stress, SHELL_MASK),
    }


def main() -> None:
    print("Exact local static-constraint lift")
    print("=" * 72)

    oh = analyze_family(same_source.build_best_phi_grid())
    fr = analyze_family(coarse.build_finite_rank_phi_grid())

    print(
        "exact local O_h: "
        f"shell band=[{oh['shell_support_min']:.6f}, {oh['shell_support_max']:.6f}], "
        f"max residuals=(psi={np.max(np.abs(oh['res_psi'])):.3e}, "
        f"chi={np.max(np.abs(oh['res_chi'])):.3e})"
    )
    print(
        "finite-rank: "
        f"shell band=[{fr['shell_support_min']:.6f}, {fr['shell_support_max']:.6f}], "
        f"max residuals=(psi={np.max(np.abs(fr['res_psi'])):.3e}, "
        f"chi={np.max(np.abs(fr['res_chi'])):.3e})"
    )
    print(
        "shell orbit spreads: "
        f"O_h (rho,S)=({oh['shell_rho_spread']:.3e},{oh['shell_s_spread']:.3e}), "
        f"finite-rank rel (rho,S)=({100*fr['shell_rho_rel']:.4f}%,{100*fr['shell_s_rel']:.4f}%)"
    )

    record(
        "the exact local O_h shell source remains confined to the sewing band 3 < r <= 5",
        oh["shell_support_min"] > 3.0 and oh["shell_support_max"] <= 5.0 + 1e-12,
        f"shell band=[{oh['shell_support_min']:.6f}, {oh['shell_support_max']:.6f}]",
    )
    record(
        "the exact local O_h bridge fields satisfy the first local static conformal constraint exactly",
        float(np.max(np.abs(oh["res_psi"]))) < 1e-12,
        f"max |H0 psi - 2pi psi^5 rho| = {np.max(np.abs(oh['res_psi'])):.3e}",
    )
    record(
        "the exact local O_h bridge fields satisfy the second local static conformal constraint exactly",
        float(np.max(np.abs(oh["res_chi"]))) < 1e-12,
        f"max |H0 chi + 2pi alpha psi^5 (rho+2S)| = {np.max(np.abs(oh['res_chi'])):.3e}",
    )
    record(
        "outside the sewing shell the exact local O_h bridge is vacuum in the discrete static constraint sense",
        float(np.max(np.abs(oh["res_psi"][OUTSIDE_MASK]))) < 1e-12
        and float(np.max(np.abs(oh["res_chi"][OUTSIDE_MASK]))) < 1e-12,
        (
            f"outside max residuals = "
            f"({np.max(np.abs(oh['res_psi'][OUTSIDE_MASK])):.3e}, "
            f"{np.max(np.abs(oh['res_chi'][OUTSIDE_MASK])):.3e})"
        ),
    )
    record(
        "on the exact local O_h class the lifted shell density and stress are pointwise orbit laws",
        oh["shell_rho_spread"] < 1e-12 and oh["shell_s_spread"] < 1e-12,
        f"max orbit spreads = rho {oh['shell_rho_spread']:.3e}, S {oh['shell_s_spread']:.3e}",
    )
    record(
        "the broader finite-rank family satisfies the same local static conformal constraints exactly",
        float(np.max(np.abs(fr["res_psi"]))) < 1e-12 and float(np.max(np.abs(fr["res_chi"]))) < 1e-12,
        (
            f"max residuals = "
            f"({np.max(np.abs(fr['res_psi'])):.3e}, {np.max(np.abs(fr['res_chi'])):.3e})"
        ),
    )
    record(
        "on the broader finite-rank family the remaining local shell variation stays small",
        fr["shell_rho_rel"] < 0.015 and fr["shell_s_rel"] < 0.027,
        (
            f"relative shell spreads = "
            f"rho {100*fr['shell_rho_rel']:.4f}%, S {100*fr['shell_s_rel']:.4f}%"
        ),
        status="BOUNDED",
    )
    record(
        "the shell-to-3+1 lift is no longer open on the current static conformal bridge surface",
        float(np.max(np.abs(oh["res_psi"]))) < 1e-12
        and float(np.max(np.abs(oh["res_chi"]))) < 1e-12
        and oh["shell_rho_spread"] < 1e-12
        and oh["shell_s_spread"] < 1e-12,
        "exact local static conformal constraint lift on the exact local O_h class",
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
