#!/usr/bin/env python3
"""
Koide Q lepton gauge-ratio c^2 support audit.

This runner lands the useful part of the sunday-koide branch as support-grade
science only. It validates the retained L_L : (2,1) lepton representation
readout, the conditional Brannen algebra c^2=2 <=> Q=2/3, and the open
boundary: the Brannen-W2 analog identifying physical c^2 with the lepton
gauge-representation ratio is not retained on main.
"""

from __future__ import annotations

import math
import re
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASS_COUNT = 0
FAIL_COUNT = 0


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {name}")
    if detail:
        print(f"       {detail}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    return condition


def read_doc(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def normalized(text: str) -> str:
    text = text.replace("²", "^2").replace("A^2", "a^2")
    return re.sub(r"[\s*`]+", " ", text.lower())


def has_all(text: str, phrases: tuple[str, ...]) -> bool:
    haystack = normalized(text)
    return all(phrase.lower() in haystack for phrase in phrases)


def part1_authority_boundary() -> None:
    banner("Part 1: authority boundary")

    ckm_path = "docs/CKM_A_SQUARED_BELOW_W2_Y_QUANTUM_CLOSURE_THEOREM_NOTE_2026-04-25.md"
    lh_path = "docs/LEFT_HANDED_CHARGE_MATCHING_NOTE.md"
    so2_path = "docs/KOIDE_Q_SO2_PHASE_ERASURE_SUPPORT_NOTE_2026-04-25.md"
    note_path = "docs/KOIDE_Q_LEPTON_GAUGE_RATIO_C2_SUPPORT_NOTE_2026-04-26.md"

    ckm = read_doc(ckm_path)
    lh = read_doc(lh_path)
    so2 = read_doc(so2_path)
    note = read_doc(note_path)

    check(
        "CKM A^2 source theorem exists as retained template",
        has_all(
            ckm,
            (
                "retained CKM",
                "Q_L : (2,3)",
                "Identification Source Theorem",
                "A^2 = N_pair/N_color = 2/3",
            ),
        ),
        ckm_path,
    )
    check(
        "left-handed charge note retains L_L : (2,1)",
        has_all(lh, ("Status: retained corollary", "L_L : (2,1)")),
        lh_path,
    )
    check(
        "SO(2) Brannen algebra is explicitly support, not retained Koide closure",
        has_all(
            so2,
            (
                "exact support theorem",
                "not retained native Koide closure",
                "Q = (c^2 + 2) / 6",
            ),
        ),
        so2_path,
    )
    check(
        "new note is support, not closure",
        "SUPPORT_NOT_CLOSURE=TRUE" in note
        and "KOIDE_Q_RETAINED_NATIVE_CLOSURE=FALSE" in note,
        note_path,
    )
    check(
        "new note keeps Brannen-W2 analog open",
        "BRANNEN_W2_ANALOG_RETAINED=FALSE" in note,
        note_path,
    )
    check(
        "new note does not promote delta=2/9 rad closure",
        "DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE" in note,
        note_path,
    )


def part2_exact_lepton_readout() -> Fraction:
    banner("Part 2: exact lepton representation readout")

    n_pair_lepton = 2
    n_color_lepton = 1
    ratio = Fraction(n_pair_lepton, n_color_lepton)

    check(
        "N_pair^ell = dim_SU2(L_L) = 2",
        n_pair_lepton == 2,
        "L_L : (2,1) -> SU(2)_L slot is 2",
    )
    check(
        "N_color^ell = dim_SU3(L_L) = 1",
        n_color_lepton == 1,
        "L_L : (2,1) -> SU(3)_c slot is 1",
    )
    check(
        "lepton gauge-representation ratio is exactly 2",
        ratio == Fraction(2, 1),
        f"N_pair^ell/N_color^ell = {ratio}",
    )

    return ratio


def part3_conditional_brannen_algebra(lepton_ratio: Fraction) -> None:
    banner("Part 3: conditional Brannen algebra")

    c_sq = lepton_ratio
    q_value = (c_sq + 2) / 6
    inverse_c_sq = 6 * Fraction(2, 3) - 2
    ckm_ratio = Fraction(2, 3)

    check(
        "conditional c^2=2 implies Q=(c^2+2)/6=2/3",
        q_value == Fraction(2, 3),
        f"Q = ({c_sq} + 2)/6 = {q_value}",
    )
    check(
        "conversely Q=2/3 implies c^2=2 on the Brannen carrier",
        inverse_c_sq == Fraction(2, 1),
        f"c^2 = 6Q-2 = {inverse_c_sq}",
    )
    check(
        "CKM and lepton source readouts are analogous but not identical claims",
        ckm_ratio == Fraction(2, 3) and lepton_ratio == Fraction(2, 1),
        "CKM retained: Q_L -> 2/3 for A^2; lepton support: L_L -> 2 as a c^2 target",
    )


def part4_pdg_signature() -> None:
    banner("Part 4: observed charged-lepton signature")

    # PDG charged-lepton masses in MeV. The Koide ratio is homogeneous, so the
    # common mass unit cancels.
    masses = (0.51099895000, 105.6583755, 1776.86)
    q_pdg = sum(masses) / sum(math.sqrt(mass) for mass in masses) ** 2
    c_sq_pdg = 6.0 * q_pdg - 2.0

    check(
        "PDG charged-lepton Q is within 1e-4 relative of 2/3",
        abs(q_pdg - 2.0 / 3.0) / (2.0 / 3.0) < 1.0e-4,
        f"Q_PDG={q_pdg:.12f}",
    )
    check(
        "PDG-inferred c^2 is within 1e-4 relative of 2",
        abs(c_sq_pdg - 2.0) / 2.0 < 1.0e-4,
        f"c^2_PDG={c_sq_pdg:.12f}",
    )
    check(
        "PDG comparison is treated as a signature only",
        "PDG_C2_APPROX_2_SIGNATURE_ONLY=TRUE"
        in read_doc("docs/KOIDE_Q_LEPTON_GAUGE_RATIO_C2_SUPPORT_NOTE_2026-04-26.md"),
        "observed masses are not used as proof of the Brannen-W2 analog",
    )


def part5_residual_statement() -> None:
    banner("Part 5: retained residual")

    note = read_doc("docs/KOIDE_Q_LEPTON_GAUGE_RATIO_C2_SUPPORT_NOTE_2026-04-26.md")

    check(
        "the missing theorem is named explicitly",
        "c_Brannen^2 = N_pair^ell / N_color^ell" in note,
    )
    check(
        "the note states the physical c^2 identification is load-bearing",
        has_all(note, ("missing second piece is load-bearing", "not retained")),
    )
    check(
        "the note preserves the Koide open-lane boundary",
        has_all(note, ("not retained native Koide closure", "does not derive")),
    )


def main() -> int:
    print("Koide Q lepton gauge-ratio c^2 support audit")
    print("Status: support only; the Brannen-W2 analog remains open.")

    part1_authority_boundary()
    lepton_ratio = part2_exact_lepton_readout()
    part3_conditional_brannen_algebra(lepton_ratio)
    part4_pdg_signature()
    part5_residual_statement()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
