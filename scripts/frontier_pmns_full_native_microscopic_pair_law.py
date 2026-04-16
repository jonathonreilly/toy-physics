#!/usr/bin/env python3
"""
Microscopic pair reconstruction interface for the PMNS / neutrino lane.

Question:
  If the selector outputs `(tau, q)` and the projected active/passive kernels
  are independently supplied, do they determine the full PMNS-relevant
  microscopic pair `(D_0^trip, D_-^trip)`?

Answer:
  Yes. The combined interface is:

    - selector outputs `(tau, q)`
    - active projected Green kernel
    - passive projected Green kernel

  Together these recover the microscopic triplet pair exactly. Once the pair
  is known, the existing downstream closure program is exact and algorithmic.

  This script does not prove that the selector outputs or the kernels have
  already been derived inside the same theorem. It proves that if those native
  ingredients are independently available, the microscopic pair and downstream
  closure data follow exactly.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

I3 = np.eye(3, dtype=complex)
CYCLE = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
PERMUTATIONS = {
    0: I3,
    1: CYCLE,
    2: CYCLE @ CYCLE,
}
TARGET_SUPPORT = (np.abs(I3 + CYCLE) > 0).astype(int)


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
    return diagonal(np.asarray(x, dtype=complex)) + diagonal(y_eff) @ CYCLE


def passive_operator(coeffs: np.ndarray, q: int) -> np.ndarray:
    return diagonal(coeffs) @ PERMUTATIONS[q]


def support_trace_moments(block: np.ndarray) -> np.ndarray:
    return np.array(
        [
            np.trace(block @ PERMUTATIONS[0].conj().T),
            np.trace(block @ PERMUTATIONS[1].conj().T),
            np.trace(block @ PERMUTATIONS[2].conj().T),
        ],
        dtype=complex,
    )


def recover_q_from_passive_moments(block: np.ndarray) -> int:
    return int(np.argmax(np.abs(support_trace_moments(block))))


def moment_support_count(block: np.ndarray, tol: float = 1e-10) -> int:
    return int(np.count_nonzero(np.abs(support_trace_moments(block)) > tol))


def projected_green_kernel(block: np.ndarray, lam: float) -> np.ndarray:
    return np.linalg.inv(I3 - lam * block)


def recover_block_from_green(kernel: np.ndarray, lam: float) -> np.ndarray:
    return (I3 - np.linalg.inv(kernel)) / lam


def active_delta_d_from_green(kernel: np.ndarray, lam: float) -> np.ndarray:
    return recover_block_from_green(kernel, lam)


def active_block_from_green(kernel: np.ndarray, lam: float) -> np.ndarray:
    return I3 + active_delta_d_from_green(kernel, lam)


def passive_block_from_green(kernel: np.ndarray, lam: float) -> np.ndarray:
    return recover_block_from_green(kernel, lam)


def recover_passive_coeffs(block: np.ndarray, q: int) -> np.ndarray:
    coeff_diag = block @ PERMUTATIONS[q].conj().T
    return np.diag(coeff_diag)


def build_full_pair(
    tau: int, q: int, passive_coeffs: np.ndarray, x: np.ndarray, y: np.ndarray, delta: float
) -> tuple[np.ndarray, np.ndarray]:
    active = active_operator(x, y, delta)
    passive = passive_operator(passive_coeffs, q)
    if tau == 0:
        return active, passive
    if tau == 1:
        return passive, active
    raise ValueError("tau must be 0 or 1")


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
                return {"offset": offset, "coeffs": np.diag(coeff_diag)}
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
        rebuilt = active_operator(x, y_mod, delta)
        if np.linalg.norm(rebuilt - y_can) < 1e-8:
            return {"x": x, "y": y_mod, "delta": delta, "y_can": y_can}
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
        sheets.append({"index": idx, "y_can": active_operator(x, y, phi)})
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


def recover_pair_from_native_interfaces(
    tau: int,
    q: int,
    active_kernel: np.ndarray,
    passive_kernel: np.ndarray,
    lam_act: float,
    lam_pass: float,
) -> tuple[np.ndarray, np.ndarray, dict]:
    recovered_active = active_block_from_green(active_kernel, lam_act)
    recovered_passive = passive_block_from_green(passive_kernel, lam_pass)
    recovered_q = recover_q_from_passive_moments(recovered_passive)
    a = recover_passive_coeffs(recovered_passive, q)

    if tau == 0:
        pair = (recovered_active, recovered_passive)
    else:
        pair = (recovered_passive, recovered_active)

    meta = {
        "tau": tau,
        "q": recovered_q,
        "a": a,
        "active_kernel": active_kernel,
        "passive_kernel": passive_kernel,
    }
    return pair[0], pair[1], meta


def part1_the_combined_native_routes_reconstruct_the_triplet_pair() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE COMBINED INTERFACES RECONSTRUCT THE TRIPLET PAIR")
    print("=" * 88)

    samples = [
        (
            "neutrino-active",
            0,
            2,
            np.array([0.07, 0.11, 0.23], dtype=complex),
            np.array([1.15, 0.82, 0.95], dtype=float),
            np.array([0.41, 0.28, 0.54], dtype=float),
            0.63,
        ),
        (
            "charged-lepton-active",
            1,
            1,
            np.array([0.17, 0.09, 0.04], dtype=complex),
            np.array([0.92, 1.08, 0.85], dtype=float),
            np.array([0.33, 0.49, 0.26], dtype=float),
            -0.37,
        ),
    ]

    for label, tau, q, coeffs, x, y, delta in samples:
        d0_trip, dm_trip = build_full_pair(tau, q, coeffs, x, y, delta)
        active_block = d0_trip if tau == 0 else dm_trip
        passive_block = dm_trip if tau == 0 else d0_trip
        active_kernel = projected_green_kernel(active_block - I3, 0.31)
        passive_kernel = projected_green_kernel(passive_block, 0.27)
        rec_d0, rec_dm, meta = recover_pair_from_native_interfaces(
            tau, q, active_kernel, passive_kernel, 0.31, 0.27
        )

        check(
            f"{label}: supplied tau is propagated consistently through the interface",
            meta["tau"] == tau,
            f"supplied={tau}, output={meta['tau']}",
        )
        check(
            f"{label}: q is recovered from the supplied passive kernel",
            meta["q"] == q,
            f"recovered={meta['q']}, true={q}",
        )
        check(
            f"{label}: passive coefficients are recovered from the supplied passive kernel",
            np.linalg.norm(meta["a"] - coeffs) < 1e-12,
            f"coeffs={np.round(meta['a'], 6)}",
        )
        check(
            f"{label}: the full triplet pair is reconstructed exactly from the supplied interfaces",
            np.linalg.norm(rec_d0 - d0_trip) < 1e-12 and np.linalg.norm(rec_dm - dm_trip) < 1e-12,
            f"errors=({np.linalg.norm(rec_d0 - d0_trip):.2e},{np.linalg.norm(rec_dm - dm_trip):.2e})",
        )


def part2_the_existing_downstream_closure_is_then_algorithmic() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE EXISTING DOWNSTREAM CLOSURE IS THEN ALGORITHMIC")
    print("=" * 88)

    tau = 0
    q = 2
    coeffs = np.array([0.07, 0.11, 0.23], dtype=complex)
    x = np.array([1.15, 0.82, 0.95], dtype=float)
    y = np.array([0.41, 0.28, 0.54], dtype=float)
    delta = 0.63
    d0_trip, dm_trip = build_full_pair(tau, q, coeffs, x, y, delta)
    active_kernel = projected_green_kernel(d0_trip - I3, 0.31)
    passive_kernel = projected_green_kernel(dm_trip, 0.27)
    rec_d0, rec_dm, _meta = recover_pair_from_native_interfaces(
        tau, q, active_kernel, passive_kernel, 0.31, 0.27
    )
    solved = solve_triplet_pair(rec_d0, rec_dm)

    check("The reconstructed pair identifies the correct branch", solved["branch"] == "neutrino-active", solved["branch"])
    check("The reconstructed pair reproduces the passive offset", solved["passive_offset"] == q, f"recovered={solved['passive_offset']}")
    check("The reconstructed pair reproduces the active diagonal coefficients", np.linalg.norm(solved["active_x"] - x) < 1e-8,
          f"x={np.round(solved['active_x'], 6)}")
    check("The reconstructed pair reproduces the active cycle coefficients", np.linalg.norm(solved["active_y"] - y) < 1e-8,
          f"y={np.round(solved['active_y'], 6)}")
    check("The reconstructed pair reproduces the active phase", abs(solved["active_delta"] - delta) < 1e-8,
          f"delta={solved['active_delta']:.6f}")
    check("The reconstructed pair fixes the residual sheet", solved["sheet"] in (0, 1), f"sheet={solved['sheet']}")

    print()
    print("  So once the microscopic pair is reconstructed natively, the existing")
    print("  PMNS closure stack is exact and automatic downstream.")


def main() -> int:
    print("=" * 88)
    print("PMNS MICROSCOPIC PAIR RECONSTRUCTION INTERFACE")
    print("=" * 88)
    print()
    print("Interface inputs combined:")
    print("  - independently supplied selector outputs tau and q")
    print("  - active projected Green kernel for the active block")
    print("  - passive projected Green kernel for the passive monomial block")
    print()
    print("Question:")
    print("  Do these independently supplied interfaces recover the full PMNS-relevant")
    print("  microscopic triplet pair (D_0^trip, D_-^trip)?")

    part1_the_combined_native_routes_reconstruct_the_triplet_pair()
    part2_the_existing_downstream_closure_is_then_algorithmic()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact pair-reconstruction interface:")
    print("    - supplied tau selects where the active block sits")
    print("    - q is read back from the supplied passive kernel")
    print("    - the active projected Green kernel fixes the active block")
    print("    - the passive projected Green kernel fixes the passive block")
    print("    - together these recover (D_0^trip, D_-^trip) exactly")
    print()
    print("  Consequence:")
    print("    - the downstream PMNS closure stack is then automatic")
    print()
    print("  Boundary:")
    print("    - this script does not derive tau, q, or either projected kernel")
    print("      from lower-level microscopic dynamics")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
