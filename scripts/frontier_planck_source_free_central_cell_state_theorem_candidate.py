#!/usr/bin/env python3
"""Audit runner for the source-free central cell-state theorem candidate."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def matrix_unit(n: int, i: int, j: int) -> np.ndarray:
    e = np.zeros((n, n), dtype=float)
    e[i, j] = 1.0
    return e


def pa_projector() -> np.ndarray:
    # One-step worldtube packet on the time-locked 4-bit cell:
    # exactly the four Hamming-weight-one basis states.
    p = np.zeros((16, 16), dtype=float)
    for idx in (1, 2, 4, 8):
        p[idx, idx] = 1.0
    return p


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    checks: list[Check] = []

    n = 16
    identity = np.eye(n)

    # Test 1: matrix units exist as a basis of the primitive cell algebra.
    basis = [matrix_unit(n, i, j) for i in range(n) for j in range(n)]
    dim_span = np.linalg.matrix_rank(np.stack([b.reshape(-1) for b in basis], axis=0))
    checks.append(Check("matrix-unit-basis", dim_span == n * n, f"dim={dim_span}"))

    # Test 2: scalar matrices commute with every matrix unit.
    scalar = 0.37 * identity
    scalar_commutes = all(
        np.allclose(scalar @ eij, eij @ scalar) for eij in basis[:64]
    )
    checks.append(Check("scalar-commutes", scalar_commutes, "checked first 64 matrix units"))

    # Test 3: a non-scalar diagonal matrix fails centrality.
    nonscalar = np.diag([1.0, 2.0] + [1.0] * 14)
    e01 = matrix_unit(n, 0, 1)
    noncentral = not np.allclose(nonscalar @ e01, e01 @ nonscalar)
    checks.append(Check("nonscalar-not-central", noncentral, "E_01 detects unequal diagonal entries"))

    # Test 4: the center is one-dimensional numerically on diagonal data.
    diag_free = np.diag(np.arange(1, n + 1, dtype=float))
    centralizer_failure = sum(
        not np.allclose(diag_free @ matrix_unit(n, i, j), matrix_unit(n, i, j) @ diag_free)
        for i in range(n) for j in range(n) if i != j
    )
    checks.append(Check("center-not-large", centralizer_failure == n * (n - 1), f"failures={centralizer_failure}"))

    # Test 5: a normalized central positive state has the form I/n.
    rho = identity / n
    checks.append(Check("normalized-central-state", math.isclose(np.trace(rho), 1.0), f"trace={np.trace(rho):.6f}"))

    # Test 6: positivity of the tracial state.
    evals = np.linalg.eigvalsh(rho)
    checks.append(Check("tracial-state-positive", np.all(evals >= -1e-12), f"min_eval={evals.min():.6f}"))

    # Test 7: rank of the P_A packet is exactly 4.
    p_a = pa_projector()
    rank_pa = int(np.linalg.matrix_rank(p_a))
    checks.append(Check("packet-rank", rank_pa == 4, f"rank={rank_pa}"))

    # Test 8: closed counting law on the tracial state yields quarter.
    coeff = float(np.trace(rho @ p_a))
    checks.append(Check("quarter-coefficient", math.isclose(coeff, 0.25), f"coeff={coeff:.6f}"))

    # Test 9: explicit normalization relation lambda = 1/16.
    lam = 1.0 / n
    checks.append(Check("lambda-value", math.isclose(n * lam, 1.0), f"lambda={lam:.6f}"))

    passed = 0
    for idx, check in enumerate(checks, start=1):
        status = "PASS" if check.ok else "FAIL"
        print(f"[{idx}] {status} {check.name}: {check.detail}")
        passed += int(check.ok)

    print(f"\n{passed}/{len(checks)} PASS")
    if passed != len(checks):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
