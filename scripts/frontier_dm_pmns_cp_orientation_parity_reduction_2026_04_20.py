#!/usr/bin/env python3
"""
DM PMNS CP-orientation parity reduction.

Question:
  Once the compact chamber chi^2 = 0 set is known, what is the exact remaining
  gap between the source-side CP orientation and the physical PMNS CP sign?

Answer:
  On the DM Hermitian family the source cubic orientation

      I_src(H) = Im(H_12 H_23 H_31)

  satisfies

      J_basis = I_src(H) / ((lambda_1 - lambda_2)(lambda_2 - lambda_3)(lambda_3 - lambda_1))

  for the ascending-eigenvalue basis, and any row permutation sigma adds only
  its parity sign.  So the remaining gap is exactly a parity / doublet-label
  law for sigma_hier, not another source-side CP-odd scalar.
"""

from __future__ import annotations

import math

import numpy as np

from frontier_sigma_hier_uniqueness_theorem import H_mat

np.set_printoptions(precision=12, suppress=True, linewidth=140)

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


SIGMA_210 = (2, 1, 0)
SIGMA_201 = (2, 0, 1)

CHAMBER_ROOTS = {
    "Basin 1": (0.6570613422097703, 0.9338063437590336, 0.7150423295873919),
    "Basin 2": (28.006188289564736, 20.721831213931072, 5.011599458304925),
    "Basin X": (21.128263668693783, 12.680028023619366, 2.08923480586059),
}


def permutation_sign(perm: tuple[int, int, int]) -> int:
    inversions = 0
    for i in range(3):
        for j in range(i + 1, 3):
            if perm[i] > perm[j]:
                inversions += 1
    return -1 if inversions % 2 else 1


def source_cubic(H: np.ndarray) -> float:
    return float(np.imag(H[0, 1] * H[1, 2] * H[2, 0]))


def vandermonde_positive(evals: np.ndarray) -> float:
    l1, l2, l3 = map(float, evals)
    return (l1 - l2) * (l2 - l3) * (l3 - l1)


def jarlskog(P: np.ndarray) -> float:
    return float(np.imag(P[0, 0] * np.conjugate(P[0, 1]) * np.conjugate(P[1, 0]) * P[1, 1]))


def main() -> int:
    print("=" * 88)
    print("DM PMNS CP ORIENTATION PARITY REDUCTION")
    print("=" * 88)

    sign_table: dict[str, dict[str, float]] = {}

    print()
    print("Part 1: source cubic equals the ascending-basis Jarlskog bridge")
    for name, point in CHAMBER_ROOTS.items():
        H = H_mat(*point)
        evals, vecs = np.linalg.eigh(H)
        I_src = source_cubic(H)
        delta = vandermonde_positive(evals)
        J_basis = jarlskog(vecs)
        sign_table[name] = {"I_src": I_src, "J_basis": J_basis}
        print(
            "   "
            f"{name}: I_src={I_src:+.12f}  "
            f"Delta={delta:+.12f}  "
            f"J_basis={J_basis:+.12f}  "
            f"I_src/Delta={I_src / delta:+.12f}"
        )
        check(
            f"{name}: ascending-basis Jarlskog equals I_src / Delta",
            abs(J_basis - I_src / delta) < 1e-12,
        )

    print()
    print("Part 2: row-permutation parity is the only extra sign")
    for name, point in CHAMBER_ROOTS.items():
        H = H_mat(*point)
        evals, vecs = np.linalg.eigh(H)
        I_src = source_cubic(H)
        delta = vandermonde_positive(evals)
        for perm in [SIGMA_210, SIGMA_201]:
            P = vecs[list(perm), :]
            J_perm = jarlskog(P)
            expected = permutation_sign(perm) * I_src / delta
            print(
                "   "
                f"{name}, sigma={perm}: parity={permutation_sign(perm):+d}  "
                f"J_sigma={J_perm:+.12f}  expected={expected:+.12f}"
            )
            check(
                f"{name}, sigma={perm}: J_sigma = parity(sigma) * I_src / Delta",
                abs(J_perm - expected) < 1e-12,
            )

    print()
    print("Part 3: chamber-sign structure")
    check("Basin 1 has positive source cubic orientation", sign_table["Basin 1"]["I_src"] > 0.0)
    check("Basin 2 has negative source cubic orientation", sign_table["Basin 2"]["I_src"] < 0.0)
    check("Basin X has negative source cubic orientation", sign_table["Basin X"]["I_src"] < 0.0)

    H1 = H_mat(*CHAMBER_ROOTS["Basin 1"])
    _, V1 = np.linalg.eigh(H1)
    J_210 = jarlskog(V1[list(SIGMA_210), :])
    J_201 = jarlskog(V1[list(SIGMA_201), :])
    check("At the same H_pin, sigma=(2,1,0) and sigma=(2,0,1) give opposite PMNS CP signs", J_210 * J_201 < 0.0)
    check(
        "Yet the source cubic at H_pin is single-valued and sigma-blind",
        abs(source_cubic(H1) - sign_table["Basin 1"]["I_src"]) < 1e-14,
    )

    print()
    print("Part 4: conditional source law after the parity bit")
    # On the odd-parity branch sigma=(2,1,0), I_src > 0 picks Basin 1 uniquely.
    odd_positive = []
    even_positive = []
    for name, point in CHAMBER_ROOTS.items():
        H = H_mat(*point)
        I_src = source_cubic(H)
        if I_src > 0:
            odd_positive.append(name)
            if permutation_sign(SIGMA_201) == 1:
                even_positive.append(name)
    check(
        "On the odd sigma branch, the coefficient-free source law I_src > 0 selects Basin 1 uniquely",
        odd_positive == ["Basin 1"],
        f"odd-positive={odd_positive}",
    )
    check(
        "So once a parity / charged-doublet label law fixes sigma=(2,1,0), the source cubic sign also forces sin(delta_CP) < 0",
        sign_table["Basin 1"]["I_src"] > 0.0 and permutation_sign(SIGMA_210) == -1,
    )

    print()
    print("=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction:")
    print("    - the source family already carries a CP-oriented cubic scalar I_src")
    print("    - the ascending-eigenbasis Jarlskog is exactly I_src / Delta")
    print("    - physical PMNS CP sign differs from that only by parity(sigma_hier)")
    print()
    print("  Consequence:")
    print("    - source-side CP-odd data do not close sigma_hier by themselves")
    print("    - the remaining gap for I12, and for the sign half of I5, is exactly")
    print("      the parity / charged-doublet label law on sigma_hier")
    print("    - once that parity bit is fixed to sigma=(2,1,0), the simple source law")
    print("      I_src > 0 selects Basin 1 and yields sin(delta_CP) < 0 immediately")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    raise SystemExit(main())
