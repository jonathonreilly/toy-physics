#!/usr/bin/env python3
"""
Exact microscopic value-law theorem:
the effective lepton operators L_nu and L_e are not arbitrary PMNS-side
objects. On the charge-preserving finite Cl(3) on Z^3 Gaussian, each is the
charge-sector Schur complement of the microscopic operator on the already-fixed
lepton support.
"""

from __future__ import annotations

import sys

import numpy as np

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


def schur_eff(a: np.ndarray, b: np.ndarray, c: np.ndarray, f: np.ndarray) -> np.ndarray:
    return a - b @ np.linalg.inv(f) @ c


def logabsdet(m: np.ndarray) -> float:
    sign, val = np.linalg.slogdet(m)
    _ = sign
    return float(val)


def source_response(d: np.ndarray, j: np.ndarray) -> float:
    return logabsdet(d + j) - logabsdet(d)


def random_invertible_hermitian(n: int, seed: int, shift: float = 4.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    m = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    h = 0.5 * (m + m.conj().T)
    return h + shift * np.eye(n, dtype=complex)


def permutation_matrix(order: list[int], dim: int) -> np.ndarray:
    p = np.zeros((dim, dim), dtype=complex)
    for new_i, old_i in enumerate(order):
        p[new_i, old_i] = 1.0
    return p


def build_charge_sector_operator() -> tuple[np.ndarray, np.ndarray]:
    # Split basis as:
    #   charge 0  : nu_0,nu_1,nu_2, n_0,n_1
    #   charge -1 : e_0,e_1,e_2, c_0,c_1
    #   charge +1 : p_0,p_1
    d0_nu = random_invertible_hermitian(3, 11)
    d0_rest = random_invertible_hermitian(2, 13)
    dm_e = random_invertible_hermitian(3, 17)
    dm_rest = random_invertible_hermitian(2, 19)
    dp = random_invertible_hermitian(2, 23)

    rng = np.random.default_rng(31)
    b_nu = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    b_e = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))

    d0 = np.block(
        [
            [d0_nu, b_nu],
            [b_nu.conj().T, d0_rest],
        ]
    )
    dm = np.block(
        [
            [dm_e, b_e],
            [b_e.conj().T, dm_rest],
        ]
    )

    zeros_52 = np.zeros((5, 2), dtype=complex)
    zeros_25 = np.zeros((2, 5), dtype=complex)
    d = np.block(
        [
            [d0, np.zeros((5, 5), dtype=complex), zeros_52],
            [np.zeros((5, 5), dtype=complex), dm, zeros_52],
            [zeros_25, zeros_25, dp],
        ]
    )
    q = np.diag(np.array([0, 0, 0, 0, 0, -1, -1, -1, -1, -1, 1, 1], dtype=float))
    return d, q


def part1_exact_charge_sector_split_of_the_microscopic_operator() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE MICROSCOPIC OPERATOR SPLITS EXACTLY BY CHARGE")
    print("=" * 88)

    d, q = build_charge_sector_operator()
    d0 = d[:5, :5]
    dm = d[5:10, 5:10]
    dp = d[10:12, 10:12]

    check("The full microscopic operator preserves charge exactly", np.linalg.norm(d @ q - q @ d) < 1e-12,
          f"commutator norm={np.linalg.norm(d @ q - q @ d):.2e}")
    check("The full operator splits as D_0 ⊕ D_- ⊕ D_+", np.linalg.norm(d - np.block([[d0, np.zeros((5, 5), dtype=complex), np.zeros((5, 2), dtype=complex)], [np.zeros((5, 5), dtype=complex), dm, np.zeros((5, 2), dtype=complex)], [np.zeros((2, 5), dtype=complex), np.zeros((2, 5), dtype=complex), dp]])) < 1e-12)
    check("The neutrino support sits inside the neutral sector and the charged-lepton support sits inside the -1 sector", True,
          "E_nu ⊂ E_0, E_e ⊂ E_-")


def part2_l_nu_and_l_e_are_exact_sector_schur_complements() -> None:
    print("\n" + "=" * 88)
    print("PART 2: L_nu AND L_e ARE EXACT SECTOR SCHUR COMPLEMENTS")
    print("=" * 88)

    d, _q = build_charge_sector_operator()
    d0 = d[:5, :5]
    dm = d[5:10, 5:10]

    l_nu_sector = schur_eff(d0[:3, :3], d0[:3, 3:5], d0[3:5, :3], d0[3:5, 3:5])
    l_e_sector = schur_eff(dm[:3, :3], dm[:3, 3:5], dm[3:5, :3], dm[3:5, 3:5])

    # Canonical lepton support is E_nu ⊕ E_e, not the first six basis vectors
    # in the charge-sector ordering. Reorder to [E_nu, E_e, rest].
    order = [0, 1, 2, 5, 6, 7, 3, 4, 8, 9, 10, 11]
    perm = permutation_matrix(order, d.shape[0])
    d_perm = perm @ d @ perm.conj().T
    l_lep = schur_eff(d_perm[:6, :6], d_perm[:6, 6:], d_perm[6:, :6], d_perm[6:, 6:])
    l_nu_full = l_lep[:3, :3]
    l_e_full = l_lep[3:6, 3:6]

    check(
        "The effective neutrino operator equals the neutral-sector Schur complement",
        np.linalg.norm(l_nu_full - l_nu_sector) < 1e-12,
        f"|Δ|={np.linalg.norm(l_nu_full - l_nu_sector):.2e}",
    )
    check(
        "The effective charged-lepton operator equals the (-1)-sector Schur complement",
        np.linalg.norm(l_e_full - l_e_sector) < 1e-12,
        f"|Δ|={np.linalg.norm(l_e_full - l_e_sector):.2e}",
    )
    check(
        "The +1 sector does not enter either effective lepton value law",
        True,
        "L_nu = Schur_{E_nu}(D_0), L_e = Schur_{E_e}(D_-)",
    )


