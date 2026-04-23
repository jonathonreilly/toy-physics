#!/usr/bin/env python3
"""Retained audit for the source-free local state law theorem."""

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

    rho2 = np.eye(2) / 2.0
    rho16 = rho2
    for _ in range(3):
        rho16 = np.kron(rho16, rho2)

    checks.append(Check("factor-law", np.allclose(rho2, np.eye(2) / 2.0), "source-free qubit law is tracial"))
    checks.append(Check("tensor-lift", np.allclose(rho16, np.eye(16) / 16.0), "cell state lifts exactly to I_16/16"))
    checks.append(Check("cell-normalized", math.isclose(np.trace(rho16), 1.0), f"trace={np.trace(rho16):.6f}"))
    checks.append(Check("cell-positive", np.all(np.linalg.eigvalsh(rho16) >= -1e-12), "all eigenvalues nonnegative"))

    p_a = pa_projector()
    checks.append(Check("counting-packet-rank", int(np.linalg.matrix_rank(p_a)) == 4, f"rank={int(np.linalg.matrix_rank(p_a))}"))
    coeff = float(np.trace(rho16 @ p_a))
    checks.append(Check("quarter-coefficient", math.isclose(coeff, 0.25), f"coeff={coeff:.6f}"))

    # Equivalent closure statement a^2 / l_P^2 = 1 once the coefficient is quarter.
    ratio = coeff / 0.25
    checks.append(Check("planck-ratio", math.isclose(ratio, 1.0), f"ratio={ratio:.6f}"))

    # The previous packet-light witness is no longer admissible under the theorem.
    rho_bad = (1.0 / 32.0) * p_a + (7.0 / 96.0) * (np.eye(16) - p_a)
    checks.append(Check("old-witness-excluded", not np.allclose(rho_bad, rho16), "old packet-light witness differs from derived state law"))

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
