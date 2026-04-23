#!/usr/bin/env python3
"""Audit runner for the source-free no-local-information theorem candidate."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def pa_projector() -> np.ndarray:
    p = np.zeros((16, 16), dtype=float)
    for idx in (1, 2, 4, 8):
        p[idx, idx] = 1.0
    return p


def entropy(rho: np.ndarray) -> float:
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 1e-15]
    return float(-np.sum(vals * np.log(vals)))


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    checks: list[Check] = []
    rho_tr = np.eye(16) / 16.0
    rho_bad = np.diag([0.10, 0.02] + [0.88 / 14.0] * 14)

    s_tr = entropy(rho_tr)
    s_bad = entropy(rho_bad)
    i_tr = math.log(16.0) - s_tr
    i_bad = math.log(16.0) - s_bad

    checks.append(Check("tracial-max-entropy", math.isclose(s_tr, math.log(16.0), rel_tol=0.0, abs_tol=1e-12), f"S_tr={s_tr:.12f}"))
    checks.append(Check("tracial-zero-local-information-defect", math.isclose(i_tr, 0.0, rel_tol=0.0, abs_tol=1e-12), f"I_tr={i_tr:.12f}"))
    checks.append(Check("nontracial-positive-local-information-defect", i_bad > 0.0, f"I_bad={i_bad:.12f}"))

    coeff = float(np.trace(rho_tr @ pa_projector()))
    checks.append(Check("quarter-coefficient", math.isclose(coeff, 0.25, rel_tol=0.0, abs_tol=1e-12), f"coeff={coeff:.6f}"))

    # Entropy defect is basis independent: unitary conjugation preserves it.
    theta = 0.37
    u2 = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]], dtype=float)
    U = np.kron(np.kron(np.kron(u2, u2), u2), u2)
    rho_rot = U @ rho_bad @ U.T
    i_rot = math.log(16.0) - entropy(rho_rot)
    checks.append(Check("information-defect-basis-independent", math.isclose(i_bad, i_rot, rel_tol=0.0, abs_tol=1e-12), f"I_bad={i_bad:.12f}, I_rot={i_rot:.12f}"))

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
