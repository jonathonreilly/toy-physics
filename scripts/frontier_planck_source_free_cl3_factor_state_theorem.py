#!/usr/bin/env python3
"""Audit runner for the source-free Cl(3) factor state theorem."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    checks: list[Check] = []

    i2 = np.eye(2)
    rho = i2 / 2.0

    # Witness inner automorphism.
    theta = 0.38
    u = np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=float,
    )

    checks.append(Check("tracial-normalized", math.isclose(np.trace(rho), 1.0), f"trace={np.trace(rho):.6f}"))
    checks.append(Check("tracial-positive", np.all(np.linalg.eigvalsh(rho) >= -1e-12), f"min_eval={np.linalg.eigvalsh(rho).min():.6f}"))
    checks.append(Check("tracial-inner-invariant", np.allclose(u @ rho @ u.T, rho), "rotation witness"))

    rho_bad = np.diag([0.7, 0.3])
    checks.append(Check("nontracial-breaks-inner-invariance", not np.allclose(u @ rho_bad @ u.T, rho_bad), "same witness breaks nontracial state"))

    sigma_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    checks.append(Check("tracial-commutes-full-m2-witness", np.allclose(rho @ sigma_x, sigma_x @ rho), "sigma_x witness"))
    checks.append(Check("nontracial-not-central", not np.allclose(rho_bad @ sigma_x, sigma_x @ rho_bad), "same witness detects noncentrality"))

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