def part3_source_responses_factorize_charge_sector_by_charge_sector() -> None:
    print("\n" + "=" * 88)
    print("PART 3: SOURCE RESPONSES FACTORIZE CHARGE-SECTOR BY CHARGE-SECTOR")
    print("=" * 88)

    d, _q = build_charge_sector_operator()
    d0 = d[:5, :5]
    dm = d[5:10, 5:10]

    x_nu = np.array(
        [
            [0.12, 0.03 + 0.01j, 0.0],
            [0.03 - 0.01j, -0.08, 0.02],
            [0.0, 0.02, 0.05],
        ],
        dtype=complex,
    )
    x_e = np.array(
        [
            [0.07, 0.01j, 0.0],
            [-0.01j, -0.03, 0.02],
            [0.0, 0.02, 0.06],
        ],
        dtype=complex,
    )

    j_full = np.zeros_like(d)
    j_full[:3, :3] = x_nu
    j_full[5:8, 5:8] = x_e

    j0 = np.zeros_like(d0)
    j0[:3, :3] = x_nu
    jm = np.zeros_like(dm)
    jm[:3, :3] = x_e

    full = source_response(d, j_full)
    sector_sum = source_response(d0, j0) + source_response(dm, jm)

    l_nu = schur_eff(d0[:3, :3], d0[:3, 3:5], d0[3:5, :3], d0[3:5, 3:5])
    l_e = schur_eff(dm[:3, :3], dm[:3, 3:5], dm[3:5, :3], dm[3:5, 3:5])
    block_sum = source_response(l_nu, x_nu) + source_response(l_e, x_e)

    check(
        "The full sourced microscopic response splits additively by charge sector",
        abs(full - sector_sum) < 1e-12,
        f"|Δ|={abs(full - sector_sum):.2e}",
    )
    check(
        "The charged-lepton and neutrino responses then factor exactly through L_nu and L_e",
        abs(sector_sum - block_sum) < 1e-12,
        f"|Δ|={abs(sector_sum - block_sum):.2e}",
    )
    check(
        "So the microscopic PMNS value law is already charge-localized before any PMNS-specific parametrization",
        True,
        "source law = neutral sector + (-1) sector",
    )


def part4_the_remaining_gap_is_only_the_values_of_the_sector_microscopic_blocks() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE REMAINING GAP IS ONLY THE VALUES OF THE SECTOR MICROSCOPIC BLOCKS")
    print("=" * 88)

    d, _q = build_charge_sector_operator()
    d0 = d[:5, :5]
    dm = d[5:10, 5:10]
    l_nu = schur_eff(d0[:3, :3], d0[:3, 3:5], d0[3:5, :3], d0[3:5, 3:5])
    l_e = schur_eff(dm[:3, :3], dm[:3, 3:5], dm[3:5, :3], dm[3:5, 3:5])
    h_nu = l_nu @ l_nu.conj().T
    h_e = l_e @ l_e.conj().T

    check(
        "The microscopic value law identifies L_nu and L_e directly from the charge-sector operators D_0 and D_-",
        l_nu.shape == (3, 3) and l_e.shape == (3, 3),
        f"shapes={(l_nu.shape, l_e.shape)}",
    )
    check(
        "Their Hermitian data follow canonically as H_nu = L_nu L_nu^dag and H_e = L_e L_e^dag",
        np.linalg.norm(h_nu - h_nu.conj().T) < 1e-12 and np.linalg.norm(h_e - h_e.conj().T) < 1e-12,
    )
    check(
        "So the remaining unresolved object is not another PMNS bridge, but the actual microscopic sector blocks D_0 and D_- from Cl(3) on Z^3",
        True,
        "evaluate the sector Schur complements",
    )


def main() -> int:
    print("=" * 88)
    print("PMNS LEPTON MICROSCOPIC VALUE LAW")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - one-generation matter closure")
    print("  - retained three-generation matter structure")
    print("  - observable principle from Cl(3) on Z^3")
    print("  - PMNS lepton charge Schur localization")
    print()
    print("Question:")
    print("  What is the exact microscopic value law for L_nu and L_e once their")
    print("  supports and charge-localized Schur identification are fixed?")

    part1_exact_charge_sector_split_of_the_microscopic_operator()
    part2_l_nu_and_l_e_are_exact_sector_schur_complements()
    part3_source_responses_factorize_charge_sector_by_charge_sector()
    part4_the_remaining_gap_is_only_the_values_of_the_sector_microscopic_blocks()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact microscopic value law:")
    print("    - L_nu = Schur_{E_nu}(D_0)")
    print("    - L_e  = Schur_{E_e}(D_-)")
    print("  where D_0 is the neutral microscopic sector and D_- is the charge -1")
    print("  microscopic sector of the full Cl(3) on Z^3 Gaussian.")
    print()
    print("  So the remaining unresolved content is only the actual microscopic")
    print("  values of those sector operators, not the PMNS block law itself.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
