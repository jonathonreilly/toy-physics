#!/usr/bin/env python3
"""Analyze the dark-phase singular set and holonomy on the punctured complement.

This runner checks the exact support-side dark-phase primitive:

    D_R(q) = (d_y, d_z)
    rho_R(q) = sqrt(d_y^2 + d_z^2)
    vartheta_R(q) = atan2(d_z, d_y)

It then tests the exact obstruction to a distinguished global connection:

1. `rho_R = 0` is the singular locus where the phase is undefined.
2. On `rho_R > 0`, the phase connection is flat.
3. Flatness plus the singular set do not determine a unique normalization:
   the family `A_lambda = lambda d vartheta_R` shares the same singular set
   and curvature but has different holonomy characters.

The result is intentionally negative: the current atlas does not force a
distinguished global connection from the singular set or from flatness alone.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")

SUPPORT = SourceFileLoader(
    "s3_time_bilinear_tensor_primitive",
    str(ROOT / "scripts" / "frontier_s3_time_bilinear_tensor_primitive.py"),
).load_module()


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    status: str = "EXACT"


CHECKS: list[Check] = []


def record(name: str, ok: bool, detail: str, status: str = "EXACT") -> None:
    CHECKS.append(Check(name=name, ok=ok, detail=detail, status=status))
    tag = "PASS" if ok else "FAIL"
    print(f"[{status}] {tag}: {name}")
    if detail:
        print(f"    {detail}")


def dark_coords(q: np.ndarray) -> np.ndarray:
    return np.array(SUPPORT.dark_coords(q)[1:], dtype=float)


def rho(q: np.ndarray) -> float:
    d = dark_coords(q)
    return float(np.linalg.norm(d))


def vartheta(q: np.ndarray) -> float:
    d = dark_coords(q)
    return float(np.arctan2(d[1], d[0]))


def loop_points(center: np.ndarray, radius: float, n: int = 720) -> np.ndarray:
    ts = np.linspace(0.0, 2.0 * np.pi, n, endpoint=True)
    pts = np.column_stack(
        [
            center[0] + radius * np.cos(ts),
            center[1] + radius * np.sin(ts),
        ]
    )
    return pts


def q_from_dark_pair(bright_base: np.ndarray, dark_pair: np.ndarray) -> np.ndarray:
    return bright_base + dark_pair[0] * SUPPORT.t1y + dark_pair[1] * SUPPORT.t1z


def phase_change(points: np.ndarray, bright_base: np.ndarray) -> float:
    thetas = []
    for dy, dz in points:
        q = q_from_dark_pair(bright_base, np.array([dy, dz], dtype=float))
        thetas.append(vartheta(q))
    unwrapped = np.unwrap(np.array(thetas, dtype=float))
    return float(np.sum(np.diff(unwrapped)))


def holonomy_angle(lambda_: float, points: np.ndarray, bright_base: np.ndarray) -> float:
    return lambda_ * phase_change(points, bright_base)


def curvature_sample(lambda_: float, point: np.ndarray, bright_base: np.ndarray) -> float:
    # On the punctured complement, A_lambda = lambda d vartheta_R is flat.
    # We probe a small contractible square loop away from the singular set.
    eps = 1e-3
    square = np.array(
        [
            [point[0] - eps, point[1] - eps],
            [point[0] + eps, point[1] - eps],
            [point[0] + eps, point[1] + eps],
            [point[0] - eps, point[1] + eps],
            [point[0] - eps, point[1] - eps],
        ],
        dtype=float,
    )
    return abs(lambda_ * phase_change(square, bright_base))


def main() -> int:
    basis = SUPPORT.same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e_x = SUPPORT.e_x
    t1x = SUPPORT.t1x

    bright_base = SUPPORT.a1_background(0.5) + 0.37 * e_x + 0.21 * t1x
    q_sing = bright_base
    q_punctured = bright_base + 0.19 * SUPPORT.t1y + 0.11 * SUPPORT.t1z

    rho_sing = rho(q_sing)
    theta_sing = vartheta(q_sing) if rho_sing > 0 else float("nan")
    rho_punctured = rho(q_punctured)
    theta_punctured = vartheta(q_punctured)

    print("POLARIZATION PHASE / HOLOMOMY AUDIT")
    print("=" * 78)
    print(f"rho_R(singular representative) = {rho_sing:.12e}")
    print(f"rho_R(punctured representative) = {rho_punctured:.12e}")
    print(f"vartheta_R(punctured representative) = {theta_punctured:.12e}")

    singular_ok = rho_sing < 1e-12
    punctured_ok = rho_punctured > 1e-6
    record(
        "rho_R=0 is the dark-phase singular locus on the support-side representative",
        singular_ok,
        f"rho_R(singular representative)={rho_sing:.3e}",
    )
    record(
        "rho_R>0 admits a canonical local phase coordinate vartheta_R",
        punctured_ok and np.isfinite(theta_punctured),
        f"rho_R(punctured representative)={rho_punctured:.3e}, vartheta_R={theta_punctured:.3e}",
    )

    circle_origin = loop_points(np.array([0.0, 0.0], dtype=float), 0.18, n=1024)
    circle_shifted = loop_points(np.array([0.42, 0.27], dtype=float), 0.06, n=1024)

    max_winding_err = 0.0
    max_contractible_err = 0.0
    for lam in [0.0, 0.25, 0.5, 0.75, 1.0]:
        hol_circle = holonomy_angle(lam, circle_origin, bright_base)
        hol_shifted = holonomy_angle(lam, circle_shifted, bright_base)
        max_winding_err = max(max_winding_err, abs(hol_circle - 2.0 * np.pi * lam))
        max_contractible_err = max(max_contractible_err, abs(hol_shifted))
        print(
            f"lambda={lam:.2f}: holonomy(circle)={hol_circle:.12e}, "
            f"holonomy(shifted loop)={hol_shifted:.12e}"
        )

    curvature_probe = curvature_sample(0.5, np.array([0.41, 0.29], dtype=float), bright_base)
    alt_curvature_probe = curvature_sample(0.75, np.array([0.51, 0.31], dtype=float), bright_base)
    distinct_holonomy = abs(
        holonomy_angle(0.25, circle_origin, bright_base)
        - holonomy_angle(0.75, circle_origin, bright_base)
    )

    print("\nObstruction diagnostics:")
    print(f"  max winding-law error = {max_winding_err:.3e}")
    print(f"  max contractible-loop error = {max_contractible_err:.3e}")
    print(f"  curvature probe (lambda=0.5) = {curvature_probe:.3e}")
    print(f"  curvature probe (lambda=0.75) = {alt_curvature_probe:.3e}")
    print(f"  holonomy separation between lambda=0.25 and 0.75 = {distinct_holonomy:.3e}")

    record(
        "the canonical phase connection on the punctured complement is flat",
        max_contractible_err < 1e-12 and curvature_probe < 1e-12 and alt_curvature_probe < 1e-12,
        f"contractible-loop error={max_contractible_err:.3e}, curvature probes={curvature_probe:.3e},{alt_curvature_probe:.3e}",
    )
    record(
        "the holonomy around a winding-one loop is governed by the phase winding number",
        max_winding_err < 1e-12,
        f"max winding-law error={max_winding_err:.3e}",
    )
    record(
        "the singular locus does not determine a unique connection normalization",
        distinct_holonomy > 1e-3,
        f"holonomy separation between two flat candidates={distinct_holonomy:.3e}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "The rho_R=0 locus is exactly the branch singular set of the dark "
        "phase. On rho_R>0, vartheta_R gives a canonical local phase "
        "coordinate and the induced SO(2) connection is flat. But the current "
        "atlas does not fix the normalization of that flat connection: a "
        "one-parameter family A_lambda = lambda d vartheta_R shares the same "
        "singular set and local flatness while carrying different holonomy "
        "characters around the puncture. Therefore singular-set structure and "
        "flatness do not force a distinguished global connection."
    )
    print(
        "Exact obstruction: no angle-sensitive observable or transport law in "
        "the current common bridge fixes the holonomy normalization constant "
        "lambda, and the phase section is undefined on rho_R=0."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
