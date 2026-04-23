#!/usr/bin/env python3
"""Audit runner for the source-free local state law theorem."""

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

    i2 = np.eye(2)
    rho2 = i2 / 2.0

    # Test 1: the source-free qubit state is normalized.
    checks.append(Check("qubit-normalized", math.isclose(np.trace(rho2), 1.0), f"trace={np.trace(rho2):.6f}"))

    # Test 2: qubit source-free state is positive.
    evals2 = np.linalg.eigvalsh(rho2)
    checks.append(Check("qubit-positive", np.all(evals2 >= -1e-12), f"min_eval={evals2.min():.6f}"))

    # Test 3: qubit state is invariant under a nontrivial unitary rotation.
    theta = 0.41
    u2 = np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=float,
    )
    checks.append(Check("qubit-unitary-invariant", np.allclose(u2 @ rho2 @ u2.T, rho2), "rotation witness"))

    # Test 4: a nontrivial qubit state is not unitary-invariant.
    rho2_bad = np.diag([0.7, 0.3])
    checks.append(Check("nontrivial-qubit-breaks-invariance", not np.allclose(u2 @ rho2_bad @ u2.T, rho2_bad), "rotation mixes unequal eigenweights"))

    # Test 5: tensor product of four source-free qubits is the tracial 16-state cell.
    rho16 = rho2
    for _ in range(3):
        rho16 = np.kron(rho16, rho2)
    checks.append(Check("cell-shape", rho16.shape == (16, 16), f"shape={rho16.shape}"))

    # Test 6: exact equality with I_16 / 16.
    checks.append(Check("cell-tracial", np.allclose(rho16, np.eye(16) / 16.0), "tensor product equals I_16/16"))

    # Test 7: cell state normalized and positive.
    evals16 = np.linalg.eigvalsh(rho16)
    ok_norm = math.isclose(np.trace(rho16), 1.0)
    ok_pos = np.all(evals16 >= -1e-12)
    checks.append(Check("cell-valid", ok_norm and ok_pos, f"trace={np.trace(rho16):.6f}, min_eval={evals16.min():.6f}"))

    # Test 8: product law is multiplicative on dimensions.
    checks.append(Check("dimension-factorization", math.isclose(np.trace(np.eye(16) / 16.0), np.trace(rho2) ** 4), "normalization composes"))

    # Test 9: counting law yields quarter.
    p_a = pa_projector()
    coeff = float(np.trace(rho16 @ p_a))
    checks.append(Check("quarter-coefficient", math.isclose(coeff, 0.25), f"coeff={coeff:.6f}"))

    # Test 10: packet rank is 4.
    rank_pa = int(np.linalg.matrix_rank(p_a))
    checks.append(Check("packet-rank", rank_pa == 4, f"rank={rank_pa}"))

    # Test 11: a nonproduct witness differs from the source-free state.
    rho_bad = (1.0 / 32.0) * p_a + (7.0 / 96.0) * (np.eye(16) - p_a)
    checks.append(Check("nonproduct-witness-different", not np.allclose(rho_bad, rho16), "packet-light witness differs from source-free law"))

    # Test 12: the witness gives the wrong coefficient.
    coeff_bad = float(np.trace(rho_bad @ p_a))
    checks.append(Check("witness-wrong-coefficient", not math.isclose(coeff_bad, coeff), f"coeff_bad={coeff_bad:.6f}"))

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
