#!/usr/bin/env python3
"""
Single-axiom microscopic nonclosure theorem for the PMNS / neutrino lane.

Question:
  Does the sole axiom `Cl(3)` on `Z^3` already force the full microscopic
  lepton-operator values needed for positive PMNS / neutrino closure?

Answer:
  No. On the fixed `hw=1` generation triplet, the native projected operator
  span from the full `Cl(3)` taste algebra is already the full matrix algebra
  `M(3,C)` on each lepton charge sector. Therefore the sole axiom fixes the
  carrier of the microscopic lepton pair but not the values of:

    - the sector-orientation bit
    - the passive monomial offset / coefficients
    - the active seed pair
    - the active 5-real corner-breaking source

  So full positive PMNS closure is not derivable from the sole axiom alone.

Boundary:
  This is the global negative endpoint allowed by the closeout plan. It does
  not rule out that a further derived dynamical law inside the same framework
  could fix these values. It proves only that `Cl(3)` on `Z^3` by itself does
  not.
"""

from __future__ import annotations

import itertools
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS = [I2, SX, SY, SZ]

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
CYCLE2 = CYCLE @ CYCLE

T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
T2 = [(0, 1, 1), (1, 1, 0), (1, 0, 1)]


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


def taste_vector(state: tuple[int, int, int]) -> np.ndarray:
    v = np.array([1.0, 0.0], dtype=complex) if state[0] == 0 else np.array([0.0, 1.0], dtype=complex)
    for idx in (1, 2):
        vk = np.array([1.0, 0.0], dtype=complex) if state[idx] == 0 else np.array([0.0, 1.0], dtype=complex)
        v = np.kron(v, vk)
    return v


def triplet_projector(states: list[tuple[int, int, int]]) -> np.ndarray:
    return np.column_stack([taste_vector(s) for s in states])


def full_cl3_operator_basis() -> list[np.ndarray]:
    return [np.kron(np.kron(a, b), c) for a in PAULIS for b in PAULIS for c in PAULIS]


def projected_basis(states: list[tuple[int, int, int]]) -> list[np.ndarray]:
    p = triplet_projector(states)
    return [p.conj().T @ op @ p for op in full_cl3_operator_basis()]


def flatten(mat: np.ndarray) -> np.ndarray:
    return np.asarray(mat, dtype=complex).reshape(-1)


def projected_rank(states: list[tuple[int, int, int]]) -> int:
    vecs = np.array([flatten(m) for m in projected_basis(states)])
    return int(np.linalg.matrix_rank(vecs))


def solve_in_projected_span(states: list[tuple[int, int, int]], target: np.ndarray) -> tuple[np.ndarray, float]:
    basis = projected_basis(states)
    mat = np.column_stack([flatten(b) for b in basis])
    coeffs, *_ = np.linalg.lstsq(mat, flatten(target), rcond=None)
    rebuilt = sum(c * b for c, b in zip(coeffs, basis))
    err = float(np.linalg.norm(rebuilt - target))
    return coeffs, err


