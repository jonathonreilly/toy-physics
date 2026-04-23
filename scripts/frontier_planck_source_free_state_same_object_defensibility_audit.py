#!/usr/bin/env python3
"""Audit runner for the defensibility of same-object semantics on source-free states."""

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

    U = np.kron(np.kron(np.kron(rot(0.37), rot(0.21)), rot(0.41)), rot(0.19))
    rho_sf = np.eye(16) / 16.0

    # Source-free state on bare cell should be presentation independent.
    checks.append(
        Check(
            "source-free-tracial-invariant",
            np.allclose(U @ rho_sf @ U.T, rho_sf),
            "I_16/16 is invariant under factor-preserving presentation changes",
        )
    )

    # Nontracial bare-cell state would create presentation-sensitive event data.
    rho_bad = np.diag([0.10, 0.02] + [0.88 / 14.0] * 14)
    p0 = np.zeros((16, 16), dtype=float)
    p0[0, 0] = 1.0
    prob_before = float(np.trace(rho_bad @ p0))
    prob_after = float(np.trace((U @ rho_bad @ U.T) @ p0))
    checks.append(
        Check(
            "nontracial-bare-cell-state-is-presentation-sensitive",
            not math.isclose(prob_before, prob_after, rel_tol=0.0, abs_tol=1e-9),
            f"prob_before={prob_before:.6f}, prob_after={prob_after:.6f}",
        )
    )

    # Prepared states are different: transform state and preparation datum together.
    rho_prep = p0.copy()
    prep_after = U @ p0 @ U.T
    prepared_readout_before = float(np.trace(rho_prep @ p0))
    prepared_readout_after = float(np.trace((U @ rho_prep @ U.T) @ prep_after))
    checks.append(
        Check(
            "prepared-state-pair-is-same-object-invariant",
            math.isclose(prepared_readout_before, prepared_readout_after, rel_tol=0.0, abs_tol=1e-12),
            f"before={prepared_readout_before:.6f}, after={prepared_readout_after:.6f}",
        )
    )

    # This shows why same-object semantics can distinguish source-free from prepared.
    checks.append(
        Check(
            "source-free-vs-prepared-distinction-real",
            not np.allclose(U @ rho_prep @ U.T, rho_prep),
            "a prepared pure state is not bare-cell invariant by itself",
        )
    )

    coeff = float(np.trace(rho_sf @ pa_projector()))
    checks.append(
        Check(
            "quarter-follows-on-source-free-route",
            math.isclose(coeff, 0.25, rel_tol=0.0, abs_tol=1e-12),
            f"coeff={coeff:.6f}",
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
