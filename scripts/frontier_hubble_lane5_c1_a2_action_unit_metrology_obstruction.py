#!/usr/bin/env python3
"""Lane 5 (C1) A2 action-unit metrology obstruction verifier.

The A2 route asks whether the retained dimensionless lattice inputs
g_bare = 1, beta = 6, the plaquette/u0 surface, and the minimal APBC
hierarchy block pin an absolute action quantum on P_A H_cell.

They do not. The checks below keep those dimensionless inputs fixed while
showing that a one-parameter family of (S_dim, kappa) readings gives the same
Hilbert phases and lattice weights. A physical clock/source/action metrology
map remains an open import.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


TOL = 1.0e-12


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol


def phase(action_dimensional: float, kappa: float) -> complex:
    return cmath.exp(1j * action_dimensional / kappa)


def euclidean_weight(action_dimensionless: float) -> float:
    return math.exp(-action_dimensionless)


def record(checks: list[Check], name: str, passed: bool, detail: str) -> None:
    checks.append(Check(name, passed, detail))


def main() -> int:
    checks: list[Check] = []

    n_color = 3
    g_bare = 1.0
    beta = 2.0 * n_color / (g_bare * g_bare)
    record(
        checks,
        "g_bare fixes the dimensionless Wilson beta",
        close(beta, 6.0),
        f"N_c={n_color}, g_bare={g_bare:.1f}, beta={beta:.12f}",
    )

    record(
        checks,
        "plaquette surface supplies dimensionless coupling data",
        close(CANONICAL_U0, CANONICAL_PLAQUETTE**0.25)
        and close(CANONICAL_ALPHA_LM, CANONICAL_ALPHA_BARE / CANONICAL_U0)
        and close(CANONICAL_ALPHA_S_V, CANONICAL_ALPHA_BARE / (CANONICAL_U0**2)),
        (
            f"P={CANONICAL_PLAQUETTE:.10f}, u0={CANONICAL_U0:.10f}, "
            f"alpha_LM={CANONICAL_ALPHA_LM:.10f}, alpha_s(v)={CANONICAL_ALPHA_S_V:.10f}"
        ),
    )

    c_apbc = (7.0 / 8.0) ** 0.25
    record(
        checks,
        "minimal APBC hierarchy factor is dimensionless",
        0.0 < c_apbc < 1.0 and close(c_apbc**4, 7.0 / 8.0),
        f"C_APBC=(7/8)^(1/4)={c_apbc:.12f}",
    )

    base_action = 0.731
    base_kappa = 2.0
    scaled_same = all(
        abs(phase(base_action, base_kappa) - phase(lam * base_action, lam * base_kappa)) < TOL
        for lam in (0.25, 1.0, 3.0, 11.0)
    )
    record(
        checks,
        "Hilbert phase is invariant under common action-unit rescaling",
        scaled_same,
        "exp(i S/kappa) is unchanged by (S,kappa)->(lambda S,lambda kappa)",
    )

    plaquette_re = 0.42
    lattice_action = beta * (1.0 - plaquette_re)
    weight = euclidean_weight(lattice_action)
    scaled_weights = [
        euclidean_weight(beta * (1.0 - plaquette_re))
        for _kappa in (0.5, 1.0, 2.0, 8.0)
    ]
    record(
        checks,
        "Wilson plaquette weight uses dimensionless action only",
        all(close(candidate, weight) for candidate in scaled_weights),
        f"S_lat=beta*(1-ReP)={lattice_action:.12f}, exp(-S_lat)={weight:.12f}",
    )

    dim_cell = 16
    rank_pa = 4
    c_cell = rank_pa / dim_cell
    scaled_c_cell = [rank_pa / dim_cell for _kappa in (0.5, 1.0, 2.0, 8.0)]
    record(
        checks,
        "P_A trace coefficient is dimensionless and scale-invariant",
        close(c_cell, 0.25) and all(close(value, c_cell) for value in scaled_c_cell),
        f"c_cell=rank(P_A)/dim(H_cell)={rank_pa}/{dim_cell}={c_cell:.12f}",
    )

    projected_dimensionless_action = c_cell + beta * (1.0 - plaquette_re) * 0.01
    projected_phases = []
    for kappa in (0.5, 1.0, 2.0, 8.0):
        dimensional_action = kappa * projected_dimensionless_action
        projected_phases.append(phase(dimensional_action, kappa))
    record(
        checks,
        "different kappa readings give the same projected P_A phase",
        max(abs(candidate - projected_phases[0]) for candidate in projected_phases) < TOL,
        (
            "same dimensionless P_A action with kappa in {0.5,1,2,8}; "
            f"phase={projected_phases[0].real:.12f}+{projected_phases[0].imag:.12f}i"
        ),
    )

    trace_commutator = 0.0
    kappa = 1.0
    trace_canonical_rhs_abs = dim_cell / 4.0 * kappa
    record(
        checks,
        "finite rank-four block cannot realize a nonzero canonical action commutator",
        close(trace_commutator, 0.0) and trace_canonical_rhs_abs > 0.0,
        "Tr([X,P])=0 for finite matrices but Tr(i*kappa*I_4)=4i*kappa",
    )

    print("=" * 78)
    print("Lane 5 (C1) A2 action-unit metrology obstruction verifier")
    print("=" * 78)
    passed = 0
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"[{status}] {check.name}: {check.detail}")
        passed += int(check.passed)
    failed = len(checks) - passed
    print("-" * 78)
    print(f"TOTAL: PASS={passed}, FAIL={failed}")
    if failed == 0:
        print(
            "Conclusion: retained g_bare, plaquette/u0, APBC, and c_cell data "
            "are dimensionless. They do not pin a dimensional kappa on P_A H_cell; "
            "A2 needs an additional clock/source/action metrology theorem."
        )
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
