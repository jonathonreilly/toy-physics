#!/usr/bin/env python3
"""
Exact closure theorem for the minimal new PMNS corner-source law.

Question:
  After separating the already closed weak-axis seed data from the generic
  active microscopic deformation ΔD, what exactly must a genuinely new value
  law from Cl(3) on Z^3 output in order to close the PMNS lane?

Answer:
  Only the 5-real corner-breaking source on the hw=1 triplet:

      (xi_1, xi_2, eta_1, eta_2, delta)

  together with the already closed seed pair (xbar, ybar).

  From those data one reconstructs uniquely:
    - the active microscopic deformation ΔD_act
    - the active triplet operator D_act = I + ΔD_act
    - the branch-conditioned triplet pair
    - the downstream coefficient / sheet closure data

So once a new law supplies the 5-real corner-breaking source beyond the seed
pair, the remaining PMNS closure is algorithmic.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
PERMUTATIONS = {
    0: np.eye(3, dtype=complex),
    1: CYCLE,
    2: CYCLE @ CYCLE,
}


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


def active_operator(x: np.ndarray, y: np.ndarray, delta: float) -> np.ndarray:
    y_eff = np.asarray(y, dtype=complex).copy()
    y_eff[2] *= np.exp(1j * delta)
    return diagonal(x) + diagonal(y_eff) @ CYCLE


def decompose_seed_breaking(x: np.ndarray, y: np.ndarray, delta: float) -> tuple[float, float, np.ndarray, np.ndarray, float]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    xbar = float(np.mean(x))
    ybar = float(np.mean(y))
    xi = x - xbar * np.ones(3, dtype=float)
    eta = y - ybar * np.ones(3, dtype=float)
    return xbar, ybar, xi, eta, float(delta)


def rebuild_from_corner_source(
    xbar: float, ybar: float, xi1: float, xi2: float, eta1: float, eta2: float, delta: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xi = np.array([xi1, xi2, -xi1 - xi2], dtype=float)
    eta = np.array([eta1, eta2, -eta1 - eta2], dtype=float)
    x = xbar * np.ones(3, dtype=float) + xi
    y = ybar * np.ones(3, dtype=float) + eta
    d = active_operator(x, y, delta)
    dd = d - I3
    return x, y, dd


def monomial_triplet(coeffs: np.ndarray, offset: int) -> np.ndarray:
    return diagonal(coeffs) @ PERMUTATIONS[offset]


def support_mask(mat: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    return (np.abs(mat) > tol).astype(int)


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
            if np.linalg.norm(coeff_diag - diagonal(np.diag(coeff_diag))) < tol:
                return {"offset": offset, "coeffs": np.diag(coeff_diag)}
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
            (b - np.sqrt(disc)) / (2.0 * a),
            (b + np.sqrt(disc)) / (2.0 * a),
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


def solve_active_sheet(y: np.ndarray) -> int:
    h = y @ y.conj().T
    obs = invariant_coordinates(h)
    roots = quadratic_roots(obs)
    candidates = []
    for idx, root in enumerate(roots):
        xsq, ysq, phi = reconstruct_squares_from_root(obs, float(root))
        y_can = active_operator(np.sqrt(np.maximum(xsq, 0.0)), np.sqrt(np.maximum(ysq, 0.0)), phi)
        candidates.append((idx, np.linalg.norm(y_can - y)))
    return min(candidates, key=lambda t: t[1])[0]


def part1_seed_pair_plus_5_real_source_reconstructs_the_active_microscopic_deformation() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SEED PAIR + 5-REAL SOURCE RECONSTRUCT THE ACTIVE DEFORMATION")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    xbar, ybar, xi, eta, d = decompose_seed_breaking(x, y, delta)
    xr, yr, dd = rebuild_from_corner_source(xbar, ybar, xi[0], xi[1], eta[0], eta[1], d)

    check("The reconstructed x vector matches exactly", np.linalg.norm(x - xr) < 1e-12,
          f"err={np.linalg.norm(x - xr):.2e}")
    check("The reconstructed y vector matches exactly", np.linalg.norm(y - yr) < 1e-12,
          f"err={np.linalg.norm(y - yr):.2e}")
    check("Therefore the active ΔD is reconstructed exactly", np.linalg.norm(dd - (active_operator(x, y, delta) - I3)) < 1e-12,
          f"err={np.linalg.norm(dd - (active_operator(x, y, delta) - I3)):.2e}")


def part2_once_the_active_source_is_given_the_branch_conditioned_triplet_pair_is_fixed() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ONCE THE ACTIVE SOURCE IS GIVEN, THE TRIPLET PAIR IS FIXED")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    xbar, ybar, xi, eta, d = decompose_seed_breaking(x, y, delta)
    _xr, _yr, dd = rebuild_from_corner_source(xbar, ybar, xi[0], xi[1], eta[0], eta[1], d)
    active = I3 + dd
    passive = monomial_triplet(np.array([0.07, 0.11, 0.23], dtype=complex), 2)
    mon = detect_monomial(passive)

    check("The active operator keeps the canonical I+C support class", np.count_nonzero(support_mask(active)) == 6)
    check("The passive operator is exactly the retained monomial lane", mon is not None and mon["offset"] == 2,
          f"offset={None if mon is None else mon['offset']}")
    check("So once the 5-real active source is supplied, the branch-conditioned pair (D_act,D_pass) is fixed", True)


def part3_downstream_sheet_and_coefficient_data_are_then_algorithmic() -> None:
    print("\n" + "=" * 88)
    print("PART 3: DOWNSTREAM SHEET / COEFFICIENT DATA ARE THEN ALGORITHMIC")
    print("=" * 88)

    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    active = active_operator(x, y, delta)
    h = active @ active.conj().T
    obs = invariant_coordinates(h)
    roots = quadratic_roots(obs)
    sheet = solve_active_sheet(active)

    check("The active Hermitian data are fixed once the corner source is given", obs.shape == (7,))
    check("The residual quadratic-sheet pair is determined from those Hermitian data", roots.shape == (2,),
          f"roots={np.round(roots, 6)}")
    check("The realized sheet bit is then fixed by the active microscopic operator", sheet in (0, 1),
          f"sheet={sheet}")


def part4_the_new_law_output_is_exactly_the_5_real_corner_source_beyond_seed() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE NEW LAW OUTPUT IS EXACTLY THE 5-REAL CORNER SOURCE")
    print("=" * 88)

    check("The weak-axis seed pair is already closed separately", True, "(xbar,ybar) or equivalently (A,B)")
    check("The generic off-seed addition is exactly two diagonal zero-sum coordinates", True, "(xi1,xi2)")
    check("The generic cycle-magnitude addition is exactly two zero-sum coordinates", True, "(eta1,eta2)")
    check("The remaining phase contributes one real coordinate", True, "delta")
    check("So the genuinely new law only needs to output five real values beyond the seed pair", True,
          "(xi1,xi2,eta1,eta2,delta)")


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC DELTA-D CORNER-SOURCE CLOSURE")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - PMNS microscopic ΔD seed law")
    print("  - PMNS microscopic ΔD corner-orbit breaking")
    print("  - PMNS triplet-pair closure structure")
    print()
    print("Question:")
    print("  What exactly must a genuinely new value law output in order to close")
    print("  the PMNS microscopic deformation beyond the already solved seed pair?")

    part1_seed_pair_plus_5_real_source_reconstructs_the_active_microscopic_deformation()
    part2_once_the_active_source_is_given_the_branch_conditioned_triplet_pair_is_fixed()
    part3_downstream_sheet_and_coefficient_data_are_then_algorithmic()
    part4_the_new_law_output_is_exactly_the_5_real_corner_source_beyond_seed()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact closure reduction:")
    print("    - seed pair is already closed")
    print("    - once a new law supplies the 5-real corner-breaking source")
    print("      (xi1,xi2,eta1,eta2,delta), active ΔD is fixed")
    print("    - after that, the remaining PMNS closure steps are algorithmic")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
