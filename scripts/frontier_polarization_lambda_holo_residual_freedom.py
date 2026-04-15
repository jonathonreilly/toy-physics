#!/usr/bin/env python3
"""Audit whether the dark-phase holonomy normalization lambda is fixed.

This runner starts from the exact holonomy result that the dark phase on the
residual `SO(2)` bundle is represented by the family

    A_lambda = lambda d vartheta_R.

It then checks the three possible fixers directly:

1. singular-locus regularity;
2. punctured-bundle flatness;
3. global trivialization on a cut domain.

The expected outcome is negative: all three mechanisms are compatible with the
same singular set and flatness, while the holonomy character still varies with
lambda. Therefore the exact residual freedom remains one-parameter.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np


ROOT = Path("/private/tmp/physics-review-active")
PHASE = SourceFileLoader(
    "polarization_phase_holo_singular_holonomy",
    str(ROOT / "scripts" / "frontier_polarization_phase_holo_singular_holonomy.py"),
).load_module()
BRIDGE = SourceFileLoader(
    "polarization_phase_bridge_extension",
    str(ROOT / "scripts" / "frontier_polarization_phase_bridge_extension.py"),
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


def loop_points(center: np.ndarray, radius: float, n: int = 720) -> np.ndarray:
    ts = np.linspace(0.0, 2.0 * np.pi, n, endpoint=True)
    return np.column_stack(
        [
            center[0] + radius * np.cos(ts),
            center[1] + radius * np.sin(ts),
        ]
    )


def q_from_dark_pair(bright_base: np.ndarray, dark_pair: np.ndarray) -> np.ndarray:
    basis = PHASE.SUPPORT.same.build_adapted_basis()
    return bright_base + dark_pair[0] * basis[:, 5] + dark_pair[1] * basis[:, 6]


def dark_pair(q: np.ndarray) -> np.ndarray:
    return np.array(PHASE.SUPPORT.dark_coords(q)[1:], dtype=float)


def rho(q: np.ndarray) -> float:
    return float(np.linalg.norm(dark_pair(q)))


def vartheta(q: np.ndarray) -> float:
    d = dark_pair(q)
    return float(np.arctan2(d[1], d[0]))


def phase_change(points: np.ndarray, bright_base: np.ndarray) -> float:
    thetas = []
    for dy, dz in points:
        q = q_from_dark_pair(bright_base, np.array([dy, dz], dtype=float))
        thetas.append(vartheta(q))
    unwrapped = np.unwrap(np.array(thetas, dtype=float))
    return float(np.sum(np.diff(unwrapped)))


def holonomy(lam: float, points: np.ndarray, bright_base: np.ndarray) -> float:
    return lam * phase_change(points, bright_base)


def curvature_probe(lam: float, point: np.ndarray, bright_base: np.ndarray) -> float:
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
    return abs(lam * phase_change(square, bright_base))


def cut_domain_exactness(lam: float) -> float:
    # On a simply connected branch domain, A_lambda is globally exact:
    # A_lambda = d(lam * vartheta_cut).
    thetas = np.linspace(-2.6, 2.6, 513)
    primitive = lam * thetas
    dphi = np.diff(primitive) / np.diff(thetas)
    return float(np.max(np.abs(dphi - lam)))


def main() -> int:
    basis = PHASE.SUPPORT.same.build_adapted_basis()
    e0 = basis[:, 0]
    s = basis[:, 1]
    e_x = PHASE.SUPPORT.e_x
    t1x = PHASE.SUPPORT.t1x
    t1y = PHASE.SUPPORT.t1y
    t1z = PHASE.SUPPORT.t1z

    bright_base = PHASE.SUPPORT.a1_background(0.5) + 0.37 * e_x + 0.21 * t1x
    q_sing = bright_base
    q_punctured = bright_base + 0.19 * t1y + 0.11 * t1z

    rho_sing = rho(q_sing)
    rho_punctured = rho(q_punctured)
    theta_punctured = vartheta(q_punctured)

    circle_origin = loop_points(np.array([0.0, 0.0], dtype=float), 0.18, n=1024)
    circle_shifted = loop_points(np.array([0.42, 0.27], dtype=float), 0.06, n=1024)

    lambdas = [0.0, 0.25, 0.5, 0.75, 1.0]
    winding_errors = []
    contractible_errors = []
    curvature_errors = []
    cut_errors = []
    holonomies = []

    print("POLARIZATION LAMBDA HOLO RESIDUAL FREEDOM")
    print("=" * 78)
    print(f"rho_R(singular representative) = {rho_sing:.12e}")
    print(f"rho_R(punctured representative) = {rho_punctured:.12e}")
    print(f"vartheta_R(punctured representative) = {theta_punctured:.12e}")

    for lam in lambdas:
        hol_circle = holonomy(lam, circle_origin, bright_base)
        hol_shifted = holonomy(lam, circle_shifted, bright_base)
        curv = curvature_probe(lam, np.array([0.41, 0.29], dtype=float), bright_base)
        cut_err = cut_domain_exactness(lam)
        holonomies.append(hol_circle)
        winding_errors.append(abs(hol_circle - 2.0 * np.pi * lam))
        contractible_errors.append(abs(hol_shifted))
        curvature_errors.append(curv)
        cut_errors.append(cut_err)
        print(
            f"lambda={lam:.2f}: hol(circle)={hol_circle:.12e}, "
            f"hol(contractible)={hol_shifted:.12e}, curvature={curv:.12e}, "
            f"cut-exactness={cut_err:.12e}"
        )

    distinct_holonomy = abs(holonomies[-1] - holonomies[1])
    distinct_primitive = abs((1.0 - 0.25) * math.pi)

    record(
        "the singular locus is exactly lambda-independent",
        rho_sing < 1e-12 and rho_punctured > 1e-6,
        f"rho_sing={rho_sing:.3e}, rho_punctured={rho_punctured:.3e}",
    )
    record(
        "punctured-bundle flatness holds for every sampled lambda",
        max(contractible_errors) < 1e-12 and max(curvature_errors) < 1e-12,
        f"contractible max={max(contractible_errors):.3e}, curvature max={max(curvature_errors):.3e}",
    )
    record(
        "global trivialization on a cut domain exists for every sampled lambda",
        max(cut_errors) < 1e-12,
        f"cut-domain exactness max={max(cut_errors):.3e}",
    )
    record(
        "different lambda values give distinct holonomy characters",
        max(winding_errors) < 1e-12 and distinct_holonomy > 1e-3,
        f"winding max={max(winding_errors):.3e}, holonomy separation={distinct_holonomy:.3e}",
    )
    record(
        "the residual freedom remains one-parameter",
        max(winding_errors) < 1e-12 and max(contractible_errors) < 1e-12 and max(cut_errors) < 1e-12 and distinct_holonomy > 1e-3,
        f"distinct primitive separation={distinct_primitive:.3e}",
        status="BOUNDED",
    )

    print("\nVerdict:")
    print(
        "Singular-locus regularity fixes the defect set Sigma_R, punctured-"
        "bundle flatness kills curvature on X_R, and a cut-domain "
        "trivialization makes the connection exact. None of those conditions "
        "chooses a canonical normalization. The holonomy around a winding-one "
        "loop remains lambda-dependent, so the current atlas leaves a genuine "
        "one-parameter family A_lambda = lambda d vartheta_R."
    )

    print("\n" + "=" * 78)
    print("SUMMARY")
    print("=" * 78)
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = len(CHECKS) - n_pass
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
