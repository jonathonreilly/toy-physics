#!/usr/bin/env python3
"""Orbit-resolved whole-shell stress law under the static isotropic bridge.

Exact content:
  1. On the full sewing band 3 < r <= 5, the orbit-mean exterior-projector
     potential profile per unit charge and orbit-mean shell-source profile per
     unit charge are identical across the current exact local O_h and
     finite-rank source families.
  2. For the exact local O_h family, these orbit-mean profiles are already
     pointwise orbit laws to machine precision.

Bounded content:
  3. For the finite-rank family, the within-orbit variation remains small.
  4. Under the static isotropic conformal bridge, the universal orbit-mean
     profiles already predict the finite-rank orbit-mean stress law with tiny
     absolute error.
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


def orbit_key(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(sorted([abs(i - CENTER), abs(j - CENTER), abs(k - CENTER)], reverse=True))


def orbit_rows(phi_grid: np.ndarray) -> tuple[float, dict[tuple[int, int, int], dict[str, tuple[float, float]]]]:
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

    out: dict[tuple[int, int, int], dict[str, tuple[float, float]]] = {}
    for key, fields in buckets.items():
        out[key] = {}
        for name, vals in fields.items():
            out[key][name] = (float(np.mean(vals)), float(np.max(vals) - np.min(vals)))
    return total_charge, out


def max_mean_diff(
    a: dict[tuple[int, int, int], dict[str, tuple[float, float]]],
    b: dict[tuple[int, int, int], dict[str, tuple[float, float]]],
    field: str,
) -> float:
    keys = sorted(set(a) | set(b))
    return max(abs(a[k][field][0] - b[k][field][0]) for k in keys)


def max_spread(
    rows: dict[tuple[int, int, int], dict[str, tuple[float, float]]],
    field: str,
) -> float:
    return max(v[field][1] for v in rows.values())


def max_rel_spread(
    rows: dict[tuple[int, int, int], dict[str, tuple[float, float]]],
    field: str,
) -> float:
    return max(v[field][1] / max(abs(v[field][0]), 1e-12) for v in rows.values())


def orbit_mean_stress_from_profiles(
    rows: dict[tuple[int, int, int], dict[str, tuple[float, float]]],
    total_charge: float,
) -> dict[tuple[int, int, int], tuple[float, float]]:
    out: dict[tuple[int, int, int], tuple[float, float]] = {}
    for key, fields in rows.items():
        u = fields["u"][0]
        k = fields["k"][0]
        psi = 1.0 + total_charge * u
        alpha = (1.0 - total_charge * u) / (1.0 + total_charge * u)
        rho = total_charge * k / (2.0 * np.pi * psi**5)
        stress = 0.5 * rho * (1.0 / alpha - 1.0)
        out[key] = (rho, stress)
    return out


def max_pred_diff(
    pred: dict[tuple[int, int, int], tuple[float, float]],
    rows: dict[tuple[int, int, int], dict[str, tuple[float, float]]],
    col: int,
) -> float:
    field = "rho" if col == 0 else "S"
    return max(abs(pred[key][col] - rows[key][field][0]) for key in pred)


def main() -> None:
    print("Orbit-resolved whole-shell stress law")
    print("=" * 72)

    q_oh, oh = orbit_rows(same_source.build_best_phi_grid())
    q_fr, fr = orbit_rows(coarse.build_finite_rank_phi_grid())

    u_mean_diff = max_mean_diff(oh, fr, "u")
    k_mean_diff = max_mean_diff(oh, fr, "k")
    oh_u_spread = max_spread(oh, "u")
    oh_k_spread = max_spread(oh, "k")
    fr_u_rel = max_rel_spread(fr, "u")
    fr_k_rel = max_rel_spread(fr, "k")
    fr_rho_rel = max_rel_spread(fr, "rho")
    fr_s_rel = max_rel_spread(fr, "S")

    fr_pred = orbit_mean_stress_from_profiles(oh, q_fr)
    fr_rho_diff = max_pred_diff(fr_pred, fr, 0)
    fr_s_diff = max_pred_diff(fr_pred, fr, 1)

    print(f"Q_local_Oh = {q_oh:.8f}")
    print(f"Q_finite_rank = {q_fr:.8f}")
    print(f"max orbit-mean u/Q difference = {u_mean_diff:.3e}")
    print(f"max orbit-mean k/Q difference = {k_mean_diff:.3e}")
    print(f"exact local O_h max orbit spreads: u={oh_u_spread:.3e}, k={oh_k_spread:.3e}")
    print(
        "finite-rank max relative orbit spreads: "
        f"u={fr_u_rel:.4%}, k={fr_k_rel:.4%}, rho={fr_rho_rel:.4%}, S={fr_s_rel:.4%}"
    )
    print(
        f"finite-rank orbit-mean stress prediction diffs: "
        f"rho={fr_rho_diff:.3e}, S={fr_s_diff:.3e}"
    )

    record(
        "the exact local O_h and finite-rank source families share the same orbit-mean exterior-projector profile per unit charge on the whole sewing band",
        u_mean_diff < 1e-12,
        f"max orbit-mean u/Q difference = {u_mean_diff:.3e}",
    )
    record(
        "the exact local O_h and finite-rank source families share the same orbit-mean shell-source profile per unit charge on the whole sewing band",
        k_mean_diff < 1e-12,
        f"max orbit-mean k/Q difference = {k_mean_diff:.3e}",
    )
    record(
        "for the exact local O_h family the orbit-mean whole-shell law is already pointwise exact on each orbit",
        oh_u_spread < 1e-12 and oh_k_spread < 1e-12,
        f"max spreads: u={oh_u_spread:.3e}, k={oh_k_spread:.3e}",
    )
    record(
        "for the finite-rank family the remaining within-orbit correction stays small on the whole sewing band",
        fr_u_rel < 0.015 and fr_k_rel < 0.017 and fr_rho_rel < 0.015 and fr_s_rel < 0.027,
        (
            f"relative spreads: u={fr_u_rel:.4%}, k={fr_k_rel:.4%}, "
            f"rho={fr_rho_rel:.4%}, S={fr_s_rel:.4%}"
        ),
        status="BOUNDED",
    )
    record(
        "the universal orbit-mean whole-shell profiles already predict the finite-rank orbit-mean bridge stress law with tiny absolute error",
        fr_rho_diff < 2e-7 and fr_s_diff < 3e-8,
        f"orbit-mean (rho,S) diffs = ({fr_rho_diff:.3e}, {fr_s_diff:.3e})",
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
