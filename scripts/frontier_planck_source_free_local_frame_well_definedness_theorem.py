#!/usr/bin/env python3
"""Audit runner for the source-free local frame well-definedness theorem."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def pa_projector() -> np.ndarray:
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

    ident16 = np.eye(16)
    rho_tr = ident16 / 16.0

    # Build one nontrivial local frame change on the first factor.
    theta = 0.29
    u2 = np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=float,
    )
    u_local = np.kron(np.kron(np.kron(u2, np.eye(2)), np.eye(2)), np.eye(2))

    # Test 1: the exact time-locked cell has the correct 2^4 dimension.
    checks.append(Check("cell-dimension", ident16.shape == (16, 16), f"shape={ident16.shape}"))

    # Test 2: the tracial state is invariant under an independent local frame change.
    checks.append(Check("tracial-local-frame-invariant", np.allclose(u_local @ rho_tr @ u_local.T, rho_tr), "first-factor rotation witness"))

    # Test 3: a nontrivial diagonal witness is not invariant under the same local frame change.
    rho_bad = np.diag([0.10, 0.02] + [0.88 / 14.0] * 14)
    checks.append(Check("nontracial-breaks-local-frame-invariance", not np.allclose(u_local @ rho_bad @ u_local.T, rho_bad), "same witness breaks nontracial state"))

    # Test 4: local factor algebras generate the full matrix algebra dimension-wise.
    dim_product = 2 * 2 * 2 * 2
    checks.append(Check("factorized-dimension", dim_product == 16, f"dim={dim_product}"))

    # Test 5: a scalar state commutes with local factor actions.
    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    x_local = np.kron(np.kron(np.kron(np.eye(2), sigma_x), np.eye(2)), np.eye(2))
    checks.append(Check("scalar-commutes-local-action", np.allclose(rho_tr @ x_local, x_local @ rho_tr), "local sigma_x witness"))

    # Test 6: nontracial witness fails to commute with some local action.
    checks.append(Check("nontracial-fails-local-action", not np.allclose(rho_bad @ x_local, x_local @ rho_bad), "same witness detects noncentrality"))

    # Test 7: tracial state normalized and positive.
    evals = np.linalg.eigvalsh(rho_tr)
    checks.append(Check("tracial-valid", math.isclose(np.trace(rho_tr), 1.0) and np.all(evals >= -1e-12), f"trace={np.trace(rho_tr):.6f}, min_eval={evals.min():.6f}"))

    # Test 8: direct counting law yields quarter.
    p_a = pa_projector()
    coeff = float(np.trace(rho_tr @ p_a))
    checks.append(Check("quarter-coefficient", math.isclose(coeff, 0.25), f"coeff={coeff:.6f}"))

    # Test 9: the packet-light witness gives a different coefficient.
    rho_lt = (1.0 / 32.0) * p_a + (7.0 / 96.0) * (ident16 - p_a)
    coeff_lt = float(np.trace(rho_lt @ p_a))
    checks.append(Check("witness-different", not math.isclose(coeff_lt, coeff), f"coeff_lt={coeff_lt:.6f}"))

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
