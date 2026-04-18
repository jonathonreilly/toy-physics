#!/usr/bin/env python3
"""
DM Wilson-to-dW_e^H structured extension criterion theorem.

Purpose:
  Verify the weakest honest extension test from a generic Hermitian Wilson
  source family Psi to a structured rank-3 embedding Phi_e.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from frontier_dm_wilson_to_dweh_local_chain_path_algebra_target_2026_04_18 import (
    chain_data,
    gram_matrix,
)

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


def chain_hermitian_basis() -> list[np.ndarray]:
    chain = chain_data()
    return [
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


def jordan(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return 0.5 * (a @ b + b @ a)


def lie(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a @ b - b @ a) / (2j)


def hermitian_parts(z: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    x = 0.5 * (z + z.conj().T)
    y = (z - z.conj().T) / (2j)
    return x, y


def real_coords(x: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    g = gram_matrix(basis)
    rhs = np.array([float(np.real(np.trace(b @ x))) for b in basis], dtype=float)
    return np.linalg.solve(g, rhs)


def psi_from_basis_images(
    x: np.ndarray, basis: list[np.ndarray], images: list[np.ndarray]
) -> np.ndarray:
    coeffs = real_coords(x, basis)
    out = np.zeros_like(images[0], dtype=complex)
    for c, img in zip(coeffs, images):
        out += c * img
    return out


def extend_psi(
    z: np.ndarray, basis: list[np.ndarray], images: list[np.ndarray]
) -> np.ndarray:
    x, y = hermitian_parts(z)
    return psi_from_basis_images(x, basis, images) + 1j * psi_from_basis_images(y, basis, images)


def random_unitary(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    q, r = np.linalg.qr(z)
    phases = np.diag(r) / np.abs(np.diag(r))
    return q @ np.diag(np.conj(phases))


def max_basis_product_defect(
    basis: list[np.ndarray], images: list[np.ndarray], product_kind: str
) -> float:
    max_defect = 0.0
    for a in basis:
        for b in basis:
            lhs_input = jordan(a, b) if product_kind == "jordan" else lie(a, b)
            lhs = psi_from_basis_images(lhs_input, basis, images)
            psi_a = psi_from_basis_images(a, basis, images)
            psi_b = psi_from_basis_images(b, basis, images)
            rhs = jordan(psi_a, psi_b) if product_kind == "jordan" else lie(psi_a, psi_b)
            max_defect = max(max_defect, float(np.linalg.norm(lhs - rhs)))
    return max_defect


def random_matrix(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))


def main() -> int:
    print("=" * 88)
    print("DM WILSON-TO-dW_e^H STRUCTURED EXTENSION CRITERION THEOREM")
    print("=" * 88)

    family_target = read("docs/DM_WILSON_TO_DWEH_HERMITIAN_SOURCE_FAMILY_TARGET_NOTE_2026-04-18.md")
    normal_form = read("docs/DM_WILSON_TO_DWEH_ADJACENT_CHAIN_NORMAL_FORM_THEOREM_NOTE_2026-04-18.md")

    basis = chain_hermitian_basis()
    u = random_unitary(17)
    good_images = [u @ b @ u.conj().T for b in basis]
    bad_images = list(good_images)
    bad_images[-1] = bad_images[-1] + 0.17 * good_images[0]

    print("\n" + "=" * 88)
    print("PART 1: THE EXTENSION QUESTION IS REALLY THE MISSING FORCING STEP")
    print("=" * 88)
    check(
        "The generic target note only fixes a 9-channel Hermitian family, not a structured embedding",
        "nine-channel Wilson Hermitian source family" in family_target
        or "with nine real channels" in family_target,
    )
    check(
        "The adjacent-chain normal-form note explicitly says universal forcing into the structured class remains open",
        "not yet universally forced across all unknown realization classes" in normal_form,
    )

    print("\n" + "=" * 88)
    print("PART 2: EVERY Herm(3) FAMILY HAS A UNIQUE COMPLEX *-PRESERVING EXTENSION")
    print("=" * 88)
    z = random_matrix(101)
    x, y = hermitian_parts(z)
    phi_z = extend_psi(z, basis, good_images)
    phi_star = extend_psi(z.conj().T, basis, good_images)
    check(
        "Every complex matrix splits uniquely into Hermitian parts X + iY",
        np.linalg.norm(z - (x + 1j * y)) < 1e-12,
        f"err={np.linalg.norm(z - (x + 1j * y)):.2e}",
    )
    check(
        "The induced extension is *-preserving",
        np.linalg.norm(phi_star - phi_z.conj().T) < 1e-12,
        f"err={np.linalg.norm(phi_star - phi_z.conj().T):.2e}",
    )
    check(
        "The extension restricts back to the original Hermitian source family",
        np.linalg.norm(extend_psi(x, basis, good_images) - psi_from_basis_images(x, basis, good_images)) < 1e-12,
        f"err={np.linalg.norm(extend_psi(x, basis, good_images) - psi_from_basis_images(x, basis, good_images)):.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 3: JORDAN-LIE PRESERVATION IS EXACTLY WHAT MAKES THE EXTENSION STRUCTURED")
    print("=" * 88)
    good_jordan = max_basis_product_defect(basis, good_images, "jordan")
    good_lie = max_basis_product_defect(basis, good_images, "lie")
    z1 = random_matrix(203)
    z2 = random_matrix(307)
    phi_z1 = extend_psi(z1, basis, good_images)
    phi_z2 = extend_psi(z2, basis, good_images)
    mult_defect_good = np.linalg.norm(
        extend_psi(z1 @ z2, basis, good_images) - phi_z1 @ phi_z2
    )
    id_image = psi_from_basis_images(np.eye(3, dtype=complex), basis, good_images)
    check(
        "A structured family preserves the Jordan products on the Hermitian basis",
        good_jordan < 1e-12,
        f"defect={good_jordan:.2e}",
    )
    check(
        "A structured family preserves the Lie products on the Hermitian basis",
        good_lie < 1e-12,
        f"defect={good_lie:.2e}",
    )
    check(
        "Those identities make the complex extension multiplicative on arbitrary complex matrices",
        mult_defect_good < 1e-12,
        f"defect={mult_defect_good:.2e}",
    )
    check(
        "The image of 1_3 has rank 3 for the structured model family",
        np.linalg.matrix_rank(id_image) == 3,
        f"rank={np.linalg.matrix_rank(id_image)}",
    )

    print("\n" + "=" * 88)
    print("PART 4: AN INJECTIVE HERMITIAN FAMILY CAN STILL FAIL TO EXTEND STRUCTURALLY")
    print("=" * 88)
    bad_rank = np.linalg.matrix_rank(
        np.column_stack([img.reshape(-1) for img in bad_images])
    )
    bad_jordan = max_basis_product_defect(basis, bad_images, "jordan")
    bad_lie = max_basis_product_defect(basis, bad_images, "lie")
    bad_mult = np.linalg.norm(
        extend_psi(z1 @ z2, basis, bad_images)
        - extend_psi(z1, basis, bad_images) @ extend_psi(z2, basis, bad_images)
    )
    check(
        "A perturbed Hermitian family can remain injective on the 9-dimensional real source space",
        bad_rank == 9,
        f"rank={bad_rank}",
    )
    check(
        "But failing the Jordan criterion already obstructs structured extension",
        bad_jordan > 1e-4,
        f"defect={bad_jordan:.2e}",
    )
    check(
        "Failing the Lie criterion also obstructs structured extension",
        bad_lie > 1e-4,
        f"defect={bad_lie:.2e}",
    )
    check(
        "Accordingly the unique complex *-preserving extension is no longer multiplicative",
        bad_mult > 1e-4,
        f"defect={bad_mult:.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 5: FINITE BASIS CHECKING IS ENOUGH")
    print("=" * 88)
    combo_a = 0.7 * basis[0] - 0.4 * basis[3] + 0.9 * basis[8]
    combo_b = -0.6 * basis[1] + 0.5 * basis[4] + 0.8 * basis[6]
    lhs_j = psi_from_basis_images(jordan(combo_a, combo_b), basis, good_images)
    rhs_j = jordan(
        psi_from_basis_images(combo_a, basis, good_images),
        psi_from_basis_images(combo_b, basis, good_images),
    )
    lhs_l = psi_from_basis_images(lie(combo_a, combo_b), basis, good_images)
    rhs_l = lie(
        psi_from_basis_images(combo_a, basis, good_images),
        psi_from_basis_images(combo_b, basis, good_images),
    )
    check(
        "Once the basis-pair Jordan identities hold, random linear combinations satisfy them too",
        np.linalg.norm(lhs_j - rhs_j) < 1e-12,
        f"err={np.linalg.norm(lhs_j - rhs_j):.2e}",
    )
    check(
        "Once the basis-pair Lie identities hold, random linear combinations satisfy them too",
        np.linalg.norm(lhs_l - rhs_l) < 1e-12,
        f"err={np.linalg.norm(lhs_l - rhs_l):.2e}",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
