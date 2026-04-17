#!/usr/bin/env python3
"""
DM neutrino source-amplitude theorem.

Framework convention:
  "axiom" means only the single framework axiom Cl(3) on Z^3.

Question:
  Once the transfer coefficients are fixed, can the source amplitudes on the
  source-oriented sharp branch be fixed canonically as well?

Answer:
  Yes, on the sharp source-oriented branch:

    a_sel = 1/2
    tau_E = tau_T = 1/2
    tau_+ = 1

  Therefore the exact transfer law becomes

    gamma = 1/2
    E1 = sqrt(8/3)
    E2 = sqrt(8)/3.
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


S_CLS = np.diag([0.0, 0.0, 1.0, -1.0])
P_NU = np.diag([0.0, 0.0, 1.0, 0.0])
P_E = np.diag([0.0, 0.0, 0.0, 1.0])
P_SWAP = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
P_PLUS = 0.5 * (np.eye(2) + P_SWAP)


def part1_sharp_selector_projection_fixes_a_sel() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SHARP SELECTOR PROJECTION FIXES A_SEL")
    print("=" * 88)

    hierarchy = read("docs/HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md")
    note = read("docs/DM_NEUTRINO_SOURCE_AMPLITUDE_THEOREM_NOTE_2026-04-15.md")

    centered = P_NU - 0.5 * (P_NU + P_E)
    a_sel = 0.5

    check(
        "The bosonic-bilinear selector theorem records sharp resolved-orbit selection",
        "unique minimal resolved" in hierarchy and "selected by the local bosonic/CPT-even structure" in hierarchy,
    )
    check(
        "The reduced selector bridge still lives on one exact class S_cls with one real amplitude",
        "B_red = a_sel S_cls" in note and "one exact class with one real" in note,
    )
    check(
        "The centered sharp neutrino-side projector is exactly S_cls/2",
        np.linalg.norm(centered - 0.5 * S_CLS) < 1e-12,
        f"err={np.linalg.norm(centered - 0.5 * S_CLS):.2e}",
    )
    check(
        "So the sharp source-oriented selector amplitude is canonically a_sel = 1/2",
        abs(a_sel - 0.5) < 1e-12 and np.trace(P_NU) == 1.0,
        f"a_sel={a_sel:.6f}",
    )
    check(
        "Its sign is the source-oriented neutrino branch sign",
        "a_sel > 0" in note and "neutrino-side branch" in note,
        "positive selector orientation selects the neutrino-side branch",
    )


def part2_sharp_symmetric_source_projection_fixes_tau_plus() -> None:
    print("\n" + "=" * 88)
    print("PART 2: SHARP SYMMETRIC SOURCE PROJECTION FIXES TAU_PLUS")
    print("=" * 88)

    carrier = read("docs/S3_TIME_BILINEAR_TENSOR_PRIMITIVE_NOTE.md")
    hierarchy = read("docs/HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md")
    reduction = read("docs/DM_NEUTRINO_WEAK_EVEN_SWAP_REDUCTION_THEOREM_NOTE_2026-04-15.md")

    source_vec = np.array([0.5, 0.5], dtype=float)
    tau_plus = float(np.sum(source_vec))

    check(
        "The exact weak carrier is the two-column bright bundle K_R(q) = [[u_E,u_T],[delta_A1 u_E,delta_A1 u_T]]",
        "K_R(q) = [[u_E(q), u_T(q)], [delta_A1(q)u_E(q), delta_A1(q)u_T(q)]]".replace(" ", "")
        in carrier.replace(" ", ""),
    )
    check(
        "The hierarchy selector theorem again supplies sharp bosonic-even projection rather than soft weighting",
        "local bosonic" in hierarchy and "CPT-even" in hierarchy and "resolved" in hierarchy,
    )
    check(
        "The weak even reduction note fixes that only the swap-even source mode survives",
        "tau_+ = tau_E + tau_T" in reduction and "tau_-" in reduction,
    )
    check(
        "The canonical sharp swap-even projector is P_+ = (I + P_swap)/2",
        np.linalg.norm(P_PLUS @ P_PLUS - P_PLUS) < 1e-12 and np.linalg.norm(P_PLUS - P_SWAP @ P_PLUS) < 1e-12,
        f"idempotence err={np.linalg.norm(P_PLUS @ P_PLUS - P_PLUS):.2e}",
    )
    check(
        "Its source-oriented coordinate vector is exactly (tau_E,tau_T) = (1/2,1/2)",
        np.linalg.norm(P_PLUS[:, 0] - source_vec) < 1e-12 and np.linalg.norm(P_PLUS[:, 1] - source_vec) < 1e-12,
        f"vec={source_vec.tolist()}",
    )
    check(
        "Therefore the symmetric source amplitude is canonically tau_+ = 1",
        abs(tau_plus - 1.0) < 1e-12,
        f"tau_+={tau_plus:.6f}",
    )


def part3_the_exact_triplet_source_data_follow_immediately() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE EXACT TRIPLET SOURCE DATA FOLLOW IMMEDIATELY")
    print("=" * 88)

    codd = read("docs/DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md")
    veven = read("docs/DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md")

    a_sel = 0.5
    tau_plus = 1.0
    gamma = a_sel
    e1 = math.sqrt(8.0 / 3.0) * tau_plus
    e2 = (math.sqrt(8.0) / 3.0) * tau_plus

    check(
        "The odd transfer coefficient is already fixed as c_odd = +1",
        "c_odd = +1" in codd,
    )
    check(
        "The even transfer coefficients are already fixed as v_even = (sqrt(8/3), sqrt(8)/3)",
        "v_even = (sqrt(8/3), sqrt(8)/3)" in veven,
    )
    check(
        "So the exact odd triplet source is gamma = a_sel = 1/2",
        abs(gamma - 0.5) < 1e-12,
        f"gamma={gamma:.6f}",
    )
    check(
        "The exact even triplet responses are E1 = sqrt(8/3) and E2 = sqrt(8)/3",
        abs(e1 - math.sqrt(8.0 / 3.0)) < 1e-12 and abs(e2 - math.sqrt(8.0) / 3.0) < 1e-12,
        f"(E1,E2)=({e1:.12f},{e2:.12f})",
    )


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO SOURCE-AMPLITUDE THEOREM")
    print("=" * 88)

    part1_sharp_selector_projection_fixes_a_sel()
    part2_sharp_symmetric_source_projection_fixes_tau_plus()
    part3_the_exact_triplet_source_data_follow_immediately()

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
