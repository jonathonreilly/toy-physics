#!/usr/bin/env python3
"""Audit runner for the source-free default-datum theorem candidate."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def rot(theta: float) -> np.ndarray:
    return np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=float,
    )


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

    rho_default = np.eye(16) / 16.0
    rho_hidden = np.diag([0.10, 0.02] + [0.88 / 14.0] * 14)

    U = np.kron(np.kron(np.kron(rot(0.37), rot(0.21)), rot(0.41)), rot(0.19))

    checks.append(
        Check(
            "default-datum-presentation-independent",
            np.allclose(U @ rho_default @ U.T, rho_default),
            "bare-cell default datum survives factor-preserving frame change",
        )
    )

    p0 = np.zeros((16, 16), dtype=float)
    p0[0, 0] = 1.0
    prob_before = float(np.trace(rho_hidden @ p0))
    prob_after = float(np.trace((U @ rho_hidden @ U.T) @ p0))
    checks.append(
        Check(
            "hidden-datum-state-detected-by-frame-change",
            not math.isclose(prob_before, prob_after, rel_tol=0.0, abs_tol=1e-9),
            f"prob_before={prob_before:.6f}, prob_after={prob_after:.6f}",
        )
    )

    rho_prep = p0.copy()
    prep_after = U @ p0 @ U.T
    pair_before = float(np.trace(rho_prep @ p0))
    pair_after = float(np.trace((U @ rho_prep @ U.T) @ prep_after))
    checks.append(
        Check(
            "prepared-pair-remains-valid",
            math.isclose(pair_before, pair_after, rel_tol=0.0, abs_tol=1e-12),
            f"before={pair_before:.6f}, after={pair_after:.6f}",
        )
    )

    coeff = float(np.trace(rho_default @ pa_projector()))
    checks.append(
        Check(
            "quarter-coefficient",
            math.isclose(coeff, 0.25, rel_tol=0.0, abs_tol=1e-12),
            f"coeff={coeff:.6f}",
        )
    )

    checks.append(
        Check(
            "default-state-normalized",
            math.isclose(float(np.trace(rho_default)), 1.0, rel_tol=0.0, abs_tol=1e-12),
            f"trace={float(np.trace(rho_default)):.6f}",
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
