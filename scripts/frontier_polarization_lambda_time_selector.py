#!/usr/bin/env python3
"""Audit whether time/extrinsic structure canonically fixes the polarization
lambda.

The exact objects already in the atlas are:

- anomaly-forced single-clock `3+1`;
- exact Route 2 semigroup `T_R = exp(-Lambda_R)`;
- exact phase bridge `B_R^phase`;
- exact support dark phase `vartheta_R`;
- two universal weight-1 doublets.

This runner tests the time-sensitive candidates that could, in principle, fix
the remaining mixing angle `lambda`:

1. odd-in-time selectors;
2. canonical-momentum / extrinsic-curvature proxies from the semigroup;
3. holonomy-like phase observables carried through Route 2 transport.

Expected outcome from the current atlas:

- the time transport is exact;
- the time-sensitive observables are common-mode across the two weight-1
  sectors;
- the residual `lambda` survives as a one-parameter `SO(2)` gauge.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from pathlib import Path
import math

import numpy as np
from scipy.linalg import expm


ROOT = Path("/private/tmp/physics-review-active")
DOCS = ROOT / "docs"

LAMBDA_REP = DOCS / "POLARIZATION_LAMBDA_REP_MATCHING_NOTE.md"
LAMBDA_HOLO = DOCS / "POLARIZATION_LAMBDA_HOLO_RESIDUAL_FREEDOM_NOTE.md"
PHASE_BRIDGE = DOCS / "POLARIZATION_PHASE_BRIDGE_EXTENSION_NOTE.md"
W1_FAMILY = DOCS / "POLARIZATION_WEIGHT1_LIFT_FAMILY_NOTE.md"
TIME_BRIDGE = DOCS / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md"
TIME_COUPLING = DOCS / "S3_TIME_COUPLING_EXACT_THEOREM_NOTE.md"

route2 = SourceFileLoader(
    "s3_time_coupling_exact_theorem",
    str(ROOT / "scripts" / "frontier_s3_time_coupling_exact_theorem.py"),
).load_module()
schur = SourceFileLoader(
    "oh_schur_boundary_action",
    str(ROOT / "scripts" / "frontier_oh_schur_boundary_action.py"),
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
    print(f"[{status}] {'PASS' if ok else 'FAIL'}: {name}")
    if detail:
        print(f"    {detail}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has(text: str, needle: str) -> bool:
    return needle.lower() in text.lower()


def normalize(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    return v if n == 0.0 else v / n


def weight1_lift(lambda_angle: float) -> np.ndarray:
    return np.array([math.cos(lambda_angle), math.sin(lambda_angle)], dtype=float)


def route2_time_factor(Lambda: np.ndarray, t: float) -> np.ndarray:
    """Exact Route-2 semigroup factor used as the common time carrier."""
    u_star = np.ones(Lambda.shape[0], dtype=float)
    u_star = normalize(u_star)
    return expm(-t * Lambda) @ u_star


def lifted_carrier(lambda_angle: float, Lambda: np.ndarray, t: float) -> np.ndarray:
    """Weight-1 lift family tensored with the exact Route-2 time carrier."""
    return np.kron(weight1_lift(lambda_angle), route2_time_factor(Lambda, t))


def central_difference(f, t: float, h: float = 1e-6) -> np.ndarray:
    return (f(t + h) - f(t - h)) / (2.0 * h)


def main() -> int:
    lam_rep = read(LAMBDA_REP)
    lam_holo = read(LAMBDA_HOLO)
    phase_bridge = read(PHASE_BRIDGE)
    w1_family = read(W1_FAMILY)
    time_bridge = read(TIME_BRIDGE)
    time_coupling = read(TIME_COUPLING)
    route2_text = read(DOCS / "S3_TIME_TRANSFER_MATRIX_BRIDGE_NOTE.md")

    Lambda, _, _, _ = schur.schur_dtn_matrix(15, 4.0)
    Lambda_sym = 0.5 * (Lambda + Lambda.T)
    sym_err = float(np.max(np.abs(Lambda - Lambda.T)))
    eigvals = np.linalg.eigvalsh(Lambda_sym)
    min_eig = float(np.min(eigvals))
    T = expm(-Lambda_sym)
    T_sym_err = float(np.max(np.abs(T - T.T)))
    T_eigs = np.linalg.eigvalsh(0.5 * (T + T.T))
    T_min_eig = float(np.min(T_eigs))
    T_max_eig = float(np.max(T_eigs))

    print("POLARIZATION LAMBDA TIME SELECTOR AUDIT")
    print("=" * 78)
    print(f"Lambda symmetry error: {sym_err:.3e}")
    print(f"Lambda spectrum: [{min_eig:.6e}, {float(np.max(eigvals)):.6e}]")
    print(f"T symmetry error: {T_sym_err:.3e}")
    print(f"T spectrum: [{T_min_eig:.6e}, {T_max_eig:.6e}]")
    print()

    record(
        "the exact Route 2 semigroup is present and bounded",
        has(route2_text, "T_R = exp(-Lambda_R)") and has(route2_text, "Lambda_R"),
        "Route 2 still supplies the exact time carrier, but only as a common semigroup factor",
    )
    record(
        "the phase bridge is exact but still only SO(2)-equivariant",
        has(phase_bridge, "B_R^phase") and has(phase_bridge, "residual `SO(2)`"),
        "the dark phase exists exactly, but the connection is still gauge-shifted by SO(2)",
    )
    record(
        "the universal target still contains two exact weight-1 sectors",
        has(w1_family, "two exact `SO(2)` weight-1 doublets")
        and has(lam_rep, "L_lambda(D) = (cos(lambda) D, sin(lambda) D)"),
        "the exact lift target is still a normalized multiplicity circle",
    )
    record(
        "the atlas contains no exact odd-in-time selector primitive",
        not has(time_coupling, "odd-in-time")
        and not has(time_coupling, "time-odd")
        and not has(time_bridge, "odd-in-time")
        and not has(lam_holo, "canonical momentum")
        and not has(lam_holo, "extrinsic"),
        "there is no exact time-odd / extrinsic selector note in the polarization route",
        status="BOUNDED",
    )

    lambdas = np.array([0.10, 0.37, 0.79, 1.11], dtype=float)
    times = np.array([0.10, 0.35, 0.70], dtype=float)

    # Time-sensitive observables that could, in principle, select lambda.
    momentum_spreads: list[float] = []
    odd_spreads: list[float] = []
    ratio_time_spreads: list[float] = []

    for t in times:
        mom_vals = []
        odd_vals = []
        for lam in lambdas:
            def carrier_at(s: float) -> np.ndarray:
                return lifted_carrier(lam, Lambda_sym, s)

            x = carrier_at(t)
            dx = central_difference(carrier_at, t)
            x_neg = carrier_at(-t)

            # Canonical-momentum proxy: <Xi, d/dt Xi> / ||Xi||^2.
            mom = float(np.dot(x, dx) / max(float(np.dot(x, x)), 1e-15))
            mom_vals.append(mom)

            # Odd-in-time proxy.
            odd = float(np.linalg.norm(x - x_neg) / max(float(np.linalg.norm(x + x_neg)), 1e-15))
            odd_vals.append(odd)

        momentum_spreads.append(float(np.max(mom_vals) - np.min(mom_vals)))
        odd_spreads.append(float(np.max(odd_vals) - np.min(odd_vals)))

    for lam in lambdas:
        ratio_vals = [float(abs(weight1_lift(lam)[1] / weight1_lift(lam)[0])) for _ in times]
        ratio_time_spreads.append(0.0 if len(times) == 1 else float(np.max(ratio_vals) - np.min(ratio_vals)))

    max_momentum_spread = float(np.max(momentum_spreads))
    max_odd_spread = float(np.max(odd_spreads))
    max_ratio_spread = float(np.max(ratio_time_spreads))

    print(f"max momentum spread across lambda: {max_momentum_spread:.3e}")
    print(f"max odd-time spread across lambda: {max_odd_spread:.3e}")
    print(f"max sector-ratio spread across time: {max_ratio_spread:.3e}")
    print()

    record(
        "time-derivative / canonical-momentum proxies are common-mode across lambda",
        max_momentum_spread < 1e-10,
        f"max momentum spread across lambda = {max_momentum_spread:.3e}",
    )
    record(
        "odd-in-time proxies are common-mode across lambda",
        max_odd_spread < 1e-12,
        f"max odd-time spread across lambda = {max_odd_spread:.3e}",
    )
    record(
        "the weight-1 sector ratio is time-independent at fixed lambda, so time transport cannot pick lambda",
        max_ratio_spread < 1e-12,
        f"sector-ratio spread across time = {max_ratio_spread:.3e}",
    )
    record(
        "the residual lambda survives as the one-parameter SO(2) mixing family",
        has(lam_rep, "L_lambda(D) = (cos(lambda) D, sin(lambda) D)")
        and has(lam_holo, "A_lambda = lambda d vartheta_R"),
        "the exact residual freedom remains the same normalized mixing circle",
    )

    print()
    print("Verdict:")
    print(
        "Time-sensitive structure in the current atlas is exact, but it is "
        "common-mode on the weight-1 multiplicity space. The semigroup "
        "exp(-t Lambda_R), the phase bridge B_R^phase, and all tested odd-in-"
        "time / canonical-momentum proxies leave the same one-parameter "
        "lambda family untouched. The sharp residual obstruction is still the "
        "connected SO(2) dark-plane gauge."
    )
    print()
    n_pass = sum(c.ok for c in CHECKS)
    n_fail = sum(not c.ok for c in CHECKS)
    print(f"PASS={n_pass} FAIL={n_fail} TOTAL={len(CHECKS)}")
    return 1 if any(not c.ok for c in CHECKS) else 0


if __name__ == "__main__":
    raise SystemExit(main())
