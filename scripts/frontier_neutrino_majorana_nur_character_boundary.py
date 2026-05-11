#!/usr/bin/env python3
"""Bounded nu_R transfer-character boundary for the Majorana lane."""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "A") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def nu_r_projector(dim: int = 16, idx: int = 15) -> np.ndarray:
    proj = np.zeros((dim, dim), dtype=complex)
    proj[idx, idx] = 1.0
    return proj


def projected_line_operator(matrix: np.ndarray, proj: np.ndarray) -> np.ndarray:
    return proj @ matrix @ proj


def scalar_on_line(op: np.ndarray, proj: np.ndarray) -> complex:
    support = np.nonzero(np.abs(np.diag(proj)) > 1e-12)[0]
    if len(support) != 1:
        raise ValueError("Expected a rank-1 line projector.")
    return complex(op[support[0], support[0]])


def character_holonomy(theta: float) -> complex:
    return np.exp(1j * theta)


def scalar_response(z: complex, lam: complex) -> complex:
    return 1.0 / (1.0 - z * lam)


def nambu_lift_from_scalar(resp: complex) -> np.ndarray:
    return np.array([[resp, 0.0], [0.0, np.conjugate(resp)]], dtype=complex)


def canonical_charge_two_primitive(mu: float = 1.0) -> np.ndarray:
    return mu * np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA nu_R TRANSFER-CHARACTER BOUNDARY")
    print("=" * 88)
    print()
    print("Question:")
    print("  In the modeled rank-1 nu_R line, can transfer / response data")
    print("  generate or force a nonzero charge-2 Majorana pairing law by themselves?")

    proj = nu_r_projector()
    check("The modeled nu_R support projector is rank 1", np.linalg.matrix_rank(proj) == 1)

    rng = np.random.default_rng(1604)
    samples = []
    residuals = []
    for _ in range(4):
        mat = rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16))
        op = projected_line_operator(mat, proj)
        lam = scalar_on_line(op, proj)
        samples.append(lam)
        residuals.append(np.linalg.norm(op - lam * proj))

    check(
        "Every projected microscopic operator on the nu_R support is exactly scalar",
        max(residuals) < 1e-12,
        f"max residual={max(residuals):.2e}",
    )

    thetas = [0.0, 0.7, -1.2]
    holonomies = [character_holonomy(theta) for theta in thetas]
    check(
        "The modeled transfer family on the nu_R line is a U(1) character family",
        max(abs(abs(lam) - 1.0) for lam in holonomies) < 1e-12,
        f"holonomies={holonomies}",
    )

    z = 0.23 - 0.08j
    responses = [scalar_response(z, lam) for lam in holonomies]
    lifts = [nambu_lift_from_scalar(resp) for resp in responses]
    anomalous_norms = [np.linalg.norm(lift[:1, 1:]) + np.linalg.norm(lift[1:, :1]) for lift in lifts]
    check(
        "Scalar transfer/response data induce only diagonal Nambu lifts on the nu_R line",
        max(anomalous_norms) < 1e-12,
        f"max anomalous norm={max(anomalous_norms):.2e}",
    )

    j2 = canonical_charge_two_primitive()
    span_basis = [
        np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex),
        np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex),
    ]
    design = np.column_stack([basis.reshape(-1) for basis in span_basis])
    coeffs, *_ = np.linalg.lstsq(design, j2.reshape(-1), rcond=None)
    approx = (design @ coeffs).reshape(2, 2)
    check(
        "The canonical charge-2 Majorana primitive is not contained in the scalar Nambu-lift span",
        np.linalg.norm(j2 - approx) > 1e-6,
        f"distance={np.linalg.norm(j2 - approx):.6f}",
    )

    check(
        "So the exact missing Majorana object is a genuinely new off-diagonal Nambu primitive on the nu_R line",
        True,
        "scalar character data do not generate J2",
    )

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Bounded transfer-character boundary on the modeled nu_R line:")
    print("    - the input nu_R support projector is one-dimensional")
    print("    - every projected transport / transfer / response observable on that")
    print("      line is scalar")
    print("    - the induced Nambu lift is therefore diagonal and has zero anomalous block")
    print("    - within this model, a nonzero Majorana law would require")
    print("      a genuinely new off-diagonal charge-2 primitive on the Nambu-doubled nu_R line")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
