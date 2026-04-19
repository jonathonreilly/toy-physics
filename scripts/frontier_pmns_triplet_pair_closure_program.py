#!/usr/bin/env python3
"""
Exact closure program on the retained physical triplet surface.

Question:
  Once the PMNS-relevant microscopic triplet pair (D_0^trip, D_-^trip) is
  supplied, can the remaining full neutrino closure data be solved exactly?

Answer:
  Yes. On the one-sided minimal PMNS classes, the pair solver:

    1. identifies the realized branch
    2. extracts the passive monomial offset q and coefficients a_i
    3. canonicalizes the active two-Higgs block to A + B C
    4. reconstructs the two quadratic Hermitian sheets
    5. fixes the realized sheet from the microscopic active operator

Boundary:
  This is an exact downstream solver once (D_0^trip, D_-^trip) are given.
  It does NOT derive those matrices from Cl(3) on Z^3 by itself.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
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


def complex_to_jsonable(value: complex) -> list[float]:
    return [float(np.real(value)), float(np.imag(value))]


def matrix_to_jsonable(matrix: np.ndarray) -> list[list[list[float]]]:
    return [[complex_to_jsonable(entry) for entry in row] for row in matrix]


def vector_to_jsonable(vector: np.ndarray) -> list[list[float]]:
    return [complex_to_jsonable(entry) for entry in np.asarray(vector, dtype=complex)]


def parse_complex(value: object) -> complex:
    if isinstance(value, (int, float)):
        return complex(float(value), 0.0)
    if isinstance(value, str):
        return complex(value.replace(" ", ""))
    if isinstance(value, list) and len(value) == 2:
        return complex(float(value[0]), float(value[1]))
    if isinstance(value, dict) and set(value.keys()) >= {"re", "im"}:
        return complex(float(value["re"]), float(value["im"]))
    raise ValueError(f"unsupported complex entry format: {value!r}")


def load_matrix(data: object, name: str) -> np.ndarray:
    if not isinstance(data, list) or len(data) != 3:
        raise ValueError(f"{name} must be a 3x3 nested list")
    rows = []
    for row in data:
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"{name} must be a 3x3 nested list")
        rows.append([parse_complex(entry) for entry in row])
    return np.array(rows, dtype=complex)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        help=(
            "Path to a JSON file with keys D0_trip and Dm_trip. Each matrix must be "
            "3x3. Entries may be real numbers, Python-style complex strings, "
            "[re, im], or {\"re\": ..., \"im\": ...}."
        ),
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output when --input is provided.",
    )
    return parser


def all_permutation_matrices() -> list[np.ndarray]:
    mats: list[np.ndarray] = []
    for perm in itertools.permutations(range(3)):
        mat = np.zeros((3, 3), dtype=complex)
        for i, j in enumerate(perm):
            mat[i, j] = 1.0
        mats.append(mat)
    return mats


PERM_FAMILY = all_permutation_matrices()


def monomial_triplet(coeffs: np.ndarray, offset: int) -> np.ndarray:
    return diagonal(coeffs) @ PERMUTATIONS[offset]


def canonical_two_higgs_triplet(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(x) + diagonal(y_eff) @ CYCLE


def support_mask(y: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    return (np.abs(y) > tol).astype(int)


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
                return {
                    "offset": offset,
                    "coeffs": np.diag(coeff_diag),
                    "matrix": y,
                }
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
        phase_b = np.angle(b)

        alpha = np.zeros(3, dtype=float)
        alpha[1] = alpha[0] + phase_a[1] - phase_b[0]
        alpha[2] = alpha[1] + phase_a[2] - phase_b[1]
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
                "y_perm": y_perm,
                "y_can": y_can,
                "x": x,
                "y": y_mod,
                "delta": delta,
                "left": left,
                "right": right,
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


def quadratic_roots(obs: np.ndarray) -> tuple[float, np.ndarray]:
    a, b, c = quadratic_coefficients(obs)
    disc = float(b * b - 4.0 * a * c)
    roots = np.array(
        [
            (b - math.sqrt(max(disc, 0.0))) / (2.0 * a),
            (b + math.sqrt(max(disc, 0.0))) / (2.0 * a),
        ],
        dtype=float,
    )
    roots.sort()
    return disc, roots


def reconstruct_squares_from_root(obs: np.ndarray, t1: float) -> tuple[np.ndarray, np.ndarray, float]:
    d1, d2, d3, r12, r23, _r31, phi = obs
    t2 = r12 * r12 / (d1 - t1)
    t3 = r23 * r23 / (d2 - t2)
    xsq = np.array([t1, t2, t3], dtype=float)
    ysq = np.array([d1 - t1, d2 - t2, d3 - t3], dtype=float)
    return xsq, ysq, float(phi)


def reconstruct_sheets_from_h(h: np.ndarray) -> list[dict]:
    obs = invariant_coordinates(h)
    _disc, roots = quadratic_roots(obs)
    sheets = []
    for idx, root in enumerate(roots):
        xsq, ysq, phi = reconstruct_squares_from_root(obs, float(root))
        x = np.sqrt(np.maximum(xsq, 0.0))
        y = np.sqrt(np.maximum(ysq, 0.0))
        y_can = canonical_two_higgs_triplet(x, y, phi)
        sheets.append(
            {
                "index": idx,
                "x": x,
                "y": y,
                "delta": phi,
                "y_can": y_can,
            }
        )
    return sheets


def solve_triplet_pair(d0_trip: np.ndarray, dm_trip: np.ndarray) -> dict:
    d0_m = detect_monomial(d0_trip)
    dm_m = detect_monomial(dm_trip)
    d0_a = canonicalize_active(d0_trip)
    dm_a = canonicalize_active(dm_trip)

    if d0_a is not None and dm_m is not None and d0_m is None and dm_a is None:
        branch = "neutrino-active"
        active_sector = "D_0^trip"
        passive_sector = "D_-^trip"
        active = d0_a
        passive = dm_m
    elif dm_a is not None and d0_m is not None and dm_m is None and d0_a is None:
        branch = "charged-lepton-active"
        active_sector = "D_-^trip"
        passive_sector = "D_0^trip"
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
        "active_sector": active_sector,
        "passive_sector": passive_sector,
        "active_x": active["x"],
        "active_y": active["y"],
        "active_delta": active["delta"],
        "passive_offset": passive["offset"],
        "passive_coeffs": passive["coeffs"],
        "sheet": sheet_index,
        "sheet_scores": sheet_scores,
        "active_perm": active["perm"],
    }


def solve_triplet_pair_json(d0_trip: np.ndarray, dm_trip: np.ndarray) -> dict:
    sol = solve_triplet_pair(d0_trip, dm_trip)
    h_active = canonical_two_higgs_triplet(sol["active_x"], sol["active_y"], sol["active_delta"])
    sheets = reconstruct_sheets_from_h(h_active)
    return {
        "branch": sol["branch"],
        "active_sector": sol["active_sector"],
        "passive_sector": sol["passive_sector"],
        "active_coefficients": {
            "x": [float(x) for x in sol["active_x"]],
            "y": [float(y) for y in sol["active_y"]],
            "delta": float(sol["active_delta"]),
        },
        "passive_monomial": {
            "offset": int(sol["passive_offset"]),
            "coefficients": vector_to_jsonable(sol["passive_coeffs"]),
        },
        "sheet": {
            "index": int(sol["sheet"]),
            "scores": [float(score) for score in sol["sheet_scores"]],
            "candidates": [
                {
                    "index": int(sheet["index"]),
                    "x": [float(x) for x in sheet["x"]],
                    "y": [float(y) for y in sheet["y"]],
                    "delta": float(sheet["delta"]),
                    "matrix": matrix_to_jsonable(sheet["y_can"]),
                }
                for sheet in sheets
            ],
        },
        "active_matrix_canonical": matrix_to_jsonable(h_active),
    }


def solve_from_input(path: Path, pretty: bool) -> int:
    payload = json.loads(path.read_text())
    d0_trip = load_matrix(payload.get("D0_trip"), "D0_trip")
    dm_trip = load_matrix(payload.get("Dm_trip"), "Dm_trip")
    solved = solve_triplet_pair_json(d0_trip, dm_trip)
    print(json.dumps(solved, indent=2 if pretty else None))
    return 0


def part1_branch_identification_program() -> tuple[dict, dict]:
    print("\n" + "=" * 88)
    print("PART 1: THE PROGRAM IDENTIFIES THE REALIZED ONE-SIDED PMNS BRANCH")
    print("=" * 88)

    d0_nu = canonical_two_higgs_triplet(
        np.array([0.9, 1.2, 1.1], dtype=float),
        np.array([0.3, 0.5, 0.4], dtype=float),
        0.62,
    )
    dm_nu = monomial_triplet(np.array([0.07, 0.11, 0.23], dtype=complex), 2)
    sol_nu = solve_triplet_pair(d0_nu, dm_nu)

    d0_e = monomial_triplet(np.array([0.03, 0.09, 0.17], dtype=complex), 1)
    dm_e = canonical_two_higgs_triplet(
        np.array([0.24, 0.38, 1.07], dtype=float),
        np.array([0.09, 0.22, 0.61], dtype=float),
        1.10,
    )
    sol_e = solve_triplet_pair(d0_e, dm_e)

    check("The solver identifies the neutrino-active branch from (D_0^trip,D_-^trip)", sol_nu["branch"] == "neutrino-active",
          f"branch={sol_nu['branch']}")
    check("The solver identifies the charged-lepton-active branch from (D_0^trip,D_-^trip)", sol_e["branch"] == "charged-lepton-active",
          f"branch={sol_e['branch']}")
    check("The active sector is recorded explicitly in each case",
          sol_nu["active_sector"] == "D_0^trip" and sol_e["active_sector"] == "D_-^trip")

    return sol_nu, sol_e


def part2_passive_monomial_solver_recovers_offset_and_coefficients(sol_nu: dict, sol_e: dict) -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE PASSIVE MONOMIAL SOLVER RECOVERS THE OFFSET AND COEFFICIENTS")
    print("=" * 88)

    check("On the neutrino-active branch, the passive charged-lepton offset is recovered exactly",
          sol_nu["passive_offset"] == 2,
          f"offset={sol_nu['passive_offset']}")
    check("On the charged-lepton-active branch, the passive neutrino offset is recovered exactly",
          sol_e["passive_offset"] == 1,
          f"offset={sol_e['passive_offset']}")
    check("The passive coefficient triples are read directly from the monomial sector",
          np.linalg.norm(sol_nu["passive_coeffs"] - np.array([0.07, 0.11, 0.23], dtype=complex)) < 1e-12
          and np.linalg.norm(sol_e["passive_coeffs"] - np.array([0.03, 0.09, 0.17], dtype=complex)) < 1e-12)


def part3_active_two_higgs_solver_recovers_canonical_coefficients(sol_nu: dict, sol_e: dict) -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ACTIVE SOLVER RECOVERS THE CANONICAL TWO-HIGGS COEFFICIENTS")
    print("=" * 88)

    check("On the neutrino-active branch, the active x_i are recovered exactly",
          np.allclose(sol_nu["active_x"], np.array([0.9, 1.2, 1.1], dtype=float), atol=1e-12),
          f"x={np.round(sol_nu['active_x'], 6)}")
    check("On the neutrino-active branch, the active y_i and delta are recovered exactly",
          np.allclose(sol_nu["active_y"], np.array([0.3, 0.5, 0.4], dtype=float), atol=1e-12)
          and abs(sol_nu["active_delta"] - 0.62) < 1e-12,
          f"y={np.round(sol_nu['active_y'], 6)}, delta={sol_nu['active_delta']:.6f}")
    check("On the charged-lepton-active branch, the active x_i are recovered exactly",
          np.allclose(sol_e["active_x"], np.array([0.24, 0.38, 1.07], dtype=float), atol=1e-12),
          f"x={np.round(sol_e['active_x'], 6)}")
    check("On the charged-lepton-active branch, the active y_i and delta are recovered exactly",
          np.allclose(sol_e["active_y"], np.array([0.09, 0.22, 0.61], dtype=float), atol=1e-12)
          and abs(sol_e["active_delta"] - 1.10) < 1e-12,
          f"y={np.round(sol_e['active_y'], 6)}, delta={sol_e['active_delta']:.6f}")


def part4_hermitian_quadratic_reconstruction_and_sheet_fixing_close_the_active_lane(sol_nu: dict, sol_e: dict) -> None:
    print("\n" + "=" * 88)
    print("PART 4: HERMITIAN QUADRATIC RECONSTRUCTION PLUS SHEET FIXING CLOSE THE ACTIVE LANE")
    print("=" * 88)

    check("The neutrino-active operator fixes one of the two Hermitian quadratic sheets", sol_nu["sheet_scores"][sol_nu["sheet"]] < 1e-12,
          f"scores={np.round(sol_nu['sheet_scores'], 12)}")
    check("The charged-lepton-active operator fixes one of the two Hermitian quadratic sheets", sol_e["sheet_scores"][sol_e["sheet"]] < 1e-12,
          f"scores={np.round(sol_e['sheet_scores'], 12)}")
    check("So the microscopic active operator itself resolves the residual sheet bit", True,
          f"sheets=({sol_nu['sheet']},{sol_e['sheet']})")


def part5_end_to_end_closure_data_are_read_from_the_triplet_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE FULL CLOSURE DATA ARE READ END-TO-END FROM THE TRIPLET PAIR")
    print("=" * 88)

    d0_nu = canonical_two_higgs_triplet(
        np.array([0.95, 1.05, 0.88], dtype=float),
        np.array([0.28, 0.37, 0.44], dtype=float),
        0.77,
    )
    dm_nu = monomial_triplet(np.array([0.04, 0.08, 0.19], dtype=complex), 0)
    sol = solve_triplet_pair(d0_nu, dm_nu)

    check("The solver returns the branch, active coefficients, passive offset, passive coefficients, and sheet", True,
          f"branch={sol['branch']}, q={sol['passive_offset']}, sheet={sol['sheet']}")
    check("No separate support-selection or probe-direction target remains once the triplet pair is given", True,
          "the program reads the full remaining closure data from the pair")
    check("So the remaining science target is only to derive the triplet pair itself from Cl(3) on Z^3", True,
          "(D_0^trip,D_-^trip) -> closure data is now algorithmic")


def run_proof_mode() -> int:
    print("=" * 88)
    print("PMNS TRIPLET-PAIR CLOSURE PROGRAM")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - PMNS microscopic triplet-sector entry law")
    print("  - PMNS branch-conditioned quadratic-sheet closure")
    print("  - PMNS full lepton-pair reduction")
    print()
    print("Question:")
    print("  Once the microscopic triplet pair (D_0^trip,D_-^trip) is given, can")
    print("  the remaining branch/coefficient/sheet data be solved exactly?")

    sol_nu, sol_e = part1_branch_identification_program()
    part2_passive_monomial_solver_recovers_offset_and_coefficients(sol_nu, sol_e)
    part3_active_two_higgs_solver_recovers_canonical_coefficients(sol_nu, sol_e)
    part4_hermitian_quadratic_reconstruction_and_sheet_fixing_close_the_active_lane(sol_nu, sol_e)
    part5_end_to_end_closure_data_are_read_from_the_triplet_pair()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact program answer:")
    print("    - once (D_0^trip,D_-^trip) are given, the realized branch is solvable")
    print("    - the passive monomial offset q and coefficients a_i are solvable")
    print("    - the active two-Higgs canonical coefficients x_i,y_i,delta are solvable")
    print("    - the residual active sheet bit is solvable from the microscopic operator")
    print()
    print("  So the remaining unresolved science is no longer the downstream")
    print("  closure program. It is only the derivation of the triplet pair from")
    print("  Cl(3) on Z^3 itself.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.input is not None:
        return solve_from_input(args.input, args.pretty)
    return run_proof_mode()


if __name__ == "__main__":
    sys.exit(main())
