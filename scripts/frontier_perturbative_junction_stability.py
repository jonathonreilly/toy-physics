#!/usr/bin/env python3
"""Perturbative junction stability for the finite-rank non-O_h source class.

Exact content:
  1. The exact local O_h and finite-rank source families share the same
     orbit-mean whole-shell junction data on 3 < r <= 5.
  2. The finite-rank family has exact zero-potential and zero-shell orbit
     sectors, plus an active perturbative sector.

Bounded content:
  3. On the active sector, the finite-rank junction law is a small
     first-order deformation of the exact orbit-mean O_h base law.
  4. The linearized correction reduces the raw within-orbit spread by several
     hundredfold and leaves only a tiny O(epsilon^2) remainder.
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


SIZE = 15
CENTER = (SIZE - 1) // 2
RADII = sew.radii_grid(SIZE)
BAND_MASK = (RADII > 3.0 + 1e-12) & (RADII <= 5.0 + 1e-12)
TOL = 1e-12


def orbit_key(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(sorted([abs(i - CENTER), abs(j - CENTER), abs(k - CENTER)], reverse=True))


def orbit_rows(phi_grid: np.ndarray):
    ext = sew.exterior_projector(phi_grid, 4.0)
    sigma = sew.full_neg_laplacian(ext)
    total_charge = float(np.sum(sigma))

    psi = 1.0 + ext
    alpha = (1.0 - ext) / (1.0 + ext)
    rho = sigma / (2.0 * np.pi * psi**5)
    stress = 0.5 * rho * (1.0 / alpha - 1.0)

    buckets: dict[tuple[int, int, int], dict[str, list[float]]] = {}
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if not BAND_MASK[i, j, k]:
                    continue
                key = orbit_key(i, j, k)
                slot = buckets.setdefault(key, {"u": [], "k": [], "rho": [], "S": []})
                slot["u"].append(float(ext[i, j, k]) / total_charge)
                slot["k"].append(float(sigma[i, j, k]) / total_charge)
                slot["rho"].append(float(rho[i, j, k]))
                slot["S"].append(float(stress[i, j, k]))

    out: dict[tuple[int, int, int], dict[str, tuple[np.ndarray, float, float]]] = {}
    for key, fields in buckets.items():
        out[key] = {}
        for name, vals in fields.items():
            arr = np.array(vals, dtype=float)
            out[key][name] = (arr, float(np.mean(arr)), float(np.max(arr) - np.min(arr)))
    return total_charge, out


def max_rel_spread(rows, field: str) -> float:
    return max(spread / max(abs(mean), TOL) for _, mean, spread in (rows[k][field] for k in rows))


def lin_response(
    q: float,
    ubar: float,
    kbar: float,
    du: float,
    dk: float,
) -> tuple[float, float, float, float]:
    psi_bar = 1.0 + q * ubar
    alpha_bar = (1.0 - q * ubar) / psi_bar
    rho_bar = q * kbar / (2.0 * np.pi * psi_bar**5)
    stress_bar = 0.5 * rho_bar * (1.0 / alpha_bar - 1.0)

    rho_lin = rho_bar * (1.0 + dk / kbar - 5.0 * q * du / psi_bar)
    stress_lin = stress_bar * (
        1.0
        + dk / kbar
        + du / ubar
        - 5.0 * q * du / psi_bar
        + q * du / (1.0 - q * ubar)
    )
    return rho_bar, stress_bar, rho_lin, stress_lin


def main() -> None:
    print("Perturbative junction stability on finite-rank non-O_h source class")
    print("=" * 72)

    q_oh, oh = orbit_rows(same_source.build_best_phi_grid())
    q_fr, fr = orbit_rows(coarse.build_finite_rank_phi_grid())

    u_mean_diff = max(abs(oh[k]["u"][1] - fr[k]["u"][1]) for k in fr)
    k_mean_diff = max(abs(oh[k]["k"][1] - fr[k]["k"][1]) for k in fr)

    fr_u_rel = max_rel_spread(fr, "u")
    fr_k_rel = max_rel_spread(fr, "k")
    fr_rho_rel = max_rel_spread(fr, "rho")
    fr_s_rel = max_rel_spread(fr, "S")

    q_u_max = max(abs(q_fr * u) for k in fr for u in fr[k]["u"][0])

    zero_u_keys = []
    zero_k_keys = []
    active_keys = []
    for key in sorted(fr):
        ubar = fr[key]["u"][1]
        kbar = fr[key]["k"][1]
        if abs(ubar) < TOL:
            zero_u_keys.append(key)
        elif abs(kbar) < TOL:
            zero_k_keys.append(key)
        else:
            active_keys.append(key)

    rho_abs_resids = []
    stress_abs_resids = []
    rho_rel_resids = []
    stress_rel_resids = []
    for key in active_keys:
        u_arr, ubar, u_spread = fr[key]["u"]
        k_arr, kbar, k_spread = fr[key]["k"]
        rho_arr, rho_bar, rho_spread = fr[key]["rho"]
        s_arr, s_bar, s_spread = fr[key]["S"]
        for u, k, rho, stress in zip(u_arr, k_arr, rho_arr, s_arr):
            du = u - ubar
            dk = k - kbar
            _, _, rho_lin, stress_lin = lin_response(q_fr, ubar, kbar, du, dk)
            rho_abs_resids.append(abs(rho - rho_lin))
            stress_abs_resids.append(abs(stress - stress_lin))
            rho_rel_resids.append(abs(rho - rho_lin) / max(abs(rho_bar), TOL))
            stress_rel_resids.append(abs(stress - stress_lin) / max(abs(s_bar), TOL))

    rho_abs = max(rho_abs_resids)
    stress_abs = max(stress_abs_resids)
    rho_rel = max(rho_rel_resids)
    stress_rel = max(stress_rel_resids)
    rho_improvement = fr_rho_rel / max(rho_rel, TOL)
    stress_improvement = fr_s_rel / max(stress_rel, TOL)

    print(f"Q_local_Oh = {q_oh:.8f}")
    print(f"Q_finite_rank = {q_fr:.8f}")
    print(f"max orbit-mean u/Q difference = {u_mean_diff:.3e}")
    print(f"max orbit-mean k/Q difference = {k_mean_diff:.3e}")
    print(f"finite-rank max relative orbit spreads: u={100*fr_u_rel:.4f}%, k={100*fr_k_rel:.4f}%, rho={100*fr_rho_rel:.4f}%, S={100*fr_s_rel:.4f}%")
    print(f"Q max(u) on finite-rank band = {q_u_max:.6f}")
    print(f"zero-u orbit types = {len(zero_u_keys)}")
    print(f"zero-k orbit types = {len(zero_k_keys)}")
    print(f"active orbit types = {len(active_keys)}")
    print(f"linearized residuals: rho={rho_abs:.3e} (rel {rho_rel:.3e}), S={stress_abs:.3e} (rel {stress_rel:.3e})")

    record(
        "the exact local O_h and finite-rank source families share the same orbit-mean junction data",
        u_mean_diff < 1e-12 and k_mean_diff < 1e-12,
        f"max orbit-mean differences: u={u_mean_diff:.3e}, k={k_mean_diff:.3e}",
    )
    record(
        "the finite-rank family stays in a small within-orbit perturbative tube",
        fr_u_rel < 0.015 and fr_k_rel < 0.017 and fr_rho_rel < 0.015 and fr_s_rel < 0.027,
        (
            f"relative spreads: u={100*fr_u_rel:.4f}%, k={100*fr_k_rel:.4f}%, "
            f"rho={100*fr_rho_rel:.4f}%, S={100*fr_s_rel:.4f}%"
        ),
        status="BOUNDED",
    )
    record(
        "the orbit-resolved bridge map stays in a regular regime on the sewing band",
        q_u_max < 0.1,
        f"Q max(u) = {q_u_max:.6f}",
        status="BOUNDED",
    )
    record(
        "the finite-rank family splits into exact zero-sector and active perturbative orbits",
        len(zero_u_keys) == 6 and len(zero_k_keys) == 3 and len(active_keys) == 8,
        (
            f"zero-u={len(zero_u_keys)}, zero-k={len(zero_k_keys)}, "
            f"active={len(active_keys)}"
        ),
    )
    record(
        "the first-order junction correction captures the active-sector non-O_h deviation",
        rho_rel < 3e-5 and stress_rel < 4e-5,
        f"linearized relative residuals: rho={rho_rel:.3e}, S={stress_rel:.3e}",
        status="BOUNDED",
    )
    record(
        "the linearized correction improves the raw within-orbit spread by several hundredfold",
        rho_improvement > 500.0 and stress_improvement > 500.0,
        (
            f"improvement factors: rho={rho_improvement:.1f}x, "
            f"S={stress_improvement:.1f}x"
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
