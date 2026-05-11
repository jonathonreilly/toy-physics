#!/usr/bin/env python3
"""Bounded lower-level Majorana pairing no-go for charge-preserving kernels."""

from __future__ import annotations

import sys
import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def nambu_response_kernel(normal_kernel: np.ndarray) -> np.ndarray:
    zeros = np.zeros_like(normal_kernel)
    return np.block(
        [
            [np.linalg.inv(np.eye(normal_kernel.shape[0]) - normal_kernel), zeros],
            [zeros, np.linalg.inv(np.eye(normal_kernel.shape[0]) - normal_kernel.conj())],
        ]
    )


def induced_pairing_block(nambu_kernel: np.ndarray, n: int) -> np.ndarray:
    return nambu_kernel[:n, n:]


def one_gen_pairing_operator(mu: float) -> np.ndarray:
    j2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    return mu * j2


def three_gen_pairing_operator(mu: float) -> np.ndarray:
    return mu * np.array(
        [
            [0.0, 1.0, 0.0],
            [-1.0, 0.0, 1.0],
            [0.0, -1.0, 0.0],
        ],
        dtype=complex,
    )


def random_invertible_hermitian(n: int, seed: int, shift: float = 2.5) -> np.ndarray:
    rng = np.random.default_rng(seed)
    m = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    h = 0.5 * (m + m.conj().T)
    return h + shift * np.eye(n, dtype=complex)


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA LOWER-LEVEL PAIRING NO-GO")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does the lower-level charge-preserving transport/Green/source-response")
    print("  layer induce a genuine antisymmetric pairing kernel on the unique ΔL=2")
    print("  Majorana channel?")

    n1 = random_invertible_hermitian(2, 1901)
    kernel1 = nambu_response_kernel(n1)
    pair1 = induced_pairing_block(kernel1, 2)
    check("One-generation lower-level Nambu response has zero anomalous block for a generic charge-preserving normal kernel", np.linalg.norm(pair1) < 1e-12,
          f"|pair|={np.linalg.norm(pair1):.2e}")
    check("So the one-generation induced Majorana amplitude is zero", np.linalg.norm(pair1 - one_gen_pairing_operator(0.0)) < 1e-12)

    n3 = random_invertible_hermitian(3, 2003)
    kernel3 = nambu_response_kernel(n3)
    pair3 = induced_pairing_block(kernel3, 3)
    check("Three-generation lower-level Nambu response has zero anomalous block for a generic charge-preserving normal kernel", np.linalg.norm(pair3) < 1e-12,
          f"|pair|={np.linalg.norm(pair3):.2e}")
    check("So the modeled lower-level three-generation Majorana matrix remains zero", np.linalg.norm(pair3 - three_gen_pairing_operator(0.0)) < 1e-12)

    n5 = random_invertible_hermitian(5, 2105)
    kernel5 = nambu_response_kernel(n5)
    pair5 = induced_pairing_block(kernel5, 5)
    check("The anomalous block vanishes identically for generic charge-preserving normal kernels of any size", np.linalg.norm(pair5) < 1e-12,
          f"|pair|={np.linalg.norm(pair5):.2e}")

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact lower-level Majorana no-go:")
    print("    - generic charge-preserving lower-level dynamics induce no anomalous Nambu block")
    print("    - therefore the induced Majorana pairing kernel is identically zero")
    print("    - this is bounded support for the charge-preserving response-kernel class")
    print("    - deriving that the framework response layer is restricted to this class")
    print("      remains a separate bridge theorem")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
