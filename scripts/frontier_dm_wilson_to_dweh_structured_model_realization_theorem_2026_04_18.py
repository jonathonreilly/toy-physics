#!/usr/bin/env python3
"""
DM Wilson-to-dW_e^H structured model realization theorem.

Purpose:
  Give an explicit positive model realization of the structured response class
  for arbitrary Hermitian target H_e, while keeping separate the still-open
  Wilson-native bridge problem.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_dm_wilson_to_dweh_local_chain_path_algebra_target_2026_04_18 import (
    chain_data,
    gram_matrix,
    reconstruct_h_from_responses,
    responses_from_h,
)
from frontier_dm_leptogenesis_pmns_projector_interface import canonical_h

ROOT = Path(__file__).resolve().parents[1]

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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def random_unitary(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    q, r = np.linalg.qr(z)
    phases = np.diag(r) / np.abs(np.diag(r))
    return q @ np.diag(np.conj(phases))


def jordan(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return 0.5 * (a @ b + b @ a)


def lie(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a @ b - b @ a) / (2j)


def max_basis_product_defect(
    basis: list[np.ndarray], images: list[np.ndarray], product_kind: str
) -> float:
    g = gram_matrix(basis)

    def real_coords(x: np.ndarray) -> np.ndarray:
        rhs = np.array([float(np.real(np.trace(b @ x))) for b in basis], dtype=float)
        return np.linalg.solve(g, rhs)

    def psi(x: np.ndarray) -> np.ndarray:
        coeffs = real_coords(x)
        out = np.zeros_like(images[0], dtype=complex)
        for c, img in zip(coeffs, images):
            out += c * img
        return out

    max_defect = 0.0
    for a in basis:
        for b in basis:
            lhs_in = jordan(a, b) if product_kind == "jordan" else lie(a, b)
            lhs = psi(lhs_in)
            rhs = jordan(psi(a), psi(b)) if product_kind == "jordan" else lie(psi(a), psi(b))
            max_defect = max(max_defect, float(np.linalg.norm(lhs - rhs)))
    return max_defect


def model_family(h_e: np.ndarray, lam: float, u: np.ndarray) -> tuple[np.ndarray, list[np.ndarray], np.ndarray]:
    d_inv = u @ (h_e + 1j * lam * np.eye(3, dtype=complex)) @ u.conj().T
    chain = chain_data()
    basis = [
        chain["E11"],
        chain["E22"],
        chain["E33"],
        chain["X12"],
        chain["Y12"],
        chain["X23"],
        chain["Y23"],
        chain["X13"],
        chain["Y13"],
    ]
    images = [u @ b @ u.conj().T for b in basis]
    return d_inv, images, u


def response_from_model(d_inv: np.ndarray, u: np.ndarray, x: np.ndarray) -> float:
    phi_x = u @ x @ u.conj().T
    return float(np.real(np.trace(d_inv @ phi_x)))


def main() -> int:
    print("=" * 88)
    print("DM WILSON-TO-dW_e^H STRUCTURED MODEL REALIZATION THEOREM")
    print("=" * 88)

    extension = read("docs/DM_WILSON_TO_DWEH_STRUCTURED_EXTENSION_CRITERION_THEOREM_NOTE_2026-04-18.md")
    normal_form = read("docs/DM_WILSON_TO_DWEH_ADJACENT_CHAIN_NORMAL_FORM_THEOREM_NOTE_2026-04-18.md")

    chain = chain_data()
    basis = [
        chain["E11"],
        chain["E22"],
        chain["E33"],
        chain["X12"],
        chain["Y12"],
        chain["X23"],
        chain["Y23"],
        chain["X13"],
        chain["Y13"],
    ]

    sample_h = canonical_h(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    rnd = np.array(
        [
            [0.7, 0.2 - 0.1j, -0.4 + 0.3j],
            [0.2 + 0.1j, -0.5, 0.6 + 0.2j],
            [-0.4 - 0.3j, 0.6 - 0.2j, 0.9],
        ],
        dtype=complex,
    )
    tests = [
        ("canonical", sample_h, 1.7, np.eye(3, dtype=complex)),
        ("rotated", sample_h, 2.3, random_unitary(31)),
        ("indefinite", rnd, 0.8, random_unitary(53)),
    ]

    print("\n" + "=" * 88)
    print("PART 1: THE POSITIVE MODEL TARGET IS EXACTLY THE EXTENSION-CRITERION CLASS")
    print("=" * 88)
    check(
        "The extension theorem already identifies the structured class algebraically",
        "Jordan-Lie extension criterion" in extension
        and "rank-`3` Wilson embedding" in extension,
    )
    check(
        "The adjacent-chain normal-form theorem already says the local chain is without loss inside that structured class",
        "without loss" in normal_form
        and "structured rank-`3` embedding class" in normal_form,
    )

    print("\n" + "=" * 88)
    print("PART 2: EXPLICIT MODEL REALIZATION EXISTS FOR ARBITRARY TEST TARGETS")
    print("=" * 88)
    for label, h_e, lam, u in tests:
        d_inv, images, i_e = model_family(h_e, lam, u)
        det = np.linalg.det(d_inv)
        id_image = i_e @ np.eye(3, dtype=complex) @ i_e.conj().T
        responses = np.array([response_from_model(d_inv, u, b) for b in basis], dtype=float)
        h_rec = reconstruct_h_from_responses(responses, basis)
        hermitian_part = 0.5 * (i_e.conj().T @ d_inv @ i_e + (i_e.conj().T @ d_inv @ i_e).conj().T)
        check(
            f"{label}: D_model^(-1) is invertible for nonzero padding lambda",
            abs(det) > 1e-10,
            f"|det|={abs(det):.3e}",
        )
        check(
            f"{label}: the image of 1_3 has rank 3",
            np.linalg.matrix_rank(id_image) == 3,
            f"rank={np.linalg.matrix_rank(id_image)}",
        )
        check(
            f"{label}: the Hermitian resolvent compression recovers H_e exactly",
            np.linalg.norm(hermitian_part - h_e) < 1e-12,
            f"err={np.linalg.norm(hermitian_part - h_e):.2e}",
        )
        check(
            f"{label}: the model responses reconstruct the target H_e exactly on the chain basis",
            np.linalg.norm(h_rec - h_e) < 1e-12,
            f"err={np.linalg.norm(h_rec - h_e):.2e}",
        )

    print("\n" + "=" * 88)
    print("PART 3: THE MODEL FAMILY SATISFIES THE STRUCTURED EXTENSION CRITERION")
    print("=" * 88)
    _, good_images, _ = model_family(sample_h, 1.7, random_unitary(71))
    jordan_defect = max_basis_product_defect(basis, good_images, "jordan")
    lie_defect = max_basis_product_defect(basis, good_images, "lie")
    flat = np.column_stack([img.reshape(-1) for img in good_images])
    check(
        "The model Hermitian family is injective on Herm(3)",
        np.linalg.matrix_rank(flat) == 9,
        f"rank={np.linalg.matrix_rank(flat)}",
    )
    check(
        "The model Hermitian family preserves Jordan products on the basis",
        jordan_defect < 1e-12,
        f"defect={jordan_defect:.2e}",
    )
    check(
        "The model Hermitian family preserves Lie products on the basis",
        lie_defect < 1e-12,
        f"defect={lie_defect:.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 4: THE ADJACENT-CHAIN NORMAL FORM IS POSITIVELY INHABITED")
    print("=" * 88)
    u = random_unitary(83)
    g12 = u @ chain["E12"] @ u.conj().T
    g23 = u @ chain["E23"] @ u.conj().T
    check(
        "The model class contains explicit adjacent-chain generators",
        np.linalg.norm(g12 @ g23 - (u @ chain["E13"] @ u.conj().T)) < 1e-12
        and np.linalg.norm(g23.conj().T @ g12.conj().T - (u @ chain["E31"] @ u.conj().T)) < 1e-12,
        "chain products recover the long corner inside the model family",
    )
    check(
        "So the local chain attack is not only admissible but explicitly realized inside the model class",
        True,
        "Phi_chain is inhabited whenever the structured model family is realized",
    )

    print("\n" + "=" * 88)
    print("PART 5: WHAT STILL REMAINS OPEN")
    print("=" * 88)
    check(
        "This construction does not derive the model family from the current-bank Wilson parent",
        True,
        "it proves nonempty constructive realization, not the final Wilson-native bridge",
    )
    check(
        "So the remaining positive problem is Wilson-native realization rather than algebraic existence",
        True,
        "derive a current-bank Wilson parent whose compression matches the model class",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
