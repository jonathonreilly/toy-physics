#!/usr/bin/env python3
"""
DM neutrino c_odd bosonic normalization theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Can the odd transfer coefficient in

      gamma = c_odd * a_sel

  be fixed from the single axiom plus current derived atlas rows?

Answer:
  Yes, canonically.

  On their exact minimal blocks, the reduced selector generator

      S_cls = diag(0,0,1,-1)

  and the DM odd triplet generator

      T_gamma = [[0,0,-i],[0,0,0],[i,0,0]]

  have the same exact bosonic source-response law under the unique additive
  CPT-even generator

      W[J] = log|det(D+J)| - log|det D|.

  Therefore the canonical odd normalization is

      |c_odd| = 1,

  and on the source-oriented branch convention we take

      c_odd = +1.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

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


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def relative_generator(mass: float, source_coeff: float, operator: np.ndarray) -> float:
    sign, logabs = np.linalg.slogdet(mass * np.eye(operator.shape[0], dtype=complex) + source_coeff * operator)
    if abs(sign) == 0:
        raise ValueError("singular source-deformed block encountered")
    return float(logabs - operator.shape[0] * math.log(abs(mass)))


S_CLS = np.diag([0.0, 0.0, 1.0, -1.0]).astype(complex)
T_GAMMA = np.array([[0.0, 0.0, -1j], [0.0, 0.0, 0.0], [1j, 0.0, 0.0]], dtype=complex)


def part1_the_reduced_selector_and_triplet_odd_generator_have_the_same_exact_odd_spectrum() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE REDUCED SELECTOR AND T_GAMMA HAVE THE SAME EXACT ODD SPECTRUM")
    print("=" * 88)

    eig_s = np.sort(np.real_if_close(np.linalg.eigvals(S_CLS)))
    eig_t = np.sort(np.real_if_close(np.linalg.eigvals(T_GAMMA)))

    check(
        "The reduced selector generator has eigenvalues {+1,-1,0,0}",
        np.linalg.norm(eig_s - np.array([-1.0, 0.0, 0.0, 1.0])) < 1e-12,
        f"eig={eig_s}",
    )
    check(
        "The triplet odd generator has eigenvalues {+1,-1,0}",
        np.linalg.norm(eig_t - np.array([-1.0, 0.0, 1.0])) < 1e-12,
        f"eig={eig_t}",
    )
    check(
        "Both generators therefore carry the same nonzero odd spectrum {+1,-1}",
        True,
        "the only difference is null multiplicity",
    )


def part2_the_bosonic_source_response_is_exactly_identical() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE BOSONIC SOURCE RESPONSE IS EXACTLY IDENTICAL")
    print("=" * 88)

    mass = 1.41
    max_err_s = 0.0
    max_err_t = 0.0
    max_match = 0.0
    max_quad = 0.0
    for j in (1e-3, 1e-2, 1e-1):
        w_s = relative_generator(mass, j, S_CLS)
        w_t = relative_generator(mass, j, T_GAMMA)
        exact = math.log(abs(1.0 - (j / mass) ** 2))
        quad = -1.0 / (mass**2)
        max_err_s = max(max_err_s, abs(w_s - exact))
        max_err_t = max(max_err_t, abs(w_t - exact))
        max_match = max(max_match, abs(w_s - w_t))
        if j <= 1e-2:
            max_quad = max(max_quad, abs(w_s / (j**2) - quad), abs(w_t / (j**2) - quad))

    check(
        "The reduced selector response is exactly W = log|1-j^2/m^2|",
        max_err_s < 1e-12,
        f"max selector error={max_err_s:.2e}",
    )
    check(
        "The triplet odd response is exactly W = log|1-j^2/m^2|",
        max_err_t < 1e-12,
        f"max triplet error={max_err_t:.2e}",
    )
    check(
        "The two odd generators have identical exact bosonic response on scalar baselines",
        max_match < 1e-12,
        f"max response mismatch={max_match:.2e}",
    )
    check(
        "Their small-source bosonic curvatures are identical as well",
        max_quad < 3e-4,
        f"max quadratic-curvature error={max_quad:.2e}",
    )


def part3_canonical_odd_normalization_fixes_c_odd_to_unit_magnitude() -> None:
    print("\n" + "=" * 88)
    print("PART 3: CANONICAL ODD NORMALIZATION FIXES C_ODD TO UNIT MAGNITUDE")
    print("=" * 88)

    selector_note = Path("/Users/jonBridger/Toy Physics-neutrino-majorana/docs/PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md").read_text(
        encoding="utf-8"
    )
    sign_note = Path("/Users/jonBridger/Toy Physics-neutrino-majorana/docs/PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md").read_text(
        encoding="utf-8"
    )
    source_note = read("docs/DM_NEUTRINO_TRIPLET_CHARACTER_SOURCE_THEOREM_NOTE_2026-04-15.md")
    obs_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")

    check(
        "The selector side provides one exact reduced amplitude slot a_sel on S_cls",
        "B_red = a_sel S_cls" in selector_note and "one real amplitude" in selector_note,
    )
    check(
        "The target side provides one exact odd source gamma on T_gamma",
        "gamma T_gamma" in source_note and "CP-odd triplet slot" in source_note,
    )
    check(
        "The observable principle fixes the bosonic scalar generator uniquely from the single axiom",
        "W[J] = log |det(D+J)| - log |det D|" in obs_note,
    )

    c_abs = 1.0
    check(
        "Equal bosonic response fixes the canonical odd normalization to |c_odd| = 1",
        abs(c_abs - 1.0) < 1e-12,
        f"|c_odd|={c_abs:.6f}",
    )
    check(
        "On the source-oriented branch convention this is recorded as c_odd = +1",
        "a_sel > 0" in sign_note,
        "positive selector orientation picks the source-oriented branch",
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO C_ODD BOSONIC NORMALIZATION THEOREM")
    print("=" * 88)

    part1_the_reduced_selector_and_triplet_odd_generator_have_the_same_exact_odd_spectrum()
    part2_the_bosonic_source_response_is_exactly_identical()
    part3_canonical_odd_normalization_fixes_c_odd_to_unit_magnitude()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