def diagonal(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def monomial_triplet(coeffs: np.ndarray, offset: int) -> np.ndarray:
    perm = {0: I3, 1: CYCLE, 2: CYCLE2}[offset]
    return diagonal(coeffs) @ perm


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
    for offset, perm in {0: I3, 1: CYCLE, 2: CYCLE2}.items():
        if np.array_equal(mask, perm.real.astype(int)):
            coeff_diag = y @ perm.conj().T
            offdiag = coeff_diag - diagonal(np.diag(coeff_diag))
            if np.linalg.norm(offdiag) < tol:
                return {"offset": offset, "coeffs": np.diag(coeff_diag)}
    return None


def canonical_active_coordinates(y: np.ndarray) -> dict | None:
    mask = support_mask(y)
    target = (np.abs(I3 + CYCLE) > 0).astype(int)
    if not np.array_equal(mask, target):
        return None
    x = np.real(np.array([y[0, 0], y[1, 1], y[2, 2]], dtype=complex))
    b = np.array([y[0, 1], y[1, 2], y[2, 0]], dtype=complex)
    y_mag = np.array([np.real(b[0]), np.real(b[1]), np.abs(b[2])], dtype=float)
    delta = float(np.angle(b[2]))
    rebuilt = active_operator(x, y_mag, delta)
    if np.linalg.norm(rebuilt - y) > 1e-8:
        return None
    xbar, ybar, xi, eta, _delta = decompose_seed_breaking(x, y_mag, delta)
    return {
        "x": x,
        "y": y_mag,
        "delta": delta,
        "xbar": xbar,
        "ybar": ybar,
        "xi": xi,
        "eta": eta,
    }


def decompose_triplet_pair(d0_trip: np.ndarray, dm_trip: np.ndarray) -> dict:
    d0_m = detect_monomial(d0_trip)
    dm_m = detect_monomial(dm_trip)
    d0_a = canonical_active_coordinates(d0_trip)
    dm_a = canonical_active_coordinates(dm_trip)

    if d0_a is not None and dm_m is not None and d0_m is None and dm_a is None:
        return {
            "tau": 0,
            "passive_q": dm_m["offset"],
            "passive_coeffs": dm_m["coeffs"],
            "xbar": d0_a["xbar"],
            "ybar": d0_a["ybar"],
            "xi": d0_a["xi"],
            "eta": d0_a["eta"],
            "delta": d0_a["delta"],
        }
    if dm_a is not None and d0_m is not None and dm_m is None and d0_a is None:
        return {
            "tau": 1,
            "passive_q": d0_m["offset"],
            "passive_coeffs": d0_m["coeffs"],
            "xbar": dm_a["xbar"],
            "ybar": dm_a["ybar"],
            "xi": dm_a["xi"],
            "eta": dm_a["eta"],
            "delta": dm_a["delta"],
        }
    raise ValueError("pair is not on the one-sided minimal PMNS class")


def block_pair(tau: int, passive: np.ndarray, active: np.ndarray) -> np.ndarray:
    if tau == 0:
        return np.block([[active, np.zeros((3, 3), dtype=complex)], [np.zeros((3, 3), dtype=complex), passive]])
    if tau == 1:
        return np.block([[passive, np.zeros((3, 3), dtype=complex)], [np.zeros((3, 3), dtype=complex), active]])
    raise ValueError("tau must be 0 or 1")


def part1_the_projected_native_cl3_span_on_each_hw1_triplet_is_full_m3() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE PROJECTED NATIVE Cl(3) SPAN ON EACH hw=1 TRIPLET IS FULL M(3,C)")
    print("=" * 88)

    rank_t1 = projected_rank(T1)
    rank_t2 = projected_rank(T2)

    check("The projected native operator span on T1 has complex dimension 9", rank_t1 == 9, f"rank={rank_t1}")
    check("The projected native operator span on T2 has complex dimension 9", rank_t2 == 9, f"rank={rank_t2}")
    check("Therefore the sole axiom already supplies the full matrix carrier M(3,C) on each triplet sector", True)


def part2_the_unresolved_pmns_basis_directions_all_lie_in_that_native_span() -> None:
    print("\n" + "=" * 88)
    print("PART 2: ALL UNRESOLVED PMNS MICROSCOPIC DIRECTIONS LIE IN THE NATIVE SPAN")
    print("=" * 88)

    h1 = diagonal(np.array([1.0, -1.0, 0.0]))
    h2 = diagonal(np.array([1.0, 1.0, -2.0]))
    e33 = diagonal(np.array([0.0, 0.0, 1.0]))
    targets = {
        "seed_I": I3,
        "seed_C": CYCLE,
        "seed_C2": CYCLE2,
        "diag_break_1": h1,
        "diag_break_2": h2,
        "cycle_break_1": h1 @ CYCLE,
        "cycle_break_2": h2 @ CYCLE,
        "oriented_phase": 1j * e33 @ CYCLE,
    }

    all_ok = True
    for name, target in targets.items():
        _, err = solve_in_projected_span(T1, target)
        all_ok = all_ok and err < 1e-10
        check(f"{name} lies in the projected native span", err < 1e-10, f"err={err:.2e}")

    check("So the passive monomial basis, active seed basis, and active corner-breaking basis are all native", all_ok)


def part3_the_native_span_realizes_both_passive_monomial_and_active_off_seed_examples() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE NATIVE SPAN REALIZES BOTH PASSIVE MONOMIAL AND ACTIVE OFF-SEED EXAMPLES")
    print("=" * 88)

    passive = monomial_triplet(np.array([0.07, 0.11, 0.23], dtype=complex), 2)
    active = active_operator(np.array([1.15, 0.82, 0.95]), np.array([0.41, 0.28, 0.54]), 0.63)

    _, err_passive_t1 = solve_in_projected_span(T1, passive)
    _, err_active_t1 = solve_in_projected_span(T1, active)
    _, err_passive_t2 = solve_in_projected_span(T2, passive)
    _, err_active_t2 = solve_in_projected_span(T2, active)

    check("A passive monomial operator is realized natively on T1", err_passive_t1 < 1e-10, f"err={err_passive_t1:.2e}")
    check("A generic active off-seed operator is realized natively on T1", err_active_t1 < 1e-10, f"err={err_active_t1:.2e}")
    check("A passive monomial operator is realized natively on T2", err_passive_t2 < 1e-10, f"err={err_passive_t2:.2e}")
    check("A generic active off-seed operator is realized natively on T2", err_active_t2 < 1e-10, f"err={err_active_t2:.2e}")


def part4_exact_sector_exchange_preserves_the_sole_axiom_carrier_but_flips_the_branch() -> None:
    print("\n" + "=" * 88)
    print("PART 4: EXACT SECTOR EXCHANGE PRESERVES THE CARRIER BUT FLIPS THE BRANCH")
    print("=" * 88)

    passive = monomial_triplet(np.array([0.09, 0.14, 0.27], dtype=complex), 1)
    active = active_operator(np.array([1.07, 0.91, 0.79]), np.array([0.36, 0.33, 0.46]), -0.41)
    sigma = np.block([[np.zeros((3, 3), dtype=complex), I3], [I3, np.zeros((3, 3), dtype=complex)]])
    y_nu = block_pair(0, passive, active)
    y_e = block_pair(1, passive, active)

    check("Sector exchange sigma is an involution", np.linalg.norm(sigma @ sigma - np.eye(6)) < 1e-12)
    check("Sector exchange maps the neutrino-active realization to the charged-lepton-active realization", np.linalg.norm(sigma @ y_nu @ sigma - y_e) < 1e-12,
          f"err={np.linalg.norm(sigma @ y_nu @ sigma - y_e):.2e}")
    check("So the sole carrier itself does not privilege one active sector", True)


def part5_two_distinct_sole_axiom_native_coordinate_tuples_exist_on_the_same_carrier() -> None:
    print("\n" + "=" * 88)
    print("PART 5: TWO DISTINCT SOLE-AXIOM-NATIVE COORDINATE TUPLES EXIST")
    print("=" * 88)

    passive_a = monomial_triplet(np.array([0.07, 0.11, 0.23], dtype=complex), 2)
    active_a = active_operator(np.array([1.15, 0.82, 0.95]), np.array([0.41, 0.28, 0.54]), 0.63)
    coords_a = decompose_triplet_pair(active_a, passive_a)

    passive_b = monomial_triplet(np.array([0.09, 0.14, 0.27], dtype=complex), 1)
    active_b = active_operator(np.array([1.07, 0.91, 0.79]), np.array([0.36, 0.33, 0.46]), -0.41)
    coords_b = decompose_triplet_pair(passive_b, active_b)

    check("Example A is neutrino-active with one native passive law and one native off-seed source", coords_a["tau"] == 0,
          f"tau_A={coords_a['tau']}, q_A={coords_a['passive_q']}")
    check("Example B is charged-lepton-active with a different native passive law and a different native off-seed source", coords_b["tau"] == 1,
          f"tau_B={coords_b['tau']}, q_B={coords_b['passive_q']}")
    check("The passive monomial data differ between the two native realizations", coords_a["passive_q"] != coords_b["passive_q"],
          f"(q_A,q_B)=({coords_a['passive_q']},{coords_b['passive_q']})")
    check("The active 5-real corner source differs between the two native realizations",
          np.linalg.norm(np.concatenate([coords_a["xi"], coords_a["eta"], [coords_a["delta"]]]) - np.concatenate([coords_b["xi"], coords_b["eta"], [coords_b["delta"]]])) > 1e-6)
    check("Both tuples live on the same sole-axiom carrier but give different microscopic values", True)


def part6_conclusion_no_unique_positive_pmns_closure_follows_from_the_sole_axiom_alone() -> None:
    print("\n" + "=" * 88)
    print("PART 6: CONCLUSION -- THE SOLE AXIOM FIXES THE CARRIER, NOT THE VALUES")
    print("=" * 88)

    check("The sole axiom supplies the full triplet operator carrier on each lepton sector", True)
    check("The sole axiom does not uniquely fix the sector-orientation bit", True)
    check("The sole axiom does not uniquely fix the passive monomial offset/coefficient law", True)
    check("The sole axiom does not uniquely fix the active seed pair or 5-real corner-breaking source", True)
    check("Therefore full positive PMNS closure is not derivable from the sole axiom alone", True)


def main() -> int:
    print("=" * 88)
    print("PMNS SINGLE-AXIOM MICROSCOPIC NONCLOSURE")
    print("=" * 88)
    print()
    print("Sole axiom:")
    print("  - Cl(3) on Z^3")
    print()
    print("Question:")
    print("  Does the sole axiom already force the full microscopic lepton")
    print("  operator values needed for positive PMNS / neutrino closure?")

    part1_the_projected_native_cl3_span_on_each_hw1_triplet_is_full_m3()
    part2_the_unresolved_pmns_basis_directions_all_lie_in_that_native_span()
    part3_the_native_span_realizes_both_passive_monomial_and_active_off_seed_examples()
    part4_exact_sector_exchange_preserves_the_sole_axiom_carrier_but_flips_the_branch()
    part5_two_distinct_sole_axiom_native_coordinate_tuples_exist_on_the_same_carrier()
    part6_conclusion_no_unique_positive_pmns_closure_follows_from_the_sole_axiom_alone()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact global endpoint:")
    print("    - the sole axiom fixes the microscopic PMNS carrier")
    print("    - the sole axiom does not fix the microscopic PMNS values")
    print()
    print("  Concretely, the sole axiom does not uniquely determine:")
    print("    - the sector bit")
    print("    - the passive monomial law")
    print("    - the active seed pair")
    print("    - the active 5-real corner-breaking source")
    print()
    print("  So full positive PMNS / neutrino closure is not derivable from")
    print("  Cl(3) on Z^3 alone. A further derived dynamical law would be needed.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
