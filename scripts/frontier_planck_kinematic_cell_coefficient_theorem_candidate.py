#!/usr/bin/env python3
"""Audit runner for the kinematic cell-coefficient theorem candidate."""

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
    p_a = pa_projector()

    rho_tr = np.eye(16) / 16.0
    rho_lt = np.diag([1.0 / 32.0 if i in (1, 2, 4, 8) else 7.0 / 96.0 for i in range(16)])

    coeff_tr = float(np.trace(rho_tr @ p_a))
    coeff_lt = float(np.trace(rho_lt @ p_a))
    p_vac = 0.25 * math.log(5.0 / 3.0)

    checks.append(
        Check(
            "count-operator-is-fixed",
            int(np.linalg.matrix_rank(p_a)) == 4,
            f"rank(P_A)={int(np.linalg.matrix_rank(p_a))}",
        )
    )
    checks.append(
        Check(
            "state-choice-changes-value",
            not math.isclose(coeff_tr, coeff_lt, rel_tol=0.0, abs_tol=1e-12),
            f"coeff_tr={coeff_tr:.6f}, coeff_lt={coeff_lt:.6f}",
        )
    )
    checks.append(
        Check(
            "tracial-default-gives-quarter",
            math.isclose(coeff_tr, 0.25, rel_tol=0.0, abs_tol=1e-12),
            f"coeff_tr={coeff_tr:.6f}",
        )
    )
    checks.append(
        Check(
            "scalar-vacuum-control-is-different",
            not math.isclose(p_vac, 0.25, rel_tol=0.0, abs_tol=1e-12),
            f"p_vac={p_vac:.6f}",
        )
    )
    checks.append(
        Check(
            "kinematic-vs-vacuum-class-distinction-visible",
            not math.isclose(p_vac, coeff_tr, rel_tol=0.0, abs_tol=1e-12),
            f"p_vac={p_vac:.6f}, coeff_tr={coeff_tr:.6f}",
        )
    )

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
