#!/usr/bin/env python3
"""Audit runner for the same-object semantics bridge on the Planck lane."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def pa_projector() -> np.ndarray:
    p = np.zeros((16, 16), dtype=float)
    for idx in (1, 2, 4, 8):
        p[idx, idx] = 1.0
    return p


def rot(theta: float) -> np.ndarray:
    return np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=float,
    )


@dataclass
class Check:
    name: str
    ok: bool
    detail: str


def main() -> None:
    checks: list[Check] = []

    ident16 = np.eye(16)
    rho_tr = ident16 / 16.0
    p0 = np.zeros((16, 16), dtype=float)
    p0[0, 0] = 1.0

    U = np.kron(np.kron(np.kron(rot(0.37), rot(0.21)), rot(0.41)), rot(0.19))

    # The tracial state is invariant under a factor-preserving presentation change.
    checks.append(
        Check(
            "tracial-state-same-object-invariant",
            np.allclose(U @ rho_tr @ U.T, rho_tr),
            "factor-preserving presentation change leaves I_16/16 fixed",
        )
    )

    # A nontracial state changes primitive event probabilities under the same witness.
    rho_bad = np.diag([0.10, 0.02] + [0.88 / 14.0] * 14)
    prob_before = float(np.trace(rho_bad @ p0))
    prob_after = float(np.trace(rho_bad @ (U @ p0 @ U.T)))
    checks.append(
        Check(
            "nontracial-state-presentation-sensitive",
            not math.isclose(prob_before, prob_after, rel_tol=0.0, abs_tol=1e-9),
            f"prob_before={prob_before:.6f}, prob_after={prob_after:.6f}",
        )
    )

    # The factor-preserving group still leaves the packet coefficient exact.
    p_a = pa_projector()
    coeff = float(np.trace(rho_tr @ p_a))
    checks.append(
        Check(
            "quarter-coefficient",
            math.isclose(coeff, 0.25, rel_tol=0.0, abs_tol=1e-12),
            f"coeff={coeff:.6f}",
        )
    )

    checks.append(
        Check(
            "packet-rank",
            int(np.linalg.matrix_rank(p_a)) == 4,
            f"rank={int(np.linalg.matrix_rank(p_a))}",
        )
    )

    checks.append(
        Check(
            "cell-normalized",
            math.isclose(float(np.trace(rho_tr)), 1.0, rel_tol=0.0, abs_tol=1e-12),
            f"trace={float(np.trace(rho_tr)):.6f}",
        )
    )

    checks.append(
        Check(
            "cell-positive",
            np.all(np.linalg.eigvalsh(rho_tr) >= -1e-12),
            f"min_eval={float(np.linalg.eigvalsh(rho_tr).min()):.6f}",
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
