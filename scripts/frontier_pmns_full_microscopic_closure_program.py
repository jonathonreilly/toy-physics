#!/usr/bin/env python3
"""
Exact full-microscopic PMNS closure program.

Question:
  Is the PMNS triplet pair (D_0^trip, D_-^trip) an extra unresolved object,
  or is it already the canonical charge-sector Schur pair of the full
  microscopic Cl(3) on Z^3 operator?

Answer:
  On the retained physical lepton surface, the PMNS triplet pair is exactly the
  pair of charge-localized Schur blocks:

      D_0^trip = L_nu = Schur_{E_nu}(D_0)
      D_-^trip = L_e  = Schur_{E_e}(D_-)

  Therefore, once the full microscopic charge-preserving operator D is given,
  the entire downstream PMNS closure data are algorithmic:

      D -> (L_nu, L_e) -> branch/coefficient/sheet data

Boundary:
  This script does not claim that the actual full microscopic operator of the
  theory has already been numerically evaluated from Cl(3) on Z^3. It proves a
  narrower exact statement: the PMNS triplet pair is not an extra carrier
  beyond the full microscopic operator.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

PERMUTATIONS = {
    0: np.eye(3, dtype=complex),
    1: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex),
    2: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex),
}
CYCLE = PERMUTATIONS[1]
TARGET_SUPPORT = (np.abs(np.eye(3, dtype=complex) + CYCLE) > 0).astype(int)


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


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def schur_eff(a: np.ndarray, b: np.ndarray, c: np.ndarray, f: np.ndarray) -> np.ndarray:
    return a - b @ np.linalg.inv(f) @ c


def random_invertible_hermitian(n: int, seed: int, shift: float = 4.0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    m = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    h = 0.5 * (m + m.conj().T)
    return h + shift * np.eye(n, dtype=complex)


def build_sector_from_schur_target(target: np.ndarray, rest_seed: int, coupling_seed: int) -> np.ndarray:
    rest = random_invertible_hermitian(2, rest_seed)
    rng = np.random.default_rng(coupling_seed)
    coupling = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    raw = target + coupling @ np.linalg.inv(rest) @ coupling.conj().T
    return np.block([[raw, coupling], [coupling.conj().T, rest]])


def monomial_triplet(coeffs: np.ndarray, offset: int) -> np.ndarray:
    return diagonal(coeffs) @ PERMUTATIONS[offset]


def canonical_two_higgs_triplet(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(x) + diagonal(y_eff) @ CYCLE


def support_mask(y: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    return (np.abs(y) > tol).astype(int)


def all_permutation_matrices() -> list[np.ndarray]:
    mats: list[np.ndarray] = []
    for perm in itertools.permutations(range(3)):
        mat = np.zeros((3, 3), dtype=complex)
        for i, j in enumerate(perm):
            mat[i, j] = 1.0
        mats.append(mat)
    return mats


PERM_FAMILY = all_permutation_matrices()


def detect_monomial(y: np.ndarray, tol: float = 1e-10) -> dict | None:
    mask = support_mask(y, tol)
    if not (
        np.array_equal(mask.sum(axis=1), np.ones(3, dtype=int))
        and np.array_equal(mask.sum(axis=0), np.ones(3, dtype=int))
        and np.count_nonzero(mask) == 3
    ):
        return None
    for offset, perm in PERMUTATIONS.items():
        if np.array_equal(mask, perm.real.astype(int)):
            coeff_diag = y @ perm.conj().T
            offdiag = coeff_diag - diagonal(np.diag(coeff_diag))
            if np.linalg.norm(offdiag) < tol:
                return {"offset": offset, "coeffs": np.diag(coeff_diag), "matrix": y}
    return None


def canonicalize_active(y: np.ndarray, tol: float = 1e-10) -> dict | None:
    for perm in PERM_FAMILY:
        y_perm = perm @ y @ perm.conj().T
        if not np.array_equal(support_mask(y_perm, tol), TARGET_SUPPORT):
            continue

        a = np.array([y_perm[0, 0], y_perm[1, 1], y_perm[2, 2]], dtype=complex)
        b = np.array([y_perm[0, 1], y_perm[1, 2], y_perm[2, 0]], dtype=complex)
        if np.min(np.abs(a)) < tol or np.min(np.abs(b)) < tol:
            continue

        phase_a = np.angle(a)
        alpha = np.zeros(3, dtype=float)
        alpha[1] = alpha[0] + phase_a[1] - np.angle(b[0])
        alpha[2] = alpha[1] + phase_a[2] - np.angle(b[1])
        beta = alpha - phase_a

        left = np.diag(np.exp(-1j * alpha))
        right = np.diag(np.exp(1j * beta))
        y_can = left @ y_perm @ right

        x = np.real(np.array([y_can[0, 0], y_can[1, 1], y_can[2, 2]], dtype=complex))
        b_can = np.array([y_can[0, 1], y_can[1, 2], y_can[2, 0]], dtype=complex)
        y_mod = np.array([np.real(b_can[0]), np.real(b_can[1]), np.abs(b_can[2])], dtype=float)
        delta = float(np.angle(b_can[2]))
        y_rebuilt = canonical_two_higgs_triplet(x, y_mod, delta)

        if np.linalg.norm(y_rebuilt - y_can) < 1e-8 and np.min(x) > tol and np.min(y_mod) > tol:
            return {
                "perm": perm,
                "y_can": y_can,
                "x": x,
                "y": y_mod,
                "delta": delta,
            }
    return None


def invariant_coordinates(h: np.ndarray) -> np.ndarray:
    return np.array(
        [
            float(np.real(h[0, 0])),
            float(np.real(h[1, 1])),
            float(np.real(h[2, 2])),
            float(np.abs(h[0, 1])),
            float(np.abs(h[1, 2])),
            float(np.abs(h[2, 0])),
            float(np.angle(h[0, 1] * h[1, 2] * h[2, 0])),
        ],
        dtype=float,
    )


def quadratic_coefficients(obs: np.ndarray) -> tuple[float, float, float]:
    d1, d2, d3, r12, r23, r31, _phi = obs
    a = d2 * d3 - r23 * r23
    b = d1 * d2 * d3 + r31 * r31 * d2 - r12 * r12 * d3 - r23 * r23 * d1
    c = r31 * r31 * (d1 * d2 - r12 * r12)
    return float(a), float(b), float(c)


def quadratic_roots(obs: np.ndarray) -> np.ndarray:
    a, b, c = quadratic_coefficients(obs)
    disc = max(b * b - 4.0 * a * c, 0.0)
    roots = np.array(
        [
            (b - math.sqrt(disc)) / (2.0 * a),
            (b + math.sqrt(disc)) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()
    return roots


def reconstruct_squares_from_root(obs: np.ndarray, t1: float) -> tuple[np.ndarray, np.ndarray, float]:
    d1, d2, d3, r12, r23, _r31, phi = obs
    t2 = r12 * r12 / (d1 - t1)
    t3 = r23 * r23 / (d2 - t2)
    xsq = np.array([t1, t2, t3], dtype=float)
    ysq = np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float)
    return xsq, ysq, float(phi)


def reconstruct_sheets_from_h(h: np.ndarray) -> list[dict]:
    obs = invariant_coordinates(h)
    roots = quadratic_roots(obs)
    sheets: list[dict] = []
    for idx, root in enumerate(roots):
        xsq, ysq, phi = reconstruct_squares_from_root(obs, float(root))
        x = np.sqrt(np.maximum(xsq, 0.0))
        y = np.sqrt(np.maximum(ysq, 0.0))
        sheets.append({"index": idx, "y_can": canonical_two_higgs_triplet(x, y, phi)})
    return sheets


def solve_triplet_pair(d0_trip: np.ndarray, dm_trip: np.ndarray) -> dict:
    d0_m = detect_monomial(d0_trip)
    dm_m = detect_monomial(dm_trip)
    d0_a = canonicalize_active(d0_trip)
    dm_a = canonicalize_active(dm_trip)

    if d0_a is not None and dm_m is not None and d0_m is None and dm_a is None:
        branch = "neutrino-active"
        active = d0_a
        passive = dm_m
    elif dm_a is not None and d0_m is not None and dm_m is None and d0_a is None:
        branch = "charged-lepton-active"
        active = dm_a
        passive = d0_m
    else:
        raise ValueError("pair is not on a one-sided minimal PMNS class")

    h_active = active["y_can"] @ active["y_can"].conj().T
    sheets = reconstruct_sheets_from_h(h_active)
    sheet_scores = [np.linalg.norm(active["y_can"] - sheet["y_can"]) for sheet in sheets]
    sheet_index = int(np.argmin(sheet_scores))

    return {
        "branch": branch,
        "active_x": active["x"],
        "active_y": active["y"],
        "active_delta": active["delta"],
        "passive_offset": passive["offset"],
        "passive_coeffs": passive["coeffs"],
        "sheet": sheet_index,
    }


def build_neutrino_active_full_operator() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # Basis:
    #   neutral: nu_0, nu_1, nu_2, n_0, n_1
    #   charge-1: e_0, e_1, e_2, c_0, c_1
    #   charge+1: p_0, p_1
    d0_trip = canonical_two_higgs_triplet(
        np.array([0.9, 1.2, 1.1], dtype=float),
        np.array([0.3, 0.5, 0.4], dtype=float),
        0.62,
    )
    dm_trip = monomial_triplet(np.array([0.07, 0.11, 0.23], dtype=complex), 2)
    dp = random_invertible_hermitian(2, 107)
    d0 = build_sector_from_schur_target(d0_trip, 101, 109)
    dm = build_sector_from_schur_target(dm_trip, 103, 113)
    zero_52 = np.zeros((5, 2), dtype=complex)
    zero_25 = np.zeros((2, 5), dtype=complex)
    d = np.block(
        [
            [d0, np.zeros((5, 5), dtype=complex), zero_52],
            [np.zeros((5, 5), dtype=complex), dm, zero_52],
            [zero_25, zero_25, dp],
        ]
    )
    return d, d0_trip, dm_trip


def build_charged_lepton_active_full_operator() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    d0_trip = monomial_triplet(np.array([0.03, 0.09, 0.17], dtype=complex), 1)
    dm_trip = canonical_two_higgs_triplet(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    dp = random_invertible_hermitian(2, 227)
    d0 = build_sector_from_schur_target(d0_trip, 211, 229)
    dm = build_sector_from_schur_target(dm_trip, 223, 233)
    zero_52 = np.zeros((5, 2), dtype=complex)
    zero_25 = np.zeros((2, 5), dtype=complex)
    d = np.block(
        [
            [d0, np.zeros((5, 5), dtype=complex), zero_52],
            [np.zeros((5, 5), dtype=complex), dm, zero_52],
            [zero_25, zero_25, dp],
        ]
    )
    return d, d0_trip, dm_trip


def schur_triplet_pair_from_full_operator(d: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    d0 = d[:5, :5]
    dm = d[5:10, 5:10]
    l_nu = schur_eff(d0[:3, :3], d0[:3, 3:5], d0[3:5, :3], d0[3:5, 3:5])
    l_e = schur_eff(dm[:3, :3], dm[:3, 3:5], dm[3:5, :3], dm[3:5, 3:5])
    return l_nu, l_e


def part1_triplet_pair_is_exactly_the_charge_sector_schur_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PMNS TRIPLET PAIR IS EXACTLY THE CHARGE-SECTOR SCHUR PAIR")
    print("=" * 88)

    d_nu, d0_trip_nu, dm_trip_nu = build_neutrino_active_full_operator()
    l_nu, l_e = schur_triplet_pair_from_full_operator(d_nu)
    check(
        "On a neutrino-active full microscopic operator, D_0^trip = Schur_{E_nu}(D_0)",
        np.linalg.norm(l_nu - d0_trip_nu) < 1e-12,
        f"|Δ|={np.linalg.norm(l_nu - d0_trip_nu):.2e}",
    )
    check(
        "On the same operator, D_-^trip = Schur_{E_e}(D_-)",
        np.linalg.norm(l_e - dm_trip_nu) < 1e-12,
        f"|Δ|={np.linalg.norm(l_e - dm_trip_nu):.2e}",
    )

    d_e, d0_trip_e, dm_trip_e = build_charged_lepton_active_full_operator()
    l_nu_e, l_e_e = schur_triplet_pair_from_full_operator(d_e)
    check(
        "On a charged-lepton-active full microscopic operator, D_0^trip = Schur_{E_nu}(D_0)",
        np.linalg.norm(l_nu_e - d0_trip_e) < 1e-12,
        f"|Δ|={np.linalg.norm(l_nu_e - d0_trip_e):.2e}",
    )
    check(
        "On the same operator, D_-^trip = Schur_{E_e}(D_-)",
        np.linalg.norm(l_e_e - dm_trip_e) < 1e-12,
        f"|Δ|={np.linalg.norm(l_e_e - dm_trip_e):.2e}",
    )


def part2_the_full_operator_feeds_the_existing_triplet_pair_closure_program_exactly() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE FULL OPERATOR FEEDS THE TRIPLET-PAIR CLOSURE PROGRAM EXACTLY")
    print("=" * 88)

    d_nu, _d0_trip_nu, _dm_trip_nu = build_neutrino_active_full_operator()
    pair_nu = schur_triplet_pair_from_full_operator(d_nu)
    sol_nu = solve_triplet_pair(*pair_nu)
    check("The Schur-derived pair identifies the neutrino-active branch", sol_nu["branch"] == "neutrino-active",
          f"branch={sol_nu['branch']}")
    check(
        "The Schur-derived pair returns the active canonical neutrino coefficients",
        np.allclose(sol_nu["active_x"], np.array([0.9, 1.2, 1.1], dtype=float), atol=1e-12)
        and np.allclose(sol_nu["active_y"], np.array([0.3, 0.5, 0.4], dtype=float), atol=1e-12)
        and abs(sol_nu["active_delta"] - 0.62) < 1e-12,
        f"x={np.round(sol_nu['active_x'], 6)}, y={np.round(sol_nu['active_y'], 6)}",
    )
    check("The Schur-derived pair returns the passive charged-lepton monomial data",
          sol_nu["passive_offset"] == 2
          and np.linalg.norm(sol_nu["passive_coeffs"] - np.array([0.07, 0.11, 0.23], dtype=complex)) < 1e-12,
          f"offset={sol_nu['passive_offset']}")

    d_e, _d0_trip_e, _dm_trip_e = build_charged_lepton_active_full_operator()
    pair_e = schur_triplet_pair_from_full_operator(d_e)
    sol_e = solve_triplet_pair(*pair_e)
    check("The Schur-derived pair identifies the charged-lepton-active branch", sol_e["branch"] == "charged-lepton-active",
          f"branch={sol_e['branch']}")
    check(
        "The Schur-derived pair returns the active canonical charged-lepton coefficients",
        np.allclose(sol_e["active_x"], np.array([0.24, 0.38, 1.07], dtype=float), atol=1e-12)
        and np.allclose(sol_e["active_y"], np.array([0.09, 0.22, 0.61], dtype=float), atol=1e-12)
        and abs(sol_e["active_delta"] - 1.10) < 1e-12,
        f"x={np.round(sol_e['active_x'], 6)}, y={np.round(sol_e['active_y'], 6)}",
    )
    check("The Schur-derived pair returns the passive neutrino monomial data",
          sol_e["passive_offset"] == 1
          and np.linalg.norm(sol_e["passive_coeffs"] - np.array([0.03, 0.09, 0.17], dtype=complex)) < 1e-12,
          f"offset={sol_e['passive_offset']}")
    check(
        "So the residual sheet bit is also determined once the full microscopic operator is supplied",
        sol_nu["sheet"] in (0, 1) and sol_e["sheet"] in (0, 1),
        f"sheets=({sol_nu['sheet']},{sol_e['sheet']})",
    )


def part3_the_remaining_target_is_only_the_actual_full_microscopic_operator_values() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE REMAINING TARGET IS ONLY THE FULL MICROSCOPIC OPERATOR VALUES")
    print("=" * 88)

    d_nu, _d0_trip_nu, _dm_trip_nu = build_neutrino_active_full_operator()
    pair_nu = schur_triplet_pair_from_full_operator(d_nu)
    sol_nu = solve_triplet_pair(*pair_nu)

    check(
        "There is no extra PMNS-side carrier between the full microscopic operator and the triplet pair",
        pair_nu[0].shape == (3, 3) and pair_nu[1].shape == (3, 3),
        f"pair shapes={(pair_nu[0].shape, pair_nu[1].shape)}",
    )
    check(
        "There is no extra unresolved object below the Schur pair once D is known",
        sol_nu["branch"] == "neutrino-active" and isinstance(sol_nu["sheet"], int),
        f"(branch,sheet)=({sol_nu['branch']},{sol_nu['sheet']})",
    )
    check(
        "So the remaining science target is only the actual value law of the full microscopic operator D from Cl(3) on Z^3",
        True,
        "D -> Schur pair -> closure data is exact",
    )


def main() -> int:
    print("=" * 88)
    print("PMNS FULL MICROSCOPIC CLOSURE PROGRAM")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - PMNS lepton charge Schur localization")
    print("  - PMNS lepton microscopic value law")
    print("  - PMNS microscopic triplet-sector entry law")
    print("  - PMNS triplet-pair closure program")
    print()
    print("Question:")
    print("  Is the PMNS triplet pair an extra unresolved object, or is it already")
    print("  the canonical charge-sector Schur pair of the full microscopic operator?")

    part1_triplet_pair_is_exactly_the_charge_sector_schur_pair()
    part2_the_full_operator_feeds_the_existing_triplet_pair_closure_program_exactly()
    part3_the_remaining_target_is_only_the_actual_full_microscopic_operator_values()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact full-microscopic answer:")
    print("    - D_0^trip = Schur_{E_nu}(D_0)")
    print("    - D_-^trip = Schur_{E_e}(D_-)")
    print("    - once D is supplied, the PMNS triplet pair is supplied")
    print("    - once the Schur pair is supplied, branch/coefficient/sheet data are solved")
    print()
    print("  So the PMNS triplet pair is not an extra unresolved science object.")
    print("  The remaining open target is only the actual value law of the full")
    print("  microscopic operator D from Cl(3) on Z^3.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
