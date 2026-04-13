#!/usr/bin/env python3
"""Pointwise whole-shell bridge law on the exact local O_h source class.

Exact content:
  1. On the exact local O_h source class, the whole-shell bridge data are
     pointwise orbit laws across 3 < r <= 5:
         u = phi_ext / Q
         k = sigma_R / Q
  2. With the native same-charge bridge fixed, the induced whole-shell bridge
     density rho and stress-trace S are also pointwise orbit laws.

Bounded content:
  3. On the broader finite-rank family, the remaining within-orbit correction
     is small rather than free.
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


def pointwise_orbit_spreads(phi_grid: np.ndarray):
    ext = sew.exterior_projector(phi_grid, 4.0)
    sigma = sew.full_neg_laplacian(ext)
    total_charge = float(np.sum(sigma))

    psi = 1.0 + ext
    alpha = (1.0 - ext) / (1.0 + ext)
    rho = sigma / (2.0 * np.pi * psi**5)
    stress = 0.5 * rho * (1.0 / alpha - 1.0)

    rows: dict[tuple[int, int, int], dict[str, list[float]]] = {}
    for i in range(SIZE):
        for j in range(SIZE):
            for k in range(SIZE):
                if not BAND_MASK[i, j, k]:
                    continue
                key = orbit_key(i, j, k)
                slot = rows.setdefault(key, {"u": [], "k": [], "rho": [], "S": []})
                slot["u"].append(float(ext[i, j, k]) / total_charge)
                slot["k"].append(float(sigma[i, j, k]) / total_charge)
                slot["rho"].append(float(rho[i, j, k]))
                slot["S"].append(float(stress[i, j, k]))

    max_spreads = {}
    max_rel_spreads = {}
    for field in ["u", "k", "rho", "S"]:
        spreads = [float(np.max(vals[field]) - np.min(vals[field])) for vals in rows.values()]
        means = [float(np.mean(vals[field])) for vals in rows.values()]
        max_spreads[field] = max(spreads)
        max_rel_spreads[field] = max(
            s / max(abs(m), 1e-12) for s, m in zip(spreads, means)
        )
    return max_spreads, max_rel_spreads


def main() -> None:
    print("Pointwise whole-shell bridge law on exact local O_h source class")
    print("=" * 72)

    oh_abs, oh_rel = pointwise_orbit_spreads(same_source.build_best_phi_grid())
    fr_abs, fr_rel = pointwise_orbit_spreads(coarse.build_finite_rank_phi_grid())

    print(
        "exact local O_h max orbit spreads: "
        + ", ".join(f"{k}={v:.3e}" for k, v in oh_abs.items())
    )
    print(
        "finite-rank max orbit spreads: "
        + ", ".join(f"{k}={v:.3e}" for k, v in fr_abs.items())
    )
    print(
        "finite-rank max relative orbit spreads: "
        + ", ".join(f"{k}={100*v:.4f}%" for k, v in fr_rel.items())
    )

    record(
        "on the exact local O_h source class the exterior projector profile is pointwise exact on each orbit",
        oh_abs["u"] < 1e-12 and oh_abs["k"] < 1e-12,
        f"max spreads: u={oh_abs['u']:.3e}, k={oh_abs['k']:.3e}",
    )
    record(
        "on the exact local O_h source class the bridge density and stress-trace are pointwise exact on each orbit",
        oh_abs["rho"] < 1e-12 and oh_abs["S"] < 1e-12,
        f"max spreads: rho={oh_abs['rho']:.3e}, S={oh_abs['S']:.3e}",
    )
    record(
        "on the broader finite-rank family the remaining pointwise whole-shell correction stays small",
        fr_rel["u"] < 0.015 and fr_rel["k"] < 0.017 and fr_rel["rho"] < 0.015 and fr_rel["S"] < 0.027,
        (
            f"relative spreads: u={100*fr_rel['u']:.4f}%, k={100*fr_rel['k']:.4f}%, "
            f"rho={100*fr_rel['rho']:.4f}%, S={100*fr_rel['S']:.4f}%"
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
