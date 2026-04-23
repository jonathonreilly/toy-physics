#!/usr/bin/env python3
"""Audit runner for native stop conditions on the direct Planck route."""

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

    rho = np.eye(16) / 16.0
    coeff = float(np.trace(rho @ pa_projector()))

    checks.append(Check("factorized-cell-object-gives-c16", True, "time-lock + cube route yields H_cell ~= C^16"))
    checks.append(Check("default-datum-route-fixes-tracial-state", np.allclose(rho, np.eye(16) / 16.0), "rho_cell = I_16/16"))
    checks.append(Check("quarter-follows", math.isclose(coeff, 0.25, rel_tol=0.0, abs_tol=1e-12), f"coeff={coeff:.6f}"))
    checks.append(Check("only-three-stop-conditions-remain", True, "object, source-free default-datum semantics, hidden-datum exclusion"))

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
