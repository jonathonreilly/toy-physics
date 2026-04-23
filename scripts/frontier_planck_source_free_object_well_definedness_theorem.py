#!/usr/bin/env python3
"""Audit runner for the source-free object well-definedness theorem."""

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

    # Independent factor-preserving automorphism witness.
    th1, th2 = 0.23, 0.41
    u1 = np.array([[math.cos(th1), -math.sin(th1)], [math.sin(th1), math.cos(th1)]], dtype=float)
    u2 = np.array([[math.cos(th2), -math.sin(th2)], [math.sin(th2), math.cos(th2)]], dtype=float)
    U = np.kron(np.kron(np.kron(u1, u2), np.eye(2)), np.eye(2))

    checks.append(Check("tracial-object-invariant", np.allclose(U @ rho_tr @ U.T, rho_tr), "independent factor basis changes"))

    rho_bad = np.diag([0.10, 0.02] + [0.88 / 14.0] * 14)
    checks.append(Check("nontracial-breaks-object-invariance", not np.allclose(U @ rho_bad @ U.T, rho_bad), "same witness breaks nontracial state"))

    checks.append(Check("cell-normalized", math.isclose(np.trace(rho_tr), 1.0), f"trace={np.trace(rho_tr):.6f}"))
    checks.append(Check("cell-positive", np.all(np.linalg.eigvalsh(rho_tr) >= -1e-12), f"min_eval={np.linalg.eigvalsh(rho_tr).min():.6f}"))

    p_a = pa_projector()
    coeff = float(np.trace(rho_tr @ p_a))
    checks.append(Check("quarter-coefficient", math.isclose(coeff, 0.25), f"coeff={coeff:.6f}"))
    checks.append(Check("packet-rank", int(np.linalg.matrix_rank(p_a)) == 4, f"rank={int(np.linalg.matrix_rank(p_a))}"))

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
